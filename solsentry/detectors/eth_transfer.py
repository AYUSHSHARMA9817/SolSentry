def detect_eth_transfer(ops):

    for _, op, var in ops:

        if op == "external_call":

            if ".call" in var or ".transfer" in var or ".send" in var:
                return True

    return False