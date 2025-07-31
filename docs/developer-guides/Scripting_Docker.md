# Developer Guide: Scripting Docker

- [Developer Guide: Scripting Docker](#developer-guide-scripting-docker)
  - [Overview](#overview)
  - [Features](#features)
  - [Key files](#key-files)
  - [Usage](#usage)
    - [Quick start](#quick-start)
    - [Your image implementation](#your-image-implementation)
  - [Conventions](#conventions)
    - [Versioning](#versioning)
    - [Variables](#variables)
    - [Platform architecture](#platform-architecture)
    - [`Dockerignore` file](#dockerignore-file)
  - [FAQ](#faq)

## Overview

This document provides instructions on how to build Docker images using our automated build process. You'll learn how to specify version tags, commit changes, and understand the build output.

Docker is a tool for developing, shipping and running applications inside containers for Serverless and Kubernetes-based workloads. It has grown in popularity due to its ability to address several challenges faced by engineers, like:

- **Consistency across environments**: One of the common challenges in software development is the "it works on my machine" problem. Docker containers ensure that applications run the same regardless of where the container is run, be it a developer's local machine, a test environment or a production server.
- **Isolation**: Docker containers are isolated from each other and from the host system. This means that you can run multiple versions of the same software (like databases or libraries) on the same machine without them interfering with each other.
- **Rapid development and deployment**: With Docker, setting up a new instance or environment is just a matter of spinning up a new container, which can be done in seconds. This is especially useful for scaling applications or rapidly deploying fixes.
- **Version control for environments**: Docker images can be versioned, allowing developers to keep track of application environments in the same way they version code. This makes it easy to roll back to a previous version if needed.
- **Resource efficiency**: Containers are lightweight compared to virtual machines (VMs) because they share the same OS kernel and do not require a full OS stack to run. This means you can run many more containers than VMs on a host machine.
- **Microservices architecture**: Docker is particularly well-suited for microservices architectures, where an application is split into smaller, independent services that run in their own containers. This allows for easier scaling, maintenance and updates of individual services.
- **Integration with development tools**: There is a rich ecosystem of tools and platforms that integrate with Docker, including CI/CD tools (like GitHub and Azure DevOps), orchestration platforms (like Kubernetes) and cloud providers (like AWS and Azure).
- **Developer productivity**: With Docker, developers can easily share their environment with teammates. If a new developer joins the team, they can get up and running quickly by simply pulling the necessary Docker images.
- **Easy maintenance and update**: With containers, it is easy to update a base image or a software component and then propagate those changes to all instances of the application.
- **Cross-platform compatibility**: Docker containers can be run on any platform that supports Docker, be it Linux, Windows or macOS. This ensures compatibility across different development and production environments.
- **Security**: Docker provides features like secure namespaces and cgroups which isolate applications. Additionally, you can define fine-grained access controls and policies for your containers.
- **Reusable components**: Docker images can be used as base images for other projects, allowing for reusable components. For example, if you have a base image with a configured web server, other teams or projects can use that image as a starting point.

## Features

Here are some key features built into this repository's Docker files:

✅ Alpine base	Minimal footprint
🧪 Removes test files, reduces size, cleans up
⚡ Uses uv	Fast, modern dependency management
📁 Isolated install	Uses [tool.poetry.group.{app}] dependencies only
🔒 Deletes pyproject	Avoids leaking source metadata
🔥 Gunicorn with uv run	clean and fast app start

## Key files

- Scripts
- Configuration
  - [`Sandbox Dockerfile`](../../sandbox/Dockerfile): Instructions for Docker to build a container image that contains everything required to run the Sandbox Application within the built container
  - [`App Dockerfile`](../../app/Dockerfile): Instructions for Docker to build a container image that contains everything required to run the Application within the built container

## Usage

### Quick start

It is assumed that you will want to build more than one docker image as part of your project. As such, we do not use a `Dockerfile` at the root of the project. Instead, each docker image that you create should go in the directory of the thing you want to build i.e. `sandbox`.

Steps to run Sandbox in a Docker container is as follows:

#### Build the Docker Image

Run the following command to build a Docker image tagged with sandbox application name


```shell
make sandbox-build 
```

#### Run the Docker Container

Run the following command to run the Sandbox application in a Docker container. The make command publishes the containers host port to the hosts machine, meaning you can access services running inside the container form your local machine.

```shell
make sandbox-docker-run
```

Test it out by making requests to port 9000


### Platform architecture

For cross-platform image support, the `--platform linux/amd64` flag is used to build Docker images, enabling containers to run without any changes on both `amd64` and `arm64` architectures (via emulation).

### `Dockerignore` file

If you need to exclude files from a `COPY` command, put a [`Dockerfile.dockerignore`](https://docs.docker.com/build/building/context/#filename-and-location) file next to the relevant `Dockerfile`. They do not live in the root directory. Any paths within `Dockerfile.dockerignore` must be relative to the repository root.
