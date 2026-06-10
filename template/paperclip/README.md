# Deploy and Host Paperclip on Sealos

Paperclip is an open-source platform for running AI teams, agent companies, issue workflows, approvals, plugins, and local coding agents. This template deploys Paperclip with PostgreSQL, persistent application storage, optional S3-compatible object storage, and public authenticated access on Sealos Cloud.

![Paperclip Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/paperclip/website-screenshot.webp)

## About Hosting Paperclip

Paperclip provides a web interface and API for organizing AI agents around companies, projects, issues, approvals, secrets, plugins, and execution workspaces. The Docker image includes local agent CLIs such as Codex, Claude, OpenCode, and Gemini so configured agents can run inside the container.

The Sealos template runs Paperclip as a Kubernetes StatefulSet. KubeBlocks provisions PostgreSQL for application data, while a persistent volume stores Paperclip home data, local encrypted secrets, workspaces, logs, and local file storage. When `use_object_storage` is enabled, Paperclip stores attachments and company assets in S3-compatible object storage.

Sealos handles public HTTPS access, database provisioning, persistent storage, resource configuration, and app entry management.

## Common Use Cases

- **AI Team Operations**: Create companies, assign agents, and coordinate work across projects.
- **Issue and Approval Workflow**: Track tasks, comments, approvals, and execution history.
- **Coding Agent Hub**: Run Codex, Claude, OpenCode, or Gemini backed agents from one web UI.
- **Plugin Platform**: Install and manage Paperclip plugins and plugin health.
- **Private Agent Workspace**: Keep workspace data and secrets in a Sealos-managed deployment.

## Dependencies for Paperclip Hosting

The Sealos template includes the required runtime dependencies:

- Paperclip image `ghcr.io/paperclipai/paperclip:sha-b8725c5`
- PostgreSQL `16.4.0` through KubeBlocks
- Persistent storage mounted at `/paperclip`
- Optional S3-compatible object storage for attachments and assets
- HTTPS Ingress and Sealos App entry

### Deployment Dependencies

- [Paperclip Official Website](https://paperclip.ing) - Product homepage
- [Paperclip Documentation](https://paperclip.ing/docs) - Official docs
- [Paperclip GitHub Repository](https://github.com/paperclipai/paperclip) - Source code and releases
- [Paperclip Docker Guide](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/docker.md) - Docker deployment reference
- [Paperclip Database Guide](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/database.md) - PostgreSQL configuration reference
- [Paperclip Storage Guide](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/storage.md) - Local disk and S3 storage reference

## Implementation Details

**Architecture Components:**

- **Paperclip StatefulSet**: Runs `ghcr.io/paperclipai/paperclip:sha-b8725c5` on port `3100`.
- **PostgreSQL Cluster**: Stores users, companies, issues, approvals, plugin state, and runtime metadata.
- **PostgreSQL Init Job**: Waits for PostgreSQL readiness and creates the `paperclip` database idempotently.
- **Paperclip Configure Init Container**: Writes `/paperclip/instances/default/config.json` and sets the agent JWT secret.
- **Persistent Paperclip Volume**: Stores `/paperclip` data, local secrets, logs, workspaces, and local storage.
- **Optional ObjectStorageBucket**: Enables S3 storage through `PAPERCLIP_STORAGE_PROVIDER=s3`.
- **Service, Ingress, and App Resource**: Expose Paperclip through a public HTTPS URL.

**Configuration:**

The template runs Paperclip in `authenticated` deployment mode with `public` exposure. It sets `PAPERCLIP_PUBLIC_URL`, `PAPERCLIP_AUTH_PUBLIC_BASE_URL`, and allowed hostnames to the Sealos public URL.

The template writes the first-run Paperclip configuration during startup. After the app is healthy, open the Paperclip StatefulSet terminal and run the bootstrap command below to generate the first CEO invite. Open the printed `Invite URL`, click **Sign in / Create account**, create the first user, then return to the invite page and click **Accept bootstrap invite**. After bootstrap completes, signed-in users land in the onboarding flow for creating the first company.

```bash
node cli/node_modules/tsx/dist/cli.mjs cli/src/index.ts auth bootstrap-ceo \
  --config "$PAPERCLIP_CONFIG" \
  --base-url "$PAPERCLIP_PUBLIC_URL" \
  --expires-hours 72
```

Optional provider keys can be configured during deployment:

- `openai_api_key` for Codex and OpenAI-backed agents
- `anthropic_api_key` for Claude-backed agents
- `gemini_api_key` for Gemini-backed agents

Object storage has two modes:

- **Local storage**: Default. Paperclip stores files under `/paperclip/instances/default/data/storage`.
- **S3 storage**: Enable `use_object_storage` to create an S3-compatible bucket and configure `PAPERCLIP_STORAGE_S3_*`.

**Resource Defaults:**

- App CPU limit: `500m`
- App memory limit: `512Mi`
- PostgreSQL CPU limit: `500m`
- PostgreSQL memory limit: `512Mi`

**Health Checks:**

Paperclip exposes `/api/health`. The template uses this endpoint for startup, readiness, and liveness probes. Live QA should also complete the first-user signup and open at least one company or issue workflow.

**License Information:**

Paperclip is licensed under the MIT License.

## Why Deploy Paperclip on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and operations. By deploying Paperclip on Sealos, you get:

- **One-Click Deployment**: Deploy Paperclip with PostgreSQL, storage, and HTTPS access from one template.
- **Persistent Agent Workspace**: Keep local secrets, logs, workspace files, and app state across restarts.
- **Optional Object Storage**: Move attachments and company assets to S3-compatible storage.
- **Instant Public Access**: Sealos provisions a public HTTPS endpoint automatically.
- **Easy Customization**: Adjust API keys, resources, and storage from the Sealos Canvas.
- **AI-Assisted Operations**: Use the Sealos AI dialog or resource cards for post-deployment changes.

## Deployment Guide

1. Open the [Paperclip template](https://sealos.io/products/app-store/paperclip) and click **Deploy Now**.
2. Configure deployment parameters:
   - **use_object_storage**: Enable this option to store attachments and assets in S3-compatible object storage.
   - **openai_api_key**: Optional key for OpenAI-backed agents.
   - **anthropic_api_key**: Optional key for Claude-backed agents.
   - **gemini_api_key**: Optional key for Gemini-backed agents.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Paperclip through the provided URL:
   - **First admin**: Open the Paperclip StatefulSet terminal and run the bootstrap command from the Configuration section, then copy the generated `Invite URL`.
   - **Paperclip Web UI**: Open the invite URL, create the first account, accept the bootstrap invite, then complete onboarding.
   - **Paperclip API**: Use the same public URL with `/api/*` paths.

## Configuration

After deployment, configure Paperclip through:

- **Web UI**: Manage companies, agents, issues, plugins, secrets, and approvals.
- **Environment Variables**: Add or rotate provider API keys from the StatefulSet resource card.
- **Storage Settings**: Keep local storage or enable S3-compatible storage at deployment time.
- **Resource Cards**: Adjust CPU, memory, persistent volume size, or Ingress settings in Canvas.

## Troubleshooting

### Health check reports bootstrap pending

- **Cause**: Paperclip is waiting for the first admin account and bootstrap flow.
- **Solution**: Open the Paperclip StatefulSet terminal, run the bootstrap command from the Configuration section, create the first account from the printed invite, and click **Accept bootstrap invite**.

### Agent runs fail because credentials are missing

- **Cause**: The selected local agent CLI needs a provider API key.
- **Solution**: Add `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` through deployment inputs or the StatefulSet environment variables.

### File uploads fail

- **Cause**: Local storage permissions or S3 credentials are incomplete.
- **Solution**: Keep the template's `/paperclip` persistent volume and permission init container. If object storage is enabled, verify the ObjectStorageBucket and object storage secrets.

## Additional Resources

- [Paperclip Official Website](https://paperclip.ing)
- [Paperclip Documentation](https://paperclip.ing/docs)
- [Paperclip GitHub Repository](https://github.com/paperclipai/paperclip)
- [Paperclip Docker Guide](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/docker.md)
- [Paperclip template on Sealos](https://sealos.io/products/app-store/paperclip)

## License

This Sealos template provides deployment configuration for running Paperclip on Sealos. Paperclip itself is distributed under the MIT License.
