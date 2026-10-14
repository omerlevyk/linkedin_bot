# Work log

This file records meaningful completed work. New entries should be added at the
top of the log.

## 2026-10-14 — Initial application

Completed:

- Created a Python application that generates DevOps and MLOps LinkedIn posts
  through the OpenAI Responses API.
- Added a broad built-in topic list and seven rotating post formats.
- Added configurable language, tone, topic, model, and length settings.
- Integrated text-only publishing through LinkedIn's official Posts API.
- Added dry-run mode and made it the deployment default.
- Added exact-duplicate detection and persistent publication history.
- Added defensive configuration and API error handling.
- Added a minimal, non-root Docker image.
- Added k3s manifests for the namespace, Secret, PVC, and daily CronJob.
- Scheduled the CronJob for 07:30 in `Asia/Jerusalem`.
- Added five unit tests covering configuration, output parsing, deterministic
  selection, and history behavior.
- Validated the tests and Kubernetes manifest parsing.

Known validation limitation:

- The image was not built locally because the current account could not access
  the Docker daemon socket.

