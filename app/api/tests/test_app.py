from uuid import uuid4
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from app.api.app import app
from app.api.exception import AccessDenied, InvalidValue, MissingValue


@pytest.fixture
def client() -> FlaskClient:
    return app.test_client()


def test_authentication_post(client: FlaskClient) -> None:
    """Test the POST /authentication endpoint."""
    # Arrange
    path = "/authentication"
    headers = {
        "NHSD-NHSlogin-Identity-Proofing-Level": "P9",
        "NHSD-NHSlogin-NHS-Number": "some nhs number",
        "NHSD-ID-Token": "some token",
        "X-ODS-Code": "some ods code",
        "X-Request-ID": str(uuid4()),
        "X-Correlation-ID": str(uuid4()),
        "X-Forward-To": "https://example.com",
    }
    # Act
    actual_result = client.post(path, headers=headers)

    # Assert
    assert actual_result.status_code == 200
    assert actual_result.get_json() == {
        "message": "Hello from the IM1 PFS Auth API!",
        "hello": "world",
    }


@patch("app.api.app.validate_nhs_number", side_effect=AccessDenied("Test exception"))
def test_authentication_post_access_denied_exception(
    _mock_validate: MagicMock, client: FlaskClient
) -> None:
    """Test the POST /authentication endpoint with an access denied exception."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 401
    assert actual_result.get_json() == {
        "message": "Missing or invalid OAuth 2.0 bearer token in request.",
    }


@patch("app.api.app.validate_nhs_number", side_effect=InvalidValue("Test exception"))
def test_authentication_post_invalid_value_exception(
    _mock_validate: MagicMock, client: FlaskClient
) -> None:
    """Test the POST /authentication endpoint with an invalid value exception."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 400
    assert actual_result.get_json() == {
        "message": "The request was unsuccessful due to invalid value.",
    }


@patch("app.api.app.validate_nhs_number", side_effect=MissingValue("Test exception"))
def test_authentication_post_missing_value_exception(
    _mock_validate: MagicMock, client: FlaskClient
) -> None:
    """Test the POST /authentication endpoint with an missing value exception."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 400
    assert actual_result.get_json() == {
        "message": "The request was unsuccessful due to missing required value.",
    }


@patch("app.api.app.validate_forward_to", side_effect=MissingValue("Test Exception"))
@patch("app.api.app.validate_correlation_id")
@patch("app.api.app.validate_request_id")
@patch("app.api.app.validate_ods_code")
@patch("app.api.app.validate_vot_level")
@patch("app.api.app.validate_proofing_level")
@patch("app.api.app.validate_nhs_number")
def test_authentication_post_last_validation_check_fails(
    mock_validate_nhs_number: MagicMock,
    mock_validate_proofing_level: MagicMock,
    mock_validate_vot_level: MagicMock,
    mock_validate_ods_code: MagicMock,
    mock_validate_request_id: MagicMock,
    mock_validate_correlation_id: MagicMock,
    mock_validate_forward_to: MagicMock,
    client: FlaskClient,
) -> None:
    """Test the POST /authentication endpoint last validation check fails."""
    # Arrange
    path = "/authentication"
    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 400
    assert actual_result.get_json() == {
        "message": "The request was unsuccessful due to missing required value.",
    }
    mock_validate_nhs_number.assert_called_once()
    mock_validate_proofing_level.assert_called_once()
    mock_validate_vot_level.assert_called_once()
    mock_validate_ods_code.assert_called_once()
    mock_validate_request_id.assert_called_once()
    mock_validate_correlation_id.assert_called_once()
    mock_validate_forward_to.assert_called_once()


@patch("app.api.app.validate_nhs_number", side_effect=Exception("Test exception"))
def test_authentication_post_exception(
    _mock_validate: MagicMock, client: FlaskClient
) -> None:
    """Test the POST /authentication endpoint with an exception."""
    # Arrange
    path = "/authentication"

    # Act
    actual_result = client.post(path)

    # Assert
    assert actual_result.status_code == 500
    assert actual_result.get_json() == {"error": "Exception: Exception"}
