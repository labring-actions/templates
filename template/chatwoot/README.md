# Deploy Chatwoot on Sealos

Chatwoot is an open-source customer support platform for live chat, shared inboxes, contacts, automation, and omnichannel conversations. This template deploys Chatwoot with managed PostgreSQL and Redis, a background worker, HTTPS ingress, and a choice of persistent local attachment storage or private Sealos S3-compatible object storage.

![Chatwoot conversation with an S3-backed attachment](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/chatwoot/website-screenshot.webp)

## What This Template Deploys

- **Chatwoot `v4.16.2` Web** running the Rails application on port `3000`
- **Chatwoot `v4.16.2` Sidekiq** for background jobs
- **PostgreSQL `16.4.0` with pgvector** through KubeBlocks
- **Redis `7.2.7` with Sentinel** through KubeBlocks
- **Database initialization and migration Jobs** using `db:chatwoot_prepare`
- **Persistent local storage** for attachments by default
- **Private Sealos S3-compatible object storage** as an optional attachment backend
- **Public HTTPS** through a Sealos-managed Service and Ingress
- **Startup, readiness, and liveness probes** on `/health` and `/api`

The Rails server, Sidekiq worker, PostgreSQL, and Redis are all required by Chatwoot's production architecture. Email delivery uses an external SMTP or transactional email provider configured through Chatwoot environment variables.

## Common Use Cases

- Website live chat and customer support
- Shared inboxes for support, sales, and operations teams
- API-driven customer conversations
- Contact and conversation management
- Email, messaging, and social channel integrations
- Support automation, reports, and help centers

## Deployment

1. Open the [Chatwoot template in the Sealos App Store](https://sealos.io/products/app-store/chatwoot).
2. Keep **Enable account signup** enabled for the first deployment.
3. Choose local attachment storage or enable private Sealos S3 storage.
4. Click **Deploy** and wait for the Web and Sidekiq workloads to become ready. PostgreSQL and Redis provisioning usually takes several minutes on the first deployment.
5. Open the HTTPS address shown by Sealos.

### Deployment Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `enable_account_signup` | `true` | Enables the first-admin setup and account registration flow |
| `enable_s3_storage` | `false` | Creates a private Sealos object-storage bucket for attachments |

The template generates `SECRET_KEY_BASE` automatically and reads database, Redis, and object-storage credentials from Sealos-managed Kubernetes Secrets.

## First Administrator and Login

The template contains zero preset user credentials. Create the first administrator from the Chatwoot setup screen:

1. Open the deployed URL.
2. Enter your **Name**, **Company Name**, **Work Email**, and a strong **Password**.
3. Click **Finish Setup**.
4. Complete the profile onboarding fields such as role, website, language, timezone, industry, and company size.
5. When Chatwoot presents the sign-in page, use the same work email and password.

After the required accounts exist, set `enable_account_signup` to `false` in the deployment configuration to close public account registration. Existing users and invited agents continue signing in with their stored credentials.

Password reset, agent invitations, and email-channel delivery require a working mail provider. Configure the relevant SMTP or transactional email environment variables in Sealos Canvas before relying on these email flows.

## Verify the Installation

After signing in:

1. Open **Settings → Inboxes → Add Inbox**.
2. Choose a channel such as **Website** or **API**.
3. Name the inbox and add an agent.
4. Start a test conversation.
5. Send a reply and upload an attachment.

The public endpoint also exposes two useful checks:

- `/health` returns `{"status":"woot"}` when the Rails process is healthy.
- `/api` returns Chatwoot version and dependency status.

## Attachment Storage

### Local Persistent Storage

With `enable_s3_storage=false`, attachments use a shared `1Gi` persistent volume mounted at `/app/storage` by the Web and Sidekiq Pods. The template places both Pods on the same worker node so the ReadWriteOnce volume remains available to both processes.

Local mode fits evaluations and small single-replica deployments. Include the Chatwoot storage volume in the backup plan together with PostgreSQL.

### Private Sealos S3 Storage

With `enable_s3_storage=true`, the template creates a private `ObjectStorageBucket` and configures Chatwoot's official `s3_compatible` Active Storage service. Sealos injects the bucket, endpoint, access key, and secret key from managed Secrets. Web and Sidekiq share the same object backend, and the application workloads require no attachment PVC.

Direct anonymous object requests receive `403`. Users download attachments through Chatwoot, where the application issues an authorized object-storage request.

Sealos S3 is the recommended option for durable attachment storage, independent backups, and future application scaling.

## Persistence

| Path or service | Purpose | Provisioned when |
| --- | --- | --- |
| PostgreSQL volume | Accounts, inboxes, contacts, conversations, settings, and attachment metadata | Always |
| Redis volumes | Queues, cache, and runtime coordination | Always |
| `/app/storage` | Local Active Storage attachments | `enable_s3_storage=false` |
| Private Sealos bucket | S3-compatible Active Storage attachments | `enable_s3_storage=true` |

Back up PostgreSQL and the selected attachment backend together. Restoring only one side can leave attachment metadata without files or files without matching records.

## Resource Defaults

The application limits come from cold-start and representative workflow tests that covered administrator setup, inbox creation, a conversation, agent replies, and attachment upload/download:

| Component | CPU limit | Memory limit | CPU request | Memory request |
| --- | ---: | ---: | ---: | ---: |
| Chatwoot Web | `100m` | `1024Mi` | `10m` | `102Mi` |
| Chatwoot Sidekiq | `100m` | `1024Mi` | `10m` | `102Mi` |
| Migration Job | `100m` | `512Mi` | `10m` | `51Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis Sentinel | `500m` | `512Mi` | `50m` | `51Mi` |
| Gate and PostgreSQL initialization containers | `100m` | `128Mi` | `10m` | `12Mi` |

Increase Web and Sidekiq CPU for concurrent traffic, channel integrations, automations, bulk operations, and large teams. Watch PostgreSQL, Redis, queue latency, and object-storage traffic as usage grows.

## Scaling

The template starts one Web replica and one Sidekiq replica. A scaled deployment should use Sealos S3, keep all replicas on the same PostgreSQL and Redis services, preserve the same `SECRET_KEY_BASE`, and size workers for queue volume. PostgreSQL and Redis topology changes deserve their own backup and failover plan.

## Upgrades

Chatwoot upgrades can include database migrations. Before changing the image tag:

1. Back up PostgreSQL and attachment storage.
2. Review the target Chatwoot release notes.
3. Update both Web and Sidekiq to the same image tag.
4. Run `bundle exec rails db:chatwoot_prepare`.
5. Verify `/health`, `/api`, sign-in, conversations, background jobs, and attachments.

Deployments created from the earlier v4.7.0 template use different immutable StatefulSet storage definitions. Upgrade those installations with a side-by-side migration: back up PostgreSQL and both attachment PVCs, deploy this template under a new application name, move the database and attachments, validate the new deployment, then switch traffic. Select local storage or Sealos S3 during the new deployment; changing that storage mode also requires a data migration.

## Troubleshooting

### The application is still starting

Open the Web, Sidekiq, PostgreSQL, Redis, and migration resource cards in Sealos Canvas. The gate containers wait for the schema and Redis before Chatwoot starts. A first database provision can take several minutes.

### The first account setup page is unavailable

Deploy with `enable_account_signup=true`, then open the public Chatwoot URL again. Keep the work email and password created on that page for subsequent sign-in.

### Invitations or password reset emails do not arrive

Configure Chatwoot's mailer environment variables for an SMTP or transactional email service and restart Web and Sidekiq.

### An S3 object URL returns `403`

The bucket policy is private. Open the attachment from an authenticated Chatwoot conversation so the application can authorize the download.

### Background actions remain pending

Check Sidekiq readiness and logs, Redis health, and queue latency. Web requests can remain healthy while asynchronous jobs wait for the worker.

## Documentation

- [Chatwoot Website](https://www.chatwoot.com)
- [Self-Hosted Installation Guide](https://developers.chatwoot.com/self-hosted)
- [Production Architecture](https://developers.chatwoot.com/self-hosted/deployment/architecture)
- [Docker Deployment Guide](https://developers.chatwoot.com/self-hosted/deployment/docker)
- [Environment Variables](https://developers.chatwoot.com/self-hosted/configuration/environment-variables)
- [Supported Storage Providers](https://developers.chatwoot.com/self-hosted/deployment/storage/supported-providers)
- [Chatwoot GitHub Repository](https://github.com/chatwoot/chatwoot)
- [Sealos App Store](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

Chatwoot Community Edition is available under the [MIT License](https://github.com/chatwoot/chatwoot/blob/v4.16.2/LICENSE). Review Chatwoot's repository and product terms for features distributed with other licensing conditions. This repository provides the Sealos deployment template and leaves the Chatwoot license unchanged.
