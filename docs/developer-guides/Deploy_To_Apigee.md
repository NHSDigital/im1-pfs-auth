# Deploy to Apigee

## Table of Contents

- [Deploy to Apigee](#deploy-to-apigee)
  - [Table of Contents](#table-of-contents)
  - [How to deploy to Apigee](#how-to-deploy-to-apigee)

## How to deploy to Apigee

1. Ensure you have the [proxygen CLI](#proxygen-cli) installed and configured. If you haven't done this yet, follow the instructions in our [Proxygen CLI developer guide](./Proxygen_CLI.md#installation-and-configuration).

2. Build the container image necessary for the deployment
   TODO: Add instructions for building the container image.

3. Deploy the API to Apigee using the proxygen CLI:

   ```shell
   make deploy ENVIRONMENT="<environment>" PROXYGEN_URL_PATH="<api-name>" CONTAINER_TAG="<container-tag>"
   ```

    Arguments:
   - `ENVIRONMENT`: The environment to deploy to (e.g., `internal-dev`, `sandbox`, `prod`). If your environment is not supported the command will fail as part of the validation.
   - `PROXYGEN_URL_PATH`: The URL path for the API (e.g., `/im1-pfs-auth`, `/im1-pfs-auth-pr-1`).
   - `CONTAINER_TAG`: The tag for the container image (e.g., `latest`, `v1.0.0`).

    > [!NOTE]
    > If you're deploying to prod, you will need machine access credentials for proxygen. See the [Proxygen CLI Secrets](./Proxygen_CLI.md#secrets) section for more information on how to set up these credentials.

    > [!TIP]
    > Deploying in CI? Use the `make deploy-ci` target instead. This will skip the interactive prompts.
