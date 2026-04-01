# Detectors

## Reentrancy

File: `solsentry/detectors/reentrancy.py`

Signals:

- state read before external call, then state write
- or any state write after external call (`detect_state_after_call`)

## Delegatecall

File: `solsentry/detectors/delegatecall.py`

Signal:

- external call string containing `.delegatecall`

## ETH transfer usage

File: `solsentry/detectors/eth_transfer.py`

Signal:

- external call string containing `.call`, `.transfer`, `.send`

## Access control

File: `solsentry/detectors/access_control.py`

Signals:

- function visibility is `internal` or `private`
- or `require_condition` contains sender equality pattern

## Unchecked external call

File: `solsentry/detectors/unchecked_call.py`

Signal:

- external call not followed by observed `require` check before next external call

## Value check

File: `solsentry/detectors/value_check.py`

Signal:

- `require_condition` contains numeric comparator (`>`, `>=`, `<`, `<=`)

Note: This flag is currently computed in `FunctionSummary` but not emitted in final vulnerability list.