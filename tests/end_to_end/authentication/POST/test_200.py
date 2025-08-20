"""All tests in this file are for the 200 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.positive
def test_lol(request: pytest.FixtureRequest, api_url: str) -> None:
    # Arrange
    uuid = str(uuid4())
    headers = {
        "Authorization": get_authentication_token(request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": "",
        "X-ODS-Code": "",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    logger.info(
        "API response:",
        extra={"status_code": response.status_code, "response": response.json()},
    )
    assert response.status_code == 200
