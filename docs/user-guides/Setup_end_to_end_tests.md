# Guide: Setup end to end tests

- [Guide: Setup end to end tests](#guide-setup-end-to-end-tests)
  - [Overview](#overview)
  - [Associating ephemeral deployments with IM1 PFS Auth Developer Test App](#associating-ephemeral-deployments-with-im1-pfs-auth-developer-test-app)
    - [Launching the ephemeral deployment](#launching-the-ephemeral-deployment)
    - [Associating the deployment with the developer app](#associating-the-deployment-with-the-developer-app)
  - [Testing](#testing)

## Overview

When performing end to end tests, a composite authentication token is retrieved from APIM's `mock-jwks` API. Composite tokens are currently, 2025-10-13, only enabled for the `internal-dev` environment. Therefore they cannot be ran against `internal-qa` in the CI/CD pipeline.

End to end tests can be ran from `internal-dev`, including ephemeral deployments created by PRs. For ephemeral deployments however, this requires associating the API Product with the IM1 PFS Auth Developer Test App, which has access to the correct instance of `mock-jwks`, as outlined below.

## Associating ephemeral deployments with IM1 PFS Auth Developer Test App

### Launching the ephemeral deployment

<!-- markdownlint-disable-next-line no-inline-html -->

A deployment is automatically span up upon the [creation of a PR](./Workflows.md#core-workflows) with the naming pattern `im1-pfs-auth-pr-<pr_number>`. The deployment can be verified by searching for `im1` in the APIGEE > Develop > API Proxies UI, the API proxy will be shown as `im1-pfs-auth--internal-dev--im1-pfs-auth-pr-<pr_number>`.

### Associating the deployment with the developer app

To allow the ephemeral deployment to access the `mock-jwks` service, it must be associated with the IM1 PFS Auth Developer Test App. To do so you must first be added to the `Proxy Dev Team` on the [NHS Internal Developer Hub](./NHS_developer_hub.md).

Once added to the `Proxy Dev Team`, the deployment can be associated to the developer app using [Apigee](https://apigee.com/edge) under the `nhsd-nonprod` organisation. To associate the deployment with the developer app:

- Navigate to `Publish` -> `Apps`
- Search for `IM1`
  - Note: searching can be a slow process due to indexing time)
- Select IM1 PFS Auth Developer Test App
- Select `Edit` in the top right of the page
- Under `Credentials` select `Add product`
- Search for `pr-<pr_number>`
- Add the `IM1 PFS Auth API - IM1 PFS Auth - P9 User Restriced Access (dev) (Internal Development)` product
  - Note: This is **not** the `(Internal Development Sandbox)` product
- Finalise the change by selecting `Save` in the top right of the page

## Testing

The deployment should now be associated with the app and end to end tests can be run as part of the [pull request checks GitHub workflow](../../.github/workflows/pull-request-checks.yml).

For the general overview of running end to end tests locally, see the relevant section of the README. The additional required inputs are:

- `PROXYGEN_URL_PATH`: `im1-pfs-auth-pr-<pr_number>`
- `APIGEE_PROXY_NAME` `im1-pfs-auth--internal-dev--im1-pfs-auth-pr-<pr_number>`

### `TEST_APP_PRIVATE_KEY`

The private key counterpart to the key pair registered on the internal NHS Developer Hub platform is required. This can be requested from the development team.
