"""Main WSGI server runner for sd-proxy
"""

import os
import logging
from sys import argv, path, stderr, exit
from gevent.wsgi import WSGIServer


class VersionedWSGIServer(WSGIServer):

    def __init__(self, server_version, *args, **kwargs):
        self.base_env['SERVER_SOFTWARE'] = server_version
        super(VersionedWSGIServer, self).__init__(*args, **kwargs)


def run(app, port=8889, listener=None):

    if listener is None:
        listener = ('', port)

    version = 'sd-proxy/%s' % (app._version,)
    http_server = VersionedWSGIServer(version, listener, app)
    http_server.serve_forever()


def main():

    if len(argv) < 1:
        print >> stderr, 'Please provide a path to your config file.'
        return 1

    os.environ['SD_PROXY_CONFIG'] = argv[1]
    from serverdensity.proxy import settings, setup_logging
    from serverdensity.proxy.app import app

    setup_logging(app)
    app.debug = settings.debug

    app.logger.info('Starting sd-proxy on port %s..' % (settings.port,))
    run(app, settings.port)

    return 0


if __name__ == '__main__':
    path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    exit(main())
