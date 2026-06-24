# Deploy and Host Langfuse on Sealos

Langfuse is an open-source LLM engineering platform for tracing, prompt management, evaluations, and observability. This template deploys Langfuse with PostgreSQL, Redis, ClickHouse, worker processing, and conditional S3-compatible object storage on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/langfuse/website-screenshot.webp)

## About Hosting Langfuse

Langfuse runs as a multi-service observability system. The web service handles the dashboard, API, authentication, and initialization, while the worker service processes background ingestion and analytics jobs.

The template provisions PostgreSQL 16.4.0 and Redis 7.2.7 through KubeBlocks. It also deploys a persistent ClickHouse instance for high-volume event data and lets you choose Sealos S3-compatible object storage for event and media blobs.

## Common Use Cases

- **LLM tracing**: Capture traces, spans, generations, scores, and metadata from AI applications.
- **Prompt management**: Version prompts and coordinate experiments across teams.
- **Evaluations**: Run human and automated evaluations against production traces.
- **Observability**: Monitor latency, cost, quality, and model behavior from one dashboard.

## Dependencies for Langfuse Hosting

The Sealos template includes all required runtime dependencies: Langfuse web, Langfuse worker, PostgreSQL, Redis, ClickHouse, conditional S3-compatible object storage, internal Services, and HTTPS ingress.

### Deployment Dependencies

- [Langfuse Documentation](https://langfuse.com/docs) - Official documentation
- [Self-Hosting Guide](https://langfuse.com/self-hosting) - Self-hosting documentation
- [Configuration Reference](https://langfuse.com/self-hosting/configuration) - Environment variables and storage configuration
- [GitHub Repository](https://github.com/langfuse/langfuse) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Langfuse Web**: Uses `docker.io/langfuse/langfuse:3.180.0` and exposes the dashboard and API on port `3000`.
- **Langfuse Worker**: Uses `docker.io/langfuse/langfuse-worker:3.180.0` for background ingestion and queue processing.
- **PostgreSQL**: KubeBlocks PostgreSQL `postgresql-16.4.0` for relational metadata.
- **Redis**: KubeBlocks Redis `7.2.7` for queues and caching.
- **ClickHouse**: Stateful analytics store using `clickhouse/clickhouse-server:25.4.2`.
- **Object Storage**: Conditional S3-compatible storage for event and media blobs. With `use_object_storage=true`, the template uses a Sealos ObjectStorageBucket. With it disabled, the template deploys a private MinIO service. Batch exports remain disabled by default.

**Configuration:**

The template generates salts, encryption keys, NextAuth secret, ClickHouse password, MinIO credentials, and the bootstrap organization identifiers. You can optionally set `init_user_email`, `init_user_name`, and `init_user_password` to bootstrap the first Langfuse user as the owner of the generated organization.

**License Information:**

Langfuse core product capabilities are MIT licensed. Enterprise modules such as SCIM, audit logging, and data retention policies require a commercial license when self-hosted.

## Why Deploy Langfuse on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying Langfuse on Sealos, you get:

- **One-Click Deployment**: Deploy the full Langfuse stack with databases and storage in one flow.
- **Auto-Scaling Built-In**: Adjust web and worker resources as tracing traffic grows.
- **Easy Customization**: Configure bootstrap users, object storage, and resource limits from the Sealos UI.
- **Zero Kubernetes Expertise Required**: Run PostgreSQL, Redis, ClickHouse, workers, and ingress without managing Kubernetes manually.
- **Persistent Storage Included**: Keep metadata, analytics data, and uploaded blobs available across restarts.
- **Instant Public Access**: Get a public HTTPS dashboard URL automatically.

Deploy Langfuse on Sealos and focus on improving AI applications instead of operating observability infrastructure.

## Deployment Guide

1. Open the [Langfuse template](https://sealos.io/products/app-store/langfuse) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **Langfuse Dashboard**: Log in with the bootstrap user if you configured one, or use the Langfuse sign-up flow on the first visit.

## Configuration

Initial user creation is controlled by `init_user_email`, `init_user_name`, and `init_user_password`. When these values are set, the template also creates the required Langfuse organization automatically. Leave them empty to use the interactive sign-up flow.

The `use_object_storage` option controls blob storage:

- `true`: Use Sealos S3-compatible object storage for Langfuse event and media blobs.
- `false`: Deploy the included MinIO service and store blobs in a template-managed persistent volume.

## Scaling

Langfuse includes separate web, worker, ClickHouse, PostgreSQL, and Redis components. Scale workers first when ingestion latency grows, then increase web resources for dashboard/API traffic and ClickHouse resources for analytics query volume.

## Troubleshooting

### Langfuse web starts slowly

- Cause: The web service waits for PostgreSQL, Redis, ClickHouse, and storage configuration.
- Solution: Check the database clusters, ClickHouse StatefulSet, object storage path, and worker logs from the Canvas.

### File or media uploads fail

- Cause: S3 endpoint or bucket credentials are unavailable.
- Solution: Confirm the selected object storage mode and inspect either the Sealos ObjectStorageBucket resources or the MinIO StatefulSet.

## Additional Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Self-Hosting Guide](https://langfuse.com/self-hosting)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)

## License

This Sealos template is provided under the repository license. Langfuse core product capabilities are MIT licensed, and selected enterprise modules require an upstream commercial license when self-hosted.
