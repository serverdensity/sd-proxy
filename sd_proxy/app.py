import requests
from flask import Flask, request
from gevent.monkey import patch_all

from . import settings

app = Flask(__name__)
patch_all()

ALLOWED_HOSTS = []

if not settings.allow_all_accounts:
    for account in settings.allowed_accounts:
        if not account.endswith('.serverdensity.com'):
            account = "{0}.serverdensity.com".format(account)

        ALLOWED_HOSTS.append(account)


@app.route('/postback/', methods=('POST',))
def postbacks():
    host = request.headers.get('host', '')
    if ':' in host:
        host = host.split(':')[0]

    if settings.allow_all_accounts or host in ALLOWED_HOSTS:
        hash = request.form.get('hash', '')
        payload = request.form.get('payload', '')

        protocol = 'https' if settings.use_outbound_ssl else 'http'

        postback_url = '{0}://{1}/'.format(protocol, host)
        requests.post(postback_url, data={'hash': hash, 'payload': payload})

    return u'"OK"'

if __name__ == '__main__':
    app.run()
