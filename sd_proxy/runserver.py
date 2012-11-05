"""Main WSGI server runner for sd-proxy
"""

from __future__ import print_function

import os
from sys import argv, path
from gevent.wsgi import WSGIServer


def main(app, port=8889):
    print('Starting sd-proxy on port {0}..'.format(port))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

if __name__ == '__main__':
    path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from sd_proxy.app import app

    port = 8889
    if len(argv) > 1:
        port = argv[1]

    main(app, port)
