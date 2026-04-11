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

## Hackathon Goal

Current focus is **Phase 1: DSSS hidden-signal demo**.

The immediate milestone is to show that:

1. a spread signal can be transmitted across bandwidth,
2. a passive observer does not see an obvious new signal,
3. the intended receiver can recover the payload with the correct spreading code, and
4. the wrong code fails to recover the payload.

This repo is **not** yet focused on full hail/ACK crypto or SCRAP-over-SISL integration. Those remain later phases after the RF path is bench-validated.

## Current Status

### Implemented in this branch
- Python repo bootstrap and smoke-demo path
- `START_HERE.md` operator notes for the hackathon workstream
- `configs/phase1_demo.toml` for intended Phase 1 parameters
- `docs/experiments/rf_bench_log.md` for bench logging
- software DSSS proof flowgraph (`spreadtest.grc`)
- first-pass split RF flowgraphs:
  - `dsss_rf_tx.grc`
  - `dsss_rf_rx.grc`
  - `dsss_rf_observer.grc`

### What that means
The project is now past pure scaffold stage and into **first-pass RF bench bring-up**.

The branch has the basic split needed for the demo narrative:
- **TX** sends a spread waveform
- **RX** knows the spreading code and attempts recovery
- **Observer** remains passive and code-unaware

### Still in progress
- aligning TX / RX / observer on final Phase 1 operating parameters
- bench-validating the live HackRF path
- comparing observer visibility against intended receiver recovery
- logging actual bench results into `docs/experiments/rf_bench_log.md`

### Not done yet
- final public-code 1023-chip Phase 1 flow locked down and verified on hardware
- recorded bench results in `docs/experiments/rf_bench_log.md`
- Phase 2 encrypted hail + ACK path
- Phase 3 SCRAP-over-SISL path

## GNU Radio Flowgraphs

### `spreadtest.grc`
Software-only DSSS proof used to validate the core signal chain before putting SDR hardware in the loop.

Purpose:
- map bits to BPSK symbols
- spread with a known code
- despread with the correct code
- compare against a wrong-code branch

### `dsss_rf_tx.grc`
Transmit-side flowgraph for the Phase 1 RF path.

Purpose:
- generate a known repeating payload
- map to BPSK
- spread with the current DSSS code
- drive a HackRF TX path
- provide local waveform / spectrum monitoring

### `dsss_rf_rx.grc`
Privileged receiver flowgraph.

Purpose:
- receive live RF from HackRF
- inspect the raw waveform
- apply the correct spreading code
- compare against a wrong-code branch
- recover and display the intended symbol stream

### `dsss_rf_observer.grc`
Passive observer flowgraph.

Purpose:
- receive live RF from HackRF
- show the band and raw waveform only
- perform no code-aware recovery

This graph is intentionally dumb. It models an observer who does not know the spreading code.

## Working Order

For bench bring-up:

1. start the observer first,
2. start the privileged receiver second,
3. start the transmitter last.

That reduces the chance of missing short TX bursts during debugging.

## Bench Logging

Use:
- `configs/phase1_demo.toml` for intended operating parameters
- `docs/experiments/rf_bench_log.md` for actual measured bench results

The key question is not just "how many dB down was the signal?" The real question is whether the observer fails to meaningfully recover the signal while the intended receiver still succeeds.

## Near-Term TODO

### Phase 1 completion
- align all flowgraphs to the intended Phase 1 hailing configuration
- run live HackRF TX/RX/observer bench tests
- dial attenuation until the observer view is uninteresting
- confirm correct-code recovery vs wrong-code failure on live RF
- log results in `docs/experiments/rf_bench_log.md`

### Repo cleanup
- clean `configs/phase1_demo.toml` into pure TOML if needed
- update graph titles and variable consistency
- remove stale experimental/generated files as the RF path stabilizes
- keep only the strongest working RF graphs in the mainline repo

### Later phases
- add `sisl_crypto.py`
- add `sisl_dsss.py`
- add `sisl_framer.py`
- add `test_sisl_crypto.py`
- add hail/ACK frame transport
- add SCRAP-over-SISL demo path

## Hackathon References

- SISL protocol spec: https://github.com/dyson-labs-org/scrap/blob/master/spec/SISL.md
- Hardware BOM seeds are tracked in [`docs/hardware/bill-of-materials.md`](docs/hardware/bill-of-materials.md)

## License

MIT License. See `LICENSE`.
