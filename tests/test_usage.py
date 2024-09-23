import pytest

from infrakit.client import InfrakitClient


@pytest.fixture
def client():
    return InfrakitClient.from_env_file(".env.secrets")


def test_list_alerts(client: InfrakitClient):
    alerts = client.alerts.list()
    assert isinstance(alerts, list)
    assert all(isinstance(alert, dict) for alert in alerts)
