from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from app.api.app import app
from app.api.domain.exception import (
    AccessDeniedError,
    ApiError,
    DownstreamError,
    InvalidValueError,
    MissingValueError,
)

FILE_PATH = "app.api.app"


@pytest.fixture
def client() -> FlaskClient:
    return app.test_client()


@patch(f"{FILE_PATH}.get_nhs_number_from_jwt_token", return_value=("patient", "proxy"))
@patch(f"{FILE_PATH}.ForwardRequest")
@patch(f"{FILE_PATH}.route_and_forward")
def test_authentication_post(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    client: FlaskClient,
) -> None:
    """Test the POST /authentication endpoint."""
    # Arrange
    mocked_forward_request_response = {"body": "Hello World!"}
    mock_instance = MagicMock()
    mock_instance.dict.return_value = mocked_forward_request_response
    mock_route_and_forward.return_value = mock_instance
    # Act
    actual_result = client.post("/authentication")

    # Assert
    assert actual_result.status_code == 200
    assert actual_result.get_json() == mocked_forward_request_response
    mock_forward_request.assert_called_once()
    mock_route_and_forward.assert_called_once_with(mock_forward_request.return_value)


@pytest.mark.parametrize(
    ("exception", "expected_status_code", "expected_message"),
    [
        (
            AccessDeniedError,
            HTTPStatus.UNAUTHORIZED,
            "Missing or invalid OAuth 2.0 bearer token in request.",
        ),
        (DownstreamError, HTTPStatus.BAD_GATEWAY, "Downstream Service Error."),
        (
            InvalidValueError,
            HTTPStatus.BAD_REQUEST,
            "The request was unsuccessful due to invalid value.",
        ),
        (
            MissingValueError,
            HTTPStatus.BAD_REQUEST,
            "The request was unsuccessful due to missing required value.",
        ),
    ],
)
@patch(f"{FILE_PATH}.get_nhs_number_from_jwt_token", return_value=("patient", "proxy"))
@patch(f"{FILE_PATH}.ForwardRequest")
@patch(f"{FILE_PATH}.route_and_forward")
def test_authentication_post_api_exception(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    exception: ApiError,
    expected_status_code: HTTPStatus,
    expected_message: str,
    client: FlaskClient,
) -> None:
    """Test the POST /authentication endpoint with an api exception."""
    # Arrange
    mock_forward_request.side_effect = exception("Testing")

    # Act
    actual_result = client.post("/authentication")

    # Assert
    assert actual_result.status_code == expected_status_code
    assert actual_result.get_json() == {"message": expected_message}
    mock_forward_request.assert_called_once()
    mock_route_and_forward.assert_not_called()


@patch(f"{FILE_PATH}.get_nhs_number_from_jwt_token", return_value=("patient", "proxy"))
@patch(f"{FILE_PATH}.ForwardRequest")
@patch(f"{FILE_PATH}.route_and_forward")
def test_authentication_post_exception(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    client: FlaskClient,
) -> None:
    """Test the POST /authentication endpoint with unknown exception."""
    # Arrange
    mock_route_and_forward.side_effect = Exception("Testing")

    # Act
    actual_result = client.post("/authentication")

    # Assert
    assert actual_result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert actual_result.get_json() == {"error": "Exception: Exception"}
    mock_forward_request.assert_called_once()
    mock_route_and_forward.assert_called_once_with(mock_forward_request.return_value)
