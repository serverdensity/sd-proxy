import hashlib
import requests
from flask import Flask, request
from gevent.monkey import patch_all
from jsonschema import validate, ValidationError

try:
    import simplejson as json
except ImportError:
    import json

from . import settings

app = Flask(__name__)
patch_all()

ALLOWED_HOSTS = []

if not settings.allow_all_accounts:
    for account in settings.allowed_accounts:
        if not account.endswith('.serverdensity.com'):
            account = "{0}.serverdensity.com".format(account)

        ALLOWED_HOSTS.append(account)

if not settings.allow_all_agents:
    ALLOWED_AGENTS = [key.strip() for key in settings.allowed_agents]
else:
    ALLOWED_AGENTS = []

SCHEMA = json.load(open(settings.payload_schema))


@app.route('/postback/', methods=('POST',))
def postbacks():
    host = request.headers.get('host', '')
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

        try:
            validate(parsed_payload, SCHEMA)
        except ValidationError as e:
            app.logger.error("Error validating payload against schema"
                             " (%s): %s", host, e)
            return '"bad payload"', 500

        protocol = 'https' if settings.use_outbound_ssl else 'http'

        postback_url = '{0}://{1}/'.format(protocol, host)
        requests.post(postback_url, data={'hash': hash, 'payload': payload})

        return '"OK"'
    else:
        app.logger.warning("Host not in allowed_accounts: %s", host)
        return '"unknown account"', 404

if __name__ == '__main__':
    app.run(debug=True)
