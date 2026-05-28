# Deploy and Host AFFiNE on Sealos

AFFiNE is a local-first, privacy-focused workspace for notes, documents, whiteboards, and knowledge management. This template deploys AFFiNE 0.26.6 with PostgreSQL, Redis, persistent storage, HTTPS ingress, and first-run admin setup on Sealos Cloud.

![AFFiNE Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/affine/website-screenshot.webp)

## About Hosting AFFiNE

AFFiNE runs in self-hosted all-in-one mode and serves the web UI, API, document collaboration, and background jobs from one application workload. The template also provisions managed PostgreSQL for workspace metadata and Redis for cache and job coordination, so the application can start without manual database wiring.

The deployment stores AFFiNE configuration and uploaded workspace files on persistent volumes mounted at `/root/.affine/config` and `/root/.affine/storage`. Sealos provides the public HTTPS endpoint, Kubernetes scheduling, resource controls, and Canvas-based operations for later updates.

## Common Use Cases

- **Personal knowledge base**: Keep notes, docs, and whiteboards in a self-hosted workspace.
- **Team documentation**: Manage project plans, meeting notes, and shared knowledge with persistent storage.
- **Whiteboard collaboration**: Use AFFiNE's canvas-style blocks for diagrams, brainstorming, and visual planning.
- **Privacy-focused workspace**: Host your workspace data in your own Sealos deployment instead of using a hosted SaaS account.

## Dependencies for AFFiNE Hosting

The Sealos template includes all required runtime dependencies:

- **AFFiNE application**: `ghcr.io/toeverything/affine:0.26.6`
- **PostgreSQL**: Kubeblocks-managed `postgresql-16.4.0` cluster with a dedicated `affine` database
- **Redis**: Kubeblocks-managed `redis-7.2.7` cluster for cache and background jobs
- **Persistent volumes**: Separate PVCs for AFFiNE config and uploaded storage
- **Ingress and App entry**: HTTPS public URL exposed through Sealos

### Deployment Dependencies

- [AFFiNE Official Website](https://affine.pro/) - Product overview and feature information
- [AFFiNE Self-host Documentation](https://docs.affine.pro/docs/self-host-affine) - Official self-hosting guide
- [AFFiNE GitHub Repository](https://github.com/toeverything/AFFiNE) - Source code, releases, and issue tracking
- [Sealos Documentation](https://sealos.io/docs) - Platform guides and operational documentation

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **AFFiNE StatefulSet**: Runs the self-hosted all-in-one AFFiNE server on port `3010`.
- **Migration Job**: Executes `node ./scripts/self-host-predeploy.js` before the application serves traffic.
- **PostgreSQL Cluster**: Stores account, workspace, and application metadata in the `affine` database.
- **Redis Cluster**: Provides cache and queue coordination for the AFFiNE server.
- **Service + Ingress + App**: Routes the generated HTTPS domain to the AFFiNE service.
- **Persistent Storage**: Keeps `/root/.affine/config` and `/root/.affine/storage` across restarts.

**Configuration:**

- `DATABASE_URL` is composed from the Kubeblocks PostgreSQL secret and points to the `affine` database.
- `REDIS_SERVER_HOST`, `REDIS_SERVER_USER`, and `REDIS_SERVER_PASSWORD` are wired from the Redis service and secret.
- `AFFINE_SERVER_EXTERNAL_URL` is set to the generated Sealos HTTPS URL so AFFiNE can build correct public links.
- `AFFINE_INDEXER_ENABLED=false` follows the upstream single-node self-hosting setup and avoids requiring an external search indexer.

**Resource Baseline:**

The tested minimum baseline keeps the AFFiNE app at `500m` CPU and `512Mi` memory, PostgreSQL at `500m` CPU and `512Mi` memory, and Redis at `500m` CPU and `512Mi` memory for each Redis component. A 256Mi AFFiNE app limit booted but restarted once during startup, so the template uses 512Mi for a stable cold start.

**License Information:**

AFFiNE uses a mixed license model. The repository root declares MIT for most source code, while backend Enterprise Edition portions are governed by the AFFiNE EE license and Community Edition portions by MPL-2.0. Review the upstream license files before using the software in production.

## Why Deploy AFFiNE on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and application operations. By deploying AFFiNE on Sealos, you get:

- **One-Click Deployment**: Launch AFFiNE with PostgreSQL, Redis, storage, and HTTPS routing from one template.
- **Managed Kubernetes Runtime**: Run AFFiNE on Kubernetes without hand-writing manifests or operating cluster primitives directly.
- **Persistent Data by Default**: Keep AFFiNE configuration and uploaded workspace data on PVC-backed storage.
- **Easy Customization**: Adjust resources, environment variables, and storage from Canvas resource cards or the AI dialog.
- **Instant Public Access**: Receive a generated HTTPS URL after deployment.
- **Pay-as-you-go Resources**: Start from the tested baseline and scale CPU, memory, and storage only when your workload needs it.

Deploy AFFiNE on Sealos to keep control of your workspace data while reducing infrastructure maintenance.

## Deployment Guide

1. Open the [AFFiNE template](https://sealos.io/products/app-store/affine) and click **Deploy Now**.
2. Review the generated app name and domain in the popup dialog. The default configuration is enough for a working deployment.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Open the generated AFFiNE URL from the app card.
5. On first access, AFFiNE redirects to `/admin/setup`. Create the first administrator account with your name, email, and password.
6. After setup, choose **Open AFFiNE** or go back to the generated app URL. Use the administrator email and password you created to sign in later.

## First Login and Registration

AFFiNE self-hosted mode requires an initial administrator before the workspace is usable.

1. Open your generated AFFiNE URL.
2. If the instance is new, you will be redirected to `https://<your-affine-domain>/admin/setup`.
3. Click **Continue** and create the first administrator account.
4. Use the same email and password to sign in to AFFiNE and to access the admin area at `/admin`.

Use a strong password. AFFiNE expects an 8-32 character password, and it is best to include at least two character types such as uppercase letters, lowercase letters, numbers, or symbols.

## Configuration

After deployment, you can configure AFFiNE through:

- **AFFiNE Admin Panel**: Open `/admin` on your generated domain to manage self-hosted settings.
- **Canvas AI Dialog**: Describe changes such as resource adjustments or environment updates and let AI apply them.
- **Resource Cards**: Edit the AFFiNE StatefulSet, PostgreSQL cluster, Redis cluster, Service, Ingress, or PVC resources.
- **AFFiNE UI**: Manage workspaces, members, and documents from the application itself.

SMTP and OAuth providers are not preconfigured by this template. Configure them later in AFFiNE admin settings or by adding the required environment variables according to the official documentation.

## Scaling

For most small AFFiNE workspaces, keep a single AFFiNE replica and scale vertically first:

1. Open the deployment in Canvas.
2. Select the AFFiNE StatefulSet resource card.
3. Increase CPU or memory if imports, large workspaces, or concurrent users increase load.
4. Scale PostgreSQL, Redis, and PVC capacity from their resource cards when data size grows.

Keep the application at one replica unless you have reviewed AFFiNE self-hosting behavior for multi-replica deployments.

## Troubleshooting

### Common Issues

**Issue: The application redirects to `/admin/setup`**
- Cause: The AFFiNE instance has not been initialized yet.
- Solution: Create the first administrator account from the setup page, then return to the app URL.

**Issue: The app page is not ready immediately after deployment**
- Cause: PostgreSQL, Redis, the database initialization job, and the migration job are still starting.
- Solution: Wait a few minutes and check that the AFFiNE StatefulSet, PostgreSQL cluster, Redis cluster, and migration job are healthy in Canvas.

**Issue: Email invitations or password reset emails do not send**
- Cause: SMTP is not configured by default.
- Solution: Configure SMTP settings according to the AFFiNE self-host documentation before relying on email workflows.

**Issue: The pod restarts during cold start**
- Cause: The app memory limit is too low for AFFiNE startup and background services.
- Solution: Keep the default 512Mi app memory limit or increase it from Canvas for larger workspaces.

### Getting Help

- [AFFiNE Self-host Documentation](https://docs.affine.pro/docs/self-host-affine)
- [AFFiNE GitHub Issues](https://github.com/toeverything/AFFiNE/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [AFFiNE Documentation](https://docs.affine.pro/)
- [AFFiNE Community](https://community.affine.pro/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the repository license. AFFiNE itself uses the upstream mixed license model described in its repository license files.
