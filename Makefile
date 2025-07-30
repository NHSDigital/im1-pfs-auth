include scripts/init.mk

# ==============================================================================
# Deploy API Commands
# ==============================================================================

# Deploy environment
deploy:
# Mandatory arguments:
# ENVIRONMENT: The environment to deploy to (e.g., internal-dev, internal-qa, int)
# PROXYGEN_URL_PATH: The URL path for the API (e.g., im1-pfs-auth)
# CONTAINER_TAG: The version of the API to deploy (e.g., latest, v1.0.0, commit hash)
	@echo "Deploying API to the NHS API Platform..."
	if [ -z "$(ENVIRONMENT)" ]; then \
		echo "No ENVIRONMENT provided. Use 'make deploy ENVIRONMENT=\"<env>\"' to specify environment."; \
		echo "Available environments include: internal-dev, internal-qa, int"; \
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
	proxygen instance deploy "$(ENVIRONMENT)" "$(PROXYGEN_URL_PATH)" specification/im1-pfs-auth-api.yaml $(PROXYGEN_ARGS)

# Deploy environment from CI
deploy-ci:
	make deploy PROXYGEN_ARGS="--no-confirm"

# ==============================================================================
# Spec Commands
# ==============================================================================

# Select the appropriate specification configuration based on the environment/version
select-spec-configuration:
ifeq ($(ENVIRONMENT), $(filter $(ENVIRONMENT), internal-dev internal-dev-sandbox ))
	@ $(MAKE) select-x-nhsd-apim-configuration
	@ $(MAKE) set-hosted-container-version
else
	@ echo ERROR: $$ENVIRONMENT is not a valid environment. Please use one of [sandbox, internal-dev, int, ref, prod]
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
# Sandbox Commands
# ==============================================================================

install:
	uv sync --all-extras
	npm install

lint:
	npm run lint
	uv run ruff check .

format:
	npm run format
	uv run ruff format .

sandbox-build:
	cp pyproject.toml sandbox/
	cp uv.lock sandbox/
	docker build -t "im1-pfs-auth-sandbox" --no-cache sandbox/

sandbox-debug-run:
	FLASK_APP=sandbox.api.app flask run --port 8000

sandbox-docker-run:
	docker run -p 9000:9000 "im1-pfs-auth-sandbox"

sandbox-test:
	uv run pytest --cov=sandbox --cov-fail-under=80

spec-compile: clean
	mkdir -p build
	npm run spec-compile

${VERBOSE}.SILENT: \
	build \
	clean \
	config \
	dependencies \
	deploy \
	deploy-ci \
