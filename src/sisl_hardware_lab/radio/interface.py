"""Protocol definition for pluggable radio backends."""

from __future__ import annotations

from typing import Protocol


class RadioLink(Protocol):
    """Common interface shared by simulator and hardware adapters."""

    def send(self, payload: bytes) -> None:
        """Transmit payload bytes to the configured link peer."""

    def receive(self) -> bytes | None:
        """Receive next payload from link peer if available."""
