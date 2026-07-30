# Deploy and Host changedetection.io on Sealos

changedetection.io is an open-source service for monitoring webpages, JSON endpoints, and PDF documents. This template deploys changedetection.io 0.55.8 with persistent storage, a public HTTPS endpoint, and health checks on Sealos Cloud.

![changedetection.io Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/changedetection/website-screenshot.webp)

## About Hosting changedetection.io

changedetection.io checks targets on a schedule, stores snapshots, highlights content differences, and sends notifications through supported integrations. Its visual selector helps focus monitoring on relevant page elements, while filters reduce noise from timestamps, counters, and other frequently changing content.

The Sealos template provisions one changedetection.io StatefulSet, a 1 GiB persistent volume mounted at `/datastore`, a Service on port 5000, a public HTTPS Ingress, and startup, readiness, and liveness probes. The application stores its settings, watches, snapshots, and history on the persistent volume.

## Common Use Cases

- **Website Change Alerts**: Monitor product pages, policy pages, release notes, and documentation.
- **Price and Availability Tracking**: Watch visible product details and receive change notifications.
- **API and Data Monitoring**: Track JSON endpoints and structured data for meaningful differences.
- **Content Review Workflows**: Preserve snapshot history and inspect changes from the dashboard.

## Dependencies for changedetection.io Hosting

The template includes the application container, persistent storage, Kubernetes networking, health probes, and a Sealos application entry.

### Deployment Dependencies

- [changedetection.io Documentation](https://github.com/dgtlmoon/changedetection.io/wiki) - Configuration and usage guides
- [changedetection.io Source](https://github.com/dgtlmoon/changedetection.io) - Source code, releases, and issue tracker
- [Notification URLs](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes) - Notification provider configuration

### Implementation Details

**Architecture Components:**

- **changedetection.io**: A single StatefulSet serving the dashboard and running scheduled checks on port 5000.
- **Persistent Storage**: A 1 GiB volume mounted at `/datastore`.
- **Public Endpoint**: A Sealos-managed HTTPS Ingress with extended request and response timeouts.
- **Health Checks**: Kubernetes probes use `/worker-health` to verify both the web process and fetch workers.

`BASE_URL` uses the generated Sealos HTTPS address, `FETCH_WORKERS` uses the deployment input, and `HIDE_REFERER` protects the dashboard address when changedetection.io fetches monitored targets.

changedetection.io is licensed under the Apache License 2.0.

## Why Deploy changedetection.io on Sealos?

- **One-Click Deployment**: Create the application, storage, network, and health checks from one template.
- **Persistent Monitoring History**: Keep watches, settings, snapshots, and history across restarts.
- **Automatic HTTPS**: Receive a public domain and TLS certificate through Sealos.
- **Kubernetes Operations**: Inspect logs, storage, network settings, and resources from Sealos Canvas.
- **Validated Starter Resources**: Begin with a live-tested low-load profile and scale with the number and frequency of watches.

## Deployment Guide

1. Open the [changedetection.io template](https://sealos.io/products/app-store/changedetection) and click **Deploy Now**.
2. Keep **Fetch workers** at `10` for a small personal deployment. Choose a lower value for very small workloads or a higher value for more concurrent checks.
3. Click **Deploy** and wait for the StatefulSet to report Ready.
4. Open the changedetection.io application entry shown in Sealos.

## Access and Password Protection

Fresh deployments open the dashboard immediately. changedetection.io uses an optional shared dashboard password:

1. Open **Settings**.
2. In the general application settings, enter a password and save the form.
3. Future visits open `/login`; enter the same password to access the dashboard.

Store this password securely. Every dashboard user signs in with the shared password.

## Add Your First Watch

1. Enter a public webpage or JSON endpoint in the URL field.
2. Select the webpage or restock processor.
3. Click **Watch**.
4. Use **Recheck** to run an immediate check.
5. Open **Edit** to configure filters, check frequency, and notifications.

## Configuration

| Name | Default | Required | Description |
|------|---------|----------|-------------|
| `fetch_workers` | `10` | No | Number of checks that changedetection.io can process concurrently. |

The tested starter profile uses a `100m` CPU limit and `128Mi` memory limit. Increase memory first when the dashboard approaches the memory ceiling, then increase CPU and `fetch_workers` for higher check concurrency.

## Persistence and Scaling

The `/datastore` volume contains application configuration and monitoring history. Back up the persistent volume before migrations or major upgrades.

Keep the StatefulSet at one replica because the scheduler and file-backed datastore share one persistent volume. Scale throughput by increasing CPU, memory, and `fetch_workers`, or by following upstream guidance for a more advanced distributed setup.

## Troubleshooting

### The dashboard is unavailable

Wait for the StatefulSet to become Ready, then verify that the Service has a ready endpoint. Review Pod logs and the `/worker-health` probe status in Sealos Canvas.

### A watch remains in an error state

Confirm that the target is publicly reachable from the application Pod. Review target authentication, TLS, rate limits, anti-bot controls, and the selected fetch method.

### Checks become slow

Inspect CPU and memory usage in Sealos. Increase memory when usage approaches `128Mi`, then increase CPU and `fetch_workers` together for additional concurrency.

### Getting Help

- [changedetection.io Issues](https://github.com/dgtlmoon/changedetection.io/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing terms of the templates repository. changedetection.io is distributed under the [Apache License 2.0](https://github.com/dgtlmoon/changedetection.io/blob/0.55.8/LICENSE).
