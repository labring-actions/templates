# Deploy and Host Paperclip on Sealos

Paperclip is an open-source control plane for running AI agent companies. It brings companies, agents, projects, tasks, approvals, plugins, secrets, and execution history into one web application. This template deploys Paperclip with managed PostgreSQL, persistent application storage, optional S3-compatible object storage, and public authenticated access on Sealos Cloud.

![Paperclip Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/paperclip/website-screenshot.webp)

## About Hosting Paperclip

Paperclip coordinates AI agents around real work. Its web interface and API let you create companies, define agent roles, manage projects and issues, review approvals, and inspect agent activity. The official container includes local agent CLIs such as Codex, Claude, OpenCode, and Gemini.

The Sealos template runs Paperclip as a Kubernetes StatefulSet. KubeBlocks provisions PostgreSQL for authenticated public deployments, while a persistent volume stores configuration, encrypted secrets, workspaces, logs, and local uploads. Enabling `use_object_storage` provisions a private Sealos Object Storage bucket for attachments and company assets.

## Common Use Cases

- **AI team operations**: Create companies, assign agents, and coordinate project work.
- **Task and approval workflows**: Track issues, comments, priorities, approvals, and execution history.
- **Coding agent hub**: Run Codex, Claude, OpenCode, or Gemini agents from one web UI.
- **Plugin operations**: Install plugins and monitor their health.
- **Private agent workspace**: Keep workspace data and secrets in a Sealos-managed deployment.

## Dependencies

- Paperclip release `v2026.720.0`, pinned to image digest `sha256:30237caad0ca3625fd10436a833c3b40809fe54b84debd702896e801d02c584e`
- PostgreSQL `16.4.0` through KubeBlocks
- Persistent storage mounted at `/paperclip`
- Optional private S3-compatible object storage
- Sealos HTTPS Ingress and App entry

### Official References

- [Paperclip website](https://paperclip.ing)
- [Paperclip documentation](https://docs.paperclip.ing)
- [Paperclip GitHub repository](https://github.com/paperclipai/paperclip)
- [Docker deployment guide](https://github.com/paperclipai/paperclip/blob/v2026.720.0/doc/DOCKER.md)
- [Database guide](https://docs.paperclip.ing/deploy/database)
- [Storage guide](https://docs.paperclip.ing/deploy/storage)

## Implementation Details

**Architecture components:**

- **Paperclip StatefulSet**: Runs the pinned Paperclip image on port `3100`.
- **PostgreSQL Cluster**: Stores users, companies, tasks, approvals, plugins, and runtime metadata.
- **PostgreSQL init Job**: Waits for PostgreSQL and creates the `paperclip` database idempotently.
- **Configuration init container**: Writes `/paperclip/instances/default/config.json` for the selected storage mode.
- **Bootstrap CEO Job**: Creates the first-admin invite used by the Sealos App entry.
- **Persistent volume**: Stores `/paperclip` configuration, secrets, logs, workspaces, and local uploads.
- **Optional ObjectStorageBucket**: Stores attachments and company assets through Paperclip's S3 provider.
- **Service, Ingress, and App resource**: Provide the public HTTPS endpoint and first-admin entry.

Paperclip runs in `authenticated` deployment mode with `public` exposure. This mode requires `DATABASE_URL`, so the template always provisions an independent PostgreSQL cluster. The app pod and helper jobs run as UID/GID `1000` with privilege escalation disabled, all Linux capabilities dropped, and the runtime-default seccomp profile.

Optional provider keys can be supplied during deployment:

- `openai_api_key` for Codex and OpenAI-backed agents
- `anthropic_api_key` for Claude-backed agents
- `gemini_api_key` for Gemini-backed agents

Storage modes:

- **Local storage**: The default. Files are stored under `/paperclip/instances/default/data/storage` on the persistent volume.
- **S3 storage**: Enable `use_object_storage` to provision a private bucket and configure Paperclip's S3 provider automatically.

**Validated resource limits:**

- Paperclip app: `100m` CPU and `512Mi` memory
- Init and bootstrap containers: `100m` CPU and `128Mi` memory
- PostgreSQL: `500m` CPU and `512Mi` memory

Paperclip exposes `/api/health`; the template uses it for startup, readiness, and liveness probes.

## Why Deploy Paperclip on Sealos?

- **One-click deployment**: Provision Paperclip, PostgreSQL, storage, and HTTPS from one template.
- **Persistent workspace**: Keep encrypted secrets, logs, workspaces, and app state across restarts.
- **Managed object storage**: Select a private S3-compatible bucket for uploaded assets.
- **Public HTTPS access**: Receive a Sealos-managed endpoint automatically.
- **Canvas operations**: Adjust provider keys, resources, storage, and networking from resource cards.

## Deployment Guide

1. Open the [Paperclip template](https://sealos.io/products/app-store/paperclip) and click **Deploy Now**.
2. Choose the storage mode. Keep `use_object_storage` disabled for persistent local storage, or enable it for a private Sealos Object Storage bucket.
3. Add any provider API keys required by your agents.
4. Wait about 2-3 minutes for PostgreSQL migrations, Paperclip startup, and the bootstrap invite.
5. Open the Paperclip entry from Sealos. The entry leads directly to the first-admin invitation.

## First Login and Registration

1. On the invitation page, click **Sign in / Create account**.
2. Select **Create account**, enter your name, email address, and password, then submit the form.
3. Return to the invitation page and click **Accept bootstrap invite**.
4. Complete onboarding by creating your first company.
5. Open the company board to create tasks, add comments, change priorities, and configure agents.

After the first administrator accepts the invitation, use the public host root URL for regular sign-in. The bootstrap invitation expires after 72 hours. The bootstrap Job remains available for five minutes after completion, which provides a short window for inspecting its generated `Invite URL` in logs.

## Configuration

- **Web UI**: Manage companies, agents, tasks, plugins, secrets, and approvals.
- **Environment variables**: Add or rotate provider API keys from the StatefulSet resource card.
- **Storage**: Select local persistent storage or S3-compatible object storage during deployment.
- **Resources**: Adjust CPU, memory, volume size, or Ingress settings from Sealos Canvas.

## Troubleshooting

### The invitation page has expired

Generate a new first-admin invitation from the Paperclip StatefulSet terminal:

```bash
node cli/node_modules/tsx/dist/cli.mjs cli/src/index.ts auth bootstrap-ceo \
  --config "$PAPERCLIP_CONFIG" \
  --base-url "$PAPERCLIP_PUBLIC_URL" \
  --expires-hours 72
```

### Agent runs report missing credentials

Add `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` through the deployment inputs or StatefulSet environment variables for the selected agent CLI.

### File uploads fail

For local storage, confirm that the `/paperclip` volume is mounted and writable by UID `1000`. For S3 storage, inspect the ObjectStorageBucket status and its generated credentials, then confirm the Paperclip pod is Ready.

## License

This Sealos template provides deployment configuration for Paperclip. Paperclip is distributed under the MIT License.
