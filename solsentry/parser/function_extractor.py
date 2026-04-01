def function_list(ast_code):

    functions = []

    for node in ast_code.get("nodes", []):

        if node.get("nodeType") == "ContractDefinition":

            for sub in node.get("nodes", []):

                if sub.get("nodeType") == "FunctionDefinition" and sub.get("implemented"):
                    functions.append(sub)

    return functions