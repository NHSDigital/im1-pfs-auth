# Proxygen CLI

The proxygen CLI is a dedicated command-line interface tool designed to streamline the interaction between producers and the Proxy Generator service. It provides producers with a convenient and intuitive way to deploy API instances, manage API specifications, manage secrets, and deploy them within specific environments without needing to directly interact with the API platform.

## Table of Contents

- [Proxygen CLI](#proxygen-cli)
  - [Table of Contents](#table-of-contents)
  - [Installation and Configuration](#installation-and-configuration)

[APIM Documentation](https://nhsd-confluence.digital.nhs.uk/spaces/APM/pages/804495095/Proxygen+CLI+user+guide#ProxygenCLIuserguide-Settingupsettingsandcredentials)

## Installation and Configuration

1. Using your favourite Python package manager, install the proxygen CLI:

    ```shell
    # UV
    uv pip install proxygen-cli
    # PIP
    pip install proxygen-cli
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

    Follow the instructions in the [APIM Documentation](https://nhsd-confluence.digital.nhs.uk/spaces/APM/pages/804495095/Proxygen+CLI+user+guide#ProxygenCLIuserguide-Configuringsettingsandcredentials) to set up your credentials and settings.

    > [!NOTE]
    > proxygen-cli doesn't use `-h` to display help. Instead, use `--help` to see available commands and options.

5. Verify the installation by running:

    ```shell
    proxygen pytest-nhsd-apim get-token
    ```
