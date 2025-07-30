include scripts/init.mk

# ==============================================================================
# Deploy API Commands
# ==============================================================================

# Deploy environment
deploy:
# Mandatory arguments:
# ENVIRONMENT: The environment to deploy to (e.g., internal-dev, internal-qa, int)
# PROXYGEN_URL_PATH: The URL path for the API (e.g., im1-pfs-auth)
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
else
	@ echo ERROR: $$ENVIRONMENT is not a valid environment. Please use one of [sandbox, internal-dev, int, ref, prod]
	@ exit 1;
endif

select-x-nhsd-apim-configuration:
	cp -f specification/x-nhsd-apim/x-nhsd-apim-$$ENVIRONMENT.yaml specification/x-nhsd-apim/x-nhsd-apim.generated.yaml
	@ $(MAKE) set-hosted-container-version

set-hosted-container-version:
	sed -i '' 's|TAG_TO_BE_REPLACED|$(VERSION)|g' specification/x-nhsd-apim/x-nhsd-apim.generated.yaml

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
