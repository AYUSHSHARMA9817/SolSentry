def resolve_name(node):

    if not isinstance(node, dict):
        return ""

    nt = node.get("nodeType")

    if nt == "Identifier":
        return node.get("name")
    
    if nt == "BinaryOperation":
        left = resolve_name(node.get("leftExpression"))
        right = resolve_name(node.get("rightExpression"))
        op = node.get("operator", "")

        if left == "" and right == "":
            return ""

        if left == "":
            return f"{op} {right}"

        if right == "":
            return f"{left} {op}"

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
    
    if nt == "FunctionCall":
        if node.get("kind") == "typeConversion":

            type_name = resolve_name(node.get("expression"))

            args = node.get("arguments", [])
            if len(args) > 0:
                arg = resolve_name(args[0])
                return f"{type_name}({arg})"

            return f"{type_name}()"
        
    if nt == "FunctionCall":
        expr = resolve_name(node.get("expression"))
        args = node.get("arguments", [])
        arg_names = [resolve_name(a) for a in args if a]
        return f"{expr}({', '.join(arg_names)})"
        
    if nt == "ElementaryTypeNameExpression":
        next = node.get("typeName")
        if next:
            return next.get("name")
        
    if nt == "TupleExpression":
        comps = node.get("components", [])
        names = []
        for c in comps:
            if c:
                names.append(resolve_name(c))
        return ", ".join(names)
    return ""