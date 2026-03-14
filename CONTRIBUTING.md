# Contributing to SolSentry

Thanks for your interest in contributing to **SolSentry** — a static security analyzer for Solidity smart contracts. This document covers everything you need to get started, whether you're fixing a bug, adding a new vulnerability detector, or improving documentation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [How to Add a New Detector](#how-to-add-a-new-detector)
- [Writing Tests](#writing-tests)
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
- `solc` (Solidity compiler) — install via [solc-select](https://github.com/crytic/solc-select)
- Git

### Setup

```bash
git clone https://github.com/AYUSHSHARMA9817/SolSentry.git
cd SolSentry
pip install -r requirements.txt
```

### Run on a contract

```bash
python solsentry.py analyze --file contracts/Example.sol
```

### Run tests

```bash
pytest tests/
```

---

## Project Structure

```
SolSentry/
├── solsentry.py              # CLI entrypoint
├── core/
│   ├── compiler.py           # Invokes solc, captures AST JSON
│   ├── ast_parser.py         # Walks AST nodes → raw IR instructions
│   ├── ir.py                 # IR data structures (Instruction, Function, Contract)
│   └── report.py             # Formats and outputs findings
├── detectors/
│   ├── base.py               # BaseDetector abstract class — all detectors inherit this
│   ├── reentrancy.py         # Reentrancy detector
│   ├── delegatecall.py       # Delegatecall misuse detector
│   ├── unchecked_calls.py    # Unchecked external call return values
│   ├── unsafe_eth.py         # Unsafe ETH transfer patterns
│   └── access_control.py     # Missing access control (onlyOwner / modifier checks)
├── tests/
│   ├── contracts/            # Vulnerable + safe Solidity fixtures
│   └── test_detectors.py     # Per-detector unit tests
└── docs/
    └── ir_spec.md            # IR instruction format reference
```

---

## How to Add a New Detector

All detectors live in `detectors/` and inherit from `BaseDetector`.

### Step 1 — Create your detector file

```python
# detectors/my_detector.py

from detectors.base import BaseDetector, Finding, Severity

class MyDetector(BaseDetector):
    """
    Detects <describe the vulnerability>.

    Vulnerability class: <e.g. SWC-107>
    References: <link to SWC registry or research>
    """

    NAME = "my-detector"
    DESCRIPTION = "Short human-readable description shown in report"
    SEVERITY = Severity.HIGH  # LOW | MEDIUM | HIGH | CRITICAL

    def analyze(self, function) -> list[Finding]:
        findings = []

        for i, instr in enumerate(function.instructions):
            # Your detection logic here
            # instr is a tuple: (line_no, opcode, operand)
            # e.g. ('external_call', 'msg.sender.call')

            if self._is_vulnerable(function.instructions, i):
                findings.append(Finding(
                    detector=self.NAME,
                    severity=self.SEVERITY,
                    function=function.name,
                    line=instr[0],
                    message=f"Potential <vulnerability> in `{function.name}` at line {instr[0]}",
                ))

        return findings

    def _is_vulnerable(self, instructions, idx):
        # Helper logic
        return False
```

### Step 2 — Register your detector

In `core/report.py` (or wherever detectors are loaded), add your detector to the registry:

```python
from detectors.my_detector import MyDetector

DETECTORS = [
    ReentrancyDetector(),
    DelegateCallDetector(),
    UncheckedCallsDetector(),
    UnsafeEthDetector(),
    AccessControlDetector(),
    MyDetector(),  # ← add here
]
```

### Step 3 — Add test fixtures

Create two Solidity files in `tests/contracts/`:

- `my_vuln_vulnerable.sol` — a contract that **should** trigger your detector
- `my_vuln_safe.sol` — a contract that **should not** trigger your detector

Then add tests in `tests/test_detectors.py`:

```python
def test_my_detector_flags_vulnerable():
    findings = run_detector(MyDetector, "tests/contracts/my_vuln_vulnerable.sol")
    assert len(findings) > 0

def test_my_detector_ignores_safe():
    findings = run_detector(MyDetector, "tests/contracts/my_vuln_safe.sol")
    assert len(findings) == 0
```

---

## Writing Tests

- Every detector **must** have both a vulnerable and a safe fixture.
- Tests live in `tests/test_detectors.py`.
- Use the `run_detector(DetectorClass, filepath)` helper (defined in `tests/conftest.py`) — it handles compilation and IR generation for you.
- Aim for edge cases: modifiers, inheritance, internal calls, try/catch blocks.

---

## Submitting a Pull Request

1. **Fork** the repo and create a branch:
   ```bash
   git checkout -b feat/my-new-detector
   ```

2. Make your changes and ensure tests pass:
   ```bash
   pytest tests/ -v
   ```

3. Keep commits focused — one logical change per commit.

4. Open a PR against `main` with:
   - A clear title: `[Detector] Add tx.origin authentication detector`
   - What vulnerability it detects and the SWC ID if applicable
   - Sample vulnerable contract snippet in the PR description
   - False positive rate if you've measured it

5. A maintainer will review within a few days. Be ready to iterate.

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
