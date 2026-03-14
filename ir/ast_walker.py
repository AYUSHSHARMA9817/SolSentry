from parser.name_resolver import resolve_name


def is_external_call(name):

    return any(x in name for x in [
        ".call",
        ".delegatecall",
        ".transfer",
        ".send",
        ".staticcall",
        ".balanceOf",
        ".transferFrom"
    ])

#--------------------- Extract Visibility -----------------
def analyze_visibility(func):

    vis = func.get("visibility")
    if vis == None:
        vis = "external"
    return vis



#--------------------- Extract Mutability -----------------
def analyze_mutability(func):

    vis = func.get("stateMutabilityity")
    if vis == None:
        vis = ""
    return vis

# -------------------- Analyze Function --------------------
def analyze_function(func, state_set):

    operations = []
    counter = [0]

    body = func.get("body")

    if not body:
        return operations

    for stmt in body.get("statements", []):
        process(stmt, operations, state_set, counter)

    return operations


def analyze_func_modifiers(func):

    mods = []

    for mod in func.get("modifiers", []):
        name = mod.get("modifierName", {}).get("name")

        if name:
            mods.append(name)

    return mods


# -------------------- AST Walker --------------------
def process(node, operations, state_set, counter):

    if not isinstance(node, dict):
        return

    nt = node.get("nodeType")

    # ---------------- Block ----------------
    if nt == "Block":
        for s in node.get("statements", []):
            process(s, operations, state_set, counter)

    # ---------------- Expression Statement ----------------
    elif nt == "ExpressionStatement":
        process(node.get("expression"), operations, state_set, counter)

    # ---------------- Assignment ----------------
    elif nt == "Assignment":

        left = node.get("leftHandSide")
        right = node.get("rightHandSide")

        process(right, operations, state_set, counter)

        left_name = resolve_name(left)
        base = left_name.split("[")[0]

        if base in state_set:
            counter[0] += 1
            operations.append((counter[0], "state_write", left_name))

    # ---------------- Binary Operation ----------------
    elif nt == "BinaryOperation":

        process(node.get("leftExpression"), operations, state_set, counter)
        process(node.get("rightExpression"), operations, state_set, counter)

    # ---------------- Unary Operation ----------------
    elif nt == "UnaryOperation":
        sub = node.get("subExpression")
        name = resolve_name(sub)
        base = name.split("[")[0]
        if base in state_set:
            counter[0] += 1
            operations.append((counter[0], "state_write", name))

        process(sub, operations, state_set, counter)

    # ---------------- Index Access ----------------
    elif nt == "IndexAccess":

        name = resolve_name(node)
        base = resolve_name(node.get("baseExpression"))
        if base in state_set:
            counter[0] += 1
            operations.append((counter[0], "state_read", name))
    
        process(node.get("indexExpression"), operations, state_set, counter)
        

    # ---------------- Member Access ----------------
    elif nt == "MemberAccess":
        process(node.get("expression"), operations, state_set, counter)

    # ---------------- Identifier ----------------
    elif nt == "Identifier":

        name = node.get("name")

        if name in state_set:
            counter[0] += 1
            operations.append((counter[0], "state_read", name))

    # ---------------- Function Call ----------------
    elif nt == "FunctionCall":

        if node.get("kind") == "typeConversion":
            for arg in node.get("arguments", []):
                process(arg, operations, state_set, counter)
            return
        
        expr = node.get("expression")
        call_name = resolve_name(expr)

        if not call_name:
            call_name = "unknown_call"

        req = require_parser(node)

        if req:
            cond, msg = req

            counter[0] += 1
            operations.append((counter[0], "require_condition", cond))

        for arg in node.get("arguments", []):
            process(arg, operations, state_set, counter)

        process(expr, operations, state_set, counter)

        counter[0] += 1

        if is_external_call(call_name):
            operations.append((counter[0], "external_call", call_name))
        elif ".push" in call_name:
            operations.append((counter[0], "state_write", call_name.split(".push")[0]))
        else:
            operations.append((counter[0], "function_call", call_name))

    # ---------------- Variable Declaration ----------------
    elif nt == "VariableDeclarationStatement":

        init = node.get("initialValue")

        if init:
            process(init, operations, state_set, counter)

    # ---------------- If Statement ----------------
    elif nt == "IfStatement":

        process(node.get("condition"), operations, state_set, counter)

        cond = resolve_name(node.get("condition"))

        counter[0]+=1
        operations.append((counter[0],"IF_COND",cond))

        process(node.get("trueBody"), operations, state_set, counter)

        if node.get("falseBody"):
            counter[0]+=1
            operations.append((counter[0],"ELSE",""))

            process(node.get("falseBody"), operations, state_set, counter)

        counter[0]+=1
        operations.append((counter[0],"ENDIF",""))

    elif nt == "ForStatement":

        counter[0]+=1
        operations.append((counter[0],"FOR_INIT",""))

        process(node.get("initializationExpression"), operations, state_set, counter)

        counter[0]+=1
        operations.append((counter[0],"FOR_COND", resolve_name(node.get("condition"))))

        process(node.get("body"), operations, state_set, counter)

        counter[0]+=1
        operations.append((counter[0],"FOR_ITER",""))

        process(node.get("loopExpression"), operations, state_set, counter)

        counter[0]+=1
        operations.append((counter[0],"ENDFOR",""))

    elif nt == "WhileStatement":

        cond = resolve_name(node.get("condition"))

        counter[0]+=1
        operations.append((counter[0],"WHILE",cond))

        process(node.get("body"), operations, state_set, counter)

        counter[0]+=1
        operations.append((counter[0],"ENDWHILE",""))

    elif nt == "Break":
        counter[0]+=1
        operations.append((counter[0],"BREAK",""))

    elif nt == "Continue":
        counter[0]+=1
        operations.append((counter[0],"CONTINUE",""))

    elif nt == "Return":
        expr = node.get("expression")

        if expr:
            val = resolve_name(expr)
        else:
            val = ""

        counter[0]+=1
        operations.append((counter[0], "RETURN", val))

    # ---------------- FunctionCallOptions ----------------
    elif nt == "FunctionCallOptions":

        process(node.get("expression"), operations, state_set, counter)

        for opt in node.get("options", []):
            process(opt, operations, state_set, counter)
    elif nt == "TupleExpression":
        for comp in node.get("components", []):
            process(comp, operations, state_set, counter)

    elif nt == "Conditional":
        process(node.get("condition"), operations, state_set, counter)
        process(node.get("trueExpression"), operations, state_set, counter)
        process(node.get("falseExpression"), operations, state_set, counter)

def require_parser(node):
    expr = node.get("expression")
    if not isinstance(expr,dict):
        return None
    if expr.get("nodeType") == "Identifier" and expr.get("name") == "require":
        args = node.get("arguments",[])
        if len(args) == 0:
                return None
        cond_node = args[0]
        # unwrap tuple
        if cond_node.get("nodeType") == "TupleExpression":
            comps = cond_node.get("components", [])
            if comps:
                cond_node = comps[0]
        condition = resolve_name(cond_node)
        message = None
        if len(args) > 1:
            message = args[1].get("value")

        return (condition, message)
    return None
