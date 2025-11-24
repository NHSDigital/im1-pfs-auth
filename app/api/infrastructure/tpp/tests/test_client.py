from json import load
from os import environ
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from requests import HTTPError

from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import Demographics, ForwardResponse
from app.api.infrastructure.tpp.client import TPPClient


@pytest.fixture(name="client")
def setup_client() -> TPPClient:
    request = ForwardRequest(
        application_id="some application id",
        forward_to="https://somewhere",
        patient_nhs_number="1234567890",
        patient_ods_code="some patient ods code",
        proxy_nhs_number="0987654321",
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
    # Arrange
    with Path("app/api/infrastructure/tpp/data/mocked_response.json").open("r") as f:
        expected_response = load(f)
    # Act
    actual_result = client.forward_request()

    # Assert
    assert actual_result == expected_response


@patch.dict(environ, {"USE_MOCK": "False"})
@patch("app.api.infrastructure.tpp.client.requests")
def test_tpp_forward_request_use_mock_off(
    mock_request: MagicMock, client: TPPClient
) -> None:
    """Test the TPPClient forward_request function when mock is turned off."""
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
@patch("app.api.infrastructure.tpp.client.requests")
def test_tpp_forward_request_use_mock_off_exception(
    mock_request: MagicMock, client: TPPClient
) -> None:
    """Test the TPPClient forward_request function when mock is turned off and there is an error."""  # noqa: E501
    # Arrange
    mock_instance = MagicMock()
    mock_instance.raise_for_status.side_effect = HTTPError("Oops")
    mock_request.post.return_value = mock_instance
    # Act & Assert
    with pytest.raises(HTTPError, match="Oops"):
        client.forward_request()


def test_tpp_client_transform_response(client: TPPClient) -> None:
    """Test the TPPClient transform_response function."""
    # Assert
    with Path("app/api/infrastructure/tpp/data/mocked_response.json").open("r") as f:
        response = load(f)
    # Act
    actual_result = client.transform_response(response)

    # Assert
    assert actual_result == ForwardResponse(
        session_id="xhvE9/jCjdafytcXBq8LMKMgc4wA/w5k/O5C4ip0Fs9GPbIQ/WRIZi4Och1Spmg7aYJR2CZVLHfu6cRVv84aEVrRE8xahJbT4TPAr8N/CYix6TBquQsZibYXYMxJktXcYKwDhBH8yr3iJYnyevP3hV76oTjVmKieBtYzSSZAOu4=",
        end_user_session_id="9cbf400000000000",
        supplier="TPP",
        proxy=Demographics(first_name="Sam", surname="Jones", title="Mr"),
        patients=[Demographics(first_name="Clare", surname="Jones", title="Mrs")],
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
