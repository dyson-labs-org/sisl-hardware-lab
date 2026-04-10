# RF Bench Log

## Purpose

Track the RF measurements and observations for the Phase 1 DSSS hidden-signal demo.

The key question is not just "how many dB down was the signal?" The key question is:

- can the observer fail to meaningfully recover it, while
- the intended receiver still recovers it with the correct code?

## Run template

### Run ID
- Date:
- Time:
- Operator:

### Hardware
- TX SDR:
- RX SDR:
- Observer SDR:
- Attenuators used:
- Cable configuration:

### Settings
- Center frequency:
- Sample rate:
- Chip rate:
- Payload rate:
- Code length:
- TX gain:
- Total attenuation:

### Waveform mode
- [ ] CW reference
- [ ] unspread BPSK
- [ ] DSSS with public code
- [ ] DSSS with wrong-code test

### Observer results
- Observer visible?:
- Observer decode possible?:
- Observer notes:

### Intended receiver results
- Correct-code decode success?:
- Wrong-code decode success?:
- Packet/frame success rate:
- Notes:

### KPI notes
- Apparent PSD suppression vs unspread reference:
- Occupied bandwidth estimate:
- Hidden-but-decodable threshold:
- Covert recovery margin estimate:
- Artifacts/spurs/LO leakage notes:

### Summary
- Pass / fail:
- What changed for next run: