# detectors/

## Files

- `reentrancy.py`
- `delegatecall.py`
- `eth_transfer.py`
- `unchecked_call.py`
- `access_control.py`
- `value_check.py`
- `vulnerability_summary.py`

## Responsibility

Run heuristic checks on operation streams and aggregate vulnerability lists.

## Current surfacing

Printed in vulnerability output:

- Reentrancy
- Delegatecall
- ETH transfer usage
- Missing access control
- Unchecked call

Computed in function summary but not currently printed in final vulnerability list:

- Value check