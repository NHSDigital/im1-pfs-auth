from os import getenv

import pytest


@pytest.fixture
def api_url(request: pytest.FixtureRequest) -> str:
    """Constructs the full API URL using the Apigee environment and proxy path.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object used to
            retrieve other fixtures.

    Returns:
        str: The constructed API URL.

    Raises:
        ValueError: If the PROXYGEN_URL_PATH environment variable is not set.
    """
    apigee_environment = request.getfixturevalue("apigee_environment")
    proxy_path_url = getenv("PROXYGEN_URL_PATH")
    if not proxy_path_url:
        msg = "PROXYGEN_URL_PATH environment variable is not set."
        raise ValueError(msg)
    return (
        f"https://{apigee_environment}.api.service.nhs.uk/{proxy_path_url}/authenticate"
    )
