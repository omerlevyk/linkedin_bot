# linkedin_bot

`linkedin_bot` generates one DevOps/MLOps post with OpenAI and publishes it to a
personal LinkedIn profile. It is designed to run as a Kubernetes `CronJob` on
k3s.

The bot rotates between educational posts, practical tips, riddles, "did you
know?" posts, career guidance, failure stories, and tool comparisons. It keeps
a small local history so recent posts are not repeated.

## Requirements

- An OpenAI API key.
- A LinkedIn developer application with the **Share on LinkedIn** product and
  the `w_member_social` OAuth scope.
- Your LinkedIn person URN (`urn:li:person:...`) and access token.
- A container registry reachable by the k3s nodes.

Use the official LinkedIn API. Browser automation can violate LinkedIn's terms
and is intentionally not part of this project.

## Run locally

Python 3.12 or newer is recommended. The application only uses the standard
library.

```bash
export OPENAI_API_KEY='...'
export LINKEDIN_ACCESS_TOKEN='...'
export LINKEDIN_AUTHOR_URN='urn:li:person:...'
export DRY_RUN=true
python -m linkedin_bot
```

`DRY_RUN=true` still calls OpenAI, but prints the post rather than publishing
it. Set `POST_LANGUAGE` to the language you want (for example `English` or
`Hebrew`).

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | required | OpenAI API key |
| `OPENAI_MODEL` | `gpt-5-mini` | Model used through the Responses API |
| `LINKEDIN_ACCESS_TOKEN` | required unless dry-run | LinkedIn OAuth token |
| `LINKEDIN_AUTHOR_URN` | required unless dry-run | `urn:li:person:...` |
| `LINKEDIN_VERSION` | `202609` | LinkedIn API version (`YYYYMM`) |
| `DRY_RUN` | `true` | Do not publish when true |
| `POST_LANGUAGE` | `English` | Output language |
| `POST_TONE` | practical and concise | Writing style |
| `POST_MAX_CHARS` | `2600` | Maximum generated post length |
| `STATE_PATH` | `/data/history.json` | Duplicate-history location |
| `TOPICS` | built-in list | Optional comma-separated topic override |

## Test, build, and deploy

```bash
python -m unittest discover -s tests -v
docker build -t REGISTRY/linkedin-bot:0.1.0 .
docker push REGISTRY/linkedin-bot:0.1.0
```

Edit the image in `k8s/cronjob.yaml`, then create the resources:

```bash
kubectl apply -f k8s/namespace.yaml
cp k8s/secret.example.yaml /tmp/linkedin-bot-secret.yaml
# Fill in /tmp/linkedin-bot-secret.yaml; never commit it.
kubectl apply -f /tmp/linkedin-bot-secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/cronjob.yaml
```

The supplied schedule is `07:30` in `Asia/Jerusalem`. Verify the first run in
dry-run mode:

```bash
kubectl -n linkedin-bot create job --from=cronjob/linkedin-bot linkedin-bot-test
kubectl -n linkedin-bot logs -f job/linkedin-bot-test
```

After reviewing the output, change `DRY_RUN` to `"false"` and re-apply the
CronJob. LinkedIn tokens expire; rotate the Secret before expiry.
