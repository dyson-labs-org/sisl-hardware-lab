# SISL Hardware Lab

SISL Hardware Lab is the working repository for Dyson SCI hackathon implementation work around the Secure Inter-Satellite Link (SISL) protocol.

This repo is intentionally scaffolded for rapid iteration across:
- protocol implementation
- radio/SDR experiments
- session/key management prototypes
- test vectors and repeatable experiment logs

## Quick Start

### 1. Create a virtual environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -e .[dev]
```

### 3. Run checks

```powershell
ruff check src tests
pytest
```

### 4. Run a smoke demo

```powershell
python examples/quickstart.py
```

## Repository Layout

```text
.
|-- configs/                  # Runtime and lab configuration files
|-- docs/                     # Architecture notes, protocol notes, experiment logs
|-- examples/                 # Minimal runnable examples
|-- scripts/                  # Local helper scripts
|-- src/sisl_hardware_lab/    # Python package
|   |-- crypto/               # Key derivation scaffolding
|   |-- protocol/             # Frame and hail message helpers
|   |-- radio/                # Radio abstractions + simulation stubs
|   |-- session/              # Session lifecycle management
|   `-- utils/                # Shared utilities
`-- tests/                    # Unit tests for skeleton behavior
```

## Hackathon References

- SISL protocol spec: https://github.com/dyson-labs-org/scrap/blob/master/spec/SISL.md
- Hardware BOM seeds are tracked in [`docs/hardware/bill-of-materials.md`](docs/hardware/bill-of-materials.md)

## Upload To GitHub

Your `origin` remote is already configured to:

`https://github.com/dyson-labs-org/sisl-hardware-lab.git`

To publish this scaffold:

```powershell
git add .
git commit -m "Scaffold SISL hardware lab repository structure"
git push origin main
```

## License

MIT License. See `LICENSE`.
