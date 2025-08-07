import pytest
from pydantic import ValidationError
from json import dumps
from requests import Response

from ...domain.forward_request_model import ForwardRequest
from ...domain.forward_response_model import ForwardResponse, Demographics
from ..emis_client import EmisClient


@pytest.fixture(name="client")
def setup_client() -> EmisClient:
    request = ForwardRequest(
        application_id="some application id",
        forward_to="https://somewhere",
        patient_nhs_number="some patient nhs number",
        patient_ods_code="some patient ods code",
        proxy_nhs_number="some proxy nhs number",
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
            "IdentifierValue": "some patient nhs number",
            "IdentifierType": "NhsNumber",
        },
        "CarerIdentifier": {
            "IdentifierValue": "some proxy nhs number",
            "IdentifierType": "NhsNumber",
        },
        "PatientNationalPracticeCode": "some patient ods code",
    }


def test_emis_client_transform_response(client: EmisClient) -> None:
    """Test the EmisClient transform_response function."""
    # Assert
    content = dumps(
        {
            "SessionId": "some session",
            "FirstName": "some first name",
            "Surname": "some surname",
            "Title": "some title",
            "UserPatientLinks": [
                {
                    "Forenames": "some other first name",
                    "Surname": "some other surname",
                    "Title": "some other title",
                }
            ],
        }
    )
    response = Response()
    response._content = content.encode("utf-8")
    # Act
    actual_result = client.transform_response(response)

    # Assert
    assert actual_result == ForwardResponse(
        first_name="some first name",
        surname="some surname",
        title="some title",
        session_id="some session",
        patients=[
            Demographics(
                first_name="some other first name",
                surname="some other surname",
                title="some other title",
            )
        ],
    )


def test_emis_client_transform_response_raise_validation_error(
    client: EmisClient,
) -> None:
    """Test the EmisClient transform_response function raises validation error."""
    # Assert
    content = dumps({})
    response = Response()
    response._content = content.encode("utf-8")
    # Act & Assert
    with pytest.raises(ValidationError):
        client.transform_response(response)
