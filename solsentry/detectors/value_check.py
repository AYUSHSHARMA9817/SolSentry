def value_check(ops):

    for _, op, var in ops:

        if op == "require_condition":

            if any(x in var for x in [">", ">=", "<", "<="]):
                return True

    return False