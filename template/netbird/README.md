# Deploy and Host NetBird on Sealos

NetBird is a WireGuard-based zero-trust networking platform for secure private connectivity across distributed devices. This template deploys a production-ready, self-hosted NetBird control plane on Sealos Cloud with embedded identity provider support, signaling, and relay services.

## About Hosting NetBird

NetBird provides a modern control plane for private networking, including peer management, policy control, signaling, and relay capabilities. In this template, NetBird runs with the built-in (embedded) identity provider, so you do not need to integrate an external OIDC provider for basic deployment.

The deployment includes four main runtime services: Dashboard, Management, Signal, and Relay. It uses persistent storage for Management and Signal state, auto-generated TLS ingress domains, and a separated gRPC domain for gRPC traffic to avoid HTTP/gRPC protocol conflicts on the same Sealos ingress host.

By default, this template follows a relay-first approach and does not provision an internal TURN server with dynamic public port ranges. If your environment requires TURN, you can configure an external TURN service through template inputs.

## Common Use Cases

- **Remote Team Access**: Build a secure private network for distributed teams and internal services.
- **Multi-Cloud Private Networking**: Connect workloads across cloud providers and on-prem nodes with unified policy control.
- **Homelab and Edge Connectivity**: Securely manage devices across home labs, branch offices, and edge locations.
- **Service-to-Service Isolation**: Enforce zero-trust connectivity rules between internal services.
- **Self-Hosted VPN Replacement**: Replace traditional VPN concentrators with WireGuard-based peer networking.

## Dependencies for NetBird Hosting

The Sealos template includes all required runtime components for a self-hosted NetBird control plane:

- NetBird Dashboard
- NetBird Management
- NetBird Signal
- NetBird Relay
- Embedded IdP (inside Management)
- Persistent volumes for stateful services

### Deployment Dependencies

- [NetBird Documentation](https://docs.netbird.io/)
- [NetBird Self-Hosted Guide](https://docs.netbird.io/selfhosted/selfhosted-guide)
- [NetBird Local Identity Provider](https://docs.netbird.io/selfhosted/identity-providers/local)
- [NetBird GitHub Repository](https://github.com/netbirdio/netbird)
- [WireGuard Documentation](https://www.wireguard.com/)

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Dashboard (`netbirdio/dashboard:v2.31.0`)**: Web UI for administration and user onboarding.
- **Management (`netbirdio/management:0.64.5`)**: Core API, embedded IdP, and control-plane logic.
- **Signal (`netbirdio/signal:0.64.5`)**: Signaling service for peer coordination.
- **Relay (`netbirdio/relay:0.64.5`)**: Relay transport endpoint for constrained network paths.

**Ingress and Domain Routing:**

- **Primary HTTPS domain** (`${app_host}.${SEALOS_CLOUD_DOMAIN}`):
  - `/` -> Dashboard
  - `/api`, `/oauth2`, `/ws-proxy/management` -> Management
  - `/ws-proxy/signal` -> Signal
  - `/relay` -> Relay
- **Dedicated gRPC domain** (`${grpc_host}.${SEALOS_CLOUD_DOMAIN}`):
  - `/management.ManagementService/` -> Management gRPC
  - `/signalexchange.SignalExchange/` -> Signal gRPC

Using a dedicated gRPC host is required because Sealos ingress cannot reliably serve both HTTP and gRPC protocols on the same host with mixed backend protocol settings.

**Resource Defaults (Current Template):**

- Each runtime container uses:
  - **limits**: `cpu: 200m`, `memory: 256Mi`
  - **requests**: `cpu: 20m`, `memory: 25Mi`

**Storage:**

- Management StatefulSet: `100Mi` PVC (`/var/lib/netbird`)
- Signal StatefulSet: `100Mi` PVC (`/var/lib/netbird`)

## Why Deploy NetBird on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies app delivery from deployment to day-2 operations. By deploying NetBird on Sealos, you get:

- **One-Click Deployment**: Deploy a multi-service NetBird control plane quickly without writing Kubernetes manifests.
- **Automatic HTTPS Access**: Public TLS domains are provisioned automatically for dashboard and APIs.
- **Seamless Runtime Operations**: Use Canvas resource cards and AI dialog to adjust configuration and resources.
- **Kubernetes Reliability**: Leverage StatefulSet/Deployment primitives and persistent volumes by default.
- **Easy Horizontal and Vertical Scaling**: Increase replicas and resource limits from Sealos UI when usage grows.
- **No External IdP Requirement by Default**: Embedded IdP lowers setup complexity for self-hosted teams.

Deploy NetBird on Sealos and focus on network policy and access governance instead of infrastructure plumbing.

## Deployment Guide

1. Visit [NetBird Template Page](https://sealos.io/products/app-store/netbird)
2. Click **Deploy Now**.
3. Configure required parameters:
   - `disable_default_policy`
   - Optional external TURN parameters (`external_turn_host`, `external_turn_username`, `external_turn_password`)
4. Wait for deployment to complete (typically 2-3 minutes).
5. Open the generated application URL from Canvas.
6. Create the initial admin account in Dashboard and complete onboarding.

## Configuration

You can update this deployment after installation through:

- **AI Dialog in Canvas**: Describe required changes and apply.
- **Resource Cards**: Edit Deployments, StatefulSets, Services, and Ingress resources directly.

### Input Parameters

- **`disable_default_policy`**: Disable the default all-to-all policy (`true`/`false`).
- **`external_turn_host`**: Optional TURN endpoint (`host:port`) such as `turn.example.com:3478`.
- **`external_turn_username`**: TURN username (required when external TURN is set).
- **`external_turn_password`**: TURN password (required when external TURN is set).

### External TURN Notes

- If `external_turn_host` is empty, TURN/STUN entries are omitted from management config.
- If you need TURN for strict NAT environments, provide a stable external TURN endpoint instead of relying on dynamic NodePort port-range mapping.

## Scaling

To scale the deployment:

1. Open the application Canvas.
2. Select the relevant resource card (`Deployment` or `StatefulSet`).
3. Adjust replicas or CPU/Memory values.
4. Apply and monitor rollout status.

## Troubleshooting

### Common Issues

**Issue: "There was an error logging you in. Error: Unauthenticated" after admin signup**
- Cause: Embedded IdP path or issuer routing mismatch.
- Check:
  - `https://<app-host>/oauth2/.well-known/openid-configuration` should return `200`.
  - Management ingress includes `/oauth2` path to Management service.
  - Dashboard `AUTH_AUTHORITY` points to `https://<app-host>/oauth2`.

**Issue: Dashboard loads but peers cannot connect reliably**
- Cause: Network path constraints requiring TURN.
- Solution: Configure an external TURN server via template inputs.

**Issue: gRPC calls fail while HTTP UI works**
- Cause: gRPC and HTTP host/protocol mismatch.
- Solution:
  - Ensure the dedicated gRPC domain is configured and resolvable.
  - Verify gRPC ingress uses `nginx.ingress.kubernetes.io/backend-protocol: GRPC`.

### Getting Help

- [NetBird Docs](https://docs.netbird.io/)
- [NetBird GitHub Issues](https://github.com/netbirdio/netbird/issues)
- [NetBird Community](https://netbird.io/community/)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [NetBird Architecture](https://docs.netbird.io/about-netbird/architecture)
- [NetBird Peer and Route Management](https://docs.netbird.io/how-to/manage-peers)
- [WireGuard Protocol Overview](https://www.wireguard.com/protocol/)

## License

This Sealos template is provided under the repository license policy of the Sealos templates project. NetBird itself is licensed under the [BSD-3-Clause License](https://github.com/netbirdio/netbird/blob/main/LICENSE).
