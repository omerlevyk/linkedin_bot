# Project readmap

This is the living implementation plan. Completed items remain visible so the
current state and next priorities are clear.

## Completed

- [x] Create the Python post-generation application.
- [x] Integrate the OpenAI Responses API.
- [x] Integrate text-only LinkedIn publishing.
- [x] Add dry-run mode.
- [x] Rotate DevOps/MLOps subjects and post styles.
- [x] Store recent publication history on a persistent volume.
- [x] Prevent exact duplicate posts.
- [x] Add unit tests and Kubernetes manifests.
- [x] Harden the container and pod security context.
- [x] Document local and k3s deployment.

## Next: first deployment

- [ ] Create and configure the LinkedIn developer application.
- [ ] Obtain the `w_member_social` permission and personal author URN.
- [ ] Create an OpenAI API key with an appropriate usage limit.
- [ ] Choose a container registry and replace `REGISTRY` in the CronJob.
- [ ] Build and push the first image.
- [ ] Create the Kubernetes Secret outside Git.
- [ ] Deploy the CronJob with dry-run enabled.
- [ ] Inspect several generated posts for voice and technical accuracy.
- [ ] Enable automatic publishing by setting `DRY_RUN=false`.

## Reliability improvements

- [ ] Add near-duplicate detection rather than exact hashes only.
- [ ] Retry generation once when the model exceeds the character limit.
- [ ] Add structured generation metadata for topic, format, and title.
- [ ] Add metrics or health notifications for successful and failed runs.
- [ ] Add alerting before the LinkedIn token expires.
- [ ] Define image tags and an upgrade/rollback procedure.
- [ ] Add CI for tests, manifest validation, and container builds.

## Content improvements

- [ ] Add optional personal context so posts better reflect the author's real
  experience without inventing stories.
- [ ] Add configurable weekly content themes.
- [ ] Add a factual review step before automatic publication.
- [ ] Support trusted source links for time-sensitive technical claims.
- [ ] Evaluate post quality and engagement without optimizing for spammy
  engagement bait.
- [ ] Add optional image generation and LinkedIn media upload support.

## Possible future features

- [ ] Add an approval workflow through email, Slack, or another channel.
- [ ] Add a small dashboard for history, drafts, and configuration.
- [ ] Support organization pages in addition to personal profiles.
- [ ] Support scheduling special posts for releases, events, or milestones.
