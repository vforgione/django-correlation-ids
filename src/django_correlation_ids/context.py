"""
Management of Correlation ID and Request ID using context variables.

This module provides functions to manage and retrieve the Correlation ID and Request ID using
context variables.
"""

from __future__ import annotations

from contextvars import ContextVar


_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

_request_id: ContextVar[str] = ContextVar("request_id", default="")


def get_correlation_id() -> str:
    """
    Gets the current Correlation ID from the context variable

    Returns:
        str: The current Correlation ID
    """
    return _correlation_id.get()


def get_request_id() -> str:
    """
    Gets the current Request ID from the context variable

    Returns:
        str: The current Request ID
    """
    return _request_id.get()
