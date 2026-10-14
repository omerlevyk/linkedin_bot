# Project overview

## Purpose

`linkedin_bot` automatically creates and publishes one useful LinkedIn post per
day for a DevOps engineer. Posts cover DevOps and MLOps subjects such as
networking, Kubernetes, OpenShift, cloud platforms, Linux, Terraform,
Crossplane, Ansible, Go, Python, Git, infrastructure as code, CI/CD,
observability, security, and career development.

The content rotates between educational explanations, practical tips,
technical riddles, "did you know?" posts, career advice, production lessons,
comparisons, and checklists.

## Architecture

The application is a short-lived Python process designed for a k3s Kubernetes
`CronJob`:

1. Load configuration and credentials from environment variables.
2. Select a deterministic topic and format for the current day.
3. Include previews of recent posts in the generation prompt.
4. Generate a text post using the OpenAI Responses API.
5. Reject empty, oversized, or exactly duplicated output.
6. Print the post in dry-run mode or publish it through LinkedIn's Posts API.
7. Record a successful publication in persistent history.

The application uses Python's standard library and has no runtime package
dependencies. A small JSON history file is stored on a Kubernetes persistent
volume.

## Safety and operations

- The example deployment starts with `DRY_RUN=true`.
- LinkedIn and OpenAI credentials are loaded from a Kubernetes Secret.
- The container runs as a non-root user with a read-only root filesystem and
  dropped Linux capabilities.
- Kubernetes prevents overlapping jobs with `concurrencyPolicy: Forbid`.
- Failed API calls return a non-zero exit status and are eligible for the
  CronJob's limited retries.
- LinkedIn OAuth access tokens must currently be rotated before they expire.

## Repository layout

| Path | Purpose |
|---|---|
| `linkedin_bot/` | Application source code |
| `tests/` | Standard-library unit tests |
| `k8s/` | Namespace, Secret example, PVC, and CronJob manifests |
| `.github/workflows/` | Tests and GHCR image publication |
| `docs/` | Architecture, progress, decisions, and planned work |
| `Dockerfile` | Minimal non-root runtime image |
| `README.md` | Setup, configuration, and deployment guide |

## Delivery

GitHub Actions runs unit tests and syntax checks for pull requests and pushes.
Pushes to `main` publish `latest` and commit-specific images to GHCR. Version
tags such as `v0.1.0` publish the corresponding `0.1.0` container tag used by
the k3s manifest.
