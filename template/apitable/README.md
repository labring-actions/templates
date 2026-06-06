# Deploy and Host APITable on Sealos

APITable is an open-source, API-oriented spreadsheet and collaborative database platform for building no-code data apps. This template deploys APITable as a multi-service stack on Sealos with MySQL, Redis, RabbitMQ, and S3-compatible object storage.

![APITable Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/apitable/website-screenshot.webp)

## About Hosting APITable

APITable combines a spreadsheet-style interface with real-time collaboration, forms, permissions, cross-table relationships, and API access. It is useful when teams need a self-hosted Airtable-style workspace with an open-source backend.

This Sealos template follows APITable's official Docker Compose service layout while replacing local containers for MySQL, Redis, and object storage with managed Sealos resources. The deployment includes automatic public HTTPS access, service discovery, persistent database storage, and optional external S3-compatible storage.

APITable performs database initialization and template data import during the first cold start. The application URL can take several minutes to become ready while MySQL, Redis, RabbitMQ, migrations, and application services start.

## Common Use Cases

- **Collaborative Databases**: Manage structured business data with spreadsheet-like editing and real-time updates.
- **Internal Tools**: Build lightweight operational apps with tables, forms, views, permissions, and APIs.
- **Data Collection**: Publish forms and collect responses into structured workspaces.
- **API-First Workflows**: Connect APITable data to scripts, widgets, integrations, and automation systems.
- **Self-Hosted Airtable Alternative**: Run an open-source collaborative database stack under your own infrastructure boundary.

## Dependencies for APITable Hosting

The Sealos template includes all required runtime dependencies for the community deployment:

- APITable web server, backend server, room server, databus server, image proxy, and gateway
- KubeBlocks MySQL for the APITable relational database
- KubeBlocks Redis for cache and real-time coordination
- RabbitMQ for APITable queue workloads
- Sealos ObjectStorageBucket by default, with an option to use an external S3-compatible bucket

### Deployment Dependencies

- [APITable GitHub Repository](https://github.com/apitable/apitable) - Source code and official Docker Compose deployment files
- [AITable Official Website](https://aitable.ai) - Product website and hosted service
- [Developer Center](https://developers.aitable.ai/) - API, widget, and scripting documentation
- [REST API Docs](https://developers.aitable.ai/api/introduction/) - APITable API reference
- [GitHub Installation Guide](https://github.com/apitable/apitable#installation) - Official self-hosted installation notes

## Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Gateway**: Nginx-based HTTP gateway that preserves APITable's official path routing for web, API, room, notification, document, and asset endpoints.
- **Web Server**: Serves the APITable frontend and static assets.
- **Backend Server**: Runs APITable's Java API service, authentication, workspace APIs, and object storage integration.
- **Room Server**: Runs real-time collaboration, socket, fusion, notification, and document channels.
- **Databus Server**: Provides APITable's databus API service.
- **Image Proxy**: Proxies and transforms asset images backed by S3-compatible storage.
- **MySQL**: KubeBlocks-managed MySQL stores APITable data and migration state.
- **Redis**: KubeBlocks-managed Redis handles cache and real-time coordination.
- **RabbitMQ**: Queue service used by APITable room and backend workflows.
- **Object Storage**: Stores attachments and image assets using Sealos ObjectStorageBucket or an external S3-compatible bucket.

**Configuration:**

- The default storage provider creates a private Sealos ObjectStorageBucket.
- Select `external-s3` when you already have an S3-compatible bucket and want APITable to use that endpoint.
- Registration is enabled for the community deployment with password-based first-account creation.
- Email and SMS delivery are disabled by default, so use the built-in registration/login flow with an email address and password.
- APITable's upstream documentation recommends a host with 4 CPUs and 8 GB RAM for the Docker deployment. This template starts with smaller component-level resources and can be scaled from the Sealos Canvas if your workload grows.

**License Information:**

APITable is licensed under the GNU Affero General Public License v3.0. This Sealos template is provided under the same repository license terms as the Sealos templates project.

## Why Deploy APITable on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, database provisioning, storage, networking, and day-two operations. By deploying APITable on Sealos, you get:

- **One-Click Deployment**: Deploy the full APITable stack without manually writing Kubernetes manifests.
- **Managed Databases**: Provision MySQL and Redis through KubeBlocks with persistent storage.
- **Built-In Object Storage**: Use a private S3-compatible bucket for uploads and attachments.
- **Instant HTTPS Access**: Each deployment receives a public URL with automatic TLS.
- **Canvas Operations**: Adjust resources, inspect logs, and update environment variables from the Sealos Canvas.
- **Pay-as-You-Go Resources**: Start with a smaller profile and scale individual services when real usage requires it.

Deploy APITable on Sealos and focus on data workflows instead of managing the platform plumbing.

## Deployment Guide

1. Open the [APITable template](https://sealos.io/products/app-store/apitable) and click **Deploy Now**.
2. Choose the storage provider:
   - `sealos-objectstorage`: create and use a private Sealos ObjectStorageBucket.
   - `external-s3`: provide an existing S3-compatible endpoint, public endpoint, access key, secret key, bucket, and region.
3. Click **Deploy** and wait for the stack to initialize. The Canvas appears after deployment starts; APITable cold start and database imports can take several minutes.
4. Open the generated APITable URL.
5. Create the first account from the login or registration page with an email address and password.
6. Sign in with that account, then create or open a workspace from the APITable workbench.

## Configuration

After deployment, configure APITable through:

- **APITable UI**: Manage workspaces, datasheets, forms, permissions, and API tokens from the web interface.
- **Sealos Canvas**: Open resource cards to inspect logs, edit environment variables, or adjust service resources.
- **AI Dialog**: Describe operational changes in the Canvas dialog and let Sealos apply supported updates.
- **Object Storage Inputs**: Redeploy with `external-s3` when you need APITable assets stored in an existing bucket.

## Scaling

APITable runs multiple services, so scale the component that matches your bottleneck:

1. Open the Canvas for your APITable deployment.
2. Inspect backend-server, room-server, MySQL, Redis, and RabbitMQ metrics and logs.
3. Increase CPU or memory for backend-server when API requests are slow.
4. Increase room-server resources when collaboration sessions, websocket traffic, or fusion API usage grow.
5. Increase MySQL storage before large attachment metadata or datasheet workloads fill the database volume.

## Troubleshooting

**First start takes several minutes**

APITable runs database creation, schema migration, and application data import during cold start. Wait until MySQL, Redis, RabbitMQ, init-db, init-appdata, backend-server, room-server, web-server, databus-server, imageproxy-server, and gateway are healthy.

**Login page loads but registration fails**

Check backend-server logs first. Failed database migration, object storage credentials, or RabbitMQ connection errors usually surface there.

**Uploads or images fail**

Verify the selected S3 provider. For `external-s3`, confirm the endpoint, public endpoint, access key, secret key, bucket, and region are valid and reachable by APITable.

### Getting Help

- [APITable GitHub Issues](https://github.com/apitable/apitable/issues)
- [Developer Center](https://developers.aitable.ai/)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [AITable Official Website](https://aitable.ai)
- [APITable GitHub Repository](https://github.com/apitable/apitable)
- [REST API Docs](https://developers.aitable.ai/api/introduction/)
- [Widget SDK](https://developers.aitable.ai/widget/introduction/)
- [Scripting Widget](https://developers.aitable.ai/script/introduction/)

## License

This Sealos template is provided under the Sealos templates project license. APITable itself is licensed under the GNU Affero General Public License v3.0.
