# Deploy and Host Plane on Sealos

Plane is an open-source project management platform for tracking issues, cycles, modules, pages, and product roadmaps. This template deploys Plane as a multi-service application with managed PostgreSQL, managed Redis, and object storage integration on Sealos Cloud.

![Plane Logo](logo.png)

## About Hosting Plane

Plane helps software, product, and operations teams manage work in one place. It combines issue tracking, sprint-style planning, modules, pages, and workspace-level collaboration in a self-hosted deployment that can be exposed securely over HTTPS.

This Sealos template provisions the Plane web app, API, background workers, admin app, and spaces app on a shared public domain with path-based routing. It also creates a KubeBlocks-managed PostgreSQL cluster for relational data, a KubeBlocks-managed Redis cluster for queueing and coordination, and a private object storage bucket for uploaded assets.

The deployment includes database initialization and migration jobs before the main application services start serving traffic. After deployment, you can continue day-2 operations from Canvas through AI dialog and resource cards.

## Common Use Cases

- **Issue and Sprint Tracking**: Manage bugs, features, backlogs, and delivery cycles for engineering teams.
- **Product Roadmapping**: Organize epics, modules, and roadmap planning across releases.
- **Cross-Functional Project Management**: Coordinate work between product, design, engineering, and operations.
- **Team Knowledge and Specs**: Use Plane pages and spaces to keep planning notes and internal documentation close to execution.
- **Self-Hosted Work Management**: Run a private project management stack with your own infrastructure and data controls.

## Dependencies for Plane Hosting

The Sealos template includes all required dependencies for a production-ready Plane deployment:

- Plane application services (`web`, `api`, `worker`, `beat-worker`, `admin`, and `space`)
- KubeBlocks-managed PostgreSQL cluster for Plane application data
- KubeBlocks-managed Redis cluster with Sentinel for queueing and coordination
- Sealos ObjectStorage bucket and credentials for file uploads
- Kubernetes Jobs for database initialization and migrations
- Kubernetes Services and Ingress resources for internal routing and public HTTPS access

### Deployment Dependencies

- [Plane Official Website](https://plane.so/) - Product overview and hosted offering
- [Plane Documentation](https://docs.plane.so/) - Official user and admin documentation
- [Plane GitHub Repository](https://github.com/makeplane/plane) - Source code, releases, and issue tracking
- [Sealos Documentation](https://sealos.io/docs) - Platform usage and operations

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Plane Web** (`makeplane/plane-frontend:v0.22-dev`): Main user-facing web application served at `/`
- **Plane API** (`makeplane/plane-backend:v0.22-dev`): Backend API and auth service exposed at `/api` and `/auth`
- **Plane Worker** (`makeplane/plane-backend:v0.22-dev`): Background job worker for asynchronous processing
- **Plane Beat Worker** (`makeplane/plane-backend:v0.22-dev`): Scheduler service for recurring background tasks
- **Plane Admin** (`makeplane/plane-admin:v0.22-dev`): Instance administration UI exposed at `/god-mode`
- **Plane Space** (`makeplane/plane-space:v0.22-dev`): Space-specific frontend exposed at `/spaces`
- **PostgreSQL Cluster**: KubeBlocks-managed PostgreSQL for persistent Plane data
- **Redis Cluster + Sentinel**: Queue, cache, and service coordination layer
- **Object Storage Bucket**: Private bucket for uploaded files and asset storage
- **Initialization Jobs**: One job creates the `plane` database and another runs backend migrations

**Configuration:**

- Public entrypoint:
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- Path routing:
  - `/` routes to Plane Web
  - `/api` and `/auth` route to Plane API
  - `/spaces` routes to Plane Space
  - `/god-mode` routes to Plane Admin
- The template injects PostgreSQL, Redis, and object storage credentials through Kubernetes secrets.
- File uploads are configured with a default `FILE_SIZE_LIMIT` of `5242880` bytes.
- All core application components start as single replicas by default.

**License Information:**

Plane is licensed under the [GNU Affero General Public License v3.0](https://github.com/makeplane/plane/blob/preview/LICENSE.txt).

## Why Deploy Plane on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies deployment and day-2 operations. By deploying Plane on Sealos, you get:

- **One-Click Deployment**: Launch the full Plane stack without manually wiring PostgreSQL, Redis, object storage, ingress, and background workers.
- **Kubernetes-Native Reliability**: Run Plane on managed Kubernetes primitives with service discovery and HTTPS ingress already in place.
- **Managed Data Services**: Use KubeBlocks PostgreSQL and Redis resources instead of operating those dependencies yourself.
- **Easy Day-2 Operations**: Change resources and settings from Canvas using AI dialog or resource cards.
- **Persistent Storage Included**: Keep database data, Redis state, and uploaded files durable across restarts.
- **Instant Public Access**: Get a public URL with TLS handled by the platform.
- **Cost Efficiency**: Use pay-as-you-go cloud resources and scale infrastructure as your workspace grows.

Deploy Plane on Sealos and focus on planning and shipping work instead of managing infrastructure.

## Deployment Guide

1. Open the [Plane template](https://sealos.io/products/app-store/plane) and click **Deploy Now**.
2. Configure the deployment parameters in the popup dialog:
   - `app_host`: Public hostname prefix for your Plane URL
   - `app_name`: Resource prefix used for Kubernetes objects
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Access Plane using the generated public URL:
   - **Main Workspace UI**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/`
   - **Spaces UI**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/spaces`
   - **Admin UI**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/god-mode`
   - **API Base**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/api`
5. Complete the initial Plane setup in the web UI and create your first workspace account if this is a fresh deployment.

## Configuration

After deployment, you can configure Plane through:

- **AI Dialog**: Describe the changes you want and let AI apply updates.
- **Resource Cards**: Modify deployments, services, ingress, database, Redis, or storage resources directly from Canvas.
- **Plane Admin UI**: Manage instance-level settings from the `/god-mode` path.

### Template Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `app_host` | Public hostname prefix used to generate the Plane URL | `plane-<random>` |
| `app_name` | Kubernetes resource name prefix for this deployment | `plane-<random>` |

### Operational Notes

- Keep the shared public domain paths intact unless you also update the related application base URL settings.
- Plane background processing depends on both Redis and the `worker` / `beat-worker` deployments staying healthy.
- Uploaded files depend on the provisioned object storage bucket and injected access credentials.

## Scaling

To scale Plane resources on Sealos:

1. Open the deployment in Canvas.
2. Click the resource card you want to adjust.
3. Update CPU, memory, storage, or replica settings as needed.
4. Apply the changes and monitor rollout status.

For most deployments, scale `api`, `worker`, PostgreSQL, and Redis resources before changing less critical frontend components. Keep `beat-worker` as a single replica unless you have validated a different scheduling strategy for your Plane version.

## Troubleshooting

### Common Issues

**Issue: The Plane URL is not reachable immediately after deployment**
- Cause: Ingress provisioning or DNS propagation is still completing.
- Solution: Wait a few minutes, then reopen the public URL from Canvas.

**Issue: Background jobs or notifications are delayed**
- Cause: Redis is not ready, or the `worker` / `beat-worker` deployment is unhealthy.
- Solution: Check Redis cluster status and review logs for the background worker deployments.

**Issue: File uploads fail**
- Cause: Object storage credentials, bucket wiring, or endpoint settings are not available to the backend.
- Solution: Verify the object storage secrets and confirm the API deployment has the expected S3-related environment variables.

**Issue: The application starts but initialization is incomplete**
- Cause: PostgreSQL initialization or migration jobs did not finish successfully.
- Solution: Review the database init job and API migration job logs, then confirm the PostgreSQL cluster is healthy.

### Getting Help

- [Plane Documentation](https://docs.plane.so/)
- [Plane GitHub Issues](https://github.com/makeplane/plane/issues)
- [Plane GitHub Discussions](https://github.com/makeplane/plane/discussions)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Plane Product Documentation](https://docs.plane.so/)
- [Plane Releases](https://github.com/makeplane/plane/releases)
- [Plane Self-Hosting Repository](https://github.com/makeplane/plane)

## License

This Sealos template follows the license policy of the templates repository. Plane itself is licensed under the [GNU Affero General Public License v3.0](https://github.com/makeplane/plane/blob/preview/LICENSE.txt).
