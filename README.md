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

# SISL Hackathon Build Plan

## Objective

Build a live SISL demo showing that:

1. A DSSS signal can be transmitted below the apparent noise floor
2. Only a receiver with the correct spreading code can recover it
3. Two parties can complete an authenticated hail + ACK exchange
4. A secure P2P channel can carry a SCRAP-style task request as a stretch goal

## Success criteria

### Minimum viable demo
- [ ] Observer waterfall shows no obvious new signal
- [ ] Receiver can recover DSSS test payload with the correct code
- [ ] Wrong code fails to recover payload
- [ ] Team can explain why the signal is hidden and how despreading works

### Strong demo
- [ ] Satellite A sends encrypted hail
- [ ] Satellite B decrypts hail and returns ACK
- [ ] Session keys are derived on both sides
- [ ] Session-derived spreading code is used for the P2P link

### Stretch demo
- [ ] SCRAP capability token is sent over SISL link
- [ ] Task request is verified
- [ ] Proof / receipt stub is returned
- [ ] Optional 5 GHz repeat of the same flow

---

## Team roles

### Calvin / Integration Lead
- [ ] Own repo structure and branch strategy
- [ ] Own hardware bench bring-up
- [ ] Own integration between radio and crypto paths
- [ ] Own final demo flow and narration
- [ ] Own go / no-go decisions on cutting scope

### Team Member 2 / Radio Path
- [ ] Own DSSS signal path
- [ ] Own GNU Radio flowgraphs
- [ ] Own observer waterfall presentation
- [ ] Own attenuation tuning and visibility tests
- [ ] Own SDR sample-rate / frequency parameterization

### Team Member 3 / Crypto + Protocol Path
- [ ] Own SISL crypto implementation
- [ ] Own hail / ACK frame encode-decode
- [ ] Own loopback tests before RF
- [ ] Own session key derivation verification
- [ ] Own session-derived spreading code handoff to radio path

---

## Repo bootstrap

- [ ] Add `README.md`
- [ ] Add `TASKS.md`
- [ ] Add `.gitignore`
- [ ] Add `requirements.txt` or `pyproject.toml`
- [ ] Add `docs/`
- [ ] Add `hackathon/`

### Required files
- [ ] `hackathon/sisl_crypto.py`
- [ ] `hackathon/sisl_dsss.py`
- [ ] `hackathon/sisl_framer.py`
- [ ] `hackathon/sisl_dsss_demo.grc`
- [ ] `hackathon/sisl_hail_flow.grc`
- [ ] `hackathon/sisl_scrap_demo.py`
- [ ] `hackathon/test_sisl_crypto.py`

### Nice-to-have files
- [ ] `hackathon/config.py`
- [ ] `hackathon/run_phase1.sh`
- [ ] `hackathon/run_phase2.sh`
- [ ] `hackathon/run_phase3.sh`
- [ ] `docs/bench_setup.md`
- [ ] `docs/demo_script.md`
- [ ] `docs/frequency_plan.md`

---

## Environment setup

### Python dependencies
- [ ] Install `cryptography`
- [ ] Install `coincurve` or `python-secp256k1`
- [ ] Install test dependencies if needed

### SDR / GNU Radio stack
- [ ] Install GNU Radio 3.10+
- [ ] Install SoapySDR
- [ ] Install HackRF support
- [ ] Install RTL-SDR support for spare observer path if needed
- [ ] Verify GNU Radio Companion launches
- [ ] Verify Gqrx launches

### Validation
- [ ] Confirm HackRF TX unit enumerates
- [ ] Confirm HackRF RX unit enumerates
- [ ] Confirm observer SDR enumerates
- [ ] Confirm 2.4 GHz live spectrum can be viewed

---

## Hardware bench bring-up

### Inventory
- [ ] 2x HackRF assigned to Satellite A and Satellite B
- [ ] 1x observer SDR assigned to passive observer
- [ ] Attenuators located and labeled
- [ ] SMA cables checked
- [ ] Host computer selected for GNU Radio work
- [ ] Backup machine ready if needed

### RF path
- [ ] Build direct bench path between A TX and B RX
- [ ] Build reverse path between B TX and A RX
- [ ] Insert stacked attenuators in each path
- [ ] Keep Ham It Up out of the signal chain
- [ ] Set HackRF transmit power to minimum
- [ ] Verify no obvious overdrive or saturation

### Critical visibility test
- [ ] Send CW tone first
- [ ] Tune attenuation until tone disappears from waterfall
- [ ] Verify total attenuation is sufficient for hidden-signal demo
- [ ] Log final attenuation configuration in `docs/bench_setup.md`

---

## Phase 1: DSSS hidden-signal demo

### Deliverable
A working DSSS demo where the observer sees no obvious signal, the correct code recovers the payload, and the wrong code fails.

### Radio path tasks
- [ ] Implement DSSS code generation entry point in `sisl_dsss.py`
- [ ] Use public hailing seed for initial demo
- [ ] Build TX chain:
  - [ ] test bits
  - [ ] BPSK mapping
  - [ ] spread with DSSS code
  - [ ] send to HackRF sink
- [ ] Build RX chain:
  - [ ] HackRF source
  - [ ] despread with DSSS code
  - [ ] integrate / accumulate
  - [ ] threshold to bits
- [ ] Add QT GUI Frequency Sink
- [ ] Add QT GUI Time Sink
- [ ] Parameterize chip rate
- [ ] Parameterize sample rate
- [ ] Parameterize center frequency

### Demo settings
- [ ] Center frequency set to `2437.0 MHz`
- [ ] Receiver sample rate set to `2.4 Msps`
- [ ] Chip rate set to `1 Mcps`
- [ ] Fixed known code offset used for first demo
- [ ] No acquisition logic required for MVP

### Validation
- [ ] Correct code recovers message
- [ ] Wrong code yields noise / failure
- [ ] Observer view does not show obvious added signal
- [ ] Screenshot / short clip captured for backup

### Definition of done
- [ ] `sisl_dsss_demo.grc` runs
- [ ] Demo can be repeated reliably
- [ ] Team can explain simplifications honestly

---

## Phase 2: encrypted hail + ACK handshake

### Deliverable
A pure-Python SISL crypto path that works in loopback before RF integration.

### Crypto tasks
- [ ] Generate static secp256k1 identity keys for A and B
- [ ] Generate ephemeral keys per session
- [ ] Build trust-list mapping `{norad_id: pubkey}`
- [ ] Implement `derive_hail_key()`
- [ ] Implement `derive_session_keys()`
- [ ] Implement hail encrypt path
- [ ] Implement ACK encrypt path
- [ ] Implement hail decrypt path
- [ ] Implement ACK decrypt path
- [ ] Verify nonce echo handling
- [ ] Verify both sides derive matching session keys

### Frame tasks
- [ ] Implement `encode_hail_frame()`
- [ ] Implement `decode_hail_frame()`
- [ ] Implement `encode_ack_frame()`
- [ ] Implement `decode_ack_frame()`
- [ ] Match expected byte layout from SISL spec
- [ ] Log frame fields for demo visibility

### Tests
- [ ] Add `test_sisl_crypto.py`
- [ ] Add loopback test for hail -> ACK -> session establishment
- [ ] Add test-vector checks where available
- [ ] Confirm deterministic behavior for fixed test inputs

### Definition of done
- [ ] `sisl_crypto.py` supports loopback handshake
- [ ] `test_sisl_crypto.py` passes
- [ ] Output logs are readable enough for live demo

---

## Phase 2b: RF transport for hail / ACK

### Deliverable
Transport the encrypted hail and ACK frames over the public DSSS channel.

### Tasks
- [ ] Implement `SISLFramer` in `sisl_framer.py`
- [ ] Implement `SISLDeframer` in `sisl_framer.py`
- [ ] Packetize hail frame into transmit path
- [ ] Depacketize received hail frame back to bytes
- [ ] Feed bytes into Python crypto layer
- [ ] Reverse the same path for ACK
- [ ] Build `sisl_hail_flow.grc`
- [ ] Verify hail over RF
- [ ] Verify ACK over RF
- [ ] Verify both sides derive same session keys after live exchange

### Definition of done
- [ ] A sends hail over RF
- [ ] B decrypts hail
- [ ] B sends ACK over RF
- [ ] A validates ACK and establishes session

---

## Phase 3: secure P2P channel

### Deliverable
Switch from the public code to a session-derived code after the handshake.

### Tasks
- [ ] Derive spreading seed from session keys
- [ ] Generate session-derived DSSS code
- [ ] Switch TX and RX despreading path to session-derived code
- [ ] Prove that parties without handshake context cannot decode
- [ ] Keep logs showing transition from hail channel to secure P2P channel

### Definition of done
- [ ] Public-code phase completes
- [ ] Session-code phase completes
- [ ] Payload can be exchanged only after handshake

---

## Phase 3b: SCRAP over SISL

### Deliverable
Send a simple SCRAP-style task request over the secure SISL channel.

### Tasks
- [ ] Choose whether to call existing SCRAP code or reimplement minimal serialization in Python
- [ ] Serialize capability token
- [ ] Serialize task request
- [ ] Send token + task request over secure channel
- [ ] Verify token on receiver
- [ ] Return proof / receipt stub
- [ ] Print result clearly on screen

### Definition of done
- [ ] `sisl_scrap_demo.py` runs end-to-end
- [ ] Demo shows token, task, and proof / receipt flow

---

## Frequency plan

### Default demo
- [ ] Hailing channel: `2437.0 MHz`
- [ ] P2P channel: `2440.0 MHz`
- [ ] Observer tuned to hailing channel during demo

### Stretch
- [ ] Parameterize 5 GHz retune
- [ ] Candidate channels captured in notes
- [ ] Only attempt after 2.4 GHz demo is stable

---

## Demo script build-out

### On-screen outputs
- [ ] Observer waterfall visible
- [ ] Receiver decode pane visible
- [ ] Key/session log pane visible
- [ ] SCRAP task/proof pane visible if Phase 3 works

### Talk track
- [ ] Opening explanation of WiFi/noise-floor view
- [ ] Explain hidden DSSS hail
- [ ] Explain correct code vs wrong code
- [ ] Explain encrypted hail + ACK
- [ ] Explain session-derived code
- [ ] Explain SCRAP overlay if available

### Rehearsal
- [ ] Run full 5-minute demo once
- [ ] Run full 5-minute demo twice without edits
- [ ] Prepare shortened 2-minute version
- [ ] Prepare fallback Phase 1-only version

---

## Risks and kill criteria

### Risk: signal still visible
- [ ] Stop and fix attenuation before adding more software
- [ ] Do not proceed if observer can clearly see the signal

### Risk: DSSS chain incorrect
- [ ] Verify despreading is done before symbol decision
- [ ] Do not use stock BPSK demod path incorrectly

### Risk: crypto bugs
- [ ] Keep RF out until loopback handshake works
- [ ] Freeze crypto interface once tests pass

### Risk: integration takes too long
- [ ] Cut to Phase 1 MVP if needed
- [ ] Only attempt Phase 3 after Phase 2 is stable

---

## Day-by-day plan

## Day 1
- [ ] Repo bootstrap complete
- [ ] Environment working
- [ ] Hardware bench up
- [ ] Attenuation tuned
- [ ] Phase 1 DSSS demo working

## Day 2
- [ ] Pure Python crypto handshake working
- [ ] Frame encode/decode working
- [ ] Hail + ACK integrated into RF path

## Day 3
- [ ] Session-derived channel working
- [ ] SCRAP overlay attempted
- [ ] Demo rehearsed
- [ ] Fallback path locked if needed

---

## Branch plan

- [ ] `main`
- [ ] `feat/dsss-demo`
- [ ] `feat/crypto-handshake`
- [ ] `feat/p2p-scrap-demo`

---

## Immediate next actions

### Person1
- [ ] Create repo skeleton
- [ ] Create branches
- [ ] Assign owners
- [ ] Start hardware visibility test with attenuators

### Person2
- [ ] Start `sisl_dsss.py`
- [ ] Start `sisl_dsss_demo.grc`
- [ ] Validate correct-code / wrong-code behavior

### Person3
- [ ] Start `sisl_crypto.py`
- [ ] Start `test_sisl_crypto.py`
- [ ] Prove loopback handshake before RF integration

## License

MIT License. See `LICENSE`.
