# Architecture Sketch

## Scope

This repository is a hackathon-focused implementation sandbox for SISL:
- frame and hail encoding/decoding scaffolding
- key derivation and session lifecycle prototypes
- radio abstraction with an in-memory simulator for early integration testing

## High-Level Modules

- `sisl_hardware_lab.protocol`: Wire-format helpers (`Frame`, `HailBody`, hail frame parsing/building)
- `sisl_hardware_lab.crypto`: HKDF-based key derivation scaffolding aligned with SISL draft constants
- `sisl_hardware_lab.session`: Session tracking and sequence counters
- `sisl_hardware_lab.radio`: Backend abstraction and local simulator
- `sisl_hardware_lab.config`: Typed TOML loading for lab runs

## Intended Growth Path

1. Replace hail plaintext scaffold with authenticated encryption/decryption.
2. Add real secp256k1 ECDH integration and verify against SISL test vectors.
3. Integrate SDR transport adapter (HackRF/Nooelec test harness).
4. Add experiment telemetry and replayable RF/capture fixtures.
