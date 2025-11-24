"""All tests in this file are for the 201 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.positive
@pytest.mark.parametrize(
    "forward_to_url, expected_response",
    [
        (
            "https://emis.com",
            {
                "patients": [
                    {"first_name": "Alex", "surname": "Taylor", "title": "Mr"},
                    {"first_name": "Jane", "surname": "Doe", "title": "Mrs"},
                    {"first_name": "Ella", "surname": "Taylor", "title": "Ms"},
                ],
                "proxy": {"first_name": "Alex", "surname": "Taylor", "title": "Mr"},
                "session_id": "SID_2qZ9yJpVxHq4N3b",
                "end_user_session_id": "SESS_mDq6nE2b8R7KQ0v",
                "supplier": "EMIS",
            },
        )
    ],
)
def test_happy_path(
    request: pytest.FixtureRequest, api_url: str, forward_to_url: str, expected_response: dict
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: a valid request is made with correct parameters
        Then: the response status code is 201
        And: the response body contains the expected data

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"  # P9 User with composite token
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
    assert response.status_code == 201
    assert response.json() == expected_response
