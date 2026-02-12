# Deploy and Host Airbyte on Sealos

Airbyte is an open-source data integration platform for building ELT pipelines from databases, APIs, and SaaS tools into your data warehouse or lake. This template deploys Airbyte Open Source with PostgreSQL, Temporal, object storage integration, and all required control-plane services on Sealos Cloud.

![Airbyte Logo](./logo.svg)

## About Hosting Airbyte

Airbyte runs as a multi-service system: a web UI, API/control server, workers, scheduler, connector builder API, workflow engine, and a metadata database. This Sealos template wires these components together with service discovery, health probes, and startup ordering so you can run Airbyte reliably without manual Kubernetes assembly.

The deployment provisions a managed PostgreSQL cluster through KubeBlocks for metadata persistence and migration bootstrap, plus an S3-compatible object storage bucket for logs, state, and workload outputs. A public HTTPS ingress is exposed for the Airbyte web application.

For security, the template enables built-in authentication and injects admin credentials/JWT secrets from deployment configuration. You can continue managing resources after deployment in Canvas via AI dialog or resource cards.

## Common Use Cases

- **Centralized ELT for Analytics**: Sync operational data from SaaS tools and databases into your warehouse.
- **Reverse ETL and Internal Data Ops**: Standardize ingestion and orchestration before downstream activation.
- **Self-Hosted Data Integration**: Run Airbyte in your own Kubernetes environment with controlled data residency.
- **Connector Development and Testing**: Use the connector builder service alongside the core platform.
- **Scheduled Batch Synchronization**: Run periodic syncs with worker-based execution and retry handling.

## Dependencies for Airbyte Hosting

This template includes all required dependencies: Airbyte control-plane services, Temporal workflow engine, PostgreSQL, object storage bucket integration, ingress, and bootstrap jobs.

### Deployment Dependencies

- [Airbyte Documentation](https://docs.airbyte.com/) - Official Airbyte docs
- [Airbyte GitHub Repository](https://github.com/airbytehq/airbyte) - Source code and releases
- [Airbyte Security Guide](https://docs.airbyte.com/operator-guides/security/#securing-airbyte-open-source) - Hardening guidance
- [Temporal Documentation](https://docs.temporal.io/) - Workflow engine reference
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Database reference

## Implementation Details

### Architecture Components

This template deploys the following resources:

- **Airbyte Webapp (`airbyte/webapp:0.63.11`)**: Public UI served through HTTPS ingress.
- **Airbyte Server (`airbyte/server:0.63.11`)**: API/control plane with authentication and orchestration logic.
- **Airbyte Worker (`airbyte/worker:0.63.11`)**: Background execution engine for sync and connector tasks.
- **Airbyte Cron (`airbyte/cron:0.63.11`)**: Scheduled control-plane and maintenance tasks.
- **Connector Builder Server (`airbyte/connector-builder-server:0.63.11`)**: Connector builder API service.
- **Temporal (`temporalio/auto-setup:1.23.0`)**: Workflow service for orchestration and retries.
- **PostgreSQL Cluster (`postgresql-16.4.0`)**: Metadata database via KubeBlocks with persistent storage.
- **Object Storage Bucket**: S3-compatible storage for logs/state/workload output.
- **Bootloader Job (`airbyte/bootloader:0.63.11`)**: Initializes/migrates database schema at startup.

### Service Topology

- Public ingress routes to `webapp`.
- `webapp` talks to `server` internally.
- `server`, `worker`, and `cron` use `temporal:7233` for workflow coordination.
- `server`, `worker`, `cron`, and bootloader use PostgreSQL credentials from KubeBlocks-generated secrets.
- `server` and `worker` use object storage credentials from Sealos object-storage secrets.

### Default Resource and Storage Profile

- Application Deployments default to conservative Kubernetes requests/limits and can be adjusted in Canvas.
- PostgreSQL requests `1Gi` persistent storage by default.
- Temporal dynamic config is mounted from ConfigMap at `/etc/temporal/config/dynamicconfig`.

### Authentication Inputs

The template exposes these security-related deployment inputs:

- `auth_admin_username`: initial admin username (default `admin`, editable)
- `auth_admin_password`: initial admin password (default random value, editable)
- JWT signature and refresh secrets: auto-generated random values

Use the configured admin credential from deployment configuration on first login, then rotate credentials according to your security policy.

### License Information

Airbyte is distributed under [Elastic License 2.0](https://github.com/airbytehq/airbyte/blob/master/LICENSE). Check upstream licensing terms before production use.

## Why Deploy Airbyte on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment and operations. By deploying Airbyte on Sealos, you get:

- **One-Click Deployment**: Deploy a multi-service Airbyte stack without hand-writing Kubernetes manifests.
- **Managed Database Provisioning**: PostgreSQL is provisioned and connected automatically.
- **Persistent Storage Included**: Durable storage for metadata, sync artifacts, and workflow state.
- **Secure Public Access**: HTTPS ingress and managed networking for the web application.
- **Easy Customization**: Adjust environment variables and resources through Canvas dialogs.
- **AI-Assisted Operations**: Use natural language updates for post-deployment changes.
- **Pay-as-You-Go Efficiency**: Scale resources based on actual sync workload demand.

Deploy Airbyte on Sealos and focus on data pipelines instead of platform plumbing.

## Deployment Guide

1. Open the [Airbyte template](https://sealos.io/appstore/airbyte) and click **Deploy Now**.
2. Configure deployment parameters in the popup dialog.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click relevant resource cards to modify settings.
4. Open the generated public URL and log in:
   - **Username**: the `auth_admin_username` value you configured
   - **Password**: the `auth_admin_password` value you configured

## Configuration

After deployment, you can configure Airbyte through:

- **AI Dialog**: Describe desired changes and let AI apply updates.
- **Resource Cards**: Modify Deployment resources, environment variables, and probes.
- **Airbyte UI**: Manage sources, destinations, workspaces, and sync schedules.

Recommended post-deployment actions:

1. Rotate admin credentials and review security settings.
2. Confirm destination and source connector permissions.
3. Validate object storage and database connectivity with a test sync.
4. Configure alerts/monitoring for worker and temporal health.

## Scaling

To scale your deployment:

1. Open your deployment in Canvas.
2. Scale the `worker` Deployment first for higher sync concurrency.
3. Increase resources for `server` and `temporal` if orchestration throughput becomes a bottleneck.
4. Reassess PostgreSQL sizing for higher metadata/write volume.

## Troubleshooting

### Common Issues

**Issue: Worker startup probe fails with `strconv.Atoi: parsing "heartbeat"`**
- Cause: Probe port references a non-resolved named port in a bad revision.
- Solution: Ensure worker probes use numeric port `9000` (or a valid named port that exists in the container port list).

**Issue: Temporal fails with `dynamic config ... development.yaml: no such file or directory`**
- Cause: Dynamic config ConfigMap is not mounted.
- Solution: Verify `dynamic-config` volume and mount path `/etc/temporal/config/dynamicconfig` exist in Temporal Deployment.

**Issue: Temporal health check connection refused on `:7233`**
- Cause: Temporal container failed to boot (often due to missing dynamic config mount).
- Solution: Fix dynamic config mount, then restart/rollout Temporal Deployment.

**Issue: Login page warns instance is publicly reachable without auth**
- Cause: Security/auth settings are incomplete.
- Solution: Verify auth-related environment values are present and follow the [Airbyte security guide](https://docs.airbyte.com/operator-guides/security/#securing-airbyte-open-source).

### Getting Help

- [Airbyte Documentation](https://docs.airbyte.com/)
- [Airbyte GitHub Issues](https://github.com/airbytehq/airbyte/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Airbyte Open Source Docs](https://docs.airbyte.com/)
- [Airbyte Connectors Catalog](https://docs.airbyte.com/integrations/)
- [Temporal Documentation](https://docs.temporal.io/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template follows repository licensing terms. Airbyte itself is licensed under [Elastic License 2.0](https://github.com/airbytehq/airbyte/blob/master/LICENSE).
