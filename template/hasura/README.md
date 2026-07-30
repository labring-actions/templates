# Deploy and Host Hasura on Sealos

Hasura turns PostgreSQL data into a GraphQL API with a browser-based Console for schema, metadata, permissions, and queries. This template deploys Hasura GraphQL Engine 2.49.5, the matching Data Connector Agent, and managed PostgreSQL 16.4 on Sealos Cloud.

![Hasura Console on Sealos](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/hasura/website-screenshot.webp)

## About Hosting Hasura

Hasura builds a GraphQL schema from tracked database objects and stores its configuration as metadata. Teams can use the Console or metadata API to manage tables, relationships, permissions, actions, events, and remote schemas.

The Sealos template creates a public HTTPS endpoint for GraphQL Engine and keeps PostgreSQL plus the Data Connector Agent on the private cluster network. A fresh deployment automatically registers the managed PostgreSQL database as the `default` source.

## Common Use Cases

- **Application Backends**: Expose PostgreSQL tables through a typed GraphQL API.
- **Internal Data APIs**: Give dashboards and internal tools a governed data layer.
- **API Prototyping**: Create and query a schema quickly from the Hasura Console.
- **Event-Driven Workflows**: Connect database changes to webhooks and asynchronous processing.
- **Composable Data Access**: Add supported external systems through Hasura Data Connectors.

## Dependencies for Hasura Hosting

The template includes every runtime component required for a fresh deployment.

### Deployment Dependencies

- [Hasura Documentation](https://hasura.io/docs/latest/) - Product, API, and operations guides
- [GraphQL Engine Repository](https://github.com/hasura/graphql-engine) - Source code and releases
- [Data Connector Documentation](https://hasura.io/docs/latest/databases/data-connectors/) - Connector concepts and supported backends
- [Metadata API Reference](https://hasura.io/docs/latest/api-reference/metadata-api/index/) - Metadata automation reference

### Implementation Details

**Architecture Components:**

- **GraphQL Engine 2.49.5**: One replica serving the Console and GraphQL API on port `8080`.
- **Data Connector Agent 2.49.5**: One private replica serving connector endpoints on port `8081`.
- **Managed PostgreSQL 16.4**: One KubeBlocks replica with a 1 GiB persistent volume.
- **HTTPS Ingress**: A Sealos-managed public domain and TLS certificate for GraphQL Engine.

GraphQL Engine waits for the PostgreSQL TCP endpoint before starting. Startup, readiness, and liveness probes cover both application workloads. PostgreSQL credentials come from the KubeBlocks-managed connection Secret, and Kubernetes environment expansion builds the metadata and application database URLs.

The live-tested starter limits are `100m/256Mi` for GraphQL Engine, `100m/256Mi` for the Data Connector Agent, and `500m/512Mi` for PostgreSQL. The database source is registered from `HASURA_GRAPHQL_DATABASE_URL`, while `HASURA_GRAPHQL_METADATA_DATABASE_URL` keeps Hasura metadata in the same managed cluster.

Hasura GraphQL Engine is licensed under the Apache License 2.0.

## Why Deploy Hasura on Sealos?

- **One-Click Stack**: Create Hasura, PostgreSQL, networking, storage, and health checks from one template.
- **Automatic Data Source**: Open the Console with the managed PostgreSQL source ready to use.
- **Required Admin Authentication**: Set the Console and API admin secret during deployment.
- **Persistent Metadata**: Keep Hasura metadata and application tables across pod restarts.
- **Automatic HTTPS**: Receive a public domain and TLS certificate through Sealos.
- **Kubernetes Operations**: Inspect logs, health, resources, and storage from Sealos Canvas.

## Deployment Guide

1. Open the [Hasura template](https://sealos.io/products/app-store/hasura) and click **Deploy Now**.
2. Enter a strong, unique value for `admin_secret` and store it in a password manager.
3. Click **Deploy** and wait for PostgreSQL, GraphQL Engine, and the Data Connector Agent to become Ready.
4. Open the Hasura application entry shown in Sealos.

Initial PostgreSQL provisioning usually takes a few minutes. The GraphQL Engine startup gate waits for the database during this period.

## Sign In to Hasura Console

1. Open the generated application URL. The root path redirects to `/console`.
2. Enter the same `admin_secret` value used in the deployment dialog.
3. Select **Remember on the browser** on a trusted device when persistent browser access is useful.
4. Open **Data** and confirm that the `default` PostgreSQL source appears.

Hasura uses the shared admin secret for Console and administrative API access. Anyone holding this value receives full administrator privileges.

For API requests, send the secret in the `x-hasura-admin-secret` header:

```bash
curl "https://<your-domain>/v1/graphql" \
  -H "content-type: application/json" \
  -H "x-hasura-admin-secret: <your-admin-secret>" \
  --data '{"query":"query { __typename }"}'
```

## Create and Query a Table

1. Open **Data**, expand `default`, and select the `public` schema.
2. Click **Create Table**, define the columns and primary key, then create the table.
3. Open **Insert Row** and add a record.
4. Open **API** and query the tracked table from GraphiQL.

The **SQL** page can also create database objects. Enable **Track this** when the new table should join the GraphQL schema immediately.

## Configuration

| Name | Required | Description |
|------|----------|-------------|
| `admin_secret` | Yes | Shared secret for Hasura Console login and administrative API requests. |

Important routes:

| Route | Purpose |
|-------|---------|
| `/console` | Hasura Console login and administration |
| `/v1/graphql` | GraphQL API |
| `/v1/metadata` | Metadata API |
| `/healthz` | Public health endpoint used by Kubernetes probes |

Development mode is enabled for the starter deployment. Production environments should set `HASURA_GRAPHQL_DEV_MODE=false` after completing setup and configure CORS, JWT, webhook, or role permissions for their authentication model.

## Persistence and Scaling

PostgreSQL stores Hasura metadata and application tables on its persistent volume. Back up this volume before database migrations or major version upgrades.

The starter topology uses one replica for GraphQL Engine, one Data Connector Agent replica, and one PostgreSQL replica. Increase CPU and memory in Sealos Canvas as query volume grows. A multi-replica or high-availability architecture requires the corresponding database, metadata, and workload design from the Hasura and PostgreSQL operations guides.

## Troubleshooting

### Console rejects the admin secret

Use the exact `admin_secret` value entered during deployment. Browser password managers and copied whitespace can change the submitted value.

### GraphQL Engine remains in initialization

Check the PostgreSQL Cluster status and the `wait-for-postgresql` init container in Sealos Canvas. GraphQL Engine starts after the managed database accepts TCP connections.

### An API request returns 401

Add the `x-hasura-admin-secret` header and confirm that its value matches the deployment input.

### The `default` database source disappears after customization

Preserve `HASURA_GRAPHQL_DATABASE_URL`, `HASURA_GRAPHQL_METADATA_DATABASE_URL`, and `PG_DATABASE_URL` when editing the Deployment environment. These values are assembled from the KubeBlocks connection Secret.

### Data Connector Agent remains unready

Review its startup probe and logs in Sealos Canvas. The validated starter memory limit is `256Mi`; a `128Mi` limit causes an out-of-memory startup failure.

### Getting Help

- [Hasura GitHub Issues](https://github.com/hasura/graphql-engine/issues)
- [Hasura Documentation](https://hasura.io/docs/latest/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing terms of the templates repository. Hasura GraphQL Engine is distributed under the [Apache License 2.0](https://github.com/hasura/graphql-engine/blob/v2.49.5/LICENSE).
