# Deploy and Host APITable on Sealos

APITable is an open-source, API-oriented spreadsheet and collaborative database platform for building data apps. This template deploys the APITable Community Edition service topology with managed MySQL, managed Redis, RabbitMQ, and optional private S3-compatible storage.

![APITable Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/apitable/website-screenshot.webp)

## About Hosting APITable

APITable combines datasheets, forms, real-time collaboration, permissions, cross-table relationships, and APIs in a self-hosted workspace. The template follows the official `v1.13.0-beta.1` Docker Compose topology and pins every application image to a concrete version or digest.

A fresh deployment runs database creation, schema migration, and template-data import before the web application becomes ready. The complete cold start usually takes several minutes.

## What Gets Deployed

| Component | Purpose | Default limit |
| --- | --- | --- |
| Backend Server | Authentication, workspace APIs, and storage integration | 1 CPU / 1 GiB |
| Room Server | Real-time collaboration and document channels | 1 CPU / 1 GiB |
| Web Server | Frontend and static assets | 200m / 256 MiB |
| Databus Server | Databus API | 200m / 256 MiB |
| Gateway | Public HTTPS routing | 100m / 128 MiB |
| Image Proxy | Image retrieval and transformation | 100m / 128 MiB |
| MySQL | Relational application data | 500m / 512 MiB, 1 GiB volume |
| Redis | Cache and coordination | 500m / 512 MiB, 1 GiB volume |
| RabbitMQ | Queue workloads | 500m / 512 MiB, 1 GiB volume |

CPU and memory requests are set to 10% of each limit so the deployment can start economically while retaining the runtime headroom required by APITable.

## Storage Modes

The `enable_s3_storage` input controls attachment and image storage.

| Value | Behavior |
| --- | --- |
| `true` (default) | Creates a private Sealos `ObjectStorageBucket` and injects its generated S3 credentials into APITable. |
| `false` | Runs the collaboration and database stack with object-backed attachments, images, and uploads disabled. |

The managed bucket uses a private policy. APITable generates authorized asset requests while anonymous object reads receive HTTP 403.

## Account and Access

The generated application URL opens the APITable login page. Community registration accepts an email address and password; email and SMS delivery are disabled in this template. Each fresh deployment allows public password registration, so apply your network or registration policy after creating the intended administrator accounts.

## Deployment Guide

1. Open the [APITable template](https://sealos.io/products/app-store/apitable) and select **Deploy Now**.
2. Keep `enable_s3_storage=true` for attachments and images, or select `false` for a database-only workspace.
3. Start the deployment and wait for MySQL, Redis, RabbitMQ, the initialization jobs, and all six APITable services to become ready.
4. Open the generated HTTPS URL and register with an email address and password.
5. Sign in, create a workspace, and create the first datasheet.

## Configuration

- **APITable UI**: Manage workspaces, datasheets, forms, permissions, and API tokens.
- **Sealos Canvas**: Inspect logs, resource metrics, services, databases, and persistent volumes.
- **Object storage**: Redeploy with `enable_s3_storage=true` when attachment and image workflows are required.
- **Application registration**: Adjust the APITable registration settings after administrator bootstrap when your environment requires restricted enrollment.

## Scaling

Scale the component that matches the observed bottleneck. Backend API workloads primarily affect Backend Server and MySQL. Collaboration sessions primarily affect Room Server, Redis, and RabbitMQ. Attachment traffic primarily affects Backend Server, Image Proxy, and object storage.

The validated startup floor keeps Backend Server and Room Server at 1 GiB. A 512 MiB Room Server cold start was OOM-killed with exit code 137, while the 1 GiB profile reached readiness with zero restarts.

## Validated Runtime

The template was deployed through the Sealos Template API in both storage modes. Both branches reached full readiness with zero restarts. Fresh users completed registration, password sign-in, authenticated profile reads, workspace creation, and datasheet creation. MySQL persisted the created workspace and datasheet rows.

The managed-S3 branch also completed a known-byte upload, authenticated download, pre-signed download, SHA-256 comparison, anonymous-access check, and object deletion.

## Troubleshooting

### The login page is still starting

Check the initialization jobs and wait for MySQL, Redis, RabbitMQ, Backend Server, Room Server, Web Server, Databus Server, Image Proxy, and Gateway to become ready.

### Registration or workspace creation fails

Inspect Backend Server logs, then verify the MySQL credential Secret, RabbitMQ readiness, and Redis endpoints.

### Attachments or images fail

Confirm that `enable_s3_storage` was enabled and that the `ObjectStorageBucket` plus generated `object-storage-key` Secrets are present.

## Resources

- [AITable Official Website](https://aitable.ai/)
- [APITable GitHub Repository](https://github.com/apitable/apitable)
- [Official Docker Compose](https://github.com/apitable/apitable/blob/v1.13.0-beta.1/docker-compose.yaml)
- [Developer Center](https://developers.aitable.ai/)
- [Sealos Documentation](https://sealos.io/docs)

## License

APITable is licensed under the GNU Affero General Public License v3.0. This template follows the Sealos templates repository license.
