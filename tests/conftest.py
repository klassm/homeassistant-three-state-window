"""Conftest for Three State Window tests."""

from typing import Any

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: Any) -> None:
    """Enable custom integrations defined in the test dir."""
    _ = enable_custom_integrations
