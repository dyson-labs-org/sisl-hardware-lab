"""Quick smoke demo for skeleton modules."""

from sisl_hardware_lab.protocol.hail import HailBody, build_hail_frame, parse_hail_frame
from sisl_hardware_lab.session.manager import SessionManager


def main() -> None:
    body = HailBody(
        source_norad=12345,
        center_freq_offset_mhz=100,
        bandwidth_code=3,
        mode_code=1,
        chip_rate_mcps=5,
        nonce=0x0102030405060708,
        flags=0x03,
    )
    packet = build_hail_frame(body=body, target_norad=54321)
    parsed = parse_hail_frame(packet)
    parsed_body = parsed.decode_body()

    manager = SessionManager(local_norad=12345)
    local_ephemeral_pub = bytes.fromhex("02" + "11" * 32)
    remote_ephemeral_pub = bytes.fromhex("03" + "22" * 32)
    session = manager.open_session(
        remote_norad=54321,
        dh1=b"\x10" * 32,
        dh2=b"\x20" * 32,
        dh3=b"\x30" * 32,
        local_ephemeral_pub=local_ephemeral_pub,
        remote_ephemeral_pub=remote_ephemeral_pub,
    )

    print(f"Hail target NORAD: {parsed.target_norad}")
    print(f"Hail source NORAD: {parsed_body.source_norad}")
    print(f"Session ID: {session.session_id}")
    print(f"TX seq -> {manager.next_tx_sequence(session.session_id)}")


if __name__ == "__main__":
    main()
