"""Main WSGI server runner for sd-proxy
"""

import os
from sys import argv, path, stderr, exit
from gevent.socket import tcp_listener
from multiprocessing import Process, cpu_count


def main():
    if len(argv) < 1:
        print >> stderr, 'Please provide a path to your config file.'
        return 1

    os.environ['SD_PROXY_CONFIG'] = argv[1]
    from serverdensity.proxy import settings, setup_logging
    from serverdensity.proxy.app import app
    from serverdensity.proxy.runserver import run

    setup_logging(app)
    app.debug = settings.debug

    process_num = settings.processes or cpu_count()
    app.logger.info('Starting %s sd-proxy(s) on port %s..' % (
                              process_num, settings.port,))

    listener = tcp_listener(('127.0.0.1', settings.port))
    for i in xrange((process_num - 1)):
        Process(target=run, args=(app, None, listener)).start()

    run(app, None, listener)
    return 0

if __name__ == '__main__':
    path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    exit(main())
