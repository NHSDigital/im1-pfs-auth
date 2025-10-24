# Guide: NHS developer hub

## Overview

The NHS developer hub is the platform for managing applications which interact with NHS APIs. The primary use case for IM1 is for the management of API keys and credentials used in accessing the mock credentials service used in testing.

## Registration

There are two instances of NHS developer hub, [production](https://onboarding.prod.api.platform.nhs.uk) and [internal](https://dos-internal.ptl.api.platform.nhs.uk). Developers are encouraged to register for both platforms however, for the purposes of IM1 development, the internal instance is of higher priority.

## Proxy Dev Team

Once registered with the developer hub, developers must be added to the `Proxy Dev Team`. This must be done by the one of the `Proxy Dev Team` owners.

## IM1 PFS Auth Developer Test App

The `Proxy Dev Team` maintains the IM1 PFS Auth Developer Test App on the internal NHS developer hub. This application is responsible for the management of API keys and public signing key.

### API keys

From the application page, the API key can be accessed via `Security details` -> `Active API keys` -> `Edit`. Here keys can be rotated, created, and revoked. This key is used as `TEST_APP_API_KEY` in our environment variables.

### Public key

The public signing key can be changed via `Security details` -> `Public key URL` -> `Edit`, where generation of the public key is documented under [Section 3](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/user-restricted-restful-apis-nhs-login-separate-authentication-and-authorisation#step-3-generate-a-key-pair) of [User-restricted RESTful APIs - NHS login separate authentication](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/user-restricted-restful-apis-nhs-login-separate-authentication-and-authorisation).
