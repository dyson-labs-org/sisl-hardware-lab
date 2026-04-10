"""Low-level SISL frame encoder/decoder helpers."""

from __future__ import annotations

import binascii
import struct
from dataclasses import dataclass

SYNC_WORD = bytes.fromhex("1ACFFC1D1ACFFC1D")
VERSION = 0x02

_HEADER_FORMAT = ">8sBBH"
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)
_CRC_SIZE = 4


@dataclass(frozen=True, slots=True)
class Frame:
    """Minimal SISL frame abstraction for scaffold development."""

    version: int
    msg_type: int
    payload: bytes

    def to_bytes(self) -> bytes:
        """Serialize frame bytes with header + CRC32 trailer."""

        payload_length = len(self.payload)
        header = struct.pack(_HEADER_FORMAT, SYNC_WORD, self.version, self.msg_type, payload_length)
        crc = binascii.crc32(header[8:] + self.payload) & 0xFFFFFFFF
        return header + self.payload + struct.pack(">I", crc)

    @classmethod
    def from_bytes(cls, packet: bytes) -> Frame:
        """Parse and validate a serialized frame."""

        if len(packet) < _HEADER_SIZE + _CRC_SIZE:
            raise ValueError("Packet too short to contain frame")

        sync, version, msg_type, payload_length = struct.unpack(
            _HEADER_FORMAT, packet[:_HEADER_SIZE]
        )
        if sync != SYNC_WORD:
            raise ValueError("Invalid sync word")

        payload_start = _HEADER_SIZE
        payload_end = payload_start + payload_length
        crc_start = payload_end
        crc_end = crc_start + _CRC_SIZE

        if len(packet) != crc_end:
            raise ValueError("Packet length mismatch")

        payload = packet[payload_start:payload_end]
        expected_crc = struct.unpack(">I", packet[crc_start:crc_end])[0]
        actual_crc = binascii.crc32(packet[8:payload_end]) & 0xFFFFFFFF
        if expected_crc != actual_crc:
            raise ValueError("CRC mismatch")

        return cls(version=version, msg_type=msg_type, payload=payload)
