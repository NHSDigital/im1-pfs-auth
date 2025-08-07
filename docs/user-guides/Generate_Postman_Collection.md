# Generate Postman Collection

## Table of Contents

- [Deploy to apigee](#deploy-to-apigee)
  - [Table of Contents](#table-of-contents)
  - [How to deploy to apigee](#how-to-deploy-to-apigee)

## How to generate Postman Collection

1. Install all dependencies by running:

   ```shell
   make install
   ```

2. Generate the Postman collection by running:

   ```shell
   make postman-generate-collection
   ```

   The Postman collection will be generated in the `postman/postman_collection.json` file.
