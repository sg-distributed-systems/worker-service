"""
Service lifecycle management for graceful shutdown handling.

Provides signal handlers for SIGINT/SIGTERM that log shutdown events and invoke
registered cleanup callbacks. Use install_signal_handlers() at startup and
register_shutdown_callback() to add cleanup logic that runs on termination.
"""
from __future__ import annotations

import signal
import threading
from typing import Callable, List, Optional

from core_logger import get_logger

_shutdown_event = threading.Event()
_shutdown_callbacks: List[Callable[[], None]] = []


def is_shutting_down() -> bool:
    return _shutdown_event.is_set()


def register_shutdown_callback(cb: Callable[[], None]) -> None:
    _shutdown_callbacks.append(cb)


def request_shutdown(reason: str) -> None:
    logger = get_logger("lifecycle")
    logger.warning("shutdown_requested", reason=reason)
    _shutdown_event.set()
    for cb in list(_shutdown_callbacks):
        try:
            cb()
        except Exception as exc:
            logger.exception("shutdown_callback_failed", exc=exc)


def install_signal_handlers(service_logger_name: str) -> None:
    logger = get_logger(service_logger_name)

    def _handler(signum: int, frame: Optional[object]) -> None:
        try:
            sig = signal.Signals(signum).name
        except ValueError:
            sig = str(signum)
        logger.warning("shutdown_signal_received", signal=sig)
        _shutdown_event.set()
        for cb in list(_shutdown_callbacks):
            try:
                cb()
            except Exception as exc:
                logger.exception("shutdown_callback_failed", exc=exc)

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)
