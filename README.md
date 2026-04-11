# SISL Hardware Lab

SISL Hardware Lab is the working repository for Dyson SCI hackathon implementation work around the **Secure Inter-Satellite Link (SISL)** protocol.

This repo is focused on turning the SISL specification into a bench-top, SDR-based demonstration in three layers:

1. **Phase 1** — DSSS hidden-signal RF demo  
2. **Phase 2** — encrypted hail + ACK handshake using real SISL crypto  
3. **Phase 3** — session-derived P2P channel and SCRAP-over-SISL demonstration  

The current branch is primarily a **Phase 1 / early Phase 2** lab branch.

## What SISL Is

Per the current SISL draft, SISL is a **link-layer protocol** for authenticated, encrypted communication between satellites. It combines:

- X3DH-style key agreement using secp256k1
- AES-256-GCM for link encryption
- spread-spectrum RF for LPI/LPD
- a **public hailing code** for initial contact
- **session-derived spreading codes** for the private P2P channel

For the hackathon, the repository is not attempting to implement all of SISL at once. It is deliberately staged so the RF story can be proven before the crypto and application layers are added.

## Hackathon Demo Target

The uploaded hackathon plan frames the live demo as:

- a transmitter sends a DSSS signal below the apparent noise floor,
- a passive observer sees nothing unusual,
- the intended receiver applies the correct spreading code and recovers data,
- then later phases add real hail / ACK crypto and a SCRAP task flow.

That means the immediate milestone is:

1. transmit a spread signal on a live SDR path,
2. show that an observer does not see an obvious new signal,
3. show that the intended receiver can recover the payload with the correct code,
4. show that a wrong code fails.

## Phase Structure

## Phase 1 — DSSS Hidden-Signal Demo

Goal:
- visually demonstrate the core SISL LPI/LPD story with SDR hardware

Target architecture:
- `dsss_rf_tx.grc`
- `dsss_rf_rx.grc`
- `dsss_rf_observer.grc`

Planned operating concept:
- public hailing code derived from `SHA256("SISL-public-hailing-code-v2")`
- BPSK test payload
- DSSS spreading
- observer remains code-unaware
- intended receiver uses the correct code
- wrong-code branch is used as a control

Target demo hailing settings from the hackathon plan:
- center frequency: **2437.0 MHz**
- chip rate: **1 Mcps**
- hail data rate: **~1 kbps**
- code length: **1023 chips**
- RX/observer sample rate target: **2.4 Msps**

Important simplification for Phase 1:
- **no acquisition correlator yet**
- both ends are allowed to start at a fixed known chip offset
- this is a deliberate demo simplification, not the final SISL design

## Phase 2 — Encrypted Hail / ACK

Goal:
- replace the synthetic payload with real SISL hailing and ACK frames

Expected files:
- `sisl_crypto.py`
- `sisl_dsss.py`
- `sisl_framer.py`
- `test_sisl_crypto.py`

Planned scope:
- X3DH-derived hail key
- hail frame encode / decode
- ACK frame encode / decode
- loopback validation against SISL test vectors before radio integration

## Phase 3 — Session-Derived P2P + SCRAP

Goal:
- switch from the public hailing code to a session-derived spreading code
- carry SCRAP data over the established SISL link

Planned scope:
- session-derived DSSS code generation
- task / token transport over the P2P channel
- proof-of-execution stub path
- end-to-end “observer sees nothing / participants exchange real protocol traffic” demo

## Current Repo Status

### Implemented / in-repo now

Repository and lab scaffolding:
- Python package scaffold under `src/sisl_hardware_lab/`
- smoke-testable quickstart path
- repo health tooling (`ruff`, `pytest`)
- `START_HERE.md`
- `configs/phase1_demo.toml`
- `docs/experiments/rf_bench_log.md`

GNU Radio work:
- `spreadtest.grc` / software-only DSSS proof
- `dsss_rf_tx.grc`
- `dsss_rf_rx.grc`
- `dsss_rf_observer.grc`

Working conceptually:
- TX, RX, and observer have been split into separate flowgraphs
- observer graph is intentionally code-unaware
- RX graph includes correct-code and wrong-code recovery branches
- software DSSS proof has already been used to validate the “correct code works / wrong code fails” logic before hardware integration

### In progress

- aligning all three RF flowgraphs to the final Phase 1 hailing configuration
- validating real HackRF bring-up on the bench
- dealing with practical SDR constraints such as supported sample rates and device ownership
- tuning attenuation and logging actual bench results
- cleaning the graphs so the repo reflects the strongest working versions rather than every intermediate experiment

### Not done yet

- final, hardware-validated 1023-chip public hailing demo at the intended Phase 1 settings
- recorded bench results in `docs/experiments/rf_bench_log.md`
- `sisl_crypto.py`
- `sisl_dsss.py`
- `sisl_framer.py`
- `test_sisl_crypto.py`
- encrypted hail / ACK radio transport
- session-derived P2P channel
- SCRAP-over-SISL application demo

## GNU Radio Flowgraphs

### `spreadtest.grc`

Software-only DSSS proof.

Purpose:
- prove the signal-processing chain without SDR hardware
- verify that:
  - the spread signal exists,
  - the correct code recovers structure,
  - the wrong code fails

This is the safest place to validate DSP logic before touching HackRF hardware.

### `dsss_rf_tx.grc`

Transmit-side Phase 1 flowgraph.

Purpose:
- generate a known repeating payload
- map to BPSK
- spread with the current DSSS code
- drive HackRF transmit
- provide local TX-side waveform / spectrum visibility

Notes:
- this graph is currently a **bench bring-up graph**, not the final polished Phase 1 demo graph
- it may temporarily use alternate bench settings while hardware is being stabilized

### `dsss_rf_rx.grc`

Privileged receiver flowgraph.

Purpose:
- receive live RF from HackRF
- inspect the raw waveform
- apply the correct spreading code
- compare against a wrong-code branch
- recover the intended symbol stream

Notes:
- this graph is the place where the “right code vs wrong code” live comparison happens
- bit decisions belong **after** despreading, not before

### `dsss_rf_observer.grc`

Passive observer flowgraph.

Purpose:
- receive live RF from HackRF
- show spectrum occupancy and raw waveform only
- remain completely ignorant of the spreading code

This graph intentionally does **not** include any recovery path. It models what an external observer sees.

## Bench Operating Order

For RF bring-up and demo rehearsal:

1. start the observer first  
2. start the privileged receiver second  
3. start the transmitter last  

This reduces the chance of missing short TX bursts during testing.

## Bench Logging

Use:

- `configs/phase1_demo.toml` for intended operating parameters
- `docs/experiments/rf_bench_log.md` for actual measured bench results

The real question is not just “how many dB down was the signal?” The important question is:

- can the observer fail to meaningfully recover it,
- while the intended receiver still succeeds with the correct code?

That is the Phase 1 success criterion.

## Known Gaps / Honest Constraints

This repo is intentionally **not** pretending to be farther along than it is.

Known current gaps include:
- no live acquisition correlator yet
- no final public-code 1023-chip hardware lock-down yet
- no completed encrypted hail / ACK transport yet
- no session-derived spreading code switch yet
- no SCRAP-over-SISL end-to-end path yet

This is expected for the current branch. The branch is still in the RF-first stage.

## Near-Term TODO

### Phase 1 completion
- align TX / RX / observer on final Phase 1 hailing settings
- lock the public hailing code implementation to the SISL spec
- complete live HackRF TX/RX/observer bench validation
- tune attenuation until the observer view is uninteresting
- validate correct-code recovery vs wrong-code failure on real RF
- record results in `docs/experiments/rf_bench_log.md`

### Phase 2 prep
- port `generate_dsss_code()` from the SISL spec into Python
- port `derive_hail_key()` and `derive_session_keys()`
- add test-vector validation
- implement hail / ACK frame encode/decode

### Repo cleanup
- keep graph titles and variable names consistent
- remove stale generated files once the winning flowgraphs are clear
- keep the README synchronized with the actual state of the branch

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
|-- dsss_rf_tx.grc            # TX-side Phase 1 flowgraph
|-- dsss_rf_rx.grc            # Privileged RX flowgraph
|-- dsss_rf_observer.grc      # Passive observer flowgraph
`-- spreadtest.grc            # Software-only DSSS proof
```

## References

- SISL spec: `scrap/spec/SISL.md`
- Hackathon plan: uploaded Dyson SCI Hackathon PDF in this conversation
- Hardware BOM seeds: `docs/hardware/bill-of-materials.md`

## License

MIT License. See `LICENSE`.
