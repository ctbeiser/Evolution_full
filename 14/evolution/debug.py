import traceback


#Integer between 0 (None) and 2 (All). 1 will print only those with the circumstance flag
DEBUG = False
VERBOSE = False

def debug(string, player_id=None, verbose=False):
    """ Prints an object to the command line if debugging is enabled.
    Use instead of print because this may be expanded in the future to use debugging facilities properly.
    :param str: String
    :player_id: Player's id, if debug is called from a player
    """
    if verbose:
        print(string)
        if not VERBOSE:
            return
    if DEBUG:
        if not player_id:
            print(string)


def debug_traceback(tb):
    """ Given a python Traceback, print it it to the command line if debugging is enabled
    :param tb: Traceback
    """
    debug(traceback.format_tb(tb))
