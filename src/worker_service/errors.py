"""
Application error types for structured error handling.

Provides AppError base class that converts exceptions into log-friendly dictionaries.
Subclass AppError and set a unique 'code' for each error type in your service.
Use to_log_fields() when logging errors to include error_type, error_code, etc.
"""
from __future__ import annotations

from typing import Any, Dict, Optional


class AppError(Exception):
    code: str = "APP_ERROR"

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def to_log_fields(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.code,
            "error_message": self.message,
            "error_details": self.details or {},
        }


class ValidationError(AppError):
    """Raised when input validation fails."""

    code: str = "VALIDATION_ERROR"


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    code: str = "NOT_FOUND"
