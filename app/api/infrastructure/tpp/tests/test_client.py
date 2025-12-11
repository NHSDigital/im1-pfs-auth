from os import environ
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import xmltodict
from pydantic import ValidationError

from app.api.domain.exception import (
    ApiError,
    DownstreamError,
    ForbiddenError,
    InvalidValueError,
    NotFoundError,
)
from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import Demographics
from app.api.infrastructure.tpp.client import TPPClient
from app.api.infrastructure.tpp.models import (
    Patient,
    ServiceAccess,
    ServiceAccessDescription,
    ServiceAccessStatus,
    ServiceAccessStatusDescription,
    SessionResponse,
)

with Path("app/api/infrastructure/tpp/data/mocked_response.xml", encoding="utf-8").open(
    "r"
) as f:
    MOCKED_RESPONSE = f.read()


@pytest.fixture(name="client")
def setup_client() -> TPPClient:
    request = ForwardRequest(
        application_id="some application id",
        forward_to="https://somewhere",
        patient_nhs_number="1234567890",
        patient_ods_code="some patient ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )
    return TPPClient(request)


def test_tpp_client_get_headers(client: TPPClient) -> None:
    """Test the TPPClient get_headers function."""
    # Act
    actual_result = client.get_headers()

    # Assert
    assert actual_result == {
        "type": "CreateSession",
    }


@patch("app.api.infrastructure.tpp.models.uuid4", return_value="unique value")
def test_tpp_client_get_data(_: MagicMock, client: TPPClient) -> None:
    """Test the TPPClient get_data function."""
    # Act
    actual_result = client.get_data()

    # Assert
    assert actual_result == {
        "apiVersion": "1",
        "uuid": "unique value",
        "User": {"Identifier": {"value": "0987654321", "type": "NhsNumber"}},
        "Patient": {
            "Identifier": {"value": "1234567890", "type": "NhsNumber"},
            "UnitId": "some patient ods code",
        },
        "Application": {
            "name": "NhsApp",
            "version": "1.0",
            "providerId": "some application id",
            "deviceType": "NhsApp",
        },
    }


@patch.dict(environ, {"USE_MOCK": "True"})
def test_tpp_forward_request_use_mock_on(client: TPPClient) -> None:
    """Test the TPPClient forward_request function when mock is turned on."""
    # Assert
    client.request.use_mock = True
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == xmltodict.parse(MOCKED_RESPONSE)


@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.tpp.client.requests")
def test_tpp_forward_request_use_mock_off(
    mock_request: MagicMock, client: TPPClient
) -> None:
    """Test the TPPClient forward_request function when mock is turned off."""
    # Arrange
    mock_instance = MagicMock()
    mock_instance.status_code = 201
    mock_instance.text = MOCKED_RESPONSE
    mock_request.post.return_value = mock_instance
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == xmltodict.parse(MOCKED_RESPONSE)


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
@patch("app.api.infrastructure.tpp.client.requests")
def test_tpp_forward_request_use_mock_off_exception(
    mock_request: MagicMock,
    client: TPPClient,
    status_code: int,
    error_msg: str,
    api_error: ApiError,
) -> None:
    """Test the TPPClient forward_request function when mock is turned off and there is an error."""  # noqa: E501
    # Arrange
    mock_instance = MagicMock()
    mock_instance.status_code = status_code
    mock_instance.text = f"""<Error>
        <message>{error_msg}</message>
        </Error>"""
    mock_request.post.return_value = mock_instance
    # Act & Assert
    with pytest.raises(api_error, match=error_msg):
        client.forward_request()


def test_tpp_client_transform_response(client: TPPClient) -> None:
    """Test the TPPClient transform_response function."""
    # Act
    actual_result = client.transform_response(xmltodict.parse(MOCKED_RESPONSE))

    # Assert
    assert actual_result == SessionResponse(
        sessionId="xhvE9/jCjdafytcXBq8LMKMgc4wA/w5k/O5C4ip0Fs9GPbIQ/WRIZi4Och1Spmg7aYJR2CZVLHfu6cRVv84aEVrRE8xahJbT4TPAr8N/CYix6TBquQsZibYXYMxJktXcYKwDhBH8yr3iJYnyevP3hV76oTjVmKieBtYzSSZAOu4=",
        supplier="TPP",
        proxy=Demographics(firstName="Sam", surname="Jones", title="Mr"),
        patients=[
            Patient(
                firstName="Clare",
                surname="Jones",
                title="Mrs",
                permissions=[
                    ServiceAccess(
                        description=ServiceAccessDescription("Full Clinical Record"),
                        serviceIdentifier=1,
                        status=ServiceAccessStatus("U"),
                        statusDescription=ServiceAccessStatusDescription("Unavailable"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=2,
                        description=ServiceAccessDescription("Appointments"),
                        status=ServiceAccessStatus("A"),
                        statusDescription=ServiceAccessStatusDescription("Available"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=4,
                        description=ServiceAccessDescription("Request Medication"),
                        status=ServiceAccessStatus("A"),
                        statusDescription=ServiceAccessStatusDescription("Available"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=8,
                        description=ServiceAccessDescription("Questionnaires"),
                        status=ServiceAccessStatus("N"),
                        statusDescription=ServiceAccessStatusDescription(
                            "Not offered by unit"
                        ),
                    ),
                    ServiceAccess(
                        serviceIdentifier=64,
                        description=ServiceAccessDescription("Summary Record"),
                        status=ServiceAccessStatus("A"),
                        statusDescription=ServiceAccessStatusDescription("Available"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=128,
                        description=ServiceAccessDescription("Detailed Coded Record"),
                        status=ServiceAccessStatus("U"),
                        statusDescription=ServiceAccessStatusDescription("Unavailable"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=512,
                        description=ServiceAccessDescription("Messaging"),
                        status=ServiceAccessStatus("A"),
                        statusDescription=ServiceAccessStatusDescription("Available"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=1024,
                        description=ServiceAccessDescription("View Sharing Status"),
                        status=ServiceAccessStatus("N"),
                        statusDescription=ServiceAccessStatusDescription(
                            "Not offered by unit"
                        ),
                    ),
                    ServiceAccess(
                        serviceIdentifier=2048,
                        description=ServiceAccessDescription("Record Audit"),
                        status=ServiceAccessStatus("A"),
                        statusDescription=ServiceAccessStatusDescription("Available"),
                    ),
                    ServiceAccess(
                        serviceIdentifier=4096,
                        description=ServiceAccessDescription("Change Pharmacy"),
                        status=ServiceAccessStatus("N"),
                        statusDescription=ServiceAccessStatusDescription(
                            "Not offered by unit"
                        ),
                    ),
                    ServiceAccess(
                        serviceIdentifier=8192,
                        description=ServiceAccessDescription(
                            "Manage Sharing Rules And Requests"
                        ),
                        status=ServiceAccessStatus("G"),
                        statusDescription=ServiceAccessStatusDescription(
                            "Only available to GMS registered patients"
                        ),
                    ),
                    ServiceAccess(
                        serviceIdentifier=65536,
                        description=ServiceAccessDescription("Access SystmConnect"),
                        status=ServiceAccessStatus("O"),
                        statusDescription=ServiceAccessStatusDescription("Other"),
                    ),
                ],
            )
        ],
    )


@pytest.mark.parametrize(
    "response",
    [
        {},
        {  # Missing PatientAccess
            "suid": "some session",
            "User": {
                "Person": {
                    "PersonName": {
                        "firstName": "someone's first name",
                        "surname": "someone's surname",
                        "title": "someone's title",
                    }
                }
            },
        },
        {  # Missing Proxy Demographic information
            "SessionId": "some session",
            "PatientAccess": [
                {
                    "PersonName": {
                        "firstName": "someone's first name",
                        "surname": "someone's surname",
                        "title": "someone's title",
                    }
                }
            ],
        },
        {  # Missing Session Id
            "User": {
                "Person": {
                    "PersonName": {
                        "firstName": "someone's first name",
                        "surname": "someone's surname",
                        "title": "someone's title",
                    }
                }
            },
            "PatientAccess": [
                {
                    "PersonName": {
                        "firstName": "someone's first name",
                        "surname": "someone's surname",
                        "title": "someone's title",
                    }
                }
            ],
        },
    ],
)
def test_tpp_client_transform_response_raise_validation_error(
    response: dict,
    client: TPPClient,
) -> None:
    """Test the TPPClient transform_response function raises validation error."""
    # Act & Assert
    with pytest.raises(ValidationError):
        client.transform_response(response)
