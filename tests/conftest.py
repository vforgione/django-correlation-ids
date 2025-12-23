from __future__ import annotations

import pytest
from django_correlation_ids import context


@pytest.fixture(autouse=True)
def clear_context():
    context._correlation_id.set("")
    context._request_id.set("")
    yield
