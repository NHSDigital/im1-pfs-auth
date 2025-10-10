from os import getenv
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from lxml import html
from pytest_nhsd_apim.identity_service import (
    KeycloakUserAuthenticator,
    KeycloakUserConfig,
    TokenExchangeAuthenticator,
    TokenExchangeConfig,
)


class KeycloakUserCompositeAuthenticator(KeycloakUserAuthenticator):
    """Derived class to allow for a different scope in Keycloak config.

    Inherits:
        KeycloakUserAuthenticator: pytest-nhsd-apim parent class.
    """

    def get_token(self) -> str:
        """Re-implementation to add 'openid delegated' scope.

        Returns:
            str: Token returned from Keycloak endpoint.
        """
        login_session = requests.session()
        # 1. Get me that auth page
        resp = login_session.get(
            f"{self.config.keycloak_url}/auth",
            params={
                "response_type": "code",
                "client_id": self.config.client_id,
                "scope": "openid delegated",
                "redirect_uri": self.config.redirect_uri,
            },
        )
        # 2. Parse it!
        tree = html.fromstring(resp.text)
        form = tree.get_element_by_id("kc-form-login")
        # 3. Complete the login form with the credentials in login_form.
        resp2 = login_session.post(form.action, data=self.config.login_form)
        location = urlparse(resp2.history[-1].headers["location"])
        params = parse_qs(location.query)
        # 4. Get me that sweet code from the redirect_uri so I can get my token
        code = params["code"]
        # 5. Get the token
        resp3 = login_session.post(
            f"{self.config.keycloak_url}/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "redirect_uri": self.config.redirect_uri,
            },
        )
        # 6. Return your deserved profit.
        return resp3.json()


def get_authentication_token(
    proxy_identifier: str, request: pytest.FixtureRequest
) -> str:
    """Get the authentication token for the IM1 PFS Auth API.

    Args:
        proxy_identifier (str): The NHS number for the proxy
        request (pytest.FixtureRequest): The pytest request fixture.

    Returns:
        str: The authentication token.
    """
    apigee_environment = request.getfixturevalue("apigee_environment")

    config1 = KeycloakUserConfig(
        realm=f"NHS-Login-mock-{apigee_environment}",
        client_id=getenv("TEST_APP_KEYCLOAK_CLIENT_ID"),
        client_secret=getenv("TEST_APP_KEYCLOAK_CLIENT_SECRET"),
        login_form={"username": proxy_identifier},
    )

    authenticator = KeycloakUserCompositeAuthenticator(config=config1)

    id_token = authenticator.get_token()["id_token"]

    config = TokenExchangeConfig(
        environment=apigee_environment,
        identity_service_base_url=f"https://{apigee_environment}.api.service.nhs.uk/oauth2-mock",
        client_id=getenv("TEST_APP_API_KEY"),
        jwt_private_key=getenv("TEST_APP_PRIVATE_KEY").replace("\\n", "\n"),
        jwt_kid="im1-pfs-auth-test",
        id_token=id_token,
    )

    authenticator = TokenExchangeAuthenticator(config=config)

    return f"Bearer {authenticator.get_token()['access_token']}"
