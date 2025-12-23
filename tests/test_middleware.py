from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper


def test_middleware_generates_correlation_id():
    url = reverse("echo_context")
    client = Client()

    res = client.get(url)
    data = res.json()
    assert data["correlation_id"] != ""
    assert res.has_header("X-Correlation-Id")
    assert data["correlation_id"] == res.headers["X-Correlation-Id"]


def test_middleware_uses_request_correlation_id():
    url = reverse("echo_context")
    client = Client()
    corrid = "test-corrlation-id"

    res = client.get(url, headers={"X-Correlation-Id": corrid})
    data = res.json()
    assert data["correlation_id"] == corrid
    assert res.has_header("X-Correlation-Id")
    assert data["correlation_id"] == res.headers["X-Correlation-Id"]


def test_middleware_recycles_request_id(settings: SettingsWrapper):
    settings.DJANGO_CORRELATION_IDS = {"recycle_request_id": True}

    url = reverse("echo_context")
    client = Client()
    reqid = "test-request-id"

    res = client.get(url, headers={"X-Request-Id": reqid})
    data = res.json()
    assert res.has_header("X-Correlation-Id")
    assert res.has_header("X-Request-Id")
    assert (
        data["request_id"]
        == data["correlation_id"]
        == res.headers["X-Request-Id"]
        == res.headers["X-Correlation-Id"]
        == reqid
    )
