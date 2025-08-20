import pytest
from pytest_nhsd_apim.identity_service import (
    KeycloakUserAuthenticator,
    KeycloakUserConfig,
    TokenExchangeAuthenticator,
    TokenExchangeConfig,
)


def get_authentication_token(request: pytest.FixtureRequest) -> str:
    """Get the authentication token for the IM1 PFS Auth API.

    Args:
        request (pytest.FixtureRequest): The pytest request fixture.

    Returns:
        str: The authentication token.
    """
    _test_app_credentials = request.getfixturevalue("_test_app_credentials")
    apigee_environment = request.getfixturevalue("apigee_environment")
    _jwt_keys = request.getfixturevalue("_jwt_keys")
    _keycloak_client_credentials = request.getfixturevalue(
        "_keycloak_client_credentials"
    )

    config1 = KeycloakUserConfig(
        realm=f"NHS-Login-mock-{apigee_environment}",
        client_id=_keycloak_client_credentials["nhs-login"]["client_id"],
        client_secret=_keycloak_client_credentials["nhs-login"]["client_secret"],
        login_form={"username": "9912003071"},
    )

    authenticator = KeycloakUserAuthenticator(config=config1)

    id_token = authenticator.get_token()["id_token"]

    config = TokenExchangeConfig(
        environment=apigee_environment,
        identity_service_base_url=f"https://{apigee_environment}.api.service.nhs.uk/oauth2-mock",
        client_id=_test_app_credentials["consumerKey"],
        jwt_private_key=_jwt_keys["private_key_pem"],
        jwt_kid="test-1",
        id_token=id_token,
    )

    authenticator = TokenExchangeAuthenticator(config=config)

    return f"Bearer {authenticator.get_token()['access_token']}"
