"""All tests in this file are for the 200 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.unhappy
@pytest.mark.parametrize("forward_to_url", [None, ""])
def test_missing_forward_to_header(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with no X-Forward-To header
        Then: the response status code is 401
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": forward_to_url,
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "message": "The request was unsuccessful due to missing required value."
    }


@pytest.mark.unhappy
@pytest.mark.parametrize("forward_to_url", ["something random", "http://example.com"])
def test_invalid_forward_to_header(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with an invalid X-Forward-To header
        Then: the response status code is 401
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": forward_to_url,
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "message": "The request was unsuccessful due to invalid value."
    }


@pytest.mark.unhappy
@pytest.mark.parametrize("ods_code", [None, ""])
def test_missing_ods_header(
    request: pytest.FixtureRequest, api_url: str, ods_code: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with no X-ODS-Code header
        Then: the response status code is 401
        And: the response body contains the expected message

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "http://emis.com",
        "X-ODS-Code": ods_code,
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "message": "The request was unsuccessful due to missing required value."
    }
