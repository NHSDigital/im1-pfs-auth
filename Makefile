#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

install:
	uv sync --all-extras
	npm install

lint:
	npm run lint
	uv run ruff check sandbox/

format:
	npm run format
	uv run ruff format sandbox/
# Locally runs sandbox application
run:
	FLASK_APP=sandbox.app flask run --port 8000

test:
	pytest


#Creates the fully expanded OAS spec in json
publish: clean
	mkdir -p build
	npm run publish


${VERBOSE}.SILENT: \
	build \
	clean \
	config \
	dependencies \
	deploy \
