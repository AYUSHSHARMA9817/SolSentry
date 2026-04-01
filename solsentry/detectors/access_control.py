def access_control(ops,vis):

    for _, op, var in ops:
        if vis in ["internal", "private"]:
            return True
        else:
            if op == "require_condition":

                if "msg.sender ==" in var or "== msg.sender" in var:
                    return True
            
    return False
