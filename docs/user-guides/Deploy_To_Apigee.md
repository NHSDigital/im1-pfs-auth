# Deploy to apigee

## Table of Contents

- [Deploy to apigee](#deploy-to-apigee)
  - [Table of Contents](#table-of-contents)
  - [How to deploy to apigee](#how-to-deploy-to-apigee)

## How to deploy to apigee

1. Ensure you have the [proxygen CLI](#proxygen-cli) installed and configured. If you haven't done this yet, follow the instructions in our [Proxygen CLI developer guide](./Proxygen_CLI.md#installation-and-configuration).

2. Build the container image necessary for the deployment

   Build application container image:

   ```shell
   make app-build PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" CONTAINER_TAG=<tag> EMIS_BASE_URL=<url> TPP_BASE_URL=<url>
   ```

   Build sandbox container image:

   ```shell
   make sandbox-build PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" CONTAINER_TAG=<tag>
   ```

   Each command builds a Docker image tagged with the specified `CONTAINER_TAG` and pushes it to the specified `PROXYGEN_DOCKER_REGISTRY_URL`. The `<tag>` is a placeholder; you can replace it with any meaningful tag for your deployment. Generally, this follows the pattern `<app/sandbox>-<commit-sha>` (e.g., `app-abc123` or `sandbox-def456`).

   > **Note**: The `CONTAINER_TAG` value you use here must match exactly when you run `make deploy` in step 3, as that's how Apigee knows which container image to deploy.

3. Deploy the API to apigee using the proxygen CLI:

   > [!TIP]
   > Deploying in CI? Use the `make deploy-ci` target instead. This will skip the interactive prompts.

   ```shell
   make deploy ENVIRONMENT="<environment>" PROXYGEN_URL_PATH="<api-name>" CONTAINER_TAG="<container-tag>"
   ```

   Arguments:
   - `ENVIRONMENT`: The environment to deploy to (e.g., `internal-dev`, `sandbox`, `prod`). If your environment is not supported the command will fail as part of the validation.
   - `PROXYGEN_URL_PATH`: The URL path for the API (e.g., `/im1-pfs-auth`, `/im1-pfs-auth-pr-1`).
   - `CONTAINER_TAG`: The tag for the container image (e.g., `latest`, `v1.0.0`).

   > [!NOTE]
   > If you're deploying to prod, you will need machine access credentials for proxygen. See the [Proxygen CLI Secrets](./Proxygen_CLI.md#secrets) section for more information on how to set up these credentials.
