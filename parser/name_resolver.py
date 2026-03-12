def resolve_name(node):

    if not isinstance(node, dict):
        return ""

    nt = node.get("nodeType")

    if nt == "Identifier":
        return node.get("name")
    
    if nt == "BinaryOperation":

        left = resolve_name(node["leftExpression"])
        right = resolve_name(node["rightExpression"])
        op = node["operator"]

        return f"{left} {op} {right}"

    if nt == "MemberAccess":
        return resolve_name(node.get("expression")) + "." + node.get("memberName")

    if nt == "IndexAccess":
        return resolve_name(node.get("baseExpression")) + "[" + resolve_name(node.get("indexExpression")) + "]"

    if nt == "FunctionCallOptions":
        return resolve_name(node.get("expression"))

    if nt == "Literal":
        return node.get("value", "")
    
    if nt == "UnaryOperation":
        op = node.get("operator")
        sub = resolve_name(node.get("subExpression"))
        return f"{op}{sub}"

    return ""