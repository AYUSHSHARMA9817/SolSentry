# Architecture

## Pipeline

```text
Solidity source
  -> solc_runner.compile_solidity()
  -> AST
  -> parser: state_vars/function_list/modifier_list
  -> ir.ast_walker.analyze_function()
  -> FunctionSummary detector evaluation
  -> vulnerability summary print
  -> CFG block build + graphviz render
```

## Main entrypoint

`solsentry/main.py`:

- parses CLI file argument
- compiles source
- computes summaries
- prints analysis
- calls `flow_graph()` to render CFG

## Key modules

- `compiler/solc_runner.py`  
  Handles project-root detection and optional `remappings.txt`.

- `ir/ast_walker.py`  
  Converts AST statements/expressions into operation tuples:
  `(index, op_type, value)`.

- `parser/function_summary.py`  
  Runs detector functions and applies modifier-derived security attributes.

- `cfg/basic_blocks.py`  
  Converts operation stream into basic blocks and control-flow edges.

- `printers/*`  
  Human-readable output and CFG graph generation.

## Known behavior notes

- CFG supports IF/FOR/RETURN/REQUIRE and function-call linking.
- While-loop CFG path is partially mismatched due to op-name inconsistency (`WHILE` vs `WHILE_COND`).