"""Tests for session manager behavior."""

from sisl_hardware_lab.session.manager import SessionManager


def test_session_manager_creates_and_tracks_session() -> None:
    manager = SessionManager(local_norad=12345)

    session = manager.open_session(
        remote_norad=54321,
        dh1=b"\x10" * 32,
        dh2=b"\x20" * 32,
        dh3=b"\x30" * 32,
        local_ephemeral_pub=bytes.fromhex("02" + "11" * 32),
        remote_ephemeral_pub=bytes.fromhex("03" + "22" * 32),
    )

    loaded = manager.get_session(session.session_id)
    assert loaded is not None
    assert loaded.remote_norad == 54321
    assert manager.next_tx_sequence(session.session_id) == 1
    assert manager.next_rx_sequence(session.session_id) == 1
