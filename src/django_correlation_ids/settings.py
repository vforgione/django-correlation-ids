"""
Settings management for django_correlation_ids.

This module provides a settings manager that loads and manages the settings for
django_correlation_ids. It ensures that the settings are loaded from the Django
settings object and provides a consistent interface for accessing them.
"""

from __future__ import annotations

from django.conf import settings as djsettings


class Settings:
    """
    Settings manager for django_correlation_ids.

    This class is responsible for loading and managing the settings for the
    django_correlation_ids package. It loads the settings from the Django settings
    object and provides a consistent interface for accessing them.
    """

    DEFAULT_SETTINGS = {
        "correlation_id_header": "X-Correlation-Id",
        "request_id_header": "X-Request-Id",
        "accept_correlation_id": True,
        "recycle_request_id": False,
        "allow_response_empty_correlation_id": False,
        "allow_response_empty_request_id": False,
    }

    def __init__(self) -> None:
        self._load()

    def _load(self) -> None:
        user_settings = getattr(djsettings, "DJANGO_CORRELATION_IDS", {})
        merged_settings = self.DEFAULT_SETTINGS.copy()
        merged_settings.update(user_settings)

        self.correlation_id_header = merged_settings["correlation_id_header"]
        self.request_id_header = merged_settings["request_id_header"]
        self.accept_correlation_id = merged_settings["accept_correlation_id"]
        self.recycle_request_id = merged_settings["recycle_request_id"]
        self.allow_response_empty_correlation_id = merged_settings[
            "allow_response_empty_correlation_id"
        ]
        self.allow_response_empty_request_id = merged_settings[
            "allow_response_empty_request_id"
        ]


settings = Settings()
