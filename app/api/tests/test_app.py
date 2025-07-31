from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from app.api.app import app


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
        "message": "Hello from the IM1 PFS Auth API!",
        "hello": "world",
    }


@patch("app.api.app.getenv", side_effect=Exception("Test exception"))
def test_authentication_post_exception(
    _mock_getenv: MagicMock, client: FlaskClient
) -> None:
    """Test the POST /authentication endpoint with an exception."""
    # Arrange
    path = "/authentication"

    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 500
    assert actual_result.get_json() == {"error": "Exception: Exception"}
