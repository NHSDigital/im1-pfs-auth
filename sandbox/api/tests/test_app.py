import pytest
from flask.testing import FlaskClient

from sandbox.api.app import app


@pytest.fixture
def client() -> FlaskClient:
    return app.test_client()


@pytest.mark.parametrize("path", ["/_status", "/_ping", "/health"])
def test_health_success(path: str, client: FlaskClient) -> None:
    # Act
    actual_result = client.get(path)

    # Assert
    assert actual_result.status_code == 200
    assert actual_result.get_json() == {
        "status": "online",
        "message": "IM1 PFS Auth API Sandbox is running",
    }


def test_post_authenticate__success(client: FlaskClient) -> None:
    # Arrange
    headers = {"X-Forward-To": "https://example.com", "X-ODS-Code": "A29929"}

    # Act
    actual_result = client.post("/authenticate", headers=headers)

    # Assert
    assert actual_result.status_code == 201
    assert actual_result.get_json() == {
        "sessionId": "123",
        "supplier": "TPP",
        "proxy": {"first_name": "Sarah", "surname": "Jones", "title": "Ms"},
        "patients": [{"first_name": "James", "surname": "Jones", "title": "Mr"}],
    }


@pytest.mark.parametrize(
    "headers",
    [
        {"X-Forward-To": "https://example.com"},
        {"X-ODS-Code": "A29929"},
        {"X-Forward-To": "https://bad_example.com", "X-ODS-Code": "A29929"},
        {"X-Forward-To": "https://example.com", "X-ODS-Code": "bad ods code"},
        {"X-Forward-To": 123, "X-ODS-Code": 123},
        {},
    ],
)
def test_post_authenticate__failure(headers: dict, client: FlaskClient) -> None:
    # Act
    actual_result = client.post("/authenticate", headers=headers)

    # Assert
    assert actual_result.status_code == 500
    assert actual_result.get_json() == {"message": "Invalid scenario"}
