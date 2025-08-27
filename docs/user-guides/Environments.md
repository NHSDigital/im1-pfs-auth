# Environments

## Table of Contents

- [Environments](#environments)
  - [Table of Contents](#table-of-contents)
  - [APIM Environments](#apim-environments)
    - [Bloomreach Environments](#bloomreach-environments)
  - [Deployment Flow](#deployment-flow)

## APIM Environments

Environments can be broken down into one of two types:

| Name    | Description                                                                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| sandbox | Sandbox environments are publicly accessible environments that host a limited/mocked version of our application                                   |
| app     | Environments that are not of type sandbox. These environment require authentication and contain application code within their deployed container. |

| Name                 | Type    | Purpose                                                                                                               | Number of environments                 | Access                                                      | URL                                                                                                                                |
| -------------------- | ------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| internal-dev         | app     | Development and testing app environment. Only used to test Pull Requests. Used before a feature is ready for main     | 1+ (depending on number of active PRs) | Public, authentication requires development composite token | [https://internal-dev.api.service.nhs.uk/<url_path_part>](https://internal-dev.api.service.nhs.uk/<url_path_part>)                 |
| internal-dev-sandbox | sandbox | Development and testing sandbox environment. Only used to test Pull Requests. Used before a feature is ready for main | 1+ (depending on number of active PRs) | Public, no authentication                                   | [https://internal-dev-sandbox.api.service.nhs.uk/<url_path_part>](https://internal-dev-sandbox.api.service.nhs.uk/<url_path_part>) |
| internal-qa          | app     | Integration environment for development team, where main is deployed on each commit to.                               | 1                                      | Public, authentication requires development composite token |                                                                                                                                    |
| internal-qa-sandbox  | sandbox | Integration environment for development team, where main is deployed on each commit to.                               | 1                                      | Public, no authentication                                   |                                                                                                                                    |
| int                  | app     |                                                                                                                       | 1                                      | Public, authentication requires development composite token |                                                                                                                                    |
| sandbox              | sandbox |                                                                                                                       | 1                                      | Public, no authentication                                   |                                                                                                                                    |
| prod                 |     app    |                                                                                                                    | 1                                      | Public, authentication requires production composite token  |                                                                                                                                    |

> [!NOTE]
> More APIM environments exist

### Bloomreach Environments

Bloomreach environments are when the specification is hosted. This allows consumers our APIs to review the documentation for the API and how to begin onboarding to our API.

| Name | Purpose         | Access                                                       |
| ---- | --------------- | ------------------------------------------------------------ |
| uat  | internal review | Access through NHS network via VDI or HSCN VPN or NHS office |
| prod | production      | Public page on API Catalogue                                 |

## Deployment Flow
