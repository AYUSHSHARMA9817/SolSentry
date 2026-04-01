# SolSentry

SolSentry is a static analyzer for Solidity smart contracts.  
It compiles contracts with `solc`, walks the AST, builds an operation-level IR, runs detectors, and prints potential vulnerabilities.

## What it does

- Compiles Solidity source to AST (`compiler/solc_runner.py`)
- Extracts:
  - state variables
  - functions
  - modifiers
- Builds operation streams from AST (`ir/ast_walker.py`)
- Runs detector checks (`detectors/`)
- Prints function operations, modifier effects, vulnerability lists
- Builds and renders a program CFG image (`program_cfg.png`) using Graphviz

## Implemented detectors

- Reentrancy (`reentrancy.py`)
- Delegatecall usage (`delegatecall.py`)
- ETH transfer call sites (`eth_transfer.py`)
- Missing access control signal (`access_control.py`)
- Unchecked external call (`unchecked_call.py`)
- Value check presence (`value_check.py`, currently computed but not printed in final summary)

## Project structure

```text
SolSentry/
├── setup.py
└── solsentry/
    ├── main.py
    ├── compiler/
    │   └── solc_runner.py
    ├── ir/
    │   └── ast_walker.py
    ├── parser/
    │   ├── state_vars.py
    │   ├── function_extractor.py
    │   ├── modifier_extractor.py
    │   ├── function_summary.py
    │   ├── modifier_summary.py
    │   └── name_resolver.py
    ├── detectors/
    │   ├── reentrancy.py
    │   ├── delegatecall.py
    │   ├── eth_transfer.py
    │   ├── access_control.py
    │   ├── unchecked_call.py
    │   ├── value_check.py
    │   └── vulnerability_summary.py
    ├── cfg/
    │   └── basic_blocks.py
    └── printers/
        ├── function_print.py
        ├── modifier_print.py
        ├── vulnerable_functions_print.py
        └── function_cfg.py
```

## Requirements

- Python `>=3.9`
- `solc` available in PATH
- Python package dependency: `graphviz>=0.20`
- Graphviz system binary (`dot`) for CFG rendering

## Install

```bash
cd /home/ayush/SolSentry
python3 -m pip install -e .
```

Install Solidity compiler (example on Linux snap):

```bash
sudo snap install solc --edge
solc --version
```

Install Graphviz binary (Ubuntu/Debian):

```bash
sudo apt-get update
sudo apt-get install -y graphviz
dot -V
```

## Run

Using console entry point:

```bash
solsentry /path/to/Contract.sol
```

Or direct module script:

```bash
python3 /home/ayush/SolSentry/solsentry/main.py /path/to/Contract.sol
```

## Output

The tool prints:

- modifier operations
- function operations
- vulnerability name lists:
  - reentrancy
  - delegatecall
  - eth transfer usage
  - missing access control
  - unchecked call

It also generates:

- `program_cfg.png` in the current working directory

## Notes and current limitations

- Analysis is pattern-based and may produce false positives/negatives.
- Access control detection is heuristic (e.g., `require(msg.sender == ...)` and visibility checks).
- Value-check analysis is computed but not surfaced in `vulnerable_functions_print.py`.
- CFG code currently expects `WHILE_COND`, while IR emits `WHILE`; while-loop CFG handling is therefore incomplete.

## Contributing

See `solsentry/CONTRIBUTING.md`.

## License

MIT (`solsentry/LICENSE`).



