def modifier_list(ast_code):

    modifiers = []

    for node in ast_code.get("nodes", []):

        if node.get("nodeType") == "ContractDefinition":

            for sub in node.get("nodes", []):

                if(sub.get("nodeType") == "ModifierDefinition"):

                    modifiers.append(sub)

    return modifiers