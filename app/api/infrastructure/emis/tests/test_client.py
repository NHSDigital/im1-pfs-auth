from json import load
from os import environ
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from app.api.domain.exception import (
    ApiError,
    DownstreamError,
    ForbiddenError,
    InvalidValueError,
    NotFoundError,
)
from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import (
    Demographics,
    ForwardResponse,
    Patient,
    Permissions,
    ViewPermissions,
)
from app.api.infrastructure.emis.client import EmisClient


@pytest.fixture(name="client")
def setup_client() -> EmisClient:
    request = ForwardRequest(
        application_id="some application id",
        forward_to="https://somewhere",
        patient_nhs_number="1234567890",
        patient_ods_code="some patient ods code",
        proxy_nhs_number="0987654321",
    )
    return EmisClient(request)


def test_emis_client_get_headers(client: EmisClient) -> None:
    """Test the EmisClient get_headers function."""
    # Act
    actual_result = client.get_headers()

    # Assert
    assert actual_result == {
        "X-API-ApplicationId": "some application id",
        "X-API-Version": "1",
    }


def test_emis_client_get_data(client: EmisClient) -> None:
    """Test the EmisClient get_data function."""
    # Act
    actual_result = client.get_data()

    # Assert
    assert actual_result == {
        "PatientIdentifier": {
            "IdentifierValue": "1234567890",
            "IdentifierType": "NhsNumber",
        },
        "UserIdentifier": {
            "IdentifierValue": "0987654321",
            "IdentifierType": "NhsNumber",
        },
        "PatientNationalPracticeCode": "some patient ods code",
    }


@patch.dict(environ, {"USE_MOCK": "True"})
def test_emis_forward_request_use_mock_on(client: EmisClient) -> None:
    """Test the EmisClient forward_request function when mock is turned on."""
    # Arrange
    with Path("app/api/infrastructure/emis/data/mocked_response.json").open("r") as f:
        expected_response = load(f)
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == expected_response


@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.emis.client.requests")
def test_emis_forward_request_use_mock_off(
    mock_request: MagicMock, client: EmisClient
) -> None:
    """Test the EmisClient forward_request function when mock is turned off."""
    # Arrange
    expected_response = {"Message": "Happy Days!"}
    mock_instance = MagicMock()
    mock_instance.status_code = 201
    mock_instance.json.return_value = expected_response
    mock_request.post.return_value = mock_instance
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == expected_response


@pytest.mark.parametrize(
    ("status_code", "error_msg", "api_error"),
    [
        (400, "No online account exists for the given user.", InvalidValueError),
        (401, "Unauthorised.", ForbiddenError),
        (404, "Not Found.", NotFoundError),
        (500, "", DownstreamError),
    ],
)
@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.emis.client.requests")
def test_tpp_forward_request_use_mock_off_exception(
    mock_request: MagicMock,
    client: EmisClient,
    status_code: int,
    error_msg: str,
    api_error: ApiError,
) -> None:
    """Test the EmisClient forward_request function when mock is turned off and there is an error."""  # noqa: E501
    # Arrange
    mock_instance = MagicMock()
    mock_instance.status_code = status_code
    mock_instance.json.return_value = {"message": error_msg}
    mock_request.post.return_value = mock_instance
    # Act & Assert
    with pytest.raises(api_error, match=error_msg):
        client.forward_request()


def test_emis_client_transform_response(client: EmisClient) -> None:
    """Test the EmisClient transform_response function."""
    # Assert
    with Path("app/api/infrastructure/emis/data/mocked_response.json").open("r") as f:
        response = load(f)
    # Act
    actual_result = client.transform_response(response)

    # Assert
    assert actual_result == ForwardResponse(
        sessionId="SID_2qZ9yJpVxHq4N3b",
        supplier="EMIS",
        proxy=Demographics(firstName="Alex", surname="Taylor", title="Mr"),
        patients=[
            Patient(
                firstName="Alex",
                surname="Taylor",
                title="Mr",
                permissions=Permissions(
                    accessSystemConnect=False,
                    bookAppointments=True,
                    changePharamacy=True,
                    messagePractice=False,
                    provideInformationToPractice=False,
                    requestMedication=True,
                    updateDemographics=True,
                    manageOnlineTriage=False,
                    view=ViewPermissions(
                        medicalRecord=True,
                        summaryMedicalRecord=True,
                        allergiesMedicalRecord=True,
                        consultationsMedicalRecord=True,
                        immunisationsMedicalRecord=True,
                        documentsMedicalRecord=True,
                        medicationMedicalRecord=True,
                        problemsMedicalRecord=True,
                        testResultsMedicalRecord=True,
                        recordAudit=True,
                        recordSharing=False,
                    ),
                ),
            ),
            Patient(
                firstName="Jane",
                surname="Doe",
                title="Mrs",
                permissions=Permissions(
                    accessSystemConnect=False,
                    bookAppointments=False,
                    changePharamacy=True,
                    messagePractice=True,
                    provideInformationToPractice=True,
                    requestMedication=True,
                    updateDemographics=True,
                    manageOnlineTriage=True,
                    view=ViewPermissions(
                        medicalRecord=True,
                        summaryMedicalRecord=True,
                        allergiesMedicalRecord=True,
                        consultationsMedicalRecord=True,
                        immunisationsMedicalRecord=True,
                        documentsMedicalRecord=True,
                        medicationMedicalRecord=True,
                        problemsMedicalRecord=True,
                        testResultsMedicalRecord=True,
                        recordAudit=True,
                        recordSharing=False,
                    ),
                ),
            ),
            Patient(
                firstName="Ella",
                surname="Taylor",
                title="Ms",
                permissions=Permissions(
                    accessSystemConnect=False,
                    bookAppointments=True,
                    changePharamacy=False,
                    messagePractice=True,
                    provideInformationToPractice=True,
                    requestMedication=False,
                    updateDemographics=True,
                    manageOnlineTriage=False,
                    view=ViewPermissions(
                        medicalRecord=True,
                        summaryMedicalRecord=True,
                        allergiesMedicalRecord=True,
                        consultationsMedicalRecord=True,
                        immunisationsMedicalRecord=True,
                        documentsMedicalRecord=True,
                        medicationMedicalRecord=True,
                        problemsMedicalRecord=True,
                        testResultsMedicalRecord=True,
                        recordAudit=True,
                        recordSharing=False,
                    ),
                ),
            ),
        ],
    )


@pytest.mark.parametrize(
    "response",
    [
        {},
        {  # Missing UserPatientLints
            "SessionId": "some session",
            "FirstName": "someone's first name",
            "Surname": "someone's surname",
            "Title": "someone's title",
        },
        {  # Missing Proxy Demographic information
            "SessionId": "some session",
            "UserPatientLinks": [
                {
                    "FirstName": "someone's first name",
                    "Surname": "someone's surname",
                    "Title": "someone's title",
                }
            ],
        },
        {  # Missing Session Id
            "FirstName": "someone's first name",
            "Surname": "someone's surname",
            "Title": "someone's title",
            "UserPatientLinks": [
                {
                    "FirstName": "someone's first name",
                    "Surname": "someone's surname",
                    "Title": "someone's title",
                }
            ],
        },
    ],
)
def test_emis_client_transform_response_raise_validation_error(
    response: dict,
    client: EmisClient,
) -> None:
    """Test the EmisClient transform_response function raises validation error."""
    # Act & Assert
    with pytest.raises(ValidationError):
        client.transform_response(response)
