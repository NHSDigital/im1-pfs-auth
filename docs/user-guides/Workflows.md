# GitHub Workflows

In this repository, we have defined several GitHub Actions workflows to automate our CI/CD processes.

The workflows use [reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) at `./.github/workflows/reusable-*.yml` and [composite actions](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action) at `./.github/actions/*/action.yml` to streamline the workflow definitions and promote reusability.

## Table of Contents

- [GitHub Workflows](#github-workflows)
  - [Table of Contents](#table-of-contents)
  - [Core Workflows](#core-workflows)
  - [Additional Workflows](#additional-workflows)
  - [Reusable Workflows](#reusable-workflows)

## Core Workflows

Core workflows you need to understand are the following:

> [!NOTE]
> Some workflows are broken down into separate stages to improve readability and maintainability. However, these stages are not intended to be reused.

- [**cicd.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/cicd.yml): The main CI/CD workflow that orchestrates the build, test, and deployment processes.
  - Triggers:
    - Push to main
  - Steps:
    - Run Core Code Checks
    - Run Additional Code Checks
    - Deploy to internal-qa
    - Run tests on internal-qa
    - Deploy to internal-qa-sandbox
    - Run postman tests on internal-qa-sandbox
    - Deploy to int and sandbox
    - Deploy spec to Bloomreach UAT
- [**pull-request-checks.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/pull-request-checks.yml): A workflow that runs on pull requests to ensure code quality and prevent broken changes from being merged.
  - Triggers:
    - Pull request to main
  - Steps:
    - Run Core Code Checks
    - Run Additional Code Checks
    - Deploy to internal-dev (temporary environment)
    - Run tests on internal-dev
    - Deploy to internal-dev-sandbox (temporary environment)
    - Run postman tests on internal-dev-sandbox

## Additional Workflows

Additional workflows that may be useful include:

- [**codeql-analysis.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/codeql-analysis.yml): A workflow that runs CodeQL analysis to identify security vulnerabilities and code quality issues.
  - Triggers:
    - Push to main
    - Pull request to main

## Reusable Workflows

- [**reusable-deploy.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/reusable-deploy.yml): A reusable workflow for deploying applications to various environments.
- [**reusable-core-code-checks.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/reusable-core-code-checks.yml): A reusable workflow for running core code checks. These checks should ensure the code is safe to deploy to development environments.
- [**reusable-additional-code-checks.yml**](https://github.com/NHSDigital/im1-pfs-auth/blob/main/.github/workflows/reusable-additional-code-checks.yml): A reusable workflow for running additional code checks. These checks should ensure the code meets all quality standards.
