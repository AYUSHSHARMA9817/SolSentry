def detect_delegatecall(ops):

    for _, op, val in ops:

        if op == "external_call" and ".delegatecall" in val:
            return True

    return False