"""Core data models shared across SISL lab modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class SatelliteIdentity:
    """Identity information for a satellite in a trust list."""

    norad_id: int
    callsign: str
    public_key_hex: str = ""


@dataclass(frozen=True, slots=True)
class HailParams:
    """Parameters needed to form a SISL hail message body."""

    source_norad: int
    target_norad: int
    center_freq_offset_mhz: int
    bandwidth_code: int
    mode_code: int
    chip_rate_mcps: int
    nonce: int
    flags: int = 0


@dataclass(slots=True)
class SessionContext:
    """Represents one active logical SISL session."""

    session_id: str
    local_norad: int
    remote_norad: int
    tx_key: bytes
    rx_key: bytes
    spreading_seed: bytes
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tx_sequence: int = 0
    rx_sequence: int = 0
