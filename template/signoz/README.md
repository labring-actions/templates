# Deploy and Host SigNoz on Sealos

SigNoz is an OpenTelemetry-native observability platform for logs, traces, metrics, dashboards, and alerts. This template deploys the official SigNoz self-hosted runtime as a persistent four-service stack on Sealos.

![SigNoz Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/signoz/website-screenshot.webp)

## About Hosting SigNoz

SigNoz gives application teams one interface for distributed tracing, application performance monitoring, log exploration, infrastructure metrics, dashboards, and alerting. Applications send OpenTelemetry data to the bundled collector, which writes telemetry into ClickHouse for querying through the SigNoz web console.

Sealos provisions the public HTTPS endpoint, persistent volumes, service discovery, health checks, and ordered migration gates. After deployment, SigNoz's first-user signup creates the initial administrator account.

## Common Use Cases

- **Application Performance Monitoring**: Inspect service latency, throughput, and error rates.
- **Distributed Tracing**: Follow requests across services and find slow spans.
- **Centralized Log Analysis**: Query application logs alongside traces and metrics.
- **Infrastructure Monitoring**: Track host, container, and Kubernetes telemetry.
- **Dashboards and Alerts**: Build operational views and receive notifications from telemetry conditions.

## Dependencies for SigNoz Hosting

The template includes the complete self-hosted runtime and its persistent data plane.

### Deployment Dependencies

- [SigNoz Documentation](https://signoz.io/docs/) - Product and instrumentation guides
- [SigNoz Self-Hosting Guide](https://signoz.io/docs/install/) - Official deployment guidance
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) - Telemetry SDK and collector guidance
- [SigNoz GitHub Repository](https://github.com/SigNoz/signoz) - Source code and issue tracking

### Implementation Details

**Architecture Components:**

- **SigNoz**: Serves the web console, API, authentication, alerting, and query engine.
- **OpenTelemetry Collector**: Receives OTLP over gRPC and HTTP, processes telemetry, and exports it to ClickHouse.
- **ClickHouse**: Stores traces, logs, metrics, metadata, analytics, and meter data.
- **ZooKeeper**: Coordinates the replicated ClickHouse table layout used by the official runtime.
- **Telemetry Store Migrator**: Runs once at deployment and completes synchronous and asynchronous ClickHouse migrations before the application starts.

**Persistent Data:**

SigNoz stores users, organizations, sessions, and application settings in SQLite on the SigNoz volume. ClickHouse data and logs use separate volumes, and ZooKeeper has its own coordination-data volume.

**Version Alignment:**

The component images and configuration follow the official SigNoz `v0.117.0` Docker deployment bundle, including SigNoz OpenTelemetry Collector `v0.144.2`, ClickHouse `25.5.6`, and ZooKeeper `3.7.1`.

**License Information:**

The SigNoz repository uses the MIT Expat license for code outside `ee/` and `cmd/enterprise/`. Enterprise directories carry the separate SigNoz Enterprise License. Review the upstream license files for the terms that apply to your use.

## Why Deploy SigNoz on Sealos?

Sealos is a Kubernetes-based cloud operating system that manages the application lifecycle through one interface.

- **One-Click Deployment**: Provision the complete SigNoz stack from a single template.
- **Persistent Storage**: Keep observability data and account state across Pod replacements.
- **Managed Networking**: Receive an HTTPS application URL and internal service discovery automatically.
- **Resource Efficiency**: Start with live-tested personal low-load resource settings and pay for allocated resources.
- **Integrated Operations**: Use Canvas, the AI dialog, resource cards, logs, and monitoring for day-two changes.

## Deployment Guide

1. Open the [SigNoz template](https://sealos.io/products/app-store/signoz) and click **Deploy Now**.
2. Start the deployment and wait for the ClickHouse migration Job and all four services to become ready. A fresh deployment usually takes several minutes.
3. Open the SigNoz URL from the completed Canvas.

## First Login

1. On a new deployment, complete the SigNoz signup form to create the first administrator account.
2. Use a password with at least 12 characters, including an uppercase letter, a lowercase letter, a number, and a symbol.
3. Sign in with the registered email and password. The first authenticated page is the SigNoz workspace home. Use **Services**, **Logs**, **Traces**, or **Dashboards** to begin exploring telemetry.

Store the registered credentials in a secure password manager. Later users can sign in through the same application URL.

## Sending Telemetry

Applications inside the same Sealos namespace can send OTLP data to:

- **OTLP gRPC**: `http://<app-name>-otel-collector:4317`
- **OTLP HTTP**: `http://<app-name>-otel-collector:4318`

Replace `<app-name>` with the generated deployment name shown on Canvas. Follow the [SigNoz instrumentation guides](https://signoz.io/docs/instrumentation/) for language-specific SDK configuration.

## Configuration and Operations

- **AI Dialog**: Describe a resource or configuration change from Canvas.
- **Resource Cards**: Inspect and edit workload resources, environment variables, and storage.
- **Scaling**: Increase CPU and memory before sustained ingestion or larger retention workloads.
- **Backups**: Snapshot the SigNoz, ClickHouse data, ClickHouse log, and ZooKeeper volumes together for a consistent recovery point.

## Troubleshooting

### Deployment remains in initialization

The first telemetry-store migration creates many ClickHouse tables. Check the Telemetry Store Migrator Job and ClickHouse Pod on Canvas, then allow the migration to finish.

### Login fails

Use the email and password registered on the first visit. Confirm that the password satisfies the 12-character complexity policy and check the SigNoz Pod logs for authentication errors.

### Queries are slow or ingestion grows

Open the SigNoz and ClickHouse resource cards and raise CPU or memory for the observed workload. Personal low-load defaults prioritize resource efficiency.

### Getting Help

- [SigNoz Documentation](https://signoz.io/docs/)
- [SigNoz GitHub Issues](https://github.com/SigNoz/signoz/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the license of the templates repository. SigNoz components retain their upstream licenses.
