

def is_natural(maybe_nat):
    return all([isinstance(maybe_nat, int),
                maybe_nat >= 0])


def is_natural_plus(maybe_nat):
    return is_natural(maybe_nat) and maybe_nat > 0


def is_list(maybe_list):
    return isinstance(maybe_list, list)


def is_string(maybe_string):
    return isinstance(maybe_string, str)