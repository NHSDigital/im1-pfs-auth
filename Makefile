#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

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

test:
	pytest


spec-compile: clean
	mkdir -p build
	npm run spec-compile


${VERBOSE}.SILENT: \
	build \
	clean \
	config \
	dependencies \
	deploy \
