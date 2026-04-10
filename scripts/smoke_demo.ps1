$ErrorActionPreference = "Stop"

if (Test-Path ".\.venv\Scripts\python.exe") {
    & .\.venv\Scripts\python examples/quickstart.py
} else {
    python examples/quickstart.py
}
