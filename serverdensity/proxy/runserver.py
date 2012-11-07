"""Main WSGI server runner for sd-proxy
"""

import os
import logging
from sys import argv, path, stdout, stderr, exit
from gevent.wsgi import WSGIServer


def run(app, port=8889):
    WSGIServer.base_env['SERVER_SOFTWARE'] = 'sd-proxy/%s' % (app._version,)
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()


def main():
    if len(argv) < 1:
        print >> stderr, 'Please provide a path to your config file.'
        exit(1)

    os.environ['SD_PROXY_CONFIG'] = argv[1]
    from serverdensity.proxy.app import app
    from serverdensity.proxy import settings

    handler = logging.StreamHandler(stderr)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)

    app.debug = settings.debug

    print >> stdout, 'Starting sd-proxy on port %s..' % (settings.port,)
    run(app, settings.port)

if __name__ == '__main__':
    path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    main()
