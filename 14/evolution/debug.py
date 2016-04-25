import traceback

DEBUG = True

def debug(string):
    """ Prints an object to the command line if debugging is enabled.
    Use instead of print because this may be expanded in the future to use debugging facilities properly.
    :param str: String
    """
    if DEBUG:
        print(string)


def debug_traceback(tb):
    """ Given a python Traceback, print it it to the command line if debugging is enabled
    :param tb: Traceback
    """
    debug(traceback.format_tb(tb))