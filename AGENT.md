# Repository instructions

These instructions apply to every change in this repository.

## Working style

- Make focused changes that are easy to review.
- Stage and commit completed work often. Do not leave a large collection of
  unrelated changes for one final commit.
- Use short, meaningful, imperative commit messages, for example:
  `add LinkedIn token validation`, `document local setup`, or
  `test duplicate detection`.
- Keep each commit limited to one coherent purpose.
- Do not amend, squash, rebase, or force-push existing commits unless the user
  explicitly requests it.
- Never commit credentials, access tokens, API keys, generated secrets, local
  `.env` files, or private LinkedIn data.

## Verification

- Run `python -m unittest discover -s tests -v` after Python changes.
- Run `git diff --check` before each commit.
- Validate Kubernetes manifests after changing them with:
  `kubectl create --dry-run=client --validate=false -f k8s/ -o name`.
- Build the container after Dockerfile or packaging changes when Docker access
  is available.
- Report any validation that could not be run and why.

## Documentation

- Keep Markdown documentation in `docs/` current with behavior changes.
- Update `docs/work-log.md` after meaningful implementation work.
- Update `docs/readmap.md` when planned work is added, completed, reprioritized,
  or removed.
- Update `docs/project.md` when architecture, deployment, configuration, or
  operational behavior changes.
- Keep the root `README.md` focused on getting started and operating the app.
- Documentation should clearly distinguish completed work from planned work.

## Application conventions

- Use LinkedIn's official APIs; do not add browser automation.
- Keep publishing disabled by default with `DRY_RUN=true` in example manifests.
- Keep secrets in environment variables populated by Kubernetes Secrets.
- Fail safely: do not record a post as published unless LinkedIn accepted it.
- Preserve the non-root container and least-privilege Kubernetes security
  settings.
- Add or update tests for behavior changes.

