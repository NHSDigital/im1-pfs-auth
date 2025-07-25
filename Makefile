#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

lint:
	npm run lint

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
