"""All tests in this file are for the 200 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.positive
@pytest.mark.parametrize("forward_to_url", ["https://emis.com"])
def test_happy_path(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: a valid request is made with correct parameters
        Then: the response status code is 200
        And: the response body contains the expected data

    NOTE: This test does not work due to missing composite derived access token.
    """
    # Arrange
    uuid = str(uuid4())
    headers = {
        "Authorization": get_authentication_token(request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": forward_to_url,
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    logger.info(
        f"API response: status_code {response.status_code}, response: {response.json()}"
    )
    assert response.status_code == 201
