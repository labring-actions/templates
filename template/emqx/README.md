# Deploy and Host EMQX on Sealos

EMQX is an open-source MQTT broker for IoT, industrial telemetry, and connected-device messaging. This template deploys EMQX Community Edition `5.8.9` as a three-node StatefulSet with DNS cluster discovery and per-node persistent data and log volumes.

![EMQX Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/emqx/website-screenshot.webp)

## About Hosting EMQX

EMQX provides MQTT, MQTT over TLS, MQTT over WebSocket, a management REST API, and a browser Dashboard. The template uses the official open-source `emqx/emqx:5.8.9` image and keeps three replicas because an odd member count provides a practical clustered baseline.

The Dashboard receives a generated HTTPS address. Public MQTT WebSocket and NodePort listeners are explicit deployment choices.

## What Gets Deployed

| Component | Purpose | Default profile |
| --- | --- | --- |
| EMQX StatefulSet | Three clustered broker nodes | 500m CPU / 512 MiB per node |
| Headless Service | Stable DNS SRV discovery for Erlang distribution | Internal |
| ClusterIP Service | Dashboard and MQTT WebSocket backends | Internal |
| Dashboard Ingress | Public HTTPS Dashboard | Enabled |
| MQTT WebSocket Ingress | Public `wss://.../mqtt` endpoint | Controlled by `WS_ENABLE` |
| MQTT NodePort Service | MQTT, TLS, WS, and WSS ports | Controlled by `TCP_ENABLE` |
| Persistent volumes | `/opt/emqx/data` and `/opt/emqx/log` | Two 1 GiB volumes per node |

Resource requests are 50m CPU and 51 MiB memory per broker node.

## Deployment Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `ADMIN_PASSWORD` | Required | Initial password for the Dashboard `admin` account; use 8-64 characters. |
| `WS_ENABLE` | `false` | Publishes MQTT over WebSocket at `wss://<app-host>/mqtt`. |
| `TCP_ENABLE` | `false` | Creates a NodePort service for ports 1883, 8883, 8083, and 8084. |

## Account and Security

The Dashboard username is `admin`, and its initial password comes from the required `ADMIN_PASSWORD` input. Change this password after the first login.

A fresh EMQX CE installation accepts unauthenticated MQTT clients under its default listener policy. Configure MQTT authentication and authorization in the Dashboard before enabling `WS_ENABLE` or `TCP_ENABLE` for production traffic.

## Deployment Guide

1. Open the [EMQX template](https://sealos.io/products/app-store/emqx) and select **Deploy Now**.
2. Set a strong `ADMIN_PASSWORD`.
3. Keep `WS_ENABLE=false` and `TCP_ENABLE=false` while configuring broker authentication.
4. Wait for all three StatefulSet pods to become ready and form one cluster.
5. Open the generated HTTPS URL and sign in as `admin`.
6. Configure MQTT authentication and authorization, then enable the required public listener during a controlled redeployment.

## Client Endpoints

- **Dashboard**: `https://<app-host>.<region-domain>/`
- **MQTT WebSocket**: `wss://<app-host>.<region-domain>/mqtt` when `WS_ENABLE=true`
- **MQTT TCP/TLS**: Use the NodePort mappings shown by Sealos when `TCP_ENABLE=true`

## Configuration

- **EMQX Dashboard**: Manage listeners, authentication, authorization, clients, rules, connectors, and cluster settings.
- **REST API**: Use `/api/v5` on the Dashboard hostname with a Dashboard access token.
- **Sealos Canvas**: Inspect logs, cluster pods, services, ingress routes, metrics, and persistent volumes.
- **Cluster discovery**: DNS SRV records from the headless Service connect the three stable pod hostnames.

## Scaling

The template fixes the initial topology at three replicas. Plan any later topology change together with MQTT session behavior, persistent-volume ownership, rolling-update order, and client reconnection tests.

The validated memory floor is 512 MiB per node. A 256 MiB cold-start candidate repeatedly reached OOMKilled with exit code 137; the 512 MiB profile formed a three-node cluster with zero restarts.

## Validated Runtime

All three nodes joined the same cluster and appeared as running through both `emqx ctl cluster status` and the authenticated `/api/v5/nodes` endpoint. Dashboard authentication reported EMQX `5.8.9` Community Edition.

With `WS_ENABLE=true`, two external TLS WebSocket clients completed MQTT v5 subscribe and publish operations at QoS 1. The received topic and payload hash matched the published values. An authenticated unknown REST path returned HTTP 404.

## Troubleshooting

### A broker pod stays unready

Check `emqx ctl status`, pod restart reasons, and memory metrics. Confirm that all pods resolve the headless Service and share the same node cookie.

### Dashboard login fails

Use username `admin` and the password supplied through `ADMIN_PASSWORD`. An administrator can reset Dashboard users with the EMQX CLI when required.

### MQTT clients cannot connect

Confirm the selected public listener input, endpoint type, port mapping, TLS mode, WebSocket path, and configured MQTT authentication policy.

## Resources

- [EMQX Documentation](https://docs.emqx.com/en/emqx/latest/)
- [EMQX 5.8.9 Release](https://github.com/emqx/emqx/releases/tag/v5.8.9)
- [Official Helm Values](https://github.com/emqx/emqx/blob/v5.8.9/deploy/charts/emqx/values.yaml)
- [EMQX Dashboard Guide](https://docs.emqx.com/en/emqx/latest/dashboard/introduction.html)
- [Sealos Documentation](https://sealos.io/docs)

## License

EMQX `5.8.9` Community Edition is distributed under Apache License 2.0. This template follows the Sealos templates repository license.
