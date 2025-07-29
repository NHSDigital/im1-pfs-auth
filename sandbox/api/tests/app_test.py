import pytest
from flask.testing import FlaskClient

from ..app import app


@pytest.fixture
def client() -> FlaskClient:
    return app.test_client()


def test_hello_world__success(client: FlaskClient) -> None:
    # Act
    actual_result = client.get("/")

    # Assert
    assert 200 == actual_result.status_code
    assert "<p>Welcome to the IM1 PFS Auth Sandbox</p>" == actual_result.get_data(
        as_text=True
    )


def test_post_authentication__success(client: FlaskClient) -> None:
    # Arrange
    headers = {"X-Forward-To": "https://example.com", "X-ODS-Code": "A29929"}

    # Act
    actual_result = client.post("/authentication", headers=headers)

    # Assert
    assert 201 == actual_result.status_code
    assert {
        "onlineUserId": "123",
        "patientId": "123",
        "sessionId": "123",
        "suid": "123",
        "userPatientLinkToken": "123",
    } == actual_result.get_json()


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
def test_post_authentication__failure(headers: dict, client: FlaskClient) -> None:
    # Act
    actual_result = client.post("/authentication", headers=headers)

    # Assert
    assert 500 == actual_result.status_code
    assert {"message": "Invalid scenario"} == actual_result.get_json()
