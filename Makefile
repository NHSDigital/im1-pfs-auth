include scripts/init.mk

# ==============================================================================
# General Commands
# ==============================================================================

install:
	uv sync --all-groups
	npm install

lint:
	npm run lint
	uv run ruff check .

format:
	npm run format
	uv run ruff format .

# ==============================================================================
# Deploy API Commands
# ==============================================================================

# Deploy environment
deploy: prepare-deploy
# Mandatory arguments:
# ENVIRONMENT: The environment to deploy to (e.g., internal-dev, internal-qa, int)
# PROXYGEN_URL_PATH: The URL path for the API (e.g., im1-pfs-auth)
# CONTAINER_TAG: The version of the API to deploy (e.g., latest, v1.0.0, commit hash)
	@echo "Deploying API to the NHS API Platform..."
	proxygen instance deploy "$(ENVIRONMENT)" "$(PROXYGEN_URL_PATH)" specification/im1-pfs-auth-api.yaml $(PROXYGEN_ARGS)

prepare-deploy:
# Mandatory arguments:
# ENVIRONMENT: The environment to deploy to (e.g., internal-dev, internal-qa, int)
# PROXYGEN_URL_PATH: The URL path for the API (e.g., im1-pfs-auth)
# CONTAINER_TAG: The version of the API to deploy (e.g., latest, v1.0.0, commit hash)
	if [ -z "$(ENVIRONMENT)" ]; then \
		echo "No ENVIRONMENT provided. Use 'make deploy ENVIRONMENT=\"<env>\"' to specify environment."; \
		echo "Available environments include: internal-dev, internal-dev-sandbox, internal-qa, internal-qa-sandbox, sandbox, int"; \
		exit 1; \
	fi
	if [ -z "$(PROXYGEN_URL_PATH)" ]; then \
		echo "No PROXYGEN_URL_PATH provided. Use 'make deploy PROXYGEN_URL_PATH=\"<path>\"' to specify URL path."; \
		echo "Example: PROXYGEN_URL_PATH=\"im1-pfs-auth\""; \
		exit 1; \
	fi
	if [ -z "$(CONTAINER_TAG)" ]; then \
		echo "No CONTAINER_TAG provided. Use 'make deploy CONTAINER_TAG=\"<version>\"' to specify version."; \
		exit 1; \
	fi
	make select-spec-configuration

# Deploy environment from CI
deploy-ci:
	make deploy PROXYGEN_ARGS="--no-confirm"

# Deploy spec to uat
deploy-spec-uat:
	proxygen spec publish --uat $(PROXYGEN_ARGS) specification/im1-pfs-auth-api.yaml

# Deploy spec to prod
deploy-spec-prod:
	proxygen spec publish $(PROXYGEN_ARGS) specification/im1-pfs-auth-api.yaml

# Deploy spec to uat in CI
deploy-spec-uat-ci:
	make deploy-spec-uat PROXYGEN_ARGS="--no-confirm"

# Deploy spec to prod in CI
deploy-spec-prod-ci:
	make deploy-spec-prod PROXYGEN_ARGS="--no-confirm"

# ==============================================================================
# Spec Commands
# ==============================================================================

# Select the appropriate specification configuration based on the environment/version
select-spec-configuration:
ifeq ($(ENVIRONMENT), $(filter $(ENVIRONMENT), internal-dev internal-dev-sandbox internal-qa internal-qa-sandbox sandbox int ))
	@ $(MAKE) select-x-nhsd-apim-configuration
	@ $(MAKE) set-hosted-container-version
else
	@ echo ERROR: $$ENVIRONMENT is not a valid environment. Please use one of [internal-dev, internal-dev-sandbox, internal-qa, internal-qa-sandbox, sandbox, int]
	@ exit 1;
endif

# Select the NHS API Platform configuration for the specified environment
select-x-nhsd-apim-configuration:
	cp -f specification/x-nhsd-apim/x-nhsd-apim-$$ENVIRONMENT.yaml specification/x-nhsd-apim/x-nhsd-apim.generated.yaml

# Set the container version in the generated specification file
set-hosted-container-version:
	@if [ "$$(uname)" = "Darwin" ]; then
		sed -i '' 's|CONTAINER_TAG_TO_BE_REPLACED|$(CONTAINER_TAG)|g' specification/x-nhsd-apim/x-nhsd-apim.generated.yaml;
	else
		sed -i 's|CONTAINER_TAG_TO_BE_REPLACED|$(CONTAINER_TAG)|g' specification/x-nhsd-apim/x-nhsd-apim.generated.yaml;
	fi

# ==============================================================================
# Postman Commands
# ==============================================================================

# Generate Postman collection from OpenAPI specification
postman-generate-collection:
	yq 'del(.x-nhsd-apim)' specification/im1-pfs-auth-api.yaml > specification/im1-pfs-auth-api.portman.generated.yaml
	npx portman --cliOptionsFile scripts/config/portman/portman-cli.json

# Run Postman tests using Newman
postman-test:
	npx newman run postman/postman_collection.json $(NEWMAN_ARGS)

# Run Postman Tests
postman-test-pr-environment:
# Mandatory arguments:
# SANDBOX_BASE_URL: The base URL for the sandbox environment (e.g., https://sandbox.api.service.nhs.uk/im1-pfs-auth/)
	@make postman-test NEWMAN_ARGS="--env-var baseUrl=$(SANDBOX_BASE_URL)"

# ==============================================================================
# App Commands
# ==============================================================================

app-build:
	cp pyproject.toml app/
	cp uv.lock app/
	docker buildx build -t "$(PROXYGEN_DOCKER_REGISTRY_URL):$(CONTAINER_TAG)" --build-arg USE_MOCK=$(USE_MOCK) --load app/

app-push:
	proxygen docker get-login | bash
	docker push $(PROXYGEN_DOCKER_REGISTRY_URL):$(CONTAINER_TAG)

app-debug-run:
	FLASK_APP=app.api.app flask run --port 8000

app-docker-run:
	docker run -p 9000:9000 "im1-pfs-auth-app"

app-unit-test:
	uv run pytest app --cov=app --cov-fail-under=80

# ==============================================================================
# Sandbox Commands
# ==============================================================================

sandbox-build:
	cp pyproject.toml sandbox/
	cp uv.lock sandbox/
	docker build -t "$(PROXYGEN_DOCKER_REGISTRY_URL):$(CONTAINER_TAG)" --load sandbox/

sandbox-push:
	proxygen docker get-login | bash
	docker push $(PROXYGEN_DOCKER_REGISTRY_URL):$(CONTAINER_TAG)

sandbox-debug-run:
	FLASK_APP=sandbox.api.app flask run --port 8000

sandbox-docker-run:
	docker run -p 9000:9000 "im1-pfs-auth"

sandbox-unit-test:
	uv run pytest sandbox --cov=sandbox --cov-fail-under=80

# ==============================================================================
# Test Commands
# ==============================================================================

# Runs End to End tests against a deployed environment
e2e-tests end-to-end-tests:
# Mandatory arguments:
# TEST_APP_KEYCLOAK_CLIENT_ID: Client Id issued to the mocked authorisation provider client. Obtained by the GET Keycloak credentials endpoint.
# TEST_APP_KEYCLOAK_SECRET: Secret assigned to the mocked authorisation provider client. Obtained by the GET Keycloak credentials endpoint.
# TEST_APP_API_KEY: API Key for test application in the developer portal (https://dos-internal.ptl.api.platform.nhs.uk/MyApplications)
# TEST_APP_PRIVATE_KEY: Private Key from key pair for test application in the developer portal (https://dos-internal.ptl.api.platform.nhs.uk/MyApplications)
# APIGEE_ACCESS_TOKEN: "proxygen pytest-nhsd-apim --api=im1-pfs-auth get-token | jq -r .pytest_nhsd_apim_token"
# APIGEE_PROXY_NAME: The name of the proxy to test (e.g., im1-pfs-auth--internal-dev--im1-pfs-auth-pr-31)
# PROXYGEN_URL_PATH: The URL path for the Proxygen API (e.g. im1-pfs-auth-pr-31)
	uv run pytest tests/end_to_end \
		--api-name=im1-pfs-auth --proxy-name=${APIGEE_PROXY_NAME} \
		--disable-warnings -o log_cli_level=INFO \
		${PYTEST_ARGS}

# ==============================================================================

${VERBOSE}.SILENT: \
	build \
	clean \
	config \
	dependencies \
	deploy \
	deploy-ci \
	prepare-deploy \
