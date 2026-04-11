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

## RF Measurement KPIs

The RF story for this repo is not just "how many dB down did the signal look." The main question is whether SISL can spread energy across bandwidth such that:

1. a passive observer does not meaningfully recover the signal, while
2. an intended receiver with the correct spreading code still recovers it reliably.

This section defines the RF metrics we care about gathering during the hackathon.

### North-star RF KPI

- **Covert recovery margin (dB)**  
  The margin between:
  - the point where the passive observer can no longer meaningfully detect or decode the signal, and
  - the point where the intended receiver still achieves acceptable recovery after despreading.

This is the primary KPI for the RF demonstration.

### Primary RF KPIs

#### 1. Power spectral density suppression
- **What it is:** How much the spread waveform lowers apparent power per FFT bin or per Hz relative to an unspread or narrowband reference at comparable total transmit power.
- **Why it matters:** SISL is trying to hide RF energy inside bandwidth rather than presenting a narrow obvious emitter.
- **How to measure it:**
  - Transmit an unspread reference waveform
  - Transmit the spread waveform
  - Compare observer-view peak level, PSD, or per-bin prominence
- **Report as:**  
  - peak suppression relative to unspread reference (dB)  
  - approximate PSD suppression (dB/bin or dB/Hz)

#### 2. Occupied bandwidth
- **What it is:** The bandwidth actually occupied by the spread signal.
- **Why it matters:** If the signal is not materially wider than the unspread case, then spreading is not doing meaningful work.
- **How to measure it:**
  - 99% occupied bandwidth
  - null-to-null bandwidth, if convenient
  - -20 dBc bandwidth, if convenient
- **Report as:** Hz or MHz

#### 3. Processing gain
- **What it is:** The gain achieved by spreading and despreading, both theoretically and as measured in practice.
- **Why it matters:** This is the core trade: sacrifice spectral efficiency to reduce observable PSD while still recovering the signal at the intended receiver.
- **Theory targets for this demo:**
  - Hail mode: ~30 dB processing gain from 1 Mcps / 1 kbps
  - P2P mode: ~20 dB processing gain from 1 Mcps / 10 kbps
- **How to measure it:**
  - Compare pre-despread observer-view SNR-like visibility to post-despread receiver recovery margin
  - Estimate effective gain from correlation / recovery results
- **Report as:**  
  - theoretical processing gain (dB)  
  - measured effective processing gain (dB)

#### 4. Hidden-but-decodable threshold
- **What it is:** The attenuation point where the observer no longer has meaningful visibility, but the intended receiver still decodes successfully.
- **Why it matters:** This is the most important experimental threshold in the demo.
- **How to measure it:**
  - Sweep attenuation
  - Record observer visibility
  - Record intended receiver decode success
- **Report as:**  
  - total attenuation at observer-loss threshold  
  - total attenuation at receiver-failure threshold  
  - hidden-but-decodable margin (dB)

#### 5. Decode success vs attenuation
- **What it is:** Reliability of recovery as attenuation increases.
- **Why it matters:** A hidden signal that only works once is not a convincing communications demo.
- **How to measure it:**
  - Repeat runs at multiple attenuation levels
  - Record payload recovery, frame recovery, or packet recovery rates
- **Report as:**  
  - packet success rate vs attenuation  
  - frame success rate vs attenuation  
  - optional BER vs attenuation

#### 6. Observer failure rate
- **What it is:** How often the passive observer can detect, correlate, frame, or decode anything useful.
- **Why it matters:** The observer must fail, not just "not be sure."
- **How to measure it:**
  - No-code observer attempt
  - Wrong-code observer attempt
  - Optional matched-filter attempt without correct sequence
- **Report as:**  
  - observer detect success rate  
  - observer decode success rate  
  - wrong-code correlation success rate

### Secondary RF KPIs

#### 7. Spectral flatness across the spread band
- **What it is:** How evenly energy is distributed across the spread signal bandwidth.
- **Why it matters:** A poor implementation may leak obvious peaks, tones, or structure even if the total waveform is technically spread.
- **What to look for:**
  - strong spurs
  - LO leakage
  - DC offset artifacts
  - uneven shaping that creates identifiable peaks

#### 8. Adjacent-channel leakage / out-of-band leakage
- **What it is:** How much energy spills outside the intended spread band.
- **Why it matters:** The demo should show controlled spreading, not just wideband mess.
- **Report as:** a relative out-of-band leakage estimate if the tooling supports it

#### 9. Spectral efficiency
- **What it is:** Useful bits per second per Hz.
- **Why it matters:** This is a context metric, not the optimization target.
- **Interpretation:** For this demo, low spectral efficiency is expected because bandwidth is being traded for lower PSD and processing gain.
- **Use it to explain the trade, not to judge success.**

### Metrics we should capture for every serious run

For each run, record:

- date / time
- center frequency
- sample rate
- chip rate
- payload rate
- spreading code type:
  - public hailing code
  - session-derived code
- TX gain / power setting
- attenuation chain used
- observer SDR used
- intended receiver SDR used
- observer visible yes/no
- observer decoded yes/no
- wrong-code decode yes/no
- intended receiver decoded yes/no
- packet / frame success
- notes on artifacts or failure mode

### Recommended plots / artifacts

The most useful outputs to save under `docs/` or `docs/experiments/` are:

- observer FFT/waterfall screenshot for unspread reference
- observer FFT/waterfall screenshot for spread waveform
- receiver correlator / despread output screenshot
- attenuation sweep log
- packet success vs attenuation plot
- short notes on the hidden-but-decodable threshold

### What counts as a strong RF result

A strong RF result is not simply "the signal was X dB down." A strong result means:

- the spread signal has materially lower apparent PSD than the unspread reference
- the passive observer cannot meaningfully recover it
- the intended receiver can recover it with the correct code
- the system remains reliable across a useful attenuation range
- the team can quantify the hidden-but-decodable margin

### Practical interpretation

For this hackathon, the key RF question is:

> How effectively can we spread RF energy across bandwidth to reduce observer-visible signal prominence while preserving reliable despread recovery for the authorized receiver?

That is the RF measurement story this repo should support.

## License

MIT License. See `LICENSE`.
