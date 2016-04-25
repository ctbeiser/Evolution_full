# This decorator is courtesy of this Stack Overflow post:
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish

from functools import wraps
import errno
import os
import signal


class TimedOutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    """ A timeout decorator— spawns a unix thread, and uses it to remind the system to kill the encapsulated function
    if it's not done by the amount of time that is specified
    :param seconds: Integer number of seconds to wait
    :param error_message: a String to use as an error.
    NOTE: This should be used with a decorator, @timeout(n, message). The arguments are the same.
    NOTE: Because the exceptions are the same, it is not reccomended to nest these timeouts— they will trigger eachother
    """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimedOutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator
