# Setting up Proxygen

## Generating a key pair

You'll need to generate a public and private key pair before raising a service now request to create the proxygen API

From the [APIM slack message](https://nhsuk.slack.com/archives/C016JRWN6AY/p1773828313442569):
```
Follow the new Key ID (KID) structure:

YYYY-mm-dd-PTL-<<api-name>>
YYYY-mm-dd-Prod-<<api-name>>
This enforces a 12-month expiry for all public keys (The date should be expiry date of the Public Key)
```

[These docs](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication#step-2-generate-a-key-pair) walkthrough how to generate the key pair. Once you've created your JWKS file called YOUR_KID.json you can move onto creating the proxygen deployment

## Creating the proxygen deployment

Once you have this key pair, you can raise a [service now request](https://nhsdigitallive.service-now.com/csm?id=sc_cat_item&sys_id=b5e2c7ee9777a610dd80f2df9153af87&sysparm_category=63f4716697731e90dd80f2df9153affe) with the information you used to create the key pair to "Create an API on Proxygen".

Once APIM have done this, they will provide you with a client ID in the service now request, e.g. im1-pfs-auth-client which you will need to setup machine access to the API.

## Setting up machine access

### Downloading proxygen-cli

proxygen-cli can be installed using pip

```
pip install proxygen-cli
```

To verify the installation

```
proxygen --version
```

This may not work initially - if it can't find proxygen then we need to find the install location and add it to our PATH

```
find ~ -name "proxygen" 2>/dev/null
```

You're looking for one that looks like `/Users/elliot/Library/Python/3.13/bin/proxygen`

Once you have this path, you can add it to your .zshrc with `export PATH="$PATH:/Users/elliot/Library/Python/3.13/bin/"`

Remember to `source ~/.zshrc`

Rerun the above `proxygen --version` command to verify it's working

### .proxygen config files

To fully setup machine access, you will need a credentials.yaml and settings.yaml file inside of ~/.proxygen

credentials.yaml
```
base_url: https://identity.{ptl | prod}.api.platform.nhs.uk/realms/api-producers
client_id: {Client ID}
key_id: {Key ID}
private_key_path: {Absolute path to private key}
```

settings.yaml
```
api: {API name}
endpoint_url: https://proxygen.{ptl | prod}.api.platform.nhs.uk
spec_output_format: yaml
```

## Pushing up a spec from your local machine

To verify you've set everything up correctly locally, you can run
```
proxygen instance deploy {Environment name e.g. internal-dev} {API Name} {path to spec}
```

To retrieve the spec you just published, you can run
```
proxygen instance get {Environment name e.g. internal-dev} {API Name}
```

## Deploying the spec via a pipeline
