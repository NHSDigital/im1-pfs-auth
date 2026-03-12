# Developer Guide: Reviewing and Resolving Dependabot PRs

- [Developer Guide: Reviewing and Resolving Dependabot PRs](#developer-guide-reviewing-and-resolving-dependabot-prs)
  - [Overview](#overview)
  - [Finding Dependabot PRs](#finding-dependabot-prs)
  - [Dependabot Configuration](#dependabot-configuration)
  - [Review Process](#review-process)
    - [1. Initial Assessment](#1-initial-assessment)
    - [2. Review Changes](#2-review-changes)
    - [3. Check for Breaking Changes](#3-check-for-breaking-changes)
    - [4. Test the Changes](#4-test-the-changes)
    - [5. Verify Compatibility](#5-verify-compatibility)
  - [Testing Dependabot PRs](#testing-dependabot-prs)
    - [Testing GitHub Actions Updates](#testing-github-actions-updates)
    - [Testing Python Dependencies (uv)](#testing-python-dependencies-uv)
    - [Testing npm Dependencies](#testing-npm-dependencies)
    - [Testing Docker Base Images](#testing-docker-base-images)
    - [Manual Deployment and End-to-End Testing](#manual-deployment-and-end-to-end-testing)
  - [Common Issues and Solutions](#common-issues-and-solutions)
    - [Version Conflicts](#version-conflicts)
    - [Lock File Issues](#lock-file-issues)
    - [Test Failures](#test-failures)
  - [Dependabot Commands](#dependabot-commands)
  - [Approval and Merge Guidelines](#approval-and-merge-guidelines)
  - [Post-Merge Verification](#post-merge-verification)

## Overview

Dependabot automatically creates pull requests to update dependencies in this repository. This guide provides a systematic approach to reviewing and resolving these PRs to ensure updates are safe, compatible, and don't introduce regressions.

This repository uses Dependabot to monitor and update:

- **GitHub Actions** workflows and actions
- **Python dependencies** managed by `uv`
- **npm packages** for Node.js tooling
- **Docker base images** for containerized applications

## Finding Dependabot PRs

You can find Dependabot PRs using GitHub's search filters in the Pull Requests tab:

**Basic filter**:

```
is:open is:pr author:app/dependabot
```

**Additional useful filters**:

- All Dependabot PRs (open and closed):

  ```
  is:pr author:app/dependabot
  ```

- Dependabot PRs by ecosystem (using labels):

  ```
  is:open is:pr author:app/dependabot label:dependencies
  is:open is:pr author:app/dependabot label:github_actions
  is:open is:pr author:app/dependabot label:docker
  ```

- Dependabot PRs with conflicts:

  ```
  is:open is:pr author:app/dependabot status:failure
  ```

- Recently updated Dependabot PRs:
  ```
  is:open is:pr author:app/dependabot sort:updated-desc
  ```

**Direct URL**: You can also bookmark this URL to quickly view all open Dependabot PRs:

```
https://github.com/NHSDigital/im1-pfs-auth/pulls?q=is%3Aopen+is%3Apr+author%3Aapp%2Fdependabot
```

## Dependabot Configuration

The Dependabot configuration is located at `.github/dependabot.yaml` and includes:

- **Update schedule**: Monthly for all ecosystems
- **Grouped updates**: Minor and patch updates are grouped together by ecosystem
- **Directories monitored**:
  - GitHub Actions: Multiple directories including workflows and custom actions
  - Python (uv): Root directory (`/`)
  - npm: Root directory (`/`)
  - Docker: `/app` and `/sandbox` directories

## Review Process

### 1. Initial Assessment

When a Dependabot PR is opened:

1. **Read the PR description** - Dependabot provides a summary of changes, including:
   - Package name and versions (from → to)
   - Release notes links
   - Changelog links
   - Commit history

2. **Check the update type**:
   - **Patch updates** (e.g., 1.2.3 → 1.2.4): Usually safe, bug fixes only
   - **Minor updates** (e.g., 1.2.0 → 1.3.0): May include new features, generally backward compatible
   - **Major updates** (e.g., 1.0.0 → 2.0.0): May include breaking changes, require careful review

3. **Review the ecosystem**:
   - Different ecosystems have different risk profiles and testing requirements

### 2. Review Changes

1. **Examine the diff** in the Files Changed tab:
   - For `uv` updates: Check `pyproject.toml` and `uv.lock`
   - For `npm` updates: Check `package.json` and `package-lock.json`
   - For GitHub Actions: Check workflow files or action version pins
   - For Docker: Check `Dockerfile` base image versions

2. **Review release notes and changelogs**:
   - Click on the release notes links in the PR description
   - Look for breaking changes, deprecations, or security fixes
   - Note any migration steps or configuration changes required

3. **Check for related updates**:
   - Does this update require changes to other dependencies?
   - Are there updates to `.tool-versions` needed? (See [Version Conflicts](#version-conflicts))
   - Do configuration files need updates?

### 3. Check for Breaking Changes

**Red flags to watch for**:

- Changes to public APIs or function signatures
- Deprecated features being removed
- Changes to default behavior
- New required configuration
- Minimum version requirements for runtime environments (Python, Node.js, etc.)

**Where to look**:

- `CHANGELOG.md` or `HISTORY.md` in the dependency's repository
- GitHub release notes marked with "BREAKING CHANGE"
- Migration guides in documentation
- Issue tracker for reported problems

### 4. Test the Changes

See [Testing Dependabot PRs](#testing-dependabot-prs) section below for detailed testing procedures.

**Minimum testing requirements**:

- [ ] CI/CD pipeline passes (check GitHub Actions status)
- [ ] Local tests pass: `make app-unit-test` and `make sandbox-unit-test`
- [ ] Linting passes: `make lint`
- [ ] Formatting passes: `make format`
- [ ] Build succeeds for affected components

### 5. Verify Compatibility

Check compatibility with related tools and dependencies:

1. **Python dependencies**: Ensure compatibility with Python version in `.tool-versions`
2. **uv version**: Verify `pyproject.toml` `required-version` is compatible with `.tool-versions`
3. **Node.js packages**: Ensure compatibility with Node.js version in `.tool-versions`
4. **GitHub Actions**: Verify runner compatibility (usually `ubuntu-latest`)

## Testing Dependabot PRs

### Testing GitHub Actions Updates

**For workflow updates**:

1. Check out the PR branch:

   ```shell
   git fetch origin pull/<PR_NUMBER>/head:dependabot-pr-<PR_NUMBER>
   git checkout dependabot-pr-<PR_NUMBER>
   ```

2. Review the workflow changes:

   ```shell
   git diff main .github/workflows/
   ```

3. Test locally using `act` (if applicable):

   ```shell
   make runner-act workflow=<workflow_name> job=<job_name>
   ```

4. **Monitor the first CI run** after merge - GitHub Actions updates can't be fully tested locally

**For action version updates**:

1. Check the action's changelog for breaking changes
2. Look for changes in input/output parameters
3. Verify the action is still maintained (check last commit date)

### Testing Python Dependencies (uv)

1. Check out the PR branch:

   ```shell
   git fetch origin pull/<PR_NUMBER>/head:dependabot-pr-<PR_NUMBER>
   git checkout dependabot-pr-<PR_NUMBER>
   ```

2. Install dependencies:

   ```shell
   make install
   ```

3. Run unit tests:

   ```shell
   make app-unit-test
   make sandbox-unit-test
   ```

4. Run linting and formatting:

   ```shell
   make lint
   make format
   ```

5. Test application locally:

   ```shell
   make app-debug-run
   # Or for sandbox
   make sandbox-debug-run
   ```

6. Build Docker containers:
   ```shell
   make app-build CONTAINER_TAG=test EMIS_BASE_URL=test TPP_BASE_URL=test PROXYGEN_DOCKER_REGISTRY_URL=test
   make sandbox-build CONTAINER_TAG=test PROXYGEN_DOCKER_REGISTRY_URL=test
   ```

### Testing npm Dependencies

1. Check out the PR branch:

   ```shell
   git fetch origin pull/<PR_NUMBER>/head:dependabot-pr-<PR_NUMBER>
   git checkout dependabot-pr-<PR_NUMBER>
   ```

2. Install dependencies:

   ```shell
   npm install
   ```

3. Run npm scripts:

   ```shell
   npm run lint
   npm run format
   ```

4. Test Postman collection generation (if affected):

   ```shell
   make postman-generate-collection
   ```

5. Check for vulnerabilities:
   ```shell
   npm audit
   ```

### Testing Docker Base Images

1. Check out the PR branch:

   ```shell
   git fetch origin pull/<PR_NUMBER>/head:dependabot-pr-<PR_NUMBER>
   git checkout dependabot-pr-<PR_NUMBER>
   ```

2. Build the affected Docker images:

   ```shell
   make app-build CONTAINER_TAG=test EMIS_BASE_URL=test TPP_BASE_URL=test PROXYGEN_DOCKER_REGISTRY_URL=test
   make sandbox-build CONTAINER_TAG=test PROXYGEN_DOCKER_REGISTRY_URL=test
   ```

3. Run the containers locally:

   ```shell
   make app-docker-run
   # Or for sandbox
   make sandbox-docker-run
   ```

4. Verify the application starts and responds correctly:

   ```shell
   curl http://localhost:9000/health  # Adjust endpoint as needed
   ```

5. Run unit tests inside the container:
   ```shell
   docker run --rm <image_name>:<tag> uv run pytest
   ```

### Manual Deployment and End-to-End Testing

> **Important**: Dependabot PRs automatically skip deployment and end-to-end tests in the CI/CD pipeline (see the `if: ${{ github.actor != 'dependabot[bot]' }}` condition in `.github/workflows/pull-request-checks.yml`). For critical updates or when you want additional confidence, you may need to manually deploy and run end-to-end tests.

End-to-end tests require a deployed instance on the NHS API Platform because they test the full integration including authentication, API gateway behavior, and backend services.

**When to consider manual deployment and e2e testing**:

- Major version updates to critical dependencies
- Updates to Flask, Gunicorn, or other core application dependencies
- Docker base image updates
- When you want to verify the full stack works correctly

**Steps to manually deploy and test a Dependabot PR**:

1. **Ensure you have proxygen-cli installed**:

   See the [Proxygen CLI guide](../user-guides/Proxygen_CLI.md) for installation instructions.

2. **Check out the Dependabot PR branch**:

   ```shell
   git fetch origin pull/<PR_NUMBER>/head:dependabot-pr-<PR_NUMBER>
   git checkout dependabot-pr-<PR_NUMBER>
   ```

3. **Build the Docker container images**:

   ```shell
   # Build app container
   make app-build \
     PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" \
     CONTAINER_TAG="dependabot-pr-<PR_NUMBER>-$(git rev-parse --short HEAD)" \
     EMIS_BASE_URL="https://nhs70apptest.emishealth.com" \
     TPP_BASE_URL="https://systmonline2.tpp-uk.com"

   # Build sandbox container (if needed)
   make sandbox-build \
     PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" \
     CONTAINER_TAG="dependabot-pr-<PR_NUMBER>-$(git rev-parse --short HEAD)"
   ```

4. **Push the container images** (requires AWS/proxygen authentication):

   ```shell
   # Push app container
   make app-push \
     PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" \
     CONTAINER_TAG="dependabot-pr-<PR_NUMBER>-$(git rev-parse --short HEAD)"

   # Push sandbox container (if needed)
   make sandbox-push \
     PROXYGEN_DOCKER_REGISTRY_URL="958002497996.dkr.ecr.eu-west-2.amazonaws.com/im1-pfs-auth" \
     CONTAINER_TAG="dependabot-pr-<PR_NUMBER>-$(git rev-parse --short HEAD)"
   ```

5. **Deploy to internal-dev environment**:

   ```shell
   make deploy \
     ENVIRONMENT="internal-dev" \
     PROXYGEN_URL_PATH="im1-pfs-auth-dependabot-pr-<PR_NUMBER>" \
     CONTAINER_TAG="dependabot-pr-<PR_NUMBER>-$(git rev-parse --short HEAD)"
   ```

6. **Associate the deployment with the IM1 PFS Auth Developer Test App**:

   This step is required to allow the deployment to access the `mock-jwks` service for authentication testing. Follow the instructions in the [Setup end to end tests guide](../user-guides/Setup_end_to_end_tests.md#associating-the-deployment-with-the-developer-app).

   Quick summary:
   - Go to [Apigee](https://apigee.com/edge) (nhsd-nonprod organization)
   - Navigate to `Publish` → `Apps`
   - Search for "IM1 PFS Auth Developer Test App"
   - Edit → Add product → Search for your deployment
   - Add the `IM1 PFS Auth API - IM1 PFS Auth - P9 User Restriced Access (dev) (Internal Development)` product
   - Save

7. **Run end-to-end tests**:

   ```shell
   make e2e-tests \
     APIGEE_PROXY_NAME="im1-pfs-auth--internal-dev--im1-pfs-auth-dependabot-pr-<PR_NUMBER>" \
     PROXYGEN_URL_PATH="im1-pfs-auth-dependabot-pr-<PR_NUMBER>" \
     TEST_APP_KEYCLOAK_CLIENT_ID="<from-secrets>" \
     TEST_APP_KEYCLOAK_CLIENT_SECRET="<from-secrets>" \
     TEST_APP_API_KEY="<from-secrets>" \
     TEST_APP_PRIVATE_KEY="<from-secrets>"
   ```

   > **Note**: The `TEST_APP_*` credentials are stored in GitHub Secrets. Contact the development team if you need access to these credentials for local testing.

8. **Clean up after testing**:

   After testing is complete, you should clean up the ephemeral deployment to avoid cluttering the internal-dev environment. This is typically done through the Apigee UI or by using proxygen commands to undeploy the instance.

**Related Documentation**:

- [Deploy to Apigee](../user-guides/Deploy_To_Apigee.md) - Full deployment guide
- [Setup end to end tests](../user-guides/Setup_end_to_end_tests.md) - Detailed e2e test setup
- [Proxygen CLI](../user-guides/Proxygen_CLI.md) - Installation and configuration
- [Environments](../user-guides/Environments.md) - Available deployment environments

## Common Issues and Solutions

### Version Conflicts

**Problem**: Dependabot updates a tool version, but it conflicts with requirements in other files.

**Example**: `.tool-versions` specifies `uv 0.8.5`, but `pyproject.toml` requires `>=0.9,<0.11`

**Solution**:

1. Identify the conflict by checking version requirements:

   ```shell
   grep -r "uv" .tool-versions pyproject.toml
   ```

2. Update `.tool-versions` to match requirements:

   ```shell
   # Edit .tool-versions to update the version
   vim .tool-versions
   ```

3. Install the updated version:

   ```shell
   asdf install uv <new_version>
   # or
   make _install-dependency name=uv
   ```

4. Add a commit to the PR branch:
   ```shell
   git add .tool-versions
   git commit -m "Update uv version in .tool-versions to match pyproject.toml requirements"
   git push
   ```

### Lock File Issues

**Problem**: `uv.lock` or `package-lock.json` conflicts or becomes out of sync.

**Solution for uv**:

```shell
# Regenerate the lock file
uv lock
git add uv.lock
git commit -m "Regenerate uv.lock"
git push
```

**Solution for npm**:

```shell
# Regenerate the lock file
npm install
git add package-lock.json
git commit -m "Regenerate package-lock.json"
git push
```

### Test Failures

**Problem**: Tests fail after dependency update.

**Solution**:

1. **Identify the failure**:

   ```shell
   make app-unit-test
   # Review the test output
   ```

2. **Check if it's a known issue**:
   - Search the dependency's issue tracker
   - Check if there's a workaround or fix

3. **Options**:
   - **Fix the code**: Update application code to work with new dependency version
   - **Pin the version**: If it's a breaking change, consider pinning to the previous version temporarily
   - **Report upstream**: If it's a bug in the dependency, report it

4. **Document the fix** in the PR comments

## Dependabot Commands

You can interact with Dependabot by commenting on PRs with specific commands:

| Command                                 | Description                                       | Example                                 |
| --------------------------------------- | ------------------------------------------------- | --------------------------------------- |
| `@dependabot rebase`                    | Rebase the PR branch onto the latest base branch  | `@dependabot rebase`                    |
| `@dependabot recreate`                  | Recreate the PR, discarding any manual changes    | `@dependabot recreate`                  |
| `@dependabot merge`                     | Merge the PR once CI passes and it's approved     | `@dependabot merge`                     |
| `@dependabot squash and merge`          | Squash and merge once approved                    | `@dependabot squash and merge`          |
| `@dependabot cancel merge`              | Cancel a previously requested merge               | `@dependabot cancel merge`              |
| `@dependabot reopen`                    | Reopen a closed PR                                | `@dependabot reopen`                    |
| `@dependabot close`                     | Close the PR and stop updates for this dependency | `@dependabot close`                     |
| `@dependabot ignore this dependency`    | Never create PRs for this dependency again        | `@dependabot ignore this dependency`    |
| `@dependabot ignore this major version` | Ignore this major version                         | `@dependabot ignore this major version` |
| `@dependabot ignore this minor version` | Ignore this minor version                         | `@dependabot ignore this minor version` |

**Usage notes**:

- Commands must be on their own line in a comment
- Only repository collaborators can use Dependabot commands
- Multiple commands can be issued in the same comment, one per line

**Example workflow**:

```markdown
Thanks @dependabot! I've reviewed the changes and they look good.

@dependabot rebase
@dependabot squash and merge
```

## Approval and Merge Guidelines

**Patch and Minor Updates** (Grouped PRs):

- ✅ Can be merged if:
  - All CI checks pass
  - No breaking changes identified in release notes
  - No version conflicts detected
- 👤 **One approval required** from a team member
- ⚡ Can use `@dependabot squash and merge` after approval

**Major Updates**:

- ⚠️ Require additional scrutiny:
  - Thorough review of breaking changes
  - Local testing required
  - Review of migration guides
  - Update of related documentation
- 👥 **Two approvals recommended**
- 🧪 **Extended testing** required
- 📝 Consider creating a separate issue for tracking related work

**When to delay or reject**:

- ❌ CI pipeline fails
- ❌ Known security vulnerabilities in the update
- ❌ Breaking changes that require significant refactoring
- ❌ Conflicts with other in-flight work
- ⏸️ During code freeze or release periods

## Post-Merge Verification

After merging a Dependabot PR:

1. **Monitor CI/CD pipelines** for the main branch:
   - Check that all workflows complete successfully
   - Verify deployments to development environments

2. **Watch for issues**:
   - Monitor error logs in deployed environments
   - Check for new issue reports
   - Review metrics for anomalies

3. **Update `.tool-versions` if needed**:
   - If a Python, Node.js, or other tool was updated in dependencies
   - Ensure versions are consistent across all configuration files
   - Create a follow-up PR if synchronization is needed

4. **Document significant updates**:
   - Update CHANGELOG if the project maintains one
   - Notify the team in Slack/Teams if the update affects their workflow
   - Update developer documentation if new features are available

5. **Plan follow-up work**:
   - Create issues for adopting new features
   - Schedule refactoring for deprecated functionality
   - Plan testing for major version updates

---

**Related Documentation**:

- [Contributing Guidelines](./CONTRIBUTING.md)
- [Bash and Make Developer Guide](./Bash_and_Make.md)
- [Test GitHub Actions Locally](../user-guides/Test_GitHub_Actions_locally.md)
