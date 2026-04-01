def state_vars(ast_code):

    vars_set = set()

    for node in ast_code.get("nodes", []):
        if node.get("nodeType") == "ContractDefinition":

            for sub in node.get("nodes", []):

                if sub.get("nodeType") == "VariableDeclaration" and sub.get("stateVariable"):
                    vars_set.add(sub.get("name"))

    return vars_set
