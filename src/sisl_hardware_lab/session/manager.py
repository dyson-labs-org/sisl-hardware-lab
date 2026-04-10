"""Session manager for scaffolded SISL exchanges."""

from __future__ import annotations

from hashlib import sha256

from sisl_hardware_lab.crypto.keys import derive_session_material
from sisl_hardware_lab.models import SessionContext


class SessionManager:
    """Track active sessions and sequence counters."""

    def __init__(self, local_norad: int) -> None:
        self.local_norad = local_norad
        self._sessions: dict[str, SessionContext] = {}

    def open_session(
        self,
        remote_norad: int,
        dh1: bytes,
        dh2: bytes,
        dh3: bytes,
        local_ephemeral_pub: bytes,
        remote_ephemeral_pub: bytes,
    ) -> SessionContext:
        """Create a new session context from pre-computed DH outputs."""

        key_material = derive_session_material(
            dh1=dh1,
            dh2=dh2,
            dh3=dh3,
            caller_norad=self.local_norad,
            responder_norad=remote_norad,
            caller_ephemeral_pub=local_ephemeral_pub,
            responder_ephemeral_pub=remote_ephemeral_pub,
        )
        session_id = sha256(local_ephemeral_pub + remote_ephemeral_pub).hexdigest()[:16]
        context = SessionContext(
            session_id=session_id,
            local_norad=self.local_norad,
            remote_norad=remote_norad,
            tx_key=key_material["p2p_tx_key"],
            rx_key=key_material["p2p_rx_key"],
            spreading_seed=key_material["spreading_seed"],
        )
        self._sessions[session_id] = context
        return context

    def get_session(self, session_id: str) -> SessionContext | None:
        """Look up an existing session by ID."""

        return self._sessions.get(session_id)

    def next_tx_sequence(self, session_id: str) -> int:
        """Increment and return the next TX sequence number."""

        context = self._require_session(session_id)
        context.tx_sequence += 1
        return context.tx_sequence

    def next_rx_sequence(self, session_id: str) -> int:
        """Increment and return the next RX sequence number."""

        context = self._require_session(session_id)
        context.rx_sequence += 1
        return context.rx_sequence

    def _require_session(self, session_id: str) -> SessionContext:
        context = self._sessions.get(session_id)
        if context is None:
            raise KeyError(f"Unknown session_id: {session_id}")
        return context
