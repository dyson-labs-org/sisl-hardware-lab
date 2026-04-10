$ErrorActionPreference = "Stop"

if (Test-Path ".\.venv\Scripts\python.exe") {
    & .\.venv\Scripts\python -m pytest
} else {
    python -m pytest
}
