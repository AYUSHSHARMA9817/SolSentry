import sys

from compiler.solc_runner import compile_solidity
from parser.state_vars import state_vars
from parser.function_extractor import function_list
from parser.modifier_extractor import modifier_list
from printers.modifier_print import print_modifiers
from printers.function_print import print_func
from printers.vulnerable_functions_print import print_vulnerabilities
from detectors.vulnerability_summary import Vulnerability_Summary

def main():

    source = compile_solidity(sys.argv[1])

    state_set = state_vars(source)
    functions = function_list(source)
    modifiers = modifier_list(source)
    vulnerability_summaries = Vulnerability_Summary()
    print("\n=== Operations ===")

    modifier_summaries = print_modifiers(modifiers,state_set)
    print_func(functions,state_set,modifier_summaries,vulnerability_summaries)
    print_vulnerabilities(vulnerability_summaries)
    
if __name__ == "__main__":
    main()