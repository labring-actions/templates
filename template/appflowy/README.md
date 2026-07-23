# Deploy and Host AppFlowy on Sealos

AppFlowy is an open-source collaborative workspace for documents, databases, boards, and real-time team collaboration. This template deploys AppFlowy Cloud 0.16.5, Admin Frontend 0.16.5, AppFlowy Web 0.15.5, AppFlowy Search 0.16.3, and their managed dependencies on Sealos.

![AppFlowy workspace](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/appflowy/website-screenshot.webp)

## About Hosting AppFlowy

AppFlowy provides a Notion-style workspace with pages, rich text editing, team workspaces, and structured knowledge management. The hosted Web client connects to AppFlowy Cloud for workspace data, authentication, collaboration APIs, WebSocket sync, and background import/export jobs.

PostgreSQL is provisioned through KubeBlocks with pgvector enabled, and Redis is provisioned through KubeBlocks for cache and background job coordination. File storage uses a managed Sealos Object Storage bucket through a private S3 compatibility proxy.

The runtime includes Web, Admin Frontend, Cloud, Worker, Search, GoTrue, PostgreSQL, Redis, and S3-compatible object storage. Sealos creates separate Canvas entries for the workspace UI and the system administration console while routing both through the same main application hostname. The optional AppFlowy AI service remains outside this deployment footprint.

## Common Use Cases

- **Team knowledge base**: Create shared documents, project notes, and internal manuals.
- **Personal productivity workspace**: Run a private workspace for notes, tasks, and planning.
- **Self-hosted collaboration**: Keep workspace data in your own Sealos environment.
- **Database-backed project tracking**: Organize tasks, content, and structured records in AppFlowy databases.
- **Lightweight workspace alternative**: Deploy an open-source alternative to hosted workspace products.

## Dependencies for AppFlowy Hosting

The Sealos template includes all required runtime dependencies:

- AppFlowy Web client
- AppFlowy Admin Frontend for system administration
- AppFlowy Cloud API and WebSocket service
- AppFlowy Worker for background jobs
- AppFlowy Search for keyword indexing and search queries
- GoTrue authentication service
- KubeBlocks PostgreSQL with pgvector enabled
- KubeBlocks Redis
- Managed Sealos Object Storage with a private compatibility proxy

### Deployment Dependencies

- [AppFlowy GitHub repository](https://github.com/AppFlowy-IO/AppFlowy) - Main AppFlowy project
- [AppFlowy Cloud repository](https://github.com/AppFlowy-IO/AppFlowy-Cloud) - Self-hosted cloud backend
- [AppFlowy documentation](https://docs.appflowy.io/) - Product and self-hosting documentation
- [Sealos App Store](https://sealos.io/products/app-store) - One-click application deployment

## Implementation Details

### Architecture Components

This template deploys the following services:

- **AppFlowy Web**: Browser UI exposed at the main application URL.
- **AppFlowy Admin Frontend**: System administration UI exposed at `/console/login` on the main application host.
- **AppFlowy Cloud**: API and WebSocket backend for workspaces, documents, collaboration, and file metadata.
- **AppFlowy Worker**: Background service for asynchronous jobs such as imports and file-related tasks.
- **AppFlowy Search**: Persistent keyword index and query service.
- **GoTrue**: Email/password authentication service used by AppFlowy.
- **PostgreSQL**: KubeBlocks database with pgvector support.
- **Redis**: KubeBlocks cache and background coordination service.
- **Object Storage**: S3-compatible storage backed by a managed Sealos bucket and private OpenResty proxy.

### Public URLs and Routing

Sealos creates two Canvas App entries. The main hostname uses path-based Ingress routing, so several Ingress resources can share one public domain and forward each path to its matching service.

| Entry or route | URL pattern | Purpose |
| --- | --- | --- |
| AppFlowy | `https://<app-host>/` | Workspace registration, login, and the Web application |
| AppFlowy Admin | `https://<app-host>/console/login` | System administration console |
| Cloud API | `https://<app-host>/api` | AppFlowy Web and Admin API requests |
| WebSocket | `wss://<app-host>/ws` | Real-time document and workspace synchronization |
| GoTrue | `https://<auth-host>/` | Authentication API used by AppFlowy Web and Admin |

The exact `/api/admin/health/postgresql` route is a compatibility endpoint used by the Admin health page. It forwards the request to AppFlowy Cloud's PostgreSQL health handler.

### Configuration

The AppFlowy Web client receives the public application, authentication, and WebSocket URLs at startup. The Admin Frontend receives the public application URL and the internal GoTrue service URL, then serves its login shell while Cloud and GoTrue complete their independent startup.

The Cloud, Worker, and Search services use internal Kubernetes service discovery for PostgreSQL, Redis, and GoTrue. Their init containers wait for the required data services and migration state before launching application processes. The Redis endpoint is wired to the KubeBlocks Redis data service generated by this template.

Backend S3 traffic passes through a pinned private OpenResty compatibility proxy while browser-facing presigned URLs use the public HTTPS endpoint. The proxy adds the required `Content-MD5` header to multi-object cleanup requests before forwarding them to Sealos Object Storage. Search uses the existing managed bucket with bucket creation disabled and runs real-time keyword workers; the optional background indexing pass stays disabled in the minimum resource profile.

AppFlowy Cloud exposes `/api/ready` for startup, liveness, and readiness checks. GoTrue remains a separate authentication API with a public client endpoint and an internal service endpoint.

### Resource Profile

The template was live-tested and tuned to the following minimal resource profile:

| Component | CPU limit | Memory limit | Storage |
| --- | ---: | ---: | ---: |
| AppFlowy Web | 100m | 256Mi | - |
| AppFlowy Admin | 100m | 128Mi | - |
| GoTrue | 100m | 128Mi | - |
| AppFlowy Cloud | 100m | 256Mi | - |
| AppFlowy Worker | 100m | 128Mi | - |
| AppFlowy Search | 100m | 128Mi | 1Gi |
| PostgreSQL | 500m | 512Mi | 1Gi |
| Redis data node | 500m | 512Mi | 1Gi |
| Redis Sentinel | 500m | 512Mi | 1Gi |
| Sealos S3 compatibility proxy | 100m | 128Mi | - |

Live workspace registration, administrator login, user search, server health checks, page creation, editing, search, authenticated object upload/read/delete, and clean 60-second stability windows selected these minimum tiers. Web and Cloud both reached the 128Mi ceiling and use the 256Mi tier. For larger teams, increase AppFlowy Cloud memory first, then scale PostgreSQL and Redis according to workspace size and traffic.

### License Information

AppFlowy and AppFlowy Cloud are licensed under the GNU Affero General Public License v3.0. This Sealos template only packages the deployment configuration.

## Why Deploy AppFlowy on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying AppFlowy on Sealos, you get:

- **One-click deployment**: Deploy the full multi-service AppFlowy stack from the App Store.
- **Managed dependencies**: PostgreSQL, Redis, public ingress, TLS, and object storage are provisioned together.
- **Persistent storage**: Database and object storage data survive application restarts.
- **Public HTTPS access**: Sealos provides public URLs and TLS certificates automatically.
- **Simple customization**: Configure administrator credentials through the deployment form, then adjust resources through the Canvas AI dialog or resource cards.
- **Kubernetes-native operations**: Adjust resources, inspect logs, and manage services without writing Kubernetes manifests manually.
- **Pay-as-you-go resources**: Start with the template defaults and increase capacity as workspace demand grows.

## Deployment Guide

1. Open the [AppFlowy template](https://sealos.io/products/app-store/appflowy) and click **Deploy Now**.
2. Configure the required parameters:
   - **GoTrue admin email**: the system administrator email used by AppFlowy Admin.
   - **GoTrue admin password**: the system administrator password used by AppFlowy Admin. Save this value because it is not generated for you.
3. Click **Deploy** and wait 2-3 minutes for the App, Search, PostgreSQL, Redis, object storage, and public routes to become ready. Sealos then opens the Canvas.
4. Choose the Canvas entry that matches your task:
   - **AppFlowy** opens the workspace Web application.
   - **AppFlowy Admin** opens the system administration console at `/console/login`.
5. Register a workspace user from the AppFlowy Web login page, or sign in to AppFlowy Admin with the credentials entered in step 2.

## Login and Registration

AppFlowy uses two account flows with separate entry points:

| Purpose | Entry | Credentials |
| --- | --- | --- |
| Create and use workspaces | **AppFlowy** at `https://<app-host>/` | A workspace account registered through AppFlowy Web |
| Manage users and inspect services | **AppFlowy Admin** at `https://<app-host>/console/login` | `gotrue_admin_email` and `gotrue_admin_password` from deployment |

### Workspace Users

Existing users sign in from the AppFlowy Web login page with their workspace email and password. New users select password registration from the login page; the route is `/login?action=signUpPassword`. GoTrue email auto-confirmation is enabled, and AppFlowy Cloud creates the user profile and default workspace before opening `/app`.

### System Administrator

The `gotrue_admin_email` and `gotrue_admin_password` values bootstrap the system administrator account. Use these credentials on the **AppFlowy Admin** login page to manage users, invitations, service health, SAML SSO, AI settings, and environment information. Create a workspace account through AppFlowy Web registration for normal document and workspace access.

The separate GoTrue public hostname is an authentication API endpoint consumed by AppFlowy clients. The **AppFlowy Admin** Canvas entry provides the browser-based administration interface.

## Configuration

| Parameter | Default | Required | Description |
| --- | --- | --- | --- |
| `gotrue_admin_email` | User supplied | Yes | System administrator email for the AppFlowy Admin login page. Use Web registration for workspace users. |
| `gotrue_admin_password` | User supplied | Yes | System administrator password for the AppFlowy Admin login page. Set and save this during deployment. |

After deployment, use the Canvas AI dialog to describe configuration changes or open the relevant resource cards to adjust environment variables and resources. The AppFlowy Admin health page reports PostgreSQL, Redis, S3, Search, GoTrue, AI embedding, and mailer status. AI embedding and mailer checks become healthy after their OpenAI and SMTP settings are configured.

## Scaling

To scale AppFlowy after deployment:

1. Open the Canvas for your AppFlowy deployment.
2. Click the AppFlowy Cloud, Web, Worker, PostgreSQL, or Redis resource card.
3. Increase CPU, memory, or storage according to workload needs.
4. Apply the changes and wait for the affected pods to restart.

For most installations, increase AppFlowy Cloud and PostgreSQL resources before increasing the Web client resources.

## Troubleshooting

### Unsure which URL to open

- Open the **AppFlowy** Canvas entry for workspace registration, login, documents, and databases.
- Open the **AppFlowy Admin** Canvas entry for user administration and service health.
- The `/`, `/console`, `/api`, and authentication routes use separate Ingress resources so each path reaches the correct service.

### Admin page returns 404 during initial deployment

- Open the exact **AppFlowy Admin** URL ending in `/console/login`.
- Check that the AppFlowy Admin Deployment and public route are Ready in Canvas.
- The template starts the Admin login shell immediately; initial public route propagation can still take a few seconds.

### Cannot sign in to AppFlowy Admin

- Use the `gotrue_admin_email` and `gotrue_admin_password` values entered during deployment.
- Check the GoTrue and AppFlowy Cloud resource cards in Canvas.

### Cannot register or sign in to a workspace

- Create a workspace user from the Web login page or `/login?action=signUpPassword`; AppFlowy Cloud initializes the profile and default workspace during this flow.
- Check GoTrue `/health` when authentication service readiness needs inspection.

### AppFlowy loads but workspace actions fail

- Check AppFlowy Cloud readiness at `/api/ready` on the main application URL.
- Inspect AppFlowy Cloud logs from the Sealos Canvas.
- Verify that the PostgreSQL and Redis resource cards are running.

### File uploads or imports fail

- Verify that the Sealos bucket resource, shared object-storage credentials, and bucket-name Secret are ready.
- Verify that the private S3 compatibility proxy is Ready.
- Confirm that Cloud, Worker, and Search reference the shared object-storage Secret plus the bucket-name Secret created for this deployment.

## Additional Resources

- [AppFlowy website](https://www.appflowy.com/)
- [AppFlowy GitHub](https://github.com/AppFlowy-IO/AppFlowy)
- [AppFlowy Cloud GitHub](https://github.com/AppFlowy-IO/AppFlowy-Cloud)
- [AppFlowy documentation](https://docs.appflowy.io/)
- [Sealos documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the same repository license as the templates project. AppFlowy and AppFlowy Cloud are licensed under the GNU Affero General Public License v3.0.
