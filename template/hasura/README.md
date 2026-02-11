# Deploy and Host Hasura on Sealos

Hasura is a high-performance GraphQL API engine for your data. This template deploys Hasura GraphQL Engine with PostgreSQL metadata storage and a Data Connector Agent on Sealos Cloud.

## About Hosting Hasura

Hasura provides instant GraphQL APIs, metadata-driven schema management, role-based authorization, and event/webhook integrations on top of your data services. In this template, Hasura runs as the primary API and console service and connects to a managed PostgreSQL cluster for metadata.

The deployment includes two application workloads: `hasura/graphql-engine` and `hasura/graphql-data-connector`. The Data Connector Agent provides connector endpoints for federated and external data backends, while Hasura keeps metadata and runtime state in PostgreSQL provisioned by Kubeblocks.

Sealos also provisions HTTPS ingress, a public domain, persistent database storage, and Kubernetes-native lifecycle management in Canvas.

## Common Use Cases

- **Internal API Platform**: Build a unified GraphQL API for internal tools and dashboards.
- **SaaS Backend Acceleration**: Expose PostgreSQL-backed GraphQL endpoints quickly for product development.
- **Composable Data Gateway**: Connect multiple data systems through Hasura metadata and data connectors.
- **Event-Driven Workflows**: Trigger webhooks and async business processes from data changes.
- **Prototype to Production**: Start with one-click deployment and scale through Canvas resource controls.

## Dependencies for Hasura Hosting

The Sealos template includes all required dependencies: Hasura GraphQL Engine, Hasura Data Connector Agent, and a managed PostgreSQL 16.4 cluster with persistent storage.

### Deployment Dependencies

- [Hasura Documentation](https://hasura.io/docs/latest/) - Official product and operation guides
- [Hasura GraphQL Engine Repository](https://github.com/hasura/graphql-engine) - Source code and release history
- [Hasura Data Connectors](https://hasura.io/docs/latest/databases/data-connectors/) - Connector and integration concepts
- [Hasura Discord Community](https://discord.gg/hasura) - Community support and discussions

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Hasura GraphQL Engine**: Main API and Console service exposed via HTTPS ingress.
- **Data Connector Agent**: Companion service for connector endpoints on port `8081`.
- **PostgreSQL (Kubeblocks)**: Metadata database cluster (`postgresql-16.4.0`) with persistent storage.

**Configuration:**

- Hasura reads database connection fields from Kubeblocks-managed secret keys (`host`, `port`, `username`, `password`).
- The startup command composes a full PostgreSQL DSN before launching `graphql-engine`.
- Ingress is provisioned with TLS and a public domain, and the default deployment is single replica for both workloads.

**License Information:**

Hasura GraphQL Engine is licensed under the [Apache License 2.0](https://github.com/hasura/graphql-engine/blob/master/LICENSE).

## Why Deploy Hasura on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies development, deployment, and operations. By deploying Hasura on Sealos, you get:

- **One-Click Deployment**: Launch Hasura, PostgreSQL, and connector components without manual YAML orchestration.
- **Managed Kubernetes Runtime**: Keep Kubernetes reliability with less operational complexity.
- **Easy Customization**: Update environment variables and resources through Canvas dialogs and resource cards.
- **Instant HTTPS Access**: Get a public URL with TLS for Hasura Console and API access.
- **Persistent Database Storage**: Store metadata safely with built-in persistent volumes.
- **Scale on Demand**: Adjust CPU, memory, and replicas from Canvas as traffic grows.
- **AI-Assisted Ops**: Describe desired changes in the AI dialog and apply updates quickly.

Deploy Hasura on Sealos to focus on API delivery instead of infrastructure management.

## Deployment Guide

1. Open the [Hasura template](https://sealos.io/appstore/hasura) and click **Deploy Now**.
2. Configure deployment parameters in the popup dialog.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas.
4. Access the generated URL and open Hasura Console:
   - **Hasura Console**: `https://<your-domain>/console`
   - **Version/Health Check**: `https://<your-domain>/v1/version` and `https://<your-domain>/healthz`

## Configuration

After deployment, configure Hasura through:

- **AI Dialog**: Describe required changes (for example enabling admin secret or changing runtime flags).
- **Resource Cards**: Edit Deployment environment variables, probes, and resource limits.
- **Hasura Console**: Manage metadata, permissions, and tracked data sources.

Recommended production baseline:

- Set `HASURA_GRAPHQL_ADMIN_SECRET`.
- Set CORS and authentication-related settings based on your environment.
- Disable development mode (`HASURA_GRAPHQL_DEV_MODE=false`) for production workloads.

## Scaling

To scale this deployment:

1. Open the application in Canvas.
2. Select the Hasura and Data Connector Deployments.
3. Increase CPU/Memory and replica count as needed.
4. Apply changes and monitor pod health and response latency.

## Troubleshooting

### Common Issues

**Issue: Hasura pod restarts during initial deployment**
- Cause: PostgreSQL cluster initialization may still be in progress.
- Solution: Wait until PostgreSQL status is `Running` and check Hasura pod logs again.

**Issue: Cannot access Console**
- Cause: Ingress propagation or TLS issuance is not completed yet.
- Solution: Wait briefly, then verify ingress host and certificate status in Canvas.

**Issue: Metadata DB connection errors after custom changes**
- Cause: Database-related env vars were overridden with incomplete values.
- Solution: Keep DB fields sourced from Kubeblocks secret keys and preserve DSN composition logic.

### Getting Help

- [Hasura Docs](https://hasura.io/docs/latest/)
- [Hasura GitHub Issues](https://github.com/hasura/graphql-engine/issues)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [Hasura Deployment Guide](https://hasura.io/docs/latest/deployment/)
- [Hasura Metadata API](https://hasura.io/docs/latest/api-reference/metadata-api/index/)
- [Hasura Permissions Guide](https://hasura.io/docs/latest/auth/authorization/permissions/)

## License

This Sealos template is provided under the template repository license. Hasura GraphQL Engine itself is licensed under Apache License 2.0.
