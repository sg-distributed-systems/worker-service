"""
Service configuration loaded from environment variables.

Provides ServiceConfig dataclass with runtime settings including environment name
and shutdown timeout. All settings have sensible defaults and can be overridden
via APP_ENV and SHUTDOWN_TIMEOUT_SECONDS environment variables.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceConfig:
    env: str = "dev"
    shutdown_timeout: int = 10


def load_config(service_name: str) -> ServiceConfig:
    env = os.getenv("APP_ENV", "dev")
    shutdown_timeout = int(os.getenv("SHUTDOWN_TIMEOUT_SECONDS", "10"))
    return ServiceConfig(env=env, shutdown_timeout=shutdown_timeout)
