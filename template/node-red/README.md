# Deploy and Host Node-RED on Sealos

Node-RED is a low-code, flow-based programming tool for wiring APIs, devices, and services. This template deploys Node-RED as a persistent, production-ready service on Sealos Cloud.

![Node-RED Logo](logo.png)

## About Hosting Node-RED

Node-RED provides a browser-based editor where you build integrations and automations by connecting visual nodes. It is widely used for IoT workflows, webhook orchestration, data routing, and internal automation tasks.

This Sealos template deploys Node-RED as a single StatefulSet with persistent storage mounted at `/data`, where flows, credentials, and runtime data are stored. Public HTTPS access is provided through Sealos Ingress with platform-managed TLS certificates.

## Common Use Cases

- **Workflow Automation**: Connect SaaS tools, internal APIs, and event streams without writing full backend services.
- **IoT Data Processing**: Collect, transform, and route sensor/device telemetry to databases, queues, or dashboards.
- **Webhook Orchestration**: Receive webhook events, enrich payloads, and trigger downstream business logic.
- **Rapid Integration Prototyping**: Validate new integrations quickly before implementing long-term services.
- **Internal Ops Tooling**: Build lightweight automations for alerting, notifications, and scheduled tasks.

## Dependencies for Node-RED Hosting

The Sealos template includes all required runtime dependencies for Node-RED:

- Node-RED application container
- Kubernetes `StatefulSet` for stable runtime identity
- Kubernetes `Service` for in-cluster traffic routing
- Kubernetes `Ingress` for public HTTPS exposure
- Persistent Volume Claim (PVC) for `/data`

### Deployment Dependencies

- [Node-RED Official Website](https://nodered.org/) - Product overview and community links
- [Node-RED Documentation](https://nodered.org/docs/) - Setup, runtime, and node development docs
- [Node-RED GitHub Repository](https://github.com/node-red/node-red) - Source code and issue tracking
- [Sealos Documentation](https://sealos.io/docs) - Platform usage and operations guides

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Node-RED StatefulSet** (`nodered/node-red:4.1.6`): Main service with `1` replica
- **Service**: Exposes container port `1880` inside the cluster
- **Ingress**: Publishes `https://<app_host>.<SEALOS_CLOUD_DOMAIN>` with TLS enabled
- **Persistent Storage**: `0.1Gi` PVC mounted at `/data`

**Configuration:**

- `app_host` controls the public hostname prefix.
- `app_name` controls Kubernetes resource naming.
- Default pod resources:
  - **limits**: `cpu: 100m`, `memory: 128Mi`
  - **requests**: `cpu: 10m`, `memory: 12Mi`
- Node-RED data persists in `/data`, including flows and credential files.

**License Information:**

Node-RED is licensed under the [Apache License 2.0](https://github.com/node-red/node-red/blob/master/LICENSE).

## Why Deploy Node-RED on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, operations, and day-2 management. By deploying Node-RED on Sealos, you get:

- **One-Click Deployment**: Launch Node-RED without manually writing Kubernetes YAML.
- **Kubernetes Reliability**: Run on proven StatefulSet, Service, and Ingress primitives.
- **Persistent Storage Included**: Keep flows and runtime data durable across restarts.
- **Instant Public HTTPS Access**: Get a public URL with managed TLS certificates.
- **Easy Customization**: Use Canvas dialogs and AI-assisted updates for configuration changes.
- **Cost Efficiency**: Use pay-as-you-go resources and scale based on real usage.

Deploy Node-RED on Sealos and focus on building automations instead of managing infrastructure.

## Deployment Guide

1. Open the [Node-RED template](https://sealos.io/appstore/node-red) and click **Deploy Now**.
2. Configure deployment parameters in the popup dialog:
   - `app_host`
   - `app_name`
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas.
4. Open the generated Node-RED URL from Canvas and start creating flows in the web editor.

## Configuration

After deployment, you can manage Node-RED through:

- **AI Dialog**: Describe configuration or resource changes and let AI apply updates.
- **Resource Cards**: Open StatefulSet, Service, Ingress, or storage cards to modify settings.
- **Node-RED Editor**: Import/export flows and configure nodes directly in the web UI.

### Template Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `app_host` | Public hostname prefix used for Node-RED URL | `node-red-<random>` |
| `app_name` | Kubernetes resource name prefix for this deployment | `node-red-<random>` |

## Scaling

To scale Node-RED resources:

1. Open your deployment in Canvas.
2. Click the Node-RED StatefulSet resource card.
3. Adjust CPU and memory limits/requests.
4. Apply the change and monitor rollout status.

For most flow-based automation workloads, start with vertical scaling (CPU and memory) before considering replica changes.

## Troubleshooting

### Common Issues

**Issue: Node-RED URL is not reachable immediately after deployment**
- Cause: Ingress provisioning or DNS propagation is still in progress.
- Solution: Wait a few minutes, then refresh the URL from Canvas.

**Issue: Flows or credentials are missing after restart**
- Cause: `/data` was not persisted correctly or storage settings were changed unexpectedly.
- Solution: Verify PVC binding status and confirm the volume is mounted at `/data`.

**Issue: Editor is publicly accessible without expected login controls**
- Cause: Node-RED does not enforce admin authentication unless configured.
- Solution: Configure `adminAuth` in Node-RED settings and redeploy with secured runtime settings.

### Getting Help

- [Node-RED Documentation](https://nodered.org/docs/)
- [Node-RED Forum](https://discourse.nodered.org/)
- [Node-RED GitHub Issues](https://github.com/node-red/node-red/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Node-RED Flows Library](https://flows.nodered.org/)
- [Node-RED Getting Started](https://nodered.org/docs/getting-started/)
- [Node-RED User Guide](https://nodered.org/docs/user-guide/)
- [Node-RED Docker Guide](https://nodered.org/docs/getting-started/docker)

## License

This Sealos template is provided under the templates repository license policy. Node-RED itself is licensed under the [Apache License 2.0](https://github.com/node-red/node-red/blob/master/LICENSE).
