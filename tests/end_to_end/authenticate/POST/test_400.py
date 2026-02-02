"""All tests in this file are for the 400 Error response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import Response, post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


def assert_invalid_header_error_response(response: Response) -> None:
    """Asserts Response indicates request is bad due to invalid header value.

    Args:
        response (Response): Response to assert against
    """
    assert response.status_code == 400
    assert response.json() == {
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
    }


def assert_missing_header_error_response(response: Response) -> None:
    """Asserts Response indicates request is bad.

    Args:
        response (Response): Response to assert against
    """
    assert response.status_code == 400
    assert response.json() == {
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
    }


@pytest.mark.unhappy
@pytest.mark.parametrize("forward_to_url", [None, ""])
def test_missing_forward_to_header(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with no NHSE-Forward-To header
        Then: the response status code is 400
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "NHSE-Application-ID": request.node.name,
        "NHSE-Request-ID": uuid,
        "NHSE-Forward-To": forward_to_url,
        "NHSE-ODS-Code": "ODS123",
        "NHSE-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert_missing_header_error_response(response)


@pytest.mark.unhappy
@pytest.mark.parametrize(
    "forward_to_url", ["something random", "www.google.com", "https://google.com"]
)
def test_invalid_forward_to_header(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with an invalid NHSE-Forward-To header
        Then: the response status code is 400
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "NHSE-Application-ID": request.node.name,
        "NHSE-Request-ID": uuid,
        "NHSE-Forward-To": forward_to_url,
        "NHSE-ODS-Code": "ODS123",
        "NHSE-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert_invalid_header_error_response(response)


@pytest.mark.unhappy
@pytest.mark.parametrize("ods_code", [None, ""])
def test_missing_ods_header(
    request: pytest.FixtureRequest, api_url: str, ods_code: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with no NHSE-ODS-Code header
        Then: the response status code is 400
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "NHSE-Application-ID": request.node.name,
        "NHSE-Request-ID": uuid,
        "NHSE-Forward-To": "http://emis.com",
        "NHSE-ODS-Code": ods_code,
        "NHSE-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert_missing_header_error_response(response)
