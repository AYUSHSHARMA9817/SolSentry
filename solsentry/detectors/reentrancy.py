def detect_reentrancy(ops):

    reads = set()
    seen_external = False

    for _, op, var in ops:

        if op == "state_read" and not seen_external:
            reads.add(var)

        elif op == "external_call":
            seen_external = True

        elif op == "state_write" and seen_external:
            if var in reads:
                return True

    return False


def detect_state_after_call(ops):

    seen_external = False

    for _, op, _ in ops:

        if op == "external_call":
            seen_external = True

        if op == "state_write" and seen_external:
            return True

    return False