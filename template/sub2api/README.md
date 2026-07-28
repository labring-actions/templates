# Deploy and Host Sub2API on Sealos

Sub2API is a self-hosted AI API gateway for managing upstream accounts, API keys, quotas, routing, and usage. This template deploys Sub2API with PostgreSQL, Redis, persistent storage, public HTTPS access, and optional private S3-compatible storage on Sealos Cloud.

![Sub2API dashboard](website-screenshot.webp)

## About Hosting Sub2API

Sub2API provides one control plane for connecting AI service subscriptions and exposing managed API access to users or internal applications. Administrators can operate upstream accounts, groups, subscriptions, billing policies, API keys, usage records, and service health from the web console.

The template provisions the full runtime stack. PostgreSQL stores application data, Redis provides cache and coordination services, and a persistent volume stores `/app/data`. A dependency gate starts Sub2API after both data services accept connections, while Sealos supplies the public domain and TLS certificate.

Sub2API also documents S3-compatible storage for asynchronous image task results. Enabling the storage option creates a private Sealos object-storage bucket and injects its managed endpoint and credentials directly into the application.

## Common Use Cases

- **Unified AI Gateway**: Route supported AI clients through one managed endpoint.
- **Account and Quota Operations**: Pool upstream accounts and distribute capacity across users or groups.
- **API Key Management**: Issue keys, control access, and review usage from one console.
- **Subscription Operations**: Manage plans, balances, redemption codes, and billing policies.
- **Async Image Workflows**: Store generated image results in a private S3-compatible bucket.

## Dependencies for Sub2API Hosting

The template includes Sub2API `0.1.166`, PostgreSQL `16.4.0`, Redis `7.2.7`, persistent volumes, HTTPS ingress, and an optional Sealos object-storage bucket.

### Deployment Dependencies

- [Sub2API repository](https://github.com/Wei-Shaw/sub2api) - Source code and upstream documentation
- [Sub2API v0.1.166 release](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.166) - Container version used by this template
- [Asynchronous image task documentation](https://github.com/Wei-Shaw/sub2api/blob/v0.1.166/docs/ASYNC_IMAGE_TASKS.md) - S3-compatible image result storage
- [PostgreSQL documentation](https://www.postgresql.org/docs/) - Database reference
- [Redis documentation](https://redis.io/docs/latest/) - Redis reference
- [Sealos documentation](https://sealos.io/docs) - Platform documentation

## Implementation Details

### Architecture Components

- **Sub2API**: One `StatefulSet` replica running `weishaw/sub2api:0.1.166` on port `8080`.
- **Dependency gate**: A resource-capped init container waits for live PostgreSQL and Redis endpoints.
- **Application storage**: A `1Gi` persistent volume mounted at `/app/data`.
- **PostgreSQL**: One KubeBlocks PostgreSQL `16.4.0` component with `1Gi` persistent storage.
- **Database initialization**: An idempotent Job creates the `sub2api` database after PostgreSQL becomes available.
- **Redis**: A KubeBlocks Redis `7.2.7` replication topology with one Redis component and one Sentinel component, each with persistent storage.
- **Object storage**: An optional private `ObjectStorageBucket` for asynchronous image task results.
- **Public access**: A Sealos-managed HTTPS Ingress and Canvas application entry.

### Resource Profile

| Component | Replicas | CPU limit | Memory limit | Storage |
| --- | ---: | ---: | ---: | ---: |
| Sub2API | 1 | `100m` | `128Mi` | `1Gi` |
| Dependency gate | 1 per start | `100m` | `128Mi` | - |
| PostgreSQL init Job | 1 per deployment | `100m` | `128Mi` | - |
| PostgreSQL | 1 | `500m` | `512Mi` | `1Gi` |
| Redis | 1 | `500m` | `512Mi` | `1Gi` |
| Redis Sentinel | 1 | `500m` | `512Mi` | `1Gi` |

### Template Inputs

| Input | Required | Purpose |
| --- | --- | --- |
| `admin_email` | Yes | Initial administrator email |
| `admin_password` | Yes | Initial administrator password, minimum 8 characters |
| `enable_s3_storage` | No | Creates and connects a private Sealos bucket for async image results |
| `timezone` | No | Application timezone, default `Asia/Shanghai` |
| `run_mode` | No | `standard` or `simple` |
| Gemini and Antigravity fields | No | Provider-specific OAuth and client configuration |
| Security allowlist fields | No | Upstream URL validation policy |
| `update_proxy_url` | No | Proxy for update checks and GitHub access |

The template generates fixed per-deployment values for `JWT_SECRET` and `TOTP_ENCRYPTION_KEY`. Database and object-storage credentials come from Sealos-managed Secrets.

### Health and Storage Behavior

- `GET /health` reports application health on port `8080`.
- `AUTO_SETUP=true` initializes the database and creates the first administrator.
- The optional S3 branch sets `IMAGE_STORAGE_ENABLED=true`, uses path-style access, and stores image objects under `images/`.
- The default local branch sets `IMAGE_STORAGE_ENABLED=false`.
- The bucket policy is private, so application-generated signed URLs control object access.

## Why Deploy Sub2API on Sealos?

- **Single Deployment Flow**: Launch the application, data services, storage, and ingress together.
- **Managed Credentials**: Sealos creates database and object-storage credentials and injects them into the correct workloads.
- **Persistent Data**: PostgreSQL, Redis, and application data use persistent volumes.
- **Optional Object Storage**: A form toggle adds private S3-compatible storage for documented image workflows.
- **Public HTTPS Endpoint**: Sealos provides the domain, ingress, and TLS certificate.
- **Canvas Operations**: Inspect logs, resource health, storage, and configuration from one deployment view.

## Deployment Guide

1. Open the [Sub2API template](https://sealos.io/products/app-store/sub2api) and click **Deploy Now**.
2. Enter `admin_email` and an `admin_password` with at least 8 characters.
3. Choose the timezone and run mode. Enable `enable_s3_storage` when asynchronous image results should use a private Sealos bucket.
4. Add provider OAuth, URL allowlist, or update proxy values that match your environment.
5. Start the deployment and wait for PostgreSQL, Redis, the database initialization Job, and Sub2API to become healthy. This usually takes several minutes.
6. Open the application URL shown in Canvas.

## Login and User Onboarding

1. Open the application URL. Sub2API displays the sign-in page.
2. Sign in with the exact `admin_email` and `admin_password` entered during deployment.
3. On the first administrator session, read the deployment and operations compliance notice, type the acknowledgement phrase displayed by Sub2API, and continue to the dashboard.
4. Create managed users from **Users > Create User**. Public registration policy is available in the application settings.

The initial administrator is created during first startup. Reusing an existing data volume keeps the administrator stored in PostgreSQL.

## Configuration

Use the Sub2API console for upstream accounts, groups, subscriptions, API keys, usage, announcements, and service settings. Use Sealos Canvas for workload resources, persistent volumes, logs, domains, and environment configuration.

When S3 storage is enabled, the application receives the private bucket configuration automatically. The **Admin > Backup** page shows the effective asynchronous image storage settings and connection test.

## Scaling

The validated starting profile targets an idle or evaluation deployment. Increase Sub2API CPU and memory in Canvas as traffic, concurrent requests, background work, or account volume grows.

Keep the current application replica count while `/app/data` uses a single `ReadWriteOnce` volume. Review Sub2API storage and session requirements before designing a multi-replica deployment.

## Troubleshooting

### The application URL is still starting

PostgreSQL and Redis initialization can take several minutes. Check both KubeBlocks clusters, the PostgreSQL init Job, and the Sub2API `StatefulSet` in Canvas.

### Administrator login fails

Use the email and password entered in the deployment form. The password is case-sensitive and requires at least 8 characters.

### The dashboard remains behind the compliance prompt

Enter the acknowledgement phrase exactly as displayed, including its language and spacing.

### Async image storage is unavailable

Confirm that `enable_s3_storage` was enabled for the deployment. In Sub2API, open **Admin > Backup**, review the image storage configuration, and run its connection test.

### A raw object URL returns an authorization error

This is expected for the private bucket. Access image results through the application-provided signed URL flow.

### Getting Help

- [Sub2API issues](https://github.com/Wei-Shaw/sub2api/issues)
- [Sealos documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

Sub2API is licensed under the [GNU Lesser General Public License v3.0 or later](https://github.com/Wei-Shaw/sub2api/blob/v0.1.166/LICENSE). This Sealos template is distributed under the license of the templates repository.
