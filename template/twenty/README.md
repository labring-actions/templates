# Deploy and Host Twenty on Sealos

Twenty is an open-source CRM for managing companies, people, opportunities, tasks, notes, dashboards, and workflows. This template deploys Twenty 2.22.0 with a dedicated server, background worker, PostgreSQL, Redis, automatic HTTPS, and selectable file storage on Sealos.

![Twenty application screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/twenty/website-screenshot.webp)

## About Hosting Twenty

Twenty combines a customizable CRM interface with workflow automation and extensible data models. Teams can organize customer records, track opportunities, assign tasks, and build operational workflows from one workspace.

The Sealos deployment preserves Twenty's official multi-service architecture. The server handles the web UI and APIs, the worker processes background queues, PostgreSQL stores application and workspace data, and Redis manages queues and caching.

Local file storage uses a shared 1 GiB persistent volume mounted by the server and worker on the same node. Enabling S3 provisions a private Sealos Object Storage bucket and removes the local file volume and its scheduling constraint.

## Common Use Cases

- **Sales CRM**: Track companies, contacts, opportunities, owners, and activities.
- **Customer operations**: Manage tasks, notes, timelines, and shared account context.
- **Custom data models**: Adapt objects, fields, views, and relationships to internal processes.
- **Workflow automation**: Run event-driven and scheduled workflows through the background worker.

## Dependencies for Twenty Hosting

The template provisions every required service and generates the application encryption key.

### Deployment Dependencies

- [Twenty documentation](https://docs.twenty.com/) - Product and self-hosting documentation
- [Twenty source code](https://github.com/twentyhq/twenty) - Upstream repository
- [Sealos App Store](https://sealos.io/products/app-store/twenty) - Template deployment page

### Implementation Details

**Architecture Components:**

- **Twenty server 2.22.0**: StatefulSet serving the web UI and API on port 3000.
- **Twenty worker 2.22.0**: Deployment processing queues, workflows, webhooks, and scheduled jobs.
- **PostgreSQL 16.4**: KubeBlocks-managed database with a 1 GiB data volume.
- **Redis 7.2.7**: KubeBlocks-managed Redis and sentinel components for queues and caching.
- **File storage**: Shared 1 GiB local volume by default, or a private S3-compatible bucket.
- **Ingress**: Provides the generated public domain and TLS termination.

The server waits for three successful PostgreSQL queries and an authenticated Redis ping before starting. This protects first-boot migrations from managed-service provisioning races. The worker starts after the server health endpoint is ready.

**Deployment Options:**

| Parameter | Default | Description |
| --- | --- | --- |
| `USE_S3_STORAGE` | `false` | Store files in private Sealos Object Storage instead of the shared local volume. |

The validated resource limits are 1 CPU and 2 GiB memory for the server, plus 500 millicores and 1 GiB memory for the worker. These limits cover first-run migrations and active queue processing.

**License Information:**

Twenty is primarily licensed under AGPL-3.0. Files marked with the upstream enterprise license notice use Twenty's commercial terms.

## Why Deploy Twenty on Sealos?

- **Complete service bundle**: Provision the server, worker, PostgreSQL, Redis, storage, and networking together.
- **Managed databases**: Run PostgreSQL and Redis through KubeBlocks with persistent volumes.
- **Selectable file storage**: Use a shared local volume for a compact deployment or private S3 storage for object-backed files.
- **Persistent CRM data**: Keep workspace records, configuration, and queue state across pod restarts.
- **Managed public access**: Receive a generated HTTPS URL with ingress and TLS configuration.

## Deployment Guide

1. Open the [Twenty template](https://sealos.io/products/app-store/twenty) and click **Deploy Now**.
2. Enable S3 storage when you want uploaded files stored in Sealos Object Storage, then confirm the deployment.
3. Wait for PostgreSQL, Redis, the server, and the worker to become ready. The first deployment can take several minutes while Twenty runs database migrations.
4. Open the URL shown on the application card.

## Register and Sign In

On the first visit, select **Continue with email**, enter your email address and password, and choose **Sign up**. Create the first workspace, complete your profile, and finish or skip the optional onboarding steps. The first registered user becomes the workspace owner and administrator.

Later visits use the same **Continue with email** flow. Enter the registered email address and password to sign in.

## Configuration

Configure objects, fields, views, roles, workflows, and integrations from the Twenty workspace settings. The template generates a stable encryption key for protected configuration values.

For infrastructure changes, open the deployment Canvas and use the AI dialog or resource cards. Keep the generated encryption key stable when updating an existing deployment.

## Scaling

The default template runs one server and one worker. Local file storage keeps both pods on one node so they can share the `ReadWriteOnce` volume. S3 storage removes that local-volume constraint and provides a cleaner base for future worker scaling.

## Troubleshooting

### First startup takes several minutes

Twenty runs database setup, migrations, and workspace upgrade commands before serving traffic. Check the server logs for migration progress and wait for the `/healthz` endpoint to become ready.

### The worker is waiting to start

The worker waits for the server health endpoint. Check PostgreSQL, Redis, and server readiness first.

### Getting Help

- [Twenty documentation](https://docs.twenty.com/)
- [Twenty GitHub issues](https://github.com/twentyhq/twenty/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the repository license. Twenty licensing details are available in the [upstream license file](https://github.com/twentyhq/twenty/blob/main/LICENSE).
