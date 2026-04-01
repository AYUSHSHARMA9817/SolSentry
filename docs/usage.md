# Usage

## Prerequisites

- Python 3.9+
- `solc`
- Graphviz (`dot` binary)

## Install

```bash
cd /home/ayush/SolSentry
python3 -m pip install -e .
```

## Run analyzer

```bash
solsentry /path/to/Contract.sol
```

Alternative:

```bash
python3 solsentry/main.py /path/to/Contract.sol
```

## Expected outputs

- Console operation traces per modifier/function
- Vulnerability lists grouped by detector
- `program_cfg.png` generated in current directory