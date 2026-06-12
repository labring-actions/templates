# Deploy and Host Loki on Sealos

Loki is Grafana's open source log aggregation system designed to store and query logs with Prometheus-style labels. This template deploys a single-node Loki instance with persistent storage and a public HTTPS endpoint on Sealos Cloud.

## About Hosting Loki

Loki stores compressed log streams and indexes metadata labels instead of full log text, which keeps ingestion lightweight for application and infrastructure logs. The Sealos template runs Loki as a StatefulSet, persists `/loki` data on a 1 GiB volume, and exposes the HTTP API on port `3100`.

This deployment is suitable for development, testing, small observability stacks, and lightweight log collection. It does not include Grafana or a log shipper, so you can connect Grafana, Promtail, Grafana Alloy, or compatible clients after deployment.

## Common Use Cases

- **Application Log Collection**: Store logs from apps, workers, and services using Loki's push API.
- **Grafana Log Exploration**: Add the Loki endpoint as a Grafana data source and query logs with LogQL.
- **Lightweight DevOps Monitoring**: Keep a small persistent log backend for development and staging environments.
- **Troubleshooting Pipelines**: Send CI, job, or batch logs into a searchable backend.

## Dependencies for Loki Hosting

The Sealos template includes all runtime dependencies required to start Loki: the official Loki container image, a Kubernetes StatefulSet, a ClusterIP Service, an Ingress, and persistent storage.

### Deployment Dependencies

- [Loki Documentation](https://grafana.com/docs/loki/latest/) - Official Loki documentation
- [Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/) - API reference for readiness, ingestion, and queries
- [LogQL Documentation](https://grafana.com/docs/loki/latest/query/) - Query language reference
- [Grafana Loki GitHub](https://github.com/grafana/loki) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Loki StatefulSet**: Runs `docker.io/grafana/loki:3.7.2` with the built-in local filesystem configuration.
- **Persistent Volume**: Mounts `/loki` for chunks, indexes, and rule data.
- **Service**: Exposes Loki internally on port `3100`.
- **Ingress and App Entry**: Provides an HTTPS endpoint for the Loki HTTP API.

**Configuration:**

Loki starts with its default single-binary local configuration. Authentication is disabled by the upstream local config, so protect the endpoint according to your workspace and network policy before sending sensitive logs. The template does not create users, passwords, or an initialization flow.

**License Information:**

Loki is licensed under the GNU Affero General Public License v3.0. This Sealos template is provided under the license terms of the templates repository.

## Why Deploy Loki on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and operations. By deploying Loki on Sealos, you get:

- **One-Click Deployment**: Deploy Loki from the App Store without writing Kubernetes YAML.
- **Persistent Storage Included**: Keep log data across restarts with a managed persistent volume.
- **Instant Public Access**: Use the generated HTTPS endpoint for API clients and Grafana data source configuration.
- **Resource Controls**: Adjust CPU, memory, and storage from the Sealos Canvas when your log volume grows.
- **Kubernetes-Based Operations**: Run Loki on a managed Kubernetes foundation without managing cluster primitives directly.

## Deployment Guide

1. Open the [Loki template](https://sealos.io/products/app-store/loki) and click **Deploy Now**.
2. Keep the default parameters or adjust the generated app name and host in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the StatefulSet, Service, Ingress, or storage resource cards to modify settings.
4. Access Loki through the generated URL:
   - **Readiness Check**: `https://[your-loki-url]/ready`
   - **Build Info**: `https://[your-loki-url]/loki/api/v1/status/buildinfo`
   - **Push API**: `https://[your-loki-url]/loki/api/v1/push`
   - **Query API**: `https://[your-loki-url]/loki/api/v1/query_range`

## API Access

Loki does not provide a standalone web UI in this template. Use its HTTP API or connect the generated URL to Grafana as a Loki data source.

Example API checks:

```bash
curl https://[your-loki-url]/ready
curl https://[your-loki-url]/loki/api/v1/status/buildinfo
```

Example log ingestion:

```bash
NOW=$(date +%s)000000000
curl -X POST "https://[your-loki-url]/loki/api/v1/push" \
  -H 'Content-Type: application/json' \
  --data "{\"streams\":[{\"stream\":{\"job\":\"demo\"},\"values\":[[\"$NOW\",\"hello from Sealos Loki\"]]}]}"
```

## Configuration

After deployment, you can configure Loki through:

- **AI Dialog**: Describe resource or runtime changes and let Sealos apply updates.
- **Resource Cards**: Click the StatefulSet, Service, Ingress, or storage cards in Canvas.
- **Client Configuration**: Point Grafana, Promtail, Grafana Alloy, or compatible clients to the generated HTTPS endpoint.

## Scaling

This template is a single-node Loki deployment intended for lightweight workloads. To scale resources:

1. Open the Canvas for your deployment.
2. Click the Loki StatefulSet resource card.
3. Adjust CPU, memory, or storage according to ingestion volume.
4. Apply the changes and wait for the pod to become ready.

For high-volume or highly available production logging, use Loki's distributed deployment mode and object storage architecture instead of this single-node template.

## Troubleshooting

### Loki endpoint returns no log results

- Cause: Loki has no ingested streams matching your LogQL query, or the query time range is too narrow.
- Solution: Push a test log through `/loki/api/v1/push`, then query with `/loki/api/v1/query_range` and a label selector such as `{job="demo"}`.

### Grafana cannot connect

- Cause: The data source URL may be wrong or the Loki pod may still be starting.
- Solution: Confirm `https://[your-loki-url]/ready` returns `ready`, then use the generated HTTPS URL as the Grafana Loki data source URL.

### Pod restarts during heavy ingestion

- Cause: The default template resources target a lightweight deployment.
- Solution: Increase CPU and memory from the StatefulSet resource card, then retry ingestion.

## Additional Resources

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- [LogQL Query Reference](https://grafana.com/docs/loki/latest/query/)
- [Grafana Data Source Setup](https://grafana.com/docs/grafana/latest/datasources/loki/)

## License

This Sealos template is provided under the license terms of the templates repository. Loki is licensed under the GNU Affero General Public License v3.0.
