def detect_unchecked_call(ops):

    for i, (_, op, val) in enumerate(ops):

        if op == "external_call":

            checked = False

            for j in range(i + 1, len(ops)):

                _, op2, val2 = ops[j]

                if op2 == "function_call" and val2 == "require":
                    checked = True
                    break

                if op2 == "external_call":
                    break

            if not checked:
                return True

    return False