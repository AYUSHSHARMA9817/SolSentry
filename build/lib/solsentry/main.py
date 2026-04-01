import sys
import os

from solsentry.compiler.solc_runner import compile_solidity
from solsentry.parser.state_vars import state_vars
from solsentry.parser.function_extractor import function_list
from solsentry.parser.modifier_extractor import modifier_list
from solsentry.printers.modifier_print import print_modifiers
from solsentry.printers.function_print import print_func
from solsentry.printers.vulnerable_functions_print import print_vulnerabilities
from solsentry.detectors.vulnerability_summary import Vulnerability_Summary
from solsentry.printers.function_cfg import flow_graph

def main():
    if(len(sys.argv) < 2):
        print("Usage: solsentry <file name>")
    file = sys.argv[1]
    file = os.path.abspath(file)
    
    print(f"Analysing {file}")
    source = compile_solidity(file)

    state_set = state_vars(source)
    functions = function_list(source)
    modifiers = modifier_list(source)
    vulnerability_summaries = Vulnerability_Summary()
    print("\n=== Operations ===")

    modifier_summaries = print_modifiers(modifiers,state_set)
    print_func(functions,state_set,modifier_summaries,vulnerability_summaries)
    print_vulnerabilities(vulnerability_summaries)
    flow_graph(functions,state_set)
    
if __name__ == "__main__":
    main()