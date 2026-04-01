# ir/

## Files

- `ast_walker.py`

## Responsibility

- Walk Solidity AST nodes
- Convert statements/expressions into operation tuples
- Detect external-call-like operations
- Extract function-level metadata (visibility, mutability, modifiers used)

## Output Shape

Typical operation tuple:

```text
(index, operation_type, value)
```

Used by detector and CFG stages.