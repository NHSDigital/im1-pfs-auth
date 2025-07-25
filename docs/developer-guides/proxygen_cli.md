# Proxygen CLI

The Proxygen CLI is a dedicated command-line interface tool designed to streamline the interaction between producers and the Proxy Generator service. It provides producers with a convenient and intuitive way to deploy API instances, manage API specifications, manage secrets, and deploy them within specific environments without needing to directly interact with the API platform.

## Table of Contents
- [Proxygen CLI](#proxygen-cli)
  - [Table of Contents](#table-of-contents)
  - [Installation and Configuration](#installation-and-configuration)

[APIM Documentation](https://nhsd-confluence.digital.nhs.uk/spaces/APM/pages/804495095/Proxygen+CLI+user+guide#ProxygenCLIuserguide-Settingupsettingsandcredentials)


## Installation and Configuration

1. Using `uv` run the following command to install the Proxygen CLI:

```shell
uv pip install proxygen-cli
```

2. Configure the CLI by running:

```shell
proxygen settings set api im1-pfs-auth
```

3. Auth: TODO
A backup of the API's RSA private key is stored in VRS Prod AWS Secrets Manager under the name `TODO`.
