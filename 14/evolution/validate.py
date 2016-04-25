

def is_natural(maybe_nat):
    """ Check if the given item is an Int >= 0
    :param maybe_nat: Any
    :return: Boolean
    """
    return isinstance(maybe_nat, int) and maybe_nat >= 0


def is_natural_plus(maybe_nat):
    """ Check if the given item is an Int >= 1
    :param maybe_nat: Any
    :return: Boolean
    """
    return is_natural(maybe_nat) and maybe_nat > 0


def is_list(maybe_list):
    """ Check if the given item is a list
    :param maybe_list: Any
    :return: Boolean
    """
    return isinstance(maybe_list, list)


def is_string(maybe_string):
    """ Check if the given item is a String
    :param maybe_string: String
    :return: Boolean
    """
    return isinstance(maybe_string, str)
