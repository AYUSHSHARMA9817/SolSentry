from parser.modifier_summary import ModifierSummary
from ir.ast_walker import analyze_function

def print_modifiers(modifiers,state_set):
    modifier_summaries = {}
    for mod in modifiers:
            name = mod.get("name")
            nms = analyze_function(mod,state_set)
            modifier_summaries[name] = ModifierSummary(name,nms)
            print(f"\nModifier: {name}")

            for num, op, var in nms:
                if var != "require":
                    print(f"   ({num}, '{op}', '{var}')")
    return modifier_summaries