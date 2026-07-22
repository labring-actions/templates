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
- **First-admin bootstrap helper**: Waits for Paperclip health, creates or rotates the setup-code invitation, and gates readiness until initialization succeeds.
- **Persistent volume**: Stores `/paperclip` configuration, secrets, logs, workspaces, and local uploads.
- **Optional ObjectStorageBucket**: Stores attachments and company assets through Paperclip's S3 provider.
- **Service, Ingress, and App resource**: Provide the public HTTPS endpoint and a compatibility link to the setup-code invitation.

Paperclip runs in `authenticated` deployment mode with `public` exposure. This mode requires `DATABASE_URL`, so the template always provisions an independent PostgreSQL cluster. The Paperclip pod and its init containers run as UID/GID `1000` with privilege escalation disabled, all Linux capabilities dropped, and the runtime-default seccomp profile. The PostgreSQL init Job also disables privilege escalation and drops all Linux capabilities.

Optional provider keys can be supplied during deployment:

- `openai_api_key` for Codex and OpenAI-backed agents
- `anthropic_api_key` for Claude-backed agents
- `gemini_api_key` for Gemini-backed agents

Storage modes:

- **Local storage**: The default. Files are stored under `/paperclip/instances/default/data/storage` on the persistent volume.
- **S3 storage**: Enable `use_object_storage` to provision a private bucket and configure Paperclip's S3 provider automatically.

**Validated resource limits:**

- Paperclip app: `100m` CPU and `1024Mi` memory
- Init containers: `100m` CPU and `128Mi` memory
- PostgreSQL: `500m` CPU and `512Mi` memory

Paperclip exposes `/api/health`. Startup and liveness use this endpoint directly. Readiness also requires `/tmp/paperclip-bootstrap-ready`, which appears after the first-admin invitation is ready or an administrator already exists.

## Why Deploy Paperclip on Sealos?

- **One-click deployment**: Provision Paperclip, PostgreSQL, storage, and HTTPS from one template.
- **Persistent workspace**: Keep encrypted secrets, logs, workspaces, and app state across restarts.
- **Managed object storage**: Select a private S3-compatible bucket for uploaded assets.
- **Public HTTPS access**: Receive a Sealos-managed endpoint automatically.
- **Canvas operations**: Adjust provider keys, resources, storage, and networking from resource cards.

## Deployment Guide

1. Open the [Paperclip template](https://sealos.io/products/app-store/paperclip) and click **Deploy Now**.
2. Record the prefilled `first_admin_setup_code` before confirming deployment. You may replace it with 32-128 URL-safe characters containing uppercase letters, lowercase letters, and numbers.
3. Choose the storage mode. Keep `use_object_storage` disabled for persistent local storage, or enable it for a private Sealos Object Storage bucket.
4. Add any provider API keys required by your agents.
5. Wait about 2-3 minutes for PostgreSQL migrations, Paperclip startup, and first-admin setup.
6. Copy the Paperclip public hostname shown in Sealos and open `https://<your-paperclip-host>/invite/<first_admin_setup_code>`. The Sealos App entry points to the same invitation URL as a compatibility shortcut.

## First Login and Registration

1. Open `https://<your-paperclip-host>/invite/<first_admin_setup_code>` with the code recorded before deployment.
2. Click **Sign in / Create account**, select **Create account**, enter your name, email address, and password, then submit the form.
3. Return to the same invitation URL and click **Accept bootstrap invite**.
4. Complete onboarding by creating your first company.
5. Open the company board to create tasks, add comments, change priorities, and configure agents.

The first-admin invitation is valid for 72 hours from its latest successful preparation and can be claimed once. A Pod restart refreshes an unclaimed invitation with the same setup code. After the first administrator accepts it, use the public host root URL for regular sign-in. Treat the setup code as a bearer credential while the invitation remains active. The compatibility App entry stores the invitation path, and opening it records the path in browser history and Paperclip request logs; keep access to the Sealos workspace and Paperclip logs within the trusted operator boundary.

## Configuration

- **Web UI**: Manage companies, agents, tasks, plugins, secrets, and approvals.
- **Environment variables**: Add or rotate provider API keys from the StatefulSet resource card.
- **First-admin setup code**: Record it before deployment and keep it private until the invitation is accepted.
- **Storage**: Select local persistent storage or S3-compatible object storage during deployment.
- **Resources**: Adjust CPU, memory, volume size, or Ingress settings from Sealos Canvas.

## Troubleshooting

### The setup code is missing or expired

Open the existing Paperclip deployment in Sealos, set a fresh valid `first_admin_setup_code`, and redeploy it. The bootstrap helper revokes the previous active invitation and creates a new invitation that remains valid for 72 hours. Record the new code before confirming the redeployment.

### Agent runs report missing credentials

Add `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` through the deployment inputs or StatefulSet environment variables for the selected agent CLI.

### File uploads fail

For local storage, confirm that the `/paperclip` volume is mounted and writable by UID `1000`. For S3 storage, inspect the ObjectStorageBucket status and its generated credentials, then confirm the Paperclip pod is Ready.

## License

This Sealos template provides deployment configuration for Paperclip. Paperclip is distributed under the MIT License.
