# Deploy and Host Prometheus on Sealos

Prometheus is an open-source monitoring system and time-series database for metrics collection, PromQL queries, alerting, and cloud-native observability. This Sealos template runs Prometheus 3.16.0 as a single-replica StatefulSet with persistent storage and a public HTTPS endpoint.

![Prometheus interface](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/prometheus/website-screenshot.webp)

## About Hosting Prometheus

Prometheus scrapes HTTP metrics endpoints on a schedule, stores samples in its local time-series database, and evaluates PromQL queries and alerting rules. The web UI provides a query console, graph view, target status, alert rules, and runtime configuration.

This template runs one StatefulSet with `prom/prometheus:v3.16.0` on port `9090`. A 1Gi persistent volume is mounted at `/prometheus` and stores the TSDB, WAL, and compaction output. The container runs as UID/GID `65534` with a non-root security context and a read-only root filesystem disabled only because Prometheus writes runtime files.

Prometheus starts with the configuration bundled in the image and the retention limits passed on the command line: 24 hours or 800MB, whichever limit is reached first. The Service maps port `80` to the UI on `9090`, and a Sealos Ingress publishes the UI over HTTPS. The template exposes no authentication layer; keep the URL private or add an auth proxy for production use.

## Common Use Cases

- **Kubernetes Monitoring**: Scrape kube-state-metrics, node-exporter, and application `/metrics` endpoints.
- **Application Observability**: Collect request rates, latencies, error counts, queue depth, and custom business metrics.
- **Alert Prototyping**: Write and test PromQL alert rules before connecting a production Alertmanager.
- **Dashboard Development**: Validate Grafana queries against a dedicated Prometheus data source.
- **Short-Term Metrics Retention**: Keep a compact local TSDB for development, staging, or edge environments.

## Dependencies for Prometheus Hosting

The template includes the Prometheus StatefulSet, a 1Gi persistent volume, a Service, an HTTPS Ingress, and the Sealos App entry. Prometheus itself needs no external database or cache.

Scrape targets must be reachable from the Pod. Common additions include node-exporter, kube-state-metrics, application `/metrics` endpoints, and the Prometheus self-scrape job. Alertmanager is optional and deploys separately when alert delivery is required.

### Deployment Dependencies

- [Prometheus documentation](https://prometheus.io/docs/) - Concepts, configuration, and PromQL reference
- [Prometheus repository](https://github.com/prometheus/prometheus) - Source code, releases, and issue tracker
- [Prometheus container image](https://hub.docker.com/r/prom/prometheus) - Official image used by this template
- [Configuration reference](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) - Scrape jobs, rule files, and service discovery
- [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/) - Query syntax and functions

## Implementation Details

**Architecture Components:**

- **Prometheus StatefulSet**: One replica running `prom/prometheus:v3.16.0` on port `9090`.
- **Persistent volume**: A 1Gi volume at `/prometheus` for the TSDB, WAL, and compaction data.
- **Service**: ClusterIP port `80` forwarding to the Prometheus UI.
- **Ingress**: Sealos-managed HTTPS host for the web UI and API.
- **Command-line retention**: `--storage.tsdb.retention.time=1d` and `--storage.tsdb.retention.size=800MB`.

**Configuration:**

- **Image**: `prom/prometheus:v3.16.0`
- **Config file**: `/etc/prometheus/prometheus.yml`
- **Storage path**: `/prometheus`
- **Retention**: 1 day or 800MB
- **Replicas**: `1`
- **Security context**: UID/GID `65534`, non-root, all capabilities dropped
- **Persistence**: 1Gi ReadWriteOnce volume

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prometheus | 10m | 100m | 12Mi | 128Mi | 1Gi |

The profile passed a cold start, `/-/ready` check, PromQL query, and a stability window with zero restarts.

## Why Deploy Prometheus on Sealos?

Sealos is an AI-assisted cloud operating system built on Kubernetes that unifies deployment, networking, storage, and operations. Deploying Prometheus on Sealos gives you:

- **One-Click Deployment**: Provision Prometheus, persistent storage, and a public HTTPS endpoint from one template.
- **Persistent Metrics**: Keep the TSDB across Pod restarts and rescheduling through a dedicated volume.
- **Canvas and AI Dialog**: Inspect the StatefulSet, Service, Ingress, PVC, logs, and resource cards, and adjust the deployment through the Sealos AI dialog.
- **Pay-as-You-Go Resources**: Start with a compact profile and raise limits as scrape volume and cardinality grow.
- **Kubernetes Foundation**: Use managed scheduling, health probes, service discovery, and declarative resources.
- **Simple Query Access**: Open the PromQL console from any browser through a managed domain.

## Deployment Guide

1. Open the [Prometheus template](https://sealos.io/products/app-store/prometheus) and click **Deploy Now**.
2. Review the generated application name and host, confirm the 1Gi storage plan, and start the deployment.
3. Wait for deployment to complete, typically in 2-3 minutes. Sealos opens the Canvas after the resources are created.
4. Open the public URL, run `up` in the query console, and switch to the **Graph** tab to confirm the query path.
5. Open **Status → Targets** to review active scrape jobs, then add your own jobs through a Prometheus ConfigMap.
6. Open Canvas to review the StatefulSet, Service, Ingress, PVC, and live logs.

## Configuration

Add scrape targets by creating a ConfigMap that contains `prometheus.yml`, mounting it at `/etc/prometheus/prometheus.yml`, and restarting the Pod. A minimal job looks like this:

```yaml
scrape_configs:
  - job_name: my-app
    metrics_path: /metrics
    static_configs:
      - targets: ["my-app.namespace.svc.cluster.local:8080"]
```

For Kubernetes service discovery, add a `kubernetes_sd_configs` block and the required RBAC permissions. The template keeps `automountServiceAccountToken: false`; service discovery needs a dedicated ServiceAccount with list and watch permissions.

Retention is controlled by the StatefulSet arguments. Raise the time or size limit when the workload needs a longer history, and expand the PVC before increasing retention significantly.

## Scaling

Prometheus runs as one StatefulSet because the local TSDB is tied to a single writer. Increase CPU and memory limits for higher cardinality, more active series, or heavier PromQL queries. Expand the 1Gi volume when retention and series count require more disk. For horizontal scale, run multiple Prometheus shards with separate scrape targets or use remote write to a long-term store.

## Troubleshooting

### The Targets page is empty

Prometheus needs scrape jobs in `prometheus.yml`. Add a job through a ConfigMap, mount it into the Pod, and restart the StatefulSet. Check that the target hostname resolves from the Prometheus namespace.

### A target shows DOWN

Open the target's error message on **Status → Targets**. Common causes are network policy, an incorrect port, a missing `/metrics` path, or a TLS certificate that Prometheus does not trust.

### The Pod restarts with disk pressure

The TSDB volume is 1Gi and retention is bounded to 800MB. Check PVC usage, reduce retention, or expand the volume from the StatefulSet resource card.

### Queries time out

High-cardinality queries and large ranges need more CPU and memory. Narrow the time range, reduce the number of series, or raise the container limits.

### Getting Help

- [Prometheus documentation](https://prometheus.io/docs/)
- [Prometheus issues](https://github.com/prometheus/prometheus/issues)
- [Sealos documentation](https://sealos.io/docs)

## License

Prometheus is licensed under the [Apache License 2.0](https://github.com/prometheus/prometheus/blob/main/LICENSE). This Sealos template is distributed under the templates repository license.
