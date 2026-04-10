"""Tests for hail frame/body scaffolding."""

from sisl_hardware_lab.protocol.hail import HailBody, build_hail_frame, parse_hail_frame


def test_hail_round_trip() -> None:
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

    assert parsed.version == 0x02
    assert parsed.target_norad == 54321
    assert parsed_body.source_norad == 12345
    assert parsed_body.nonce == 0x0102030405060708
