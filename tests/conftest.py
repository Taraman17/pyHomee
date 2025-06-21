"""Fixtures for pyHomee tests."""

import pytest

from pyHomee import Homee


HOMEE_IP = "192.168.1.1"
HOMEE_USER = "homee_user"
HOMEE_PASSWORD = "homee_password"
HOMEE_DEVICE_ID = "testdevice"
RECONNECT_INTERVAL = 10
MAX_RETRIES = 100
TEST_TOKEN = "VwZ5S9I1nMFbuHcY41I6eoAa2yjHWsvVdvbZibq4cf7EP9hBjIgKHBaUjrV4vRjq"
TEST_EXPIRATION = 31536000


@pytest.fixture
def test_homee() -> Homee:
    """Return a Homee instance."""
    return Homee(
        host=HOMEE_IP,
        user=HOMEE_USER,
        password=HOMEE_PASSWORD,
        device=HOMEE_DEVICE_ID,
        reconnect_interval=RECONNECT_INTERVAL,
        max_retries=MAX_RETRIES,
    )
