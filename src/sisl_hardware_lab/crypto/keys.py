"""SISL key derivation scaffold based on HKDF-SHA256."""

from __future__ import annotations

import hmac
import struct
from hashlib import sha256

SISL_X3DH_SALT = sha256(b"SISL-v2-X3DH").digest()
SISL_HAIL_SALT = sha256(b"SISL-v2-hail").digest()


def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    """Derive `length` bytes via HKDF-SHA256 (RFC 5869)."""

    if length <= 0:
        raise ValueError("length must be positive")
    if length > 32 * 255:
        raise ValueError("length exceeds HKDF output limit")

    if not salt:
        salt = b"\x00" * 32

    prk = hmac.new(salt, ikm, sha256).digest()
    okm = b""
    t = b""
    counter = 1

    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), sha256).digest()
        okm += t
        counter += 1

    return okm[:length]


def derive_session_material(
    dh1: bytes,
    dh2: bytes,
    dh3: bytes,
    caller_norad: int,
    responder_norad: int,
    caller_ephemeral_pub: bytes,
    responder_ephemeral_pub: bytes,
) -> dict[str, bytes]:
    """Derive session keys and spreading seed from X3DH-like inputs."""

    shared_secret = dh1 + dh2 + dh3
    transcript = (
        struct.pack(
            ">II",
            min(caller_norad, responder_norad),
            max(caller_norad, responder_norad),
        )
        + caller_ephemeral_pub
        + responder_ephemeral_pub
    )

    key_material = hkdf_sha256(
        ikm=shared_secret,
        salt=SISL_X3DH_SALT,
        info=transcript,
        length=160,
    )

    return {
        "hail_key": key_material[0:32],
        "ack_key": key_material[32:64],
        "p2p_tx_key": key_material[64:96],
        "p2p_rx_key": key_material[96:128],
        "spreading_seed": key_material[128:160],
    }


def derive_hail_key(dh1: bytes, responder_norad: int) -> bytes:
    """Derive initial hail encryption key from DH1 and target NORAD."""

    info = struct.pack(">I", responder_norad)
    return hkdf_sha256(
        ikm=dh1,
        salt=SISL_HAIL_SALT,
        info=info,
        length=32,
    )
