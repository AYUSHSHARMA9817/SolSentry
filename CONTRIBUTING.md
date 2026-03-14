# Contributing to SolSentry

Thanks for your interest in contributing to **SolSentry** — a static security analyzer for Solidity smart contracts. This document covers everything you need to get started, whether you're fixing a bug, adding a new vulnerability detector, or improving documentation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Code Style](#code-style)
- [Detector Ideas & Roadmap](#detector-ideas--roadmap)

---

## Project Overview

SolSentry works in a 5-stage pipeline:

```
Solidity Contract
      ↓
  solc Compilation
      ↓
  AST Extraction
      ↓
  IR Generation
      ↓
Vulnerability Detectors
      ↓
  Security Report
```

Each **detector** is an independent module that receives the IR of a function and emits findings. This modularity is intentional — you can add a new detector without touching anything else.

---

## Getting Started

### Prerequisites

- Python 3.9+
- `solc` (Solidity compiler) — install via ```sudo snap install solc --edge ```.
- Git

### Setup

```bash
git clone https://github.com/AYUSHSHARMA9817/SolSentry.git
cd SolSentry
```

### Run on a contract

```bash
python3 main.py test.sol
```
---

## Project Structure

```
SolSentry/
│
├── compiler/
│   └── solc_runner.py
│
├── detectors/
│   ├── access_control.py
│   ├── delegatecall.py
│   ├── eth_transfer.py
│   ├── reentrancy.py
│   ├── unchecked_call.py
│   ├── value_check.py
│   └── vulnerability_summary.py
│
├── ir/
│   └── ast_walker.py
│
├── parser/
│   ├── function_extractor.py
│   ├── function_summary.py
│   ├── modifier_extractor.py
│   ├── modifier_summary.py
│   ├── name_resolver.py
│   └── state_vars.py
│
├── printers/
│   ├── function_print.py
│   ├── modifier_print.py
│   └── vulnerable_functions_print.py
│
├── main.py
└── test.sol
```

---

## Submitting a Pull Request

1. **Fork** the repo and create a branch:
   ```bash
   git checkout -b feat/my-new-detector
   ```

2. Make your changes and ensure to test it properly.

3. Keep commits focused — one logical change per commit.

4. Open a PR against `main` with:
   - A clear title: `[Detector] Add tx.origin authentication detector`
   - What vulnerability it detects and the SWC ID if applicable
   - Sample vulnerable contract snippet in the PR description
   - False positive rate if you've measured it

5. I will review within a few days. Be ready to iterate.

---

## Reporting Issues

Use [GitHub Issues](https://github.com/AYUSHSHARMA9817/SolSentry/issues) and include:

- The Solidity contract (or a minimal reproducer)
- The SolSentry command you ran
- Expected output vs actual output
- Your `solc` version (`solc --version`)

For **false positives** (detector fires on safe code), label the issue `false-positive` — these are high priority.

For **false negatives** (detector misses a real vulnerability), label it `missed-detection` and include the vulnerability class.

---

## Code Style

- Follow **PEP 8** with a line length of 100.
- Use type hints everywhere.
- Docstrings on all public classes and methods.
- Run `black .` before committing (formatter is enforced in CI).

---

## Detector Ideas & Roadmap

Looking for something to work on? Here are open detector ideas:

| Detector | Vulnerability | SWC ID | Difficulty |
|---|---|---|---|
| `tx_origin` | Authentication via `tx.origin` | SWC-115 | Easy |
| `integer_overflow` | Unchecked arithmetic (pre-0.8) | SWC-101 | Medium |
| `selfdestruct` | Unprotected `selfdestruct` | SWC-106 | Easy |
| `timestamp_dependence` | `block.timestamp` misuse | SWC-116 | Medium |
| `front_running` | Unprotected state before external call | SWC-114 | Hard |
| `storage_collision` | Proxy storage slot collisions | — | Hard |
| `cross_function_reentrancy` | Reentrancy across multiple functions | SWC-107 | Hard |

If you're working on one of these, open a draft PR early so others know it's in progress.

---

## Questions?

Open a [GitHub Discussion](https://github.com/AYUSHSHARMA9817/SolSentry/discussions) or reach out via the issue tracker. Happy to help you get your detector merged.
