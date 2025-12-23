from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from pytest import LogCaptureFixture
    from pytest_django.fixtures import SettingsWrapper


def test_logs_contain_contextvars(caplog: LogCaptureFixture, settings: SettingsWrapper):
    settings.DJANGO_CORRELATION_IDS = {"log_request_id": True}

    url = reverse("echo_context")
    client = Client()

    _ = client.get(url)
    assert caplog.records[0].correlation_id != ""  # pyright: ignore[reportAttributeAccessIssue]
    assert caplog.records[0].request_id == ""  # pyright: ignore[reportAttributeAccessIssue]

    caplog.clear()
    settings.DJANGO_CORRELATION_IDS = {
        "log_request_id": True,
        "recycle_request_id": True,
    }
    reqid = "test-request-id"

    _ = client.get(url, headers={"X-Request-Id": reqid})
    assert caplog.records[0].correlation_id == reqid  # pyright: ignore[reportAttributeAccessIssue]
    assert caplog.records[0].request_id == reqid  # pyright: ignore[reportAttributeAccessIssue]
