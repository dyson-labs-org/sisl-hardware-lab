param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

& $Python -m venv .venv
& .\.venv\Scripts\python -m pip install --upgrade pip
& .\.venv\Scripts\python -m pip install -e .[dev]

Write-Host "Environment bootstrapped."
