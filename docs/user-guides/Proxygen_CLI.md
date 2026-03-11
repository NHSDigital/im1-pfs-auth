# proxygen CLI

The proxygen CLI is a dedicated command-line interface tool designed to streamline the interaction between producers and the Proxy Generator service. It provides producers with a convenient and intuitive way to deploy API instances, manage API specifications, manage secrets, and deploy them within specific environments without needing to directly interact with the API platform.

## Table of Contents

- [proxygen CLI](#proxygen-cli)
  - [Table of Contents](#table-of-contents)
  - [Installation and Configuration](#installation-and-configuration)
  - [Secrets](#secrets)
    - [Secrets in GitHub](#secrets-in-github)

[APIM Documentation](https://nhsd-confluence.digital.nhs.uk/spaces/APM/pages/804495095/Proxygen+CLI+user+guide#ProxygenCLIuserguide-Settingupsettingsandcredentials)

## Installation and Configuration

1. Install proxygen-cli in a separate virtual environment:

   **Why a separate environment?** `proxygen-cli` (latest version: 3.0.2) requires `pydantic` v1 (`pydantic>=1.9.1,<2.0.0`), while this project uses `pydantic` v2 (`pydantic==2.9.2`). These versions are incompatible, so proxygen-cli must be installed in its own virtual environment.

   ```shell
   # Create a separate directory for proxygen
   mkdir -p ~/.proxygen-venv
   cd ~/.proxygen-venv

   # Create a virtual environment (will use Python 3.13 needed for the specified proxygen version)
   uv venv -p 3.13

   # Activate the virtual environment
   source .venv/bin/activate

   # Install proxygen-cli (latest version: 3.0.2)
   uv pip install proxygen-cli==3.0.2

   # Deactivate and return to your project
   deactivate
   cd -
   ```

   **Make proxygen available globally** by creating a wrapper script or adding to your PATH:

   ```shell
   # Option 1: Create a symlink (recommended)
   sudo ln -s ~/.proxygen-venv/.venv/bin/proxygen /usr/local/bin/proxygen

   # Option 2: Add to PATH in your shell profile (~/.bashrc, ~/.zshrc, etc.)
   export PATH="$HOME/.proxygen-venv/.venv/bin:$PATH"
   ```

2. Confirm the installation by checking the version:

   ```shell
   proxygen --version
   ```

   If there is an error with the command, ensure that `pydantic` and all proxygen's dependencies are installed correctly.

3. Configure the CLI by running:

   ```shell
   proxygen settings set api im1-pfs-auth
   ```

4. Set up proxygen credentials and settings

   Complete steps 2.2 from instructions in the [APIM Documentation](https://nhsd-confluence.digital.nhs.uk/spaces/APM/pages/804495095/Proxygen+CLI+user+guide#ProxygenCLIuserguide-Configuringsettingsandcredentials) to set up your credentials and settings.

   > [!NOTE]
   > proxygen-cli doesn't use `-h` to display help. Instead, use `--help` to see available commands and options.

5. Verify the installation by running:

   ```shell
   proxygen pytest-nhsd-apim get-token
   ```

## Secrets

Secrets used for machine access are stored in Validated Relationships Service's (VRS) AWS Prod Secrets Manager with the prefix `im1-pfs-auth/proxygen/<secret>`. As well the private key is available in GitHub Secrets under the name `PROXYGEN_PRIVATE_KEY`.
Secrets used for machine access are stored in Validated Relationships Service's (VRS) AWS Prod Secrets Manager with the prefix `im1-pfs-auth/proxygen/<secret>`.

### Secrets in GitHub

As well secrets are held in GitHub Secrets for the project. The secrets are used to authenticate the workflows to deploy the API to the NHS API Platform. The secrets are:
the private key is available in GitHub Secrets under the names `PROXYGEN_CLIENT_ID`, `PROXYGEN_KEY_ID`, and `PROXYGEN_PRIVATE_KEY`.
