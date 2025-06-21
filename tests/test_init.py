"""Test initialization of the Homee class."""
from pyHomee import Homee

from .conftest import (
    HOMEE_IP,
    HOMEE_USER,
    HOMEE_PASSWORD,
    HOMEE_DEVICE_ID,
    RECONNECT_INTERVAL,
    MAX_RETRIES
)

def test_initialize_homee() -> None:
    """Test that Homee can be initialized correctly."""
    homee = Homee(
        host=HOMEE_IP,
        user=HOMEE_USER,
        password=HOMEE_PASSWORD,
        device=HOMEE_DEVICE_ID,
        reconnect_interval=RECONNECT_INTERVAL,
        max_retries=MAX_RETRIES,
    )
    assert homee.host == HOMEE_IP
    assert homee.user == HOMEE_USER
    assert homee.password == HOMEE_PASSWORD
    assert homee.device == HOMEE_DEVICE_ID
    assert homee.reconnect_interval == RECONNECT_INTERVAL
    assert homee.max_retries == MAX_RETRIES
    assert not homee.connected
