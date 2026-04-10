# Protocol Notes

## Canonical Spec

- SISL draft: https://github.com/dyson-labs-org/scrap/blob/master/spec/SISL.md

## Current Scaffold Status

- Version byte: `0x02` wired into frame/hail helpers.
- Hail body layout: 17-byte plaintext structure modeled after draft section examples.
- Session derivation: HKDF-SHA256 scaffold with SISL salts.

## Important TODOs

1. Implement full frame security trailer + AES-256-GCM integration.
2. Add strict validation for message types and capability negotiation flags.
3. Implement replay protection with sequence-number-derived IV construction.
4. Add interoperability test vectors from the SISL spec.
