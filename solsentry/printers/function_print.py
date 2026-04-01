from solsentry.parser.function_summary import FunctionSummary
from solsentry.parser.modifier_summary import ModifierSummary
from solsentry.ir.ast_walker import analyze_function, analyze_func_modifiers, analyze_visibility, analyze_mutability

def print_func(functions,state_set,modifier_summaries,vulnerability_summaries):
    for func in functions:

            name = func.get("name") or "constructor"
            ops = analyze_function(func, state_set)
            mods = analyze_func_modifiers(func)
            visibility = analyze_visibility(func)
            mutability = analyze_mutability(func)
            modifier_summary = []


            print(f"\nFunction: {name}")
            if(len(mods) > 0):
                print(f"\nModifiers Used:")
                for i in mods:
                    print(f" {i} ")
                    summary = modifier_summaries.get(i)
                    if summary:
                        modifier_summary.append(summary)
                    else:
                        modifier_summaries[i] = ModifierSummary(i,[])
                        modifier_summary.append(modifier_summaries[i])
                print("\n")

            summary = FunctionSummary(name,ops,modifier_summary,visibility,mutability)

            for num, op, var in ops:
                print(f"   ({num}, '{op}', '{var}')")

            if(name != "constructor"):
                if(summary.reentrancy):
                    vulnerability_summaries.reentrancy.append(name)

                if(summary.delegatecall):
                    vulnerability_summaries.delegatecall.append(name)

                if(summary.eth_transfer):
                    vulnerability_summaries.eth_transfer.append(name)

                if (summary.access_control == False and summary.visibility in ["external","public"]):
                    vulnerability_summaries.missing_access_control.append(name)

                if(summary.unchecked_call):
                    vulnerability_summaries.unchecked_call.append(name)