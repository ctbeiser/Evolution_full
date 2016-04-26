import traceback


#Integer between 0 (None) and 2 (All). 1 will print only those with the circumstance flag
DEBUG_LEVEL = 0


def debug(string, circumstance=False):
    """ Prints an object to the command line if debugging is enabled.
    Use instead of print because this may be expanded in the future to use debugging facilities properly.
    :param str: String
    :circumstance: Override to print debug statements
    """
    if DEBUG_LEVEL + circumstance >= 2:
        print(string)


def debug_traceback(tb):
    """ Given a python Traceback, print it it to the command line if debugging is enabled
    :param tb: Traceback
    """
    debug(traceback.format_tb(tb))
