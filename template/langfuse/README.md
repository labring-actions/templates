# Deploy and Host Langfuse on Sealos

Langfuse is an open-source LLM engineering platform for tracing, prompt management, evaluations, and observability. This template deploys Langfuse `3.224.2` with PostgreSQL, Redis, ClickHouse, background workers, private Sealos object storage, and public HTTPS access.

![Langfuse prompt management](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/langfuse/website-screenshot.webp)

## About Hosting Langfuse

Langfuse gives AI teams one place to inspect traces, version prompts, evaluate outputs, and monitor application quality. The web service provides the dashboard, API, and authentication, while a separate worker handles ingestion and background jobs.

The Sealos template provisions every required service in one deployment. Relational metadata is stored in PostgreSQL, queues use Redis and Sentinel, analytics data is stored in persistent ClickHouse volumes, and event, media, and batch-export objects use a private Sealos S3-compatible bucket.

## Common Use Cases

- **LLM observability**: Capture traces, generations, spans, latency, cost, and model metadata.
- **Prompt management**: Create versioned text or chat prompts and promote production labels.
- **Evaluation workflows**: Add scores, datasets, evaluators, and human annotation queues.
- **Application debugging**: Search traces and compare behavior across releases and environments.

## Dependencies for Langfuse Hosting

The template includes Langfuse web and worker images, PostgreSQL, Redis, Redis Sentinel, ClickHouse, object storage, internal Services, persistent volumes, and HTTPS ingress.

### Deployment Dependencies

- [Langfuse documentation](https://langfuse.com/docs) - Product and SDK documentation
- [Langfuse self-hosting guide](https://langfuse.com/self-hosting) - Official deployment guidance
- [Langfuse configuration reference](https://langfuse.com/self-hosting/configuration) - Environment variables
- [Langfuse repository](https://github.com/langfuse/langfuse) - Source code and releases
- [Sealos documentation](https://sealos.io/docs) - Platform documentation

## Implementation Details

### Architecture Components

- **Langfuse Web**: One `Deployment` running `docker.io/langfuse/langfuse:3.224.2` on port `3000`.
- **Langfuse Worker**: One `Deployment` running `docker.io/langfuse/langfuse-worker:3.224.2` for ingestion and background queues.
- **PostgreSQL**: One KubeBlocks PostgreSQL `16.4.0` component with a `1Gi` persistent volume.
- **Database initialization**: An idempotent Job creates the `langfuse` database before application migrations run.
- **Redis**: KubeBlocks Redis `7.2.7` replication topology with one Redis component and one Sentinel component.
- **ClickHouse**: One persistent `clickhouse/clickhouse-server:25.4.2` StatefulSet with separate `1Gi` data and log volumes.
- **Object storage**: One private Sealos `ObjectStorageBucket` for event uploads, media, and batch exports.
- **Public access**: A Sealos-managed HTTPS Ingress and Canvas application entry.

### Resource Profile

| Component | Replicas | CPU limit | Memory limit | Persistent storage |
| --- | ---: | ---: | ---: | ---: |
| Langfuse Web | 1 | `100m` | `2048Mi` | - |
| Langfuse Worker | 1 | `100m` | `512Mi` | - |
| ClickHouse | 1 | `100m` | `256Mi` | `2Gi` |
| PostgreSQL | 1 | `500m` | `512Mi` | `1Gi` |
| Redis | 1 | `500m` | `512Mi` | `1Gi` |
| Redis Sentinel | 1 | `500m` | `512Mi` | `1Gi` |
| Init containers and database Job | Per start | `100m` | `128Mi` | - |

This profile is a validated starting point for evaluation and light workloads. Increase web and worker CPU for higher request or ingestion throughput, and increase ClickHouse resources as trace volume and query concurrency grow.

### Template Inputs

| Input | Required | Purpose |
| --- | --- | --- |
| `init_user_email` | No | Creates the initial Langfuse owner when paired with a password |
| `init_user_name` | No | Display name for the initialized owner |
| `init_user_password` | No | Password for the initialized owner |

Per-deployment salts, encryption keys, authentication secrets, ClickHouse credentials, database credentials, and object-storage credentials are generated or managed automatically.

### Storage and Health Behavior

- `/api/public/health` reports process health, and `/api/public/ready` reports dependency readiness.
- PostgreSQL, Redis, Redis Sentinel, and ClickHouse retain data on persistent volumes.
- Event data, media, and batch exports use path-style access to the private Sealos bucket.
- Raw bucket object URLs require authorization. Langfuse generates signed upload and download URLs for application workflows.
- Application deletion jobs remove associated media objects with an S3-compatible MD5 multi-delete checksum.

## Why Deploy Langfuse on Sealos?

- **Complete Runtime Stack**: Deploy the dashboard, worker, databases, analytics store, and object storage together.
- **Managed Credentials**: Sealos creates service credentials and injects them into the correct workloads.
- **Persistent Data**: PostgreSQL, Redis, ClickHouse, and object data survive workload restarts.
- **Private Object Storage**: Event, media, and export objects stay in a dedicated private bucket.
- **Public HTTPS Endpoint**: Sealos provides the domain, ingress, and TLS certificate.
- **Canvas Operations**: Inspect logs, resource health, storage, and configuration from one deployment view.

## Deployment Guide

1. Open the [Langfuse template](https://sealos.io/products/app-store/langfuse) and click **Deploy Now**.
2. Choose an onboarding path:
   - Enter `init_user_email`, `init_user_name`, and `init_user_password` to create the first owner automatically.
   - Leave the user fields empty to create the first account from the sign-up page.
3. Start the deployment and wait for PostgreSQL, Redis, ClickHouse, the initialization Job, Langfuse Web, and Langfuse Worker to become healthy. A cold deployment usually takes several minutes.
4. Open the HTTPS application URL shown in Canvas.

## Login and Registration

### Initialized User

1. Open `/auth/sign-in` on the application domain.
2. Enter the exact email and password supplied in the deployment form.
3. The template creates the `Sealos Langfuse` organization automatically.
4. Create a project, then use **Prompts**, **Tracing**, **Datasets**, or **Settings > API Keys**.

### Interactive Registration

1. Open `/auth/sign-up` on the application domain.
2. Create the first account.
3. Follow the Langfuse onboarding flow to create an organization and project.
4. Create a project API key from **Settings > API Keys** before connecting an SDK.

## Configuration

Use the Langfuse dashboard for projects, prompts, API keys, model definitions, evaluators, datasets, and members. Use Sealos Canvas for workload resources, persistent volumes, logs, domains, and environment configuration.

The private object-storage bucket is part of every deployment because Langfuse `3.224.2` uses S3-compatible storage for event ingestion, media, and exports.

## Scaling

Increase worker CPU and replicas when queue latency grows. Increase web CPU or replicas for dashboard and API traffic. Increase ClickHouse CPU, memory, and storage for larger trace volumes and analytical queries.

Review Langfuse concurrency guidance and database capacity before adding replicas. Keep the persistent ClickHouse StatefulSet and managed data services intact while scaling stateless web and worker components.

## Troubleshooting

### The application URL is still starting

A cold deployment applies PostgreSQL and ClickHouse migrations before the dashboard becomes ready. Check the PostgreSQL cluster, Redis cluster, ClickHouse StatefulSet, initialization Job, and web logs in Canvas.

### Login fails

For initialized deployments, use the exact email and password entered in the template form at `/auth/sign-in`. For interactive onboarding, create the first account at `/auth/sign-up`.

### Media or event uploads fail

Confirm that the `ObjectStorageBucket` is ready and that both Langfuse deployments reference the Sealos-managed object-storage Secrets.

### The web pod exits with code 137

Langfuse Web needs the validated `2048Mi` memory limit during startup. Preserve that limit or increase it for larger installations.

### Getting Help

- [Langfuse issues](https://github.com/langfuse/langfuse/issues)
- [Langfuse self-hosting documentation](https://langfuse.com/self-hosting)
- [Sealos documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

Langfuse core product capabilities are licensed under the [MIT License](https://github.com/langfuse/langfuse/blob/main/LICENSE). Selected enterprise features require an upstream commercial license. This Sealos template is distributed under the templates repository license.
