import hashlib
import requests
from flask import Flask, request
from gevent.monkey import patch_all

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
            app.logger.error("Error parsing payload for %s: %s", host, e)
            return '"payload error"', 500

        if not settings.allow_all_agents and parsed_payload.get('agentKey',
                                        '').strip() not in ALLOWED_AGENTS:
            return '"unknown agent"', 404

        if settings.check_hashes and hashlib.md5(payload).hexdigest() != hash:
            return '"hash mismatch"', 500

        protocol = 'https' if settings.use_outbound_ssl else 'http'

        postback_url = '{0}://{1}/'.format(protocol, host)
        requests.post(postback_url, data={'hash': hash, 'payload': payload})

        return '"OK"'
    else:
        return '"unknown account"', 404

if __name__ == '__main__':
    app.run(debug=True)
