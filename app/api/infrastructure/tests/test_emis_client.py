from json import load
from os import environ
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from requests import HTTPError

from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import Demographics, ForwardResponse
from app.api.infrastructure.emis_client import EmisClient


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


@patch.dict(environ, {"USE_MOCK": "True"})
def test_emis_forward_request_use_mock(client: EmisClient) -> None:
    """Test the EmisClient forward_request function when mock is turned on."""
    # Arrange
    with Path("app/api/infrastructure/data/mocked_emis_response.json").open("r") as f:
        expected_response = load(f)
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == expected_response


@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.emis_client.requests")
def test_emis_forward_request_use_mock_on(
    mock_request: MagicMock, client: EmisClient
) -> None:
    """Test the EmisClient forward_request function when mock is turned off."""
    # Arrange
    expected_response = {"Message": "Happy Days!"}
    mock_instance = MagicMock()
    mock_instance.json.return_value = expected_response
    mock_request.post.return_value = mock_instance
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == expected_response


@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.emis_client.requests")
def test_emis_forward_request_use_mock_off(
    mock_request: MagicMock, client: EmisClient
) -> None:
    """Test the EmisClient forward_request function when mock is turned off and there is an error."""
    # Arrange
    mock_instance = MagicMock()
    mock_instance.raise_for_status.side_effect = HTTPError("Oops")
    mock_request.post.return_value = mock_instance
    # Act & Assert
    with pytest.raises(HTTPError, match="Oops"):
        client.forward_request()


def test_emis_client_transform_response(client: EmisClient) -> None:
    """Test the EmisClient transform_response function."""
    # Assert
    response = {
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
    # Act
    actual_result = client.transform_response(response)

    # Assert
    assert actual_result == ForwardResponse(
        session_id="some session",
        supplier="EMIS",
        proxy=Demographics(
            first_name="some first name",
            surname="some surname",
            title="some title",
        ),
        patients=[
            Demographics(
                first_name="some other first name",
                surname="some other surname",
                title="some other title",
            )
        ],
    )


@pytest.mark.parametrize(
    "response",
    [
        {},
        {  # Missing UserPatientLints
            "SessionId": "some session",
            "FistName": "someone's first name",
            "Surname": "someone's surname",
            "Title": "someone's title",
        },
        {  # Missing Proxy Demographic information
            "SessionId": "some session",
            "UserPatientLinks": [
                {
                    "FistName": "someone's first name",
                    "Surname": "someone's surname",
                    "Title": "someone's title",
                }
            ],
        },
        {  # Missing Session Id
            "FistName": "someone's first name",
            "Surname": "someone's surname",
            "Title": "someone's title",
            "UserPatientLinks": [
                {
                    "FistName": "someone's first name",
                    "Surname": "someone's surname",
                    "Title": "someone's title",
                }
            ],
        },
    ],
)
def test_emis_client_transform_response_raise_validation_error(
    response: Any,
    client: EmisClient,
) -> None:
    """Test the EmisClient transform_response function raises validation error."""
    # Act & Assert
    with pytest.raises(ValidationError):
        client.transform_response(response)
