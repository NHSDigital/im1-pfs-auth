"""All tests in this file are for the 200 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.positive
def test_happy_path__emis(request: pytest.FixtureRequest, api_url: str) -> None:
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
        "Authorization": get_authentication_token(
            request
        ),  # Should be an access token for a composite token
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "",  # We need to update this to be EMIS
        "X-ODS-Code": "",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    logger.info(
        f"API response: status_code {response.status_code}, response: {response.json()}"
    )
    assert response.status_code == 200
