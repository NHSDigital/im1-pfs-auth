#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist


lint:
	npm run lint
	ruff format sandbox/

install:
	uv pip compile pyproject.toml --extra dev
	npm install

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
