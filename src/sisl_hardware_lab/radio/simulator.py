"""In-memory radio link simulator for local protocol testing."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass(slots=True)
class InMemoryRadio:
    """Simple half-duplex-ish in-memory peer radio simulation."""

    name: str
    _inbox: deque[bytes] = field(default_factory=deque, repr=False)
    _peer: InMemoryRadio | None = field(default=None, repr=False)

    def connect(self, peer: InMemoryRadio) -> None:
        """Connect this radio to a peer radio."""

        self._peer = peer
        peer._peer = self

    def send(self, payload: bytes) -> None:
        """Send bytes to peer inbox."""

        if self._peer is None:
            raise RuntimeError(f"Radio {self.name} is not connected")
        self._peer._inbox.append(payload)

    def receive(self) -> bytes | None:
        """Pop next received payload if available."""

        if not self._inbox:
            return None
        return self._inbox.popleft()
