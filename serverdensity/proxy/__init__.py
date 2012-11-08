import os
import logging
from sys import stdout, stderr


def get_version_string():
    return open(os.path.join(os.path.dirname(__file__),
                'version.txt'), 'r').read().strip()


def get_version():
    return get_version_string().split('.')

__version__ = get_version_string()


class SingleLevelFilter(logging.Filter):
    def __init__(self, pass_level, reject):
        self.pass_level = pass_level
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno is not self.pass_level)
        else:
            return (record.levelno is self.pass_level)


def setup_logging(app):
    app.logger.setLevel(logging.INFO)

    # Error filter, rejects INFO and DEBUG messages
    ignore_info_filter = SingleLevelFilter(logging.INFO, True)
    ignore_debug_filter = SingleLevelFilter(logging.DEBUG, True)
    stderr_handler = logging.StreamHandler(stderr)
    stderr_handler.addFilter(ignore_info_filter)
    stderr_handler.addFilter(ignore_debug_filter)

    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(stderr_handler)

    # Info filter, only accepts INFO
    info_only_filter = SingleLevelFilter(logging.INFO, False)
    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.addFilter(info_only_filter)

    stdout_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    app.logger.addHandler(stdout_handler)
