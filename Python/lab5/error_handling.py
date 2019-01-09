import functools
import logging
from contextlib import contextmanager

import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


@contextmanager
def handle_error_context(re_raise=True, log_traceback=True, exc_type=Exception):
    try:
        yield
    except exc_type:
        if log_traceback:
            logger.exception('')
        if re_raise:
            raise


def handle_error(re_raise=True, log_traceback=True, exc_type=Exception):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with handle_error_context(re_raise, log_traceback, exc_type):
                f(*args, **kwargs)

        return wrapped
    return wrapper
