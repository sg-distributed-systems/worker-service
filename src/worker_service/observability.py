"""
Observability initialization for request/job tracing.

Provides init_correlation_id() which sets up a correlation ID for the current
execution context. The ID is either read from the CORRELATION_ID environment
variable or auto-generated as a UUID4. Once set, the ID appears in all log entries.
"""
from __future__ import annotations

import os
import uuid

from core_logger import set_correlation_id


def init_correlation_id() -> str:
    cid = os.getenv("CORRELATION_ID")
    if not cid:
        cid = str(uuid.uuid4())
    set_correlation_id(cid)
    return cid
