# Glossary

A reference guide for key terms, tools, and concepts used in the IM1 PFS Auth project.

---

## APIM (API Management Platform)

The **NHS API Management Platform**, built and operated by NHS England. It provides the infrastructure for publishing, securing, monitoring, and managing APIs across the NHS. APIM is built on top of **Apigee** and is the platform that `im1-pfs-auth` is deployed to. It is accessible via `*.api.service.nhs.uk` URLs (e.g. `https://int.api.service.nhs.uk/im1-pfs-auth`).

---

## Apigee

**Apigee** is Google's API gateway and management product, which underpins the NHS APIM platform. It handles:

- Routing inbound API requests to backend containers
- Authentication and authorisation enforcement (e.g. composite token validation)
- Analytics and monitoring

In this project, Apigee proxies are deployed via the **Proxygen CLI** using the OpenAPI specification in the `specification/` directory. The Apigee UI is accessible at [https://apigee.com/edge](https://apigee.com/edge) under the `nhsd-nonprod` (non-production) and `nhsd-prod` (production) organisations.

---

## Proxygen (Service)

**Proxygen** (short for Proxy Generator) is an NHS England-built service that sits in front of Apigee and acts as the control plane for API producers. It abstracts the complexity of directly interacting with Apigee by accepting an OpenAPI specification and handling the creation and management of Apigee API proxies on your behalf.

The Proxygen service is accessible at:

```text
https://proxygen.prod.api.platform.nhs.uk
```

It is also responsible for managing the **AWS ECR container registry** that holds the Docker images that back deployed API proxies.

---

## Proxygen CLI

The **Proxygen CLI** (`proxygen-cli`) is a Python command-line tool provided by NHS England that allows API producer teams to interact with the Proxygen service. In this project it is used to:

- **Deploy API proxy instances** to APIM environments (e.g. `internal-dev`, `int`, `prod`) via `proxygen instance deploy`
- **Publish the OpenAPI spec** to the NHS developer portal via `proxygen spec publish`
- **Obtain Docker credentials** for pushing container images to the NHS ECR registry via `proxygen docker get-login`
- **Obtain test tokens** for running end-to-end tests via `proxygen pytest-nhsd-apim get-token`

The CLI authenticates against the NHS identity service at:

```text
https://identity.prod.api.platform.nhs.uk/realms/api-producers
```

This is a **Keycloak** identity provider used for machine-to-machine authentication for API producer teams. Authentication requires three credentials: a `client_id`, a `key_id`, and a `private_key` (PEM file). In CI/CD these are stored as GitHub secrets (`PROXYGEN_CLIENT_ID`, `PROXYGEN_KEY_ID`, `PROXYGEN_PRIVATE_KEY`) and also in the VRS AWS Prod Secrets Manager under the prefix `im1-pfs-auth/proxygen/<secret>`.

See the [Proxygen CLI guide](./Proxygen_CLI.md) for installation and configuration instructions.

---

## IM1

**IM1** (Interface Mechanism 1) is a GP system integration standard used in the NHS. It defines how third-party applications (such as patient-facing services) can integrate with GP clinical systems (supplied by GPIT suppliers such as EMIS and TPP/SystmOne). IM1 allows authorised applications to act on behalf of patients, interacting with their GP practice's system.

---

## IM1 PFS Auth (`im1-pfs-auth`)

**IM1 Patient Facing Service Auth** is this project. It is an intermediary API service that enables patient-facing applications to authenticate and establish sessions with GP practice systems via the IM1 interface. It sits between a patient-facing application and a GPIT supplier system (e.g. EMIS, TPP), handling:

- Validation of NHS login proxy tokens
- Session initiation with the appropriate supplier system based on ODS code
- Transformation of supplier responses

It is deployed as an Apigee API proxy backed by a Docker container, and is accessible at `*.api.service.nhs.uk/im1-pfs-auth`.

---

## IM1 PFS Auth Developer Test App

The **IM1 PFS Auth Developer Test App** is a registered application in the Apigee developer portal (under the `nhsd-nonprod` organisation) used specifically for running end-to-end tests. It has access to the `mock-jwks` service, which is required for generating composite authentication tokens in the `internal-dev` environment.

When a new ephemeral deployment is created (e.g. from a pull request), it must be manually associated with this test app in the Apigee UI before end-to-end tests can be run against it. See the [Setup end to end tests guide](./Setup_end_to_end_tests.md) for instructions.

---

## Composite Token / mock-jwks

A **composite token** is a development-environment authentication token used in APIM's `internal-dev` environment to simulate authenticated requests without requiring real NHS login credentials. It is obtained from APIM's `mock-jwks` service.

The `mock-jwks` service is only enabled in the `internal-dev` environment. The **IM1 PFS Auth Developer Test App** must be associated with a deployment before composite tokens can be used against it.

---

## GPIT Supplier

A **GPIT supplier** is a provider of GP IT systems in the NHS — primarily **EMIS Health** and **TPP (The Phoenix Partnership)**, who make SystmOne. These are the systems that `im1-pfs-auth` communicates with when establishing patient sessions. Their base URLs are configured at build time via the `EMIS_BASE_URL` and `TPP_BASE_URL` environment variables.

---

## ODS Code

An **ODS (Organisation Data Service) code** is a unique identifier assigned to NHS organisations, including GP practices. `im1-pfs-auth` uses the ODS code of a patient's GP practice to determine which GPIT supplier system to route a session request to.

---

## ECR (Elastic Container Registry)

**AWS ECR** is the container image registry used to store the Docker images for `im1-pfs-auth`. The NHS-managed registry is at:

```text
958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth
```

Docker credentials to push to this registry are obtained via `proxygen docker get-login`. Apigee pulls the container from this registry when serving API requests.

---

## NHS Developer Hub / Developer Portal

The **NHS Internal Developer Hub** (accessible at `https://dos-internal.ptl.api.platform.nhs.uk`) is the portal where API producer teams manage their applications, API keys, and key pairs used for testing. It is also where the **IM1 PFS Auth Developer Test App** API key (`TEST_APP_API_KEY`) and private key (`TEST_APP_PRIVATE_KEY`) are registered and managed.

Access to the developer hub for end-to-end testing requires membership of the `Proxy Dev Team`. See the [NHS Developer Hub guide](./NHS_developer_hub.md) for more detail.

---

## Keycloak

**Keycloak** is an open-source identity and access management solution. NHS England uses a Keycloak instance at `https://identity.prod.api.platform.nhs.uk/realms/api-producers` as the identity provider for authenticating API producer machine users (i.e. the Proxygen CLI). It is also used in the test setup — `TEST_APP_KEYCLOAK_CLIENT_ID` and `TEST_APP_KEYCLOAK_CLIENT_SECRET` are credentials for a mocked authorisation provider client used in end-to-end tests.

---

## Sandbox

The **sandbox** is a simulated version of the `im1-pfs-auth` API that returns mock responses without connecting to real GPIT supplier systems. It is deployed alongside the main app in certain environments (e.g. `internal-dev-sandbox`, `sandbox`) and does not require authentication. It allows developers and API consumers to explore the API without needing to onboard or hold real credentials.

---

## Ephemeral Deployment

An **ephemeral deployment** is a temporary deployment of `im1-pfs-auth` created automatically when a pull request is opened. It is deployed to the `internal-dev` environment with a URL path following the pattern `im1-pfs-auth-pr-<pr_number>`, resulting in an Apigee proxy named `im1-pfs-auth--internal-dev--im1-pfs-auth-pr-<pr_number>`. These deployments are used to run end-to-end tests against code changes before they are merged to `main`.
