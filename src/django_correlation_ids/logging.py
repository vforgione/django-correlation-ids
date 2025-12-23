"""
Logging resources for adding Correlation IDs and Request IDs to log records.

This module provides a logging filter that adds the Correlation ID and Request ID to log records.
"""

from __future__ import annotations

from logging import Filter
from typing import TYPE_CHECKING

from django_correlation_ids import context

if TYPE_CHECKING:
    from logging import LogRecord


class CorrelationFilter(Filter):
    """
    Logging filter to add Correlation ID and Request ID to log records.
    """

    def filter(self, record: LogRecord) -> bool:
        record.correlation_id = context.get_correlation_id()
        record.request_id = context.get_request_id()
        return True
