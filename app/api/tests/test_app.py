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
def test_authenticate_post(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    client: FlaskClient,
) -> None:
    """Test the POST /authenticate endpoint."""
    # Arrange
    application_id = "some application id"
    forward_url = "some url"
    ods_code = "some ods code"
    use_mock = True
    mocked_forward_request_response = {"body": "Hello World!"}
    mock_instance = MagicMock()
    mock_instance.model_dump_json.return_value = mocked_forward_request_response
    mock_route_and_forward.return_value = mock_instance
    # Act
    actual_result = client.post(
        "/authenticate",
        headers={
            "NHSE-Application-ID": application_id,
            "NHSE-Forward-To": forward_url,
            "NHSE-ODS-Code": ods_code,
            "NHSE-Use-Mock": use_mock,
            "NHSE-ID-Token": "some token",
        },
    )

    # Assert
    assert actual_result.status_code == 201
    assert actual_result.get_json() == mocked_forward_request_response
    mock_forward_request.assert_called_once_with(
        application_id=application_id,
        forward_to=forward_url,
        patient_nhs_number="patient",
        patient_ods_code=ods_code,
        proxy_nhs_number="proxy",
        use_mock=use_mock,
    )
    mock_route_and_forward.assert_called_once_with(mock_forward_request.return_value)


@pytest.mark.parametrize(
    ("exception", "expected_status_code", "expected_body"),
    [
        (
            AccessDeniedError,
            HTTPStatus.UNAUTHORIZED,
            {
                "issue": [
                    {
                        "code": "forbidden",
                        "details": {
                            "coding": [
                                {
                                    "code": "ACCESS_DENIED",
                                    "display": "Missing or invalid OAuth 2.0 bearer token in request",  # noqa: E501
                                    "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                                    "version": "1",
                                }
                            ]
                        },
                        "diagnostics": "Missing or invalid OAuth 2.0 bearer token in request",  # noqa: E501
                        "severity": "error",
                    }
                ],
                "resourceType": "OperationOutcome",
            },
        ),
        (
            DownstreamError,
            HTTPStatus.BAD_GATEWAY,
            {
                "issue": [
                    {
                        "code": "processing",
                        "details": {
                            "coding": [
                                {
                                    "code": "DOWNSTREAM_SERVICE_ERROR",
                                    "display": "Failed to generate response",
                                    "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                                    "version": "1",
                                }
                            ]
                        },
                        "diagnostics": "Downstream Service Error - Failed to generate response is present in the response",  # noqa: E501
                        "severity": "error",
                    }
                ],
                "resourceType": "OperationOutcome",
            },
        ),
        (
            InvalidValueError,
            HTTPStatus.BAD_REQUEST,
            {
                "issue": [
                    {
                        "code": "exception",
                        "details": {
                            "coding": [
                                {
                                    "code": "INVALID_HEADER",
                                    "display": "A header is invalid",
                                    "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                                    "version": "1",
                                }
                            ]
                        },
                        "diagnostics": "Invalid header request",
                        "severity": "error",
                    }
                ],
                "resourceType": "OperationOutcome",
            },
        ),
        (
            MissingValueError,
            HTTPStatus.BAD_REQUEST,
            {
                "issue": [
                    {
                        "code": "exception",
                        "details": {
                            "coding": [
                                {
                                    "code": "MISSING_HEADER",
                                    "display": "A required header is missing",
                                    "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                                    "version": "1",
                                }
                            ]
                        },
                        "diagnostics": "The request was unsuccessful due to missing required value",  # noqa: E501
                        "severity": "error",
                    }
                ],
                "resourceType": "OperationOutcome",
            },
        ),
    ],
)
@patch(f"{FILE_PATH}.get_nhs_number_from_jwt_token", return_value=("patient", "proxy"))
@patch(f"{FILE_PATH}.ForwardRequest")
@patch(f"{FILE_PATH}.route_and_forward")
def test_authenticate_post_api_exception(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    exception: ApiError,
    expected_status_code: HTTPStatus,
    expected_body: dict,
    client: FlaskClient,
) -> None:
    """Test the POST /authenticate endpoint with an api exception."""
    # Arrange
    mock_forward_request.side_effect = exception("Testing")

    # Act
    actual_result = client.post("/authenticate")

    # Assert
    assert actual_result.status_code == expected_status_code
    assert actual_result.get_json() == expected_body
    mock_forward_request.assert_called_once()
    mock_route_and_forward.assert_not_called()


@patch(f"{FILE_PATH}.get_nhs_number_from_jwt_token", return_value=("patient", "proxy"))
@patch(f"{FILE_PATH}.ForwardRequest")
@patch(f"{FILE_PATH}.route_and_forward")
def test_authenticate_post_exception(
    mock_route_and_forward: MagicMock,
    mock_forward_request: MagicMock,
    _mock_get_nhs_number_from_jwt_token: MagicMock,
    client: FlaskClient,
) -> None:
    """Test the POST /authenticate endpoint with unknown exception."""
    # Arrange
    mock_route_and_forward.side_effect = Exception("Testing")

    # Act
    actual_result = client.post("/authenticate")

    # Assert
    assert actual_result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert actual_result.get_json() == {
        "issue": [
            {
                "code": "exception",
                "details": {
                    "coding": [
                        {
                            "code": "SERVER_ERROR",
                            "display": "Failed to generate response",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "Internal Server Error - Failed to generate response is present in the response",  # noqa: E501
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }
    mock_forward_request.assert_called_once()
    mock_route_and_forward.assert_called_once_with(mock_forward_request.return_value)
