"""Configuration loader for SISL hardware lab runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11
    import tomli as tomllib


@dataclass(frozen=True, slots=True)
class RadioConfig:
    center_freq_mhz: int = 2400
    bandwidth_mhz: int = 5
    chip_rate_mcps: int = 5
    mode: str = "DSSS"


@dataclass(frozen=True, slots=True)
class SessionConfig:
    max_payload_bytes: int = 51200
    default_data_rate_kbps: int = 10
    enable_fhss: bool = True


@dataclass(frozen=True, slots=True)
class LabConfig:
    local_norad_id: int = 0
    local_callsign: str = "LAB-NODE"
    radio: RadioConfig = field(default_factory=RadioConfig)
    session: SessionConfig = field(default_factory=SessionConfig)


def load_config(path: str | Path) -> LabConfig:
    """Load TOML config from disk and return strongly typed lab config."""

    config_path = Path(path)
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))

    radio = raw.get("radio", {})
    session = raw.get("session", {})

    return LabConfig(
        local_norad_id=int(raw.get("local_norad_id", 0)),
        local_callsign=str(raw.get("local_callsign", "LAB-NODE")),
        radio=RadioConfig(
            center_freq_mhz=int(radio.get("center_freq_mhz", 2400)),
            bandwidth_mhz=int(radio.get("bandwidth_mhz", 5)),
            chip_rate_mcps=int(radio.get("chip_rate_mcps", 5)),
            mode=str(radio.get("mode", "DSSS")),
        ),
        session=SessionConfig(
            max_payload_bytes=int(session.get("max_payload_bytes", 51200)),
            default_data_rate_kbps=int(session.get("default_data_rate_kbps", 10)),
            enable_fhss=bool(session.get("enable_fhss", True)),
        ),
    )
