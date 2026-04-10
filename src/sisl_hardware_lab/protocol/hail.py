"""SISL hail message scaffolding."""

from __future__ import annotations

import struct
from dataclasses import dataclass

from .frame import Frame, VERSION

HAIL_MSG_TYPE = 0x01
BODY_SIZE = 17
EPHEMERAL_KEY_SIZE = 33
IV_SIZE = 12
TAG_SIZE = 16


@dataclass(frozen=True, slots=True)
class HailBody:
    """Plaintext hail body fields from SISL v0x02 layout."""

    source_norad: int
    center_freq_offset_mhz: int
    bandwidth_code: int
    mode_code: int
    chip_rate_mcps: int
    nonce: int
    flags: int

    def encode(self) -> bytes:
        """Encode plaintext body into fixed-size 17-byte payload."""

        _validate_u24(self.source_norad, "source_norad")
        _validate_u16(self.center_freq_offset_mhz, "center_freq_offset_mhz")
        _validate_u8(self.bandwidth_code, "bandwidth_code")
        _validate_u8(self.mode_code, "mode_code")
        _validate_u8(self.chip_rate_mcps, "chip_rate_mcps")
        _validate_u64(self.nonce, "nonce")
        _validate_u8(self.flags, "flags")

        return (
            self.source_norad.to_bytes(3, "big")
            + struct.pack(
                ">HBBBQB",
                self.center_freq_offset_mhz,
                self.bandwidth_code,
                self.mode_code,
                self.chip_rate_mcps,
                self.nonce,
                self.flags,
            )
        )

    @classmethod
    def decode(cls, data: bytes) -> "HailBody":
        """Decode 17-byte payload into typed hail body."""

        if len(data) != BODY_SIZE:
            raise ValueError(f"Hail body must be {BODY_SIZE} bytes")

        source_norad = int.from_bytes(data[:3], "big")
        center_freq_offset_mhz, bandwidth_code, mode_code, chip_rate_mcps, nonce, flags = struct.unpack(
            ">HBBBQB", data[3:]
        )
        return cls(
            source_norad=source_norad,
            center_freq_offset_mhz=center_freq_offset_mhz,
            bandwidth_code=bandwidth_code,
            mode_code=mode_code,
            chip_rate_mcps=chip_rate_mcps,
            nonce=nonce,
            flags=flags,
        )


@dataclass(frozen=True, slots=True)
class HailFrame:
    """Parsed scaffold hail frame."""

    version: int
    target_norad: int
    caller_ephemeral_pub: bytes
    iv: bytes
    encrypted_body: bytes
    auth_tag: bytes

    def decode_body(self) -> HailBody:
        """Decode the plaintext scaffold body field."""

        return HailBody.decode(self.encrypted_body)


def build_hail_frame(
    body: HailBody,
    target_norad: int,
    caller_ephemeral_pub: bytes | None = None,
    iv: bytes | None = None,
    auth_tag: bytes | None = None,
) -> bytes:
    """Build a scaffold hail frame (body remains plaintext placeholder)."""

    _validate_u24(target_norad, "target_norad")
    caller_ephemeral_pub = caller_ephemeral_pub or (b"\x02" + b"\x00" * 32)
    iv = iv or (b"\x00" * IV_SIZE)
    auth_tag = auth_tag or (b"\x00" * TAG_SIZE)

    if len(caller_ephemeral_pub) != EPHEMERAL_KEY_SIZE:
        raise ValueError("caller_ephemeral_pub must be 33 bytes")
    if len(iv) != IV_SIZE:
        raise ValueError("iv must be 12 bytes")
    if len(auth_tag) != TAG_SIZE:
        raise ValueError("auth_tag must be 16 bytes")

    payload = (
        target_norad.to_bytes(3, "big")
        + caller_ephemeral_pub
        + iv
        + body.encode()
        + auth_tag
    )
    frame = Frame(version=VERSION, msg_type=HAIL_MSG_TYPE, payload=payload)
    return frame.to_bytes()


def parse_hail_frame(packet: bytes) -> HailFrame:
    """Parse serialized hail frame bytes into a typed object."""

    frame = Frame.from_bytes(packet)
    if frame.msg_type != HAIL_MSG_TYPE:
        raise ValueError("Frame is not a hail message")

    expected_size = 3 + EPHEMERAL_KEY_SIZE + IV_SIZE + BODY_SIZE + TAG_SIZE
    if len(frame.payload) != expected_size:
        raise ValueError("Unexpected hail payload length")

    target_norad = int.from_bytes(frame.payload[:3], "big")
    cursor = 3
    caller_ephemeral_pub = frame.payload[cursor : cursor + EPHEMERAL_KEY_SIZE]
    cursor += EPHEMERAL_KEY_SIZE
    iv = frame.payload[cursor : cursor + IV_SIZE]
    cursor += IV_SIZE
    encrypted_body = frame.payload[cursor : cursor + BODY_SIZE]
    cursor += BODY_SIZE
    auth_tag = frame.payload[cursor : cursor + TAG_SIZE]

    return HailFrame(
        version=frame.version,
        target_norad=target_norad,
        caller_ephemeral_pub=caller_ephemeral_pub,
        iv=iv,
        encrypted_body=encrypted_body,
        auth_tag=auth_tag,
    )


def _validate_u8(value: int, field_name: str) -> None:
    if not 0 <= value <= 0xFF:
        raise ValueError(f"{field_name} must fit in 1 byte")


def _validate_u16(value: int, field_name: str) -> None:
    if not 0 <= value <= 0xFFFF:
        raise ValueError(f"{field_name} must fit in 2 bytes")


def _validate_u24(value: int, field_name: str) -> None:
    if not 0 <= value <= 0xFFFFFF:
        raise ValueError(f"{field_name} must fit in 3 bytes")


def _validate_u64(value: int, field_name: str) -> None:
    if not 0 <= value <= 0xFFFFFFFFFFFFFFFF:
        raise ValueError(f"{field_name} must fit in 8 bytes")
