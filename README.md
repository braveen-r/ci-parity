# ⚖️ ci-parity-cli

> A terminal engine that proactively compares your local development environment against GitHub Actions CI pipelines to eliminate "works on my machine" errors before you even commit.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python&logoColor=white)
![PyPI](https://img.shields.io/badge/PyPI-v0.1.3-F1C40F.svg?style=flat-square&logo=pypi&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF.svg?style=flat-square&logo=github-actions&logoColor=white)
![Terminal](https://img.shields.io/badge/UI-Rich_TUI-8A2BE2.svg?style=flat-square&logo=linux&logoColor=white)

---

## 🎯 Overview

**ci-parity-cli** bridges the blind spot between a developer's physical laptop and the cloud server where their code will eventually run. By parsing your project's `.github/workflows/*.yml` files and cross-referencing them against your local system state (OS, Node, Python, Docker services, Env Vars), it detects version mismatches and missing infrastructure instantly. If your CI runs Node 22 on Ubuntu but your local machine runs Node 26 on Arch Linux, `ci-parity-cli` catches the drift and generates the exact CLI commands needed to fix it.

---

## 💻 Development Environment

This project was natively engineered and tested in the following environment:

* **Operating System:** Arch Linux (Wayland / Hyprland)
* **Terminal Environment:** `sunraku` (ZSH / Foot)
* **Core Languages/Tools:** Python 3.14 (Typer, Rich, PyYAML)
* **Package Management & Build System:** `uv`, `hatchling`

---

## 🚀 Installation

Because `ci-parity-cli` is published on the global Python Package Index (PyPI), you can run it instantly without manual installation or cloning using `uvx`.

### Zero-Install Execution (Recommended)

If you have `uv` installed, simply run the tool from anywhere on your system:

```bash
uvx ci-parity-cli check

```

### Local Development Setup

If you want to contribute or modify the source code:

1. **Clone the repository:**

```bash
git clone https://github.com/Braveen811/ci-parity.git
cd ci-parity

```

2. **Build and test locally with `uv`:**

```bash
uv run python ci_parity/main.py check

```

---

## 🎮 How to Run (Usage)

### 1. Check Environment Parity

Navigate to any project repository containing a `.github/workflows/` directory and run the engine:

```bash
uvx ci-parity-cli check

```

*The engine will output a styled `Rich` table comparing `EXPECTED (CI)` against `ACTUAL (LOCAL)`, immediately followed by recommended fix commands (e.g., `uv python install 3.12`, `docker run postgres`).*

### 2. Explain CI Failures

Translate cryptic GitHub Actions pipeline errors into plain-English root causes:

```bash
uvx ci-parity-cli explain https://github.com/user/repo/actions/runs/123

```

*Extracts the failing log step and provides AI-driven or heuristic insights on missing dependencies or version conflicts.*

---

## 🏗️ System Architecture

```text
[ .github/workflows/ci.yml ] ──────┐
                                   ▼
                            [ YAML Parser ]
                                   │
                                   ▼
[ Local OS & Binaries ] ───► [ Probe Engine ] 
                                   │
                                   ▼
                       [ Semantic Version Comparator ]
                                   │
                                   ▼
               [ Rich TUI Matrix & Actionable Fix Generator ]

```

---

## 🛠️ Tech Stack

* **CLI Interface Framework:** `Typer` (Strict argument parsing and command routing)
* **Terminal UI & Styling:** `Rich` (Tables, Panels, and Theme formatting)
* **Configuration Parsing:** `PyYAML` (GitHub Actions workflow extraction)
* **Distribution & Build:** `uv`, `hatchling`, PyPI

---

## 📂 Project Structure

```text
ci-parity/
├── ci_parity/
│   ├── parsers/
│   │   └── workflows.py     # Parses GitHub Actions YAML files
│   ├── probes/
│   │   └── local.py         # Inspects physical machine state (OS, Node, Docker)
│   ├── compare/
│   │   └── versions.py      # Semantic version logic (major/minor mismatch evaluation)
│   ├── fixes/
│   │   └── suggestions.py   # Generates automated CLI fixes (nvm, uv, docker)
│   ├── explain/
│   │   └── analyzer.py      # Analyzes failing CI logs
│   └── main.py              # Core Typer application and Rich TUI layout
├── pyproject.toml           # Hatchling build config and dependencies
└── README.md

```

---

## 🚀 Key Features

* **Cross-Platform OS Detection:** Automatically translates and maps CI environments (e.g., `ubuntu-24.04`) against your physical machine (`Arch Linux`, `Windows`, `macOS`).
* **Semantic Version Drift Detection:** Differentiates between harmless minor version bumps (Python 3.12 vs 3.14) and pipeline-breaking major version differences (Node 22 vs 26).
* **Service & Infrastructure Probing:** Actively pings your local Docker daemon and shell environment to verify if required CI databases (like `postgres:16`) and `ENV_VARS` are actively running locally.
* **Copy-Paste Fix Suggestions:** Doesn't just point out errors—it writes the exact terminal commands needed to sync your environment (`nvm use`, `docker run`, `export`).

---

## ⚙️ Custom Tweaks & Architecture Decisions

* **UX-First Table Headers:** Early iterations used `CI` and `YOU`. This was refactored to `EXPECTED (CI)` and `ACTUAL (LOCAL)` to instantly orient developers on exactly what the data represents (Cloud Server vs Physical Laptop).
* **Graceful Directory Degradation:** If executed in a directory lacking a `.github/workflows` folder (like a system home directory), the tool catches the empty state and exits cleanly with a helpful Rich-formatted error panel, preventing obscure stack traces.
* **PyPI Typosquatting Prevention:** The internal package logic remains `ci_parity`, but the PyPI distribution and command-line execution are explicitly mapped to `ci-parity-cli` in the `pyproject.toml` to bypass global naming collisions and establish a professional CLI namespace.

---

## 🛠️ System Tweaks & Troubleshooting

* **`uvx` Aggressive Caching:** `uvx` caches remote PyPI binaries to execute instantly. If a new version of `ci-parity-cli` is released but you are still seeing old UI elements, force a cache overwrite:
```bash
uvx --force-reinstall ci-parity-cli@latest check

```


* **"❌ No CI configuration found":** `ci-parity-cli` is context-aware. You must be standing directly inside a Git repository that has a `.github/workflows` directory for the tool to have something to compare your local system against.

---

**Author:** [Braveen R](https://braveenr.linklee.in/)

---

## ✌️ Wrapping Up

Stop playing guessing games with your CI/CD pipelines. Sync your environment, generate your fixes, and guarantee your code works on the cloud server before it ever leaves your terminal! 🚀

See you in the terminal!
