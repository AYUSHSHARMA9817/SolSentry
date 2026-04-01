# SolSentry

Static analyzer for Solidity contracts using AST parsing, IR-like operation extraction, detector passes, and CFG rendering.

## Quick Start

```bash
cd /home/ayush/SolSentry
python3 -m pip install -e .
solc --version
dot -V
solsentry /path/to/Contract.sol
```

## Repository Docs

- Package overview: `solsentry/README.md`
- Documentation index: `docs/README.md`
- Architecture: `docs/architecture.md`
- Detectors: `docs/detectors.md`
- Usage: `docs/usage.md`
- Development notes: `docs/development.md`

## Package Layout

- `solsentry/compiler/` — Solidity compilation and remappings
- `solsentry/ir/` — AST walking and operation extraction
- `solsentry/parser/` — function/modifier/state extraction and summaries
- `solsentry/detectors/` — vulnerability checks
- `solsentry/cfg/` — basic-block CFG builder
- `solsentry/printers/` — terminal output + CFG visualization