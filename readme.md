
---

# 🔍 Solidity Static Analyzer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Solidity](https://img.shields.io/badge/solidity-0.8.x-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Security](https://img.shields.io/badge/security-analysis-red)

A **static analysis tool for Solidity smart contracts** that detects common security vulnerabilities using **AST parsing and intermediate representation (IR)**.

The analyzer compiles Solidity contracts with `solc`, extracts the AST, builds a **custom IR**, and runs **detectors for security vulnerabilities**.

Designed as a **research-oriented security tool** similar in spirit to:

* Slither
* Mythril
* Semgrep

---

# ⚡ Features

### 🔎 Static Analysis

* Solidity AST parsing
* Intermediate Representation (IR) generation
* Modifier analysis
* Visibility analysis

---

### 🛡 Vulnerability Detection

Current detectors include:

| Detector               | Description                                 |
| ---------------------- | ------------------------------------------- |
| Reentrancy             | Detects state writes after external calls   |
| Delegatecall           | Flags unsafe `delegatecall` usage           |
| Unchecked Call         | External calls without validation           |
| ETH Transfer           | Detects `.call`, `.send`, `.transfer`       |
| Missing Access Control | State-changing functions without protection |
| Value Checks           | Validates require conditions on values      |

---

# 🧠 Architecture

The analyzer follows a **multi-stage static analysis pipeline**.

```
Solidity Contract
       │
       ▼
     solc
       │
       ▼
      AST
       │
       ▼
 Intermediate Representation (IR)
       │
       ▼
 Function Analysis
       │
       ▼
 Vulnerability Detectors
       │
       ▼
 Vulnerability Summary
```

---

# 🗂 Project Structure

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

# 🚀 Usage

### 1️⃣ Install Solidity compiler

```
sudo snap install solc --edge
```

Verify:

```
solc --version
```

---

### 2️⃣ Run the analyzer

```
python3 main.py Contract.sol
```

---

# 📊 Example Output

```
=== Operations ===

Modifier: onlyOwner
   (1, 'require_condition', 'msg.sender == owner')
   (2, 'state_read', 'owner')

Function: withdraw

Modifiers Used:
 onlyWhitelisted

   (1, 'state_read', 'balances[msg.sender]')
   (2, 'require_condition', 'bal >= amount')
   (3, 'external_call', 'msg.sender.call')
   (4, 'state_write', 'balances[msg.sender]')

(Potentially) Reentrancy Vulnerable Functions:
 withdraw
 complexFlow
```

---

# 🔬 Current Analysis Model

The analyzer converts Solidity code into a **custom IR operation stream**.

Example IR:

```
(1, state_read, balances[msg.sender])
(2, external_call, msg.sender.call)
(3, state_write, balances[msg.sender])
```

This representation allows detectors to identify patterns such as:

```
state_read → external_call → state_write
```

which indicates **possible reentrancy**.

---

# 🧩 Modifiers Support

The analyzer resolves modifiers and propagates their security properties.

Example:

```
modifier onlyOwner {
    require(msg.sender == owner);
}
```

The system detects:

```
access_control = True
```

and applies it to functions using the modifier.

---

# 🛠 Planned Features

Next major upgrades:
```
✔ AST Parsing
✔ IR Generation
✔ Security Detectors
⬜ Control Flow Graph (CFG)
⬜ Path-Sensitive Analysis
⬜ Call Graph Construction
⬜ Inter-Function Analysis
⬜ Advanced Vulnerability Detection
```

### Control Flow Graph (CFG)

```
IR
 │
 ▼
Basic Blocks
 │
 ▼
Control Flow Graph
```

This will enable:

* Path-sensitive analysis
* Branch-aware vulnerability detection
* Loop analysis
* Multi-path reentrancy detection

---

### Future Detectors

Planned detectors include:

* Integer overflow patterns
* Reentrancy via cross-function calls
* Dangerous `tx.origin`
* Storage collision (proxy patterns)
* Uninitialized storage pointers

---

# 📚 Learning Goals

This project is also a **research implementation of static analysis concepts**, including:

* AST traversal
* Intermediate representations
* Control flow graphs
* Security pattern detection

---

# 🤝 Contributing

Contributions are welcome.

Possible contributions:

* New vulnerability detectors
* CFG implementation
* IR improvements
* Performance optimizations
* Visualization tools

---

# 📜 License

MIT License

---

# ⭐ Acknowledgments

Inspired by:

* Slither
* Mythril
* Solidity AST documentation

---

# 👨‍💻 Author

**Ayush Sharma**
B.Tech CSE — IIT Guwahati

Focus areas:

* Smart Contract Security
* Static Analysis
* Web3 Infrastructure

---

# ⭐ Future Vision

SOL-Parser aims to become a **lightweight research framework for Solidity analysis**, enabling experimentation with:

* CFG-based vulnerability detection
* symbolic reasoning
* security pattern mining

---



