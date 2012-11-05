"""Main WSGI server runner for sd-proxy
"""

from __future__ import print_function

from sys import argv
from gevent.wsgi import WSGIServer


def main(app, port=8889):
    print('Starting sd-proxy on port {0}..'.format(port))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

if __name__ == '__main__':
    from app import app
    port = 8889

    if len(argv) > 1:
        port = argv[1]

    main(app, port)
