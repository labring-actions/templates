# Deploy and Host Pocket ID on Sealos

Pocket ID is a simple OIDC provider that authenticates users with passkeys instead of passwords. This template deploys Pocket ID as a production-ready, persistent service on Sealos Cloud.

## About Hosting Pocket ID

Pocket ID is designed for teams and individuals who want lightweight, self-hosted identity with modern passkey-based authentication. It provides OpenID Connect (OIDC) endpoints that your internal or public applications can use for secure sign-in.

This Sealos template deploys Pocket ID as a single StatefulSet with persistent storage mounted at `/app/data`, so identity data survives pod restarts and updates. Public access is exposed through Sealos-managed HTTPS ingress with automatic TLS, and runtime configuration is injected through template inputs and environment variables.

## Common Use Cases

- **Self-Hosted SSO for Internal Tools**: Use Pocket ID as an OIDC provider for dashboards, admin panels, and engineering tools.
- **Passkey-First Authentication**: Replace password-based login flows with phishing-resistant passkeys.
- **Homelab or SMB Identity Gateway**: Centralize authentication for multiple self-hosted services with minimal setup complexity.
- **Developer Environments**: Provide consistent OIDC auth in staging or test clusters.

## Dependencies for Pocket ID Hosting

The Sealos template includes all required runtime dependencies for Pocket ID:

- Pocket ID application container
- Kubernetes `StatefulSet` for stable identity and storage binding
- Kubernetes `Service` for internal traffic routing
- Kubernetes `Ingress` with TLS for public HTTPS access
- Persistent Volume Claim (PVC) for `/app/data`

### Deployment Dependencies

- [Pocket ID Website](https://pocket-id.org) - Product overview and release information
- [Pocket ID Documentation](https://docs.pocket-id.org) - Setup and configuration guides
- [Pocket ID GitHub Repository](https://github.com/pocket-id/pocket-id) - Source code and issue tracking
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) - OIDC protocol reference

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Pocket ID StatefulSet** (`ghcr.io/pocket-id/pocket-id:v2.2.0`): Main identity provider service (1 replica)
- **Service**: Exposes container port `1411` to cluster networking
- **Ingress**: Publishes `https://<app_host>.<SEALOS_CLOUD_DOMAIN>` with TLS enabled
- **Persistent Storage**: `1Gi` PVC mounted to `/app/data` for durable application state

**Configuration:**

- `APP_URL` is generated from `app_host` and Sealos domain settings.
- `ENCRYPTION_KEY` is injected from a template variable (randomized by default).
- `TRUST_PROXY` defaults to `false`.
- Default resource profile per pod:
  - **limits**: `cpu: 200m`, `memory: 256Mi`
  - **requests**: `cpu: 20m`, `memory: 25Mi`

**License Information:**

Pocket ID is licensed under the [BSD 2-Clause License](https://github.com/pocket-id/pocket-id/blob/main/LICENSE).

## Why Deploy Pocket ID on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, operations, and iteration in one workspace. By deploying Pocket ID on Sealos, you get:

- **One-Click Deployment**: Launch Pocket ID without manually writing Kubernetes manifests.
- **Kubernetes Reliability**: Run on proven StatefulSet, Service, and Ingress primitives.
- **Easy Day-2 Operations**: Use Canvas resource cards and AI dialog to tune resources and settings.
- **Persistent Storage Included**: Keep identity data durable across restarts.
- **Instant Public HTTPS Access**: Get a public URL with managed TLS by default.
- **Cost-Efficient Scaling**: Use pay-as-you-go compute and storage based on actual usage.

## Deployment Guide

1. Open the [Pocket ID template](https://sealos.io/appstore/pocket-id) and click **Deploy Now**.
2. Configure deployment parameters:
   - `app_host`
   - `app_name`
   - `encryption_key`
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas.
4. Open the generated Pocket ID URL from Canvas and complete your initial provider setup.

## Configuration

After deployment, you can manage Pocket ID through:

- **AI Dialog**: Describe the change you want and let AI apply updates.
- **Resource Cards**: Click StatefulSet, Service, Ingress, or storage cards to adjust settings.

### Template Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `app_host` | Public hostname prefix used for the Pocket ID URL | `pocket-id-<random>` |
| `app_name` | Kubernetes resource name prefix for this deployment | `pocket-id-<random>` |
| `encryption_key` | Application encryption key used by Pocket ID | Random 32-character value |

### Operational Notes

- Keep `encryption_key` stable after first deployment to avoid cryptographic/session issues.
- This template is configured as a single-replica StatefulSet to preserve state consistency.

## Scaling

To scale Pocket ID on Sealos:

1. Open your Pocket ID deployment in Canvas.
2. Click the StatefulSet resource card.
3. Adjust CPU and memory limits/requests as needed.
4. Apply the change and monitor rollout status.

For storage growth, edit the PVC capacity from the storage-related resource card. For most deployments, keep replicas at `1` unless you have validated an HA strategy for your identity workload.

## Troubleshooting

### Common Issues

**Issue: OIDC callbacks fail or redirect URIs look incorrect**
- Cause: `APP_URL` does not match the actual public URL.
- Solution: Verify `app_host` and ingress host settings, then redeploy or update configuration.

**Issue: Users cannot decrypt data or sessions break after update**
- Cause: `encryption_key` was changed after initialization.
- Solution: Restore the original key value and restart the pod.

**Issue: Service URL is not reachable immediately after deployment**
- Cause: DNS and ingress provisioning may still be propagating.
- Solution: Wait a few minutes, then retry access from Canvas.

### Getting Help

- [Pocket ID Documentation](https://docs.pocket-id.org)
- [Pocket ID GitHub Issues](https://github.com/pocket-id/pocket-id/issues)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [Pocket ID Demo](https://demo.pocket-id.org)
- [Pocket ID Project Site](https://pocket-id.org)
- [OIDC Discovery Endpoint Basics](https://openid.net/specs/openid-connect-discovery-1_0.html)

## License

This Sealos template is provided under the repository license policy of the Sealos templates project. Pocket ID itself is licensed under the [BSD 2-Clause License](https://github.com/pocket-id/pocket-id/blob/main/LICENSE).
