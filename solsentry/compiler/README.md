# compiler/

## Files

- `solc_runner.py`

## Responsibility

- Locate project root from target file path
- Load `remappings.txt` (if present)
- Invoke `solc --combined-json ast`
- Return parsed AST JSON for downstream analysis

## Notes

- `solc` must be available in `PATH`.
- `lib/` is included as include-path by default.