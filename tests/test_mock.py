from unittest.mock import MagicMock, patch

import pytest

from infrakit.client import InfrakitClient


@pytest.fixture
def client():
    return InfrakitClient(
        customer_id="test_customer",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )


@patch("infrakit.client.requests.get")
@patch("infrakit.client.requests.post")
def test_list_and_post_alerts(mock_post, mock_get, client):
    # Mock the responses for the GET and POST requests
    def mock_get_side_effect(url, *args, **kwargs):
        if "openid-configuration" in url:
            return MagicMock(
                status_code=200,
                json=lambda: {"token_endpoint": "https://auth.infrakit.com/token"},
            )
        elif "alerts" in url:
            return MagicMock(
                status_code=200, json=lambda: [{"id": 1, "message": "Test alert"}]
            )
        return MagicMock(status_code=404)

    mock_get.side_effect = mock_get_side_effect

    def mock_post_side_effect(url, *args, **kwargs):
        if "token" in url:
            return MagicMock(
                status_code=200, json=lambda: {"access_token": "test_access_token"}
            )
        elif "alert" in url:
            return MagicMock(
                status_code=200, json=lambda: {"id": 2, "message": "New alert"}
            )
        return MagicMock(status_code=404)

    mock_post.side_effect = mock_post_side_effect

    # Test listing alerts
    alerts = client.alerts.list()
    assert alerts == [{"id": 1, "message": "Test alert"}]
    mock_get.assert_any_call(
        f"{client.base_url()}/alerts", headers=client.auth_headers()
    )

    # Test posting an alert
    new_alert = {"message": "New alert"}
    response = client.alerts.post(new_alert)
    assert response == {"id": 2, "message": "New alert"}
    mock_post.assert_any_call(
        f"{client.base_url()}/alert", json=new_alert, headers=client.auth_headers()
    )
