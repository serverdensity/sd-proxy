"""Main WSGI server runner for sd-proxy
"""

from __future__ import print_function

import os
import logging
from sys import argv, path, stderr, exit
from gevent.wsgi import WSGIServer


def main(app, port=8889):
    print(u'Starting sd-proxy on port {0}..'.format(port))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

if __name__ == '__main__':

    if len(argv) < 1:
        print(u'Please provide a path to your config file.', file=stderr)
        exit(1)

    os.environ['SD_PROXY_CONFIG'] = argv[1]

    path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from sd_proxy.app import app
    from sd_proxy import settings

    handler = logging.StreamHandler(stderr)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)

    main(app, settings.port)
