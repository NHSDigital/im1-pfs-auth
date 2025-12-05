"""All tests in this file are for the 401 Error response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.unhappy
def test_p5_user(request: pytest.FixtureRequest, api_url: str) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with p5 user
        Then: the response status code is 401

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003072"  # P5 User with composite token
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "https://emis.com",
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 401


@pytest.mark.unhappy
def test_missing_authorization_header(
    request: pytest.FixtureRequest, api_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with no Authorization header
        Then: the response status code is 401

    """
    # Arrange
    uuid = str(uuid4())
    headers = {
        "Authorization": None,
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "https://emis.com",
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 401


@pytest.mark.unhappy
def test_invalid_authorization_header(
    request: pytest.FixtureRequest, api_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: an invalid request is made with an invalid Authorization header
        Then: the response status code is 401

    """
    # Arrange
    uuid = str(uuid4())
    headers = {
        "Authorization": "something random",
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "https://emis.com",
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 401
