# cfg/

## Files

- `basic_blocks.py`

## Responsibility

- Build `BasicBlock` graph from operation stream
- Track next/prev block links
- Mark terminal blocks (`return`, etc.)
- Return block graph for visualization layer

## Notes

CFG is functional but still evolving for loop/path precision.