import pytest
from flask.testing import FlaskClient

from appp.api.app import app


@pytest.fixture
def client() -> FlaskClient:
    return app.test_client()


def test_authentication_post(client: FlaskClient) -> None:
    """Test the POST /authentication endpoint."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 200
    assert actual_result.get_json() == {
        "message": "Hello from the application API!",
        "hello": "world",
    }


def test_authentication_post__error(client: FlaskClient) -> None:
    """Test the POST /authentication endpoint errors produce a 500 response."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 500
    assert actual_result.get_json() == {
        "status": "error",
        "message": "An error occurred: Internal Server Error",
    }
