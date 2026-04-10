"""Logging configuration helpers."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure process-level logging once for scripts and demos."""

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
