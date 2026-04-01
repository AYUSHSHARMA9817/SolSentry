def print_vulnerabilities(vulnerability_summaries):  
    print("\n(Potentially) Reentrancy Vulnerable Functions:")
    for op in vulnerability_summaries.reentrancy:
        print(f" {op} ")

    print("\n(Potentially) DelegateCall Vulnerable Functions:")
    for op in vulnerability_summaries.delegatecall:
        print(f" {op} ")

    print("\n(Potentially vulnerable) Having Eth_Transfer Functions:")
    for op in vulnerability_summaries.eth_transfer:
        print(f" {op} ")

    print("\n(Potentially) Missing Access Control Vulnerable Functions:")
    for op in vulnerability_summaries.missing_access_control:
        print(f" {op} ")

    print("\n(Potentially) Unchecked Call Vulnerable Functions:")
    for op in vulnerability_summaries.unchecked_call:
        print(f" {op} ")