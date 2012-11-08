import re
import socket
import hashlib
import requests
from flask import Flask, request
from gevent.monkey import patch_all
from jsonschema import validate, ValidationError

try:
    import simplejson as json
except ImportError:
    import json

from serverdensity.proxy import get_version_string, settings

app = Flask('sd-proxy')
app._version = get_version_string()
patch_all()

ALLOWED_HOSTS = []
if not settings.allow_all_accounts:
    for account in settings.allowed_accounts:
        if not account.endswith('.serverdensity.com'):
            account = "%s.serverdensity.com" % (account,)

        ALLOWED_HOSTS.append(account)

ALLOWED_AGENTS = []
if not settings.allow_all_agents:
    ALLOWED_AGENTS = [key.strip() for key in settings.allowed_agents]

if settings.use_schema:
    SCHEMA = json.load(open(settings.payload_schema))

# Pre-compile ALL THE REGEXES!
BLACKLIST_REGEXES = [re.compile(rx) for rx in settings.blacklist_regexes]


# TODO: refactor as a series of tubes, err, I mean a bunch of unit-testable
# mini functions
@app.route('/postback/', methods=('POST',))
def postbacks():
    """Server Density postback handler.
    Performs validation of JSON payloads from an sd-agent instance before
    forwarding the payload to Server Density.
    See the settings module for configurable options.
    """

    host = request.headers.get('host', '')
    # Don't include port, when testing locally against a different port
    # this will be included in the Host header.
    if ':' in host:
        host = host.split(':')[0]

    if settings.allow_all_accounts or host in ALLOWED_HOSTS:
        hash = request.form.get('hash', '')
        payload = request.form.get('payload', '')

        try:
            parsed_payload = json.loads(payload)
        except Exception as e:
            app.logger.error("Error parsing payload (%s): %s", host, e)
            return '"payload error"', 500

        agent_key = parsed_payload.get('agentKey', '').strip()

        if not settings.allow_all_agents and agent_key not in ALLOWED_AGENTS:
            app.logger.warning("agentKey not in allowed_agents: %s", agent_key)
            return '"unknown agent"', 404

        check_hash = hashlib.md5(payload).hexdigest()
        if settings.check_hashes and check_hash != hash:
            app.logger.warning("Payload md5 mismatch: theirs: %s, ours: %s",
                                                        hash, check_hash)
            return '"hash mismatch"', 500

        if settings.use_schema:
            try:
                validate(parsed_payload, SCHEMA)
            except ValidationError as e:
                app.logger.error("Error validating payload against schema"
                                 " (%s): %s", host, e)
                return '"bad payload"', 500

        for rx in (rx for rx in BLACKLIST_REGEXES if rx.search(payload,
                                                               re.MULTILINE)):
            app.logger.warning("Payload blacklisted by regex: %s", rx.pattern)
            return '"bad payload"', 500

        protocol = 'https' if settings.use_outbound_ssl else 'http'

        if settings.check_ip_address:
            hostname = socket.gethostbyname(host)

            if hostname not in settings.ip_addresses:
                # If the IP we're posting back to resolves to something else,
                # just force it to use a random approved IP, this is either due
                # to bad DNS, local /etc/hosts resolution, or an out of date
                # settings.ip_addresses, so we'll also add a warning
                app.logger.error("%s not in settings.ip_addresses", hostname)
                return '"dns error"', 500

        postback_url = '%s://%s/postback/' % (protocol, host)
        try:
            resp = requests.post(postback_url,
                                 data={'hash': hash, 'payload': payload},
                                 headers={'Host': host})
        except Exception as e:
            app.logger.error("Failed to forward postback to %s: %s",
                                                            host, e.message)
            return '"upstream error"', 500

        return resp.text, resp.status_code
    else:
        app.logger.warning("Host not in allowed_accounts: %s", host)
        return '"unknown account"', 404

if __name__ == '__main__':
    # Probably never used, run with the runserver entrypoint instead
    app.run(debug=True)
