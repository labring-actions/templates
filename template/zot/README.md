# Deploy and Host Zot Registry on Sealos

Zot Registry is an OCI-native container image registry for storing and distributing container artifacts. This template deploys Zot `v2.1.14` on Sealos Cloud with built-in basic authentication and two storage backends: local filesystem or S3-compatible object storage.

![Zot Logo](logo.svg)

## About Hosting Zot Registry

Zot provides a lightweight OCI registry implementation with a web UI and registry APIs, making it suitable for private image hosting, edge distribution, and internal CI/CD artifact workflows. It supports standard Docker/OCI push and pull operations, while keeping operational complexity low.

This Sealos template supports two runtime profiles. In `filesystem` mode, Zot runs as a StatefulSet with persistent storage for registry data. In `objectstorage` mode, Zot runs as a Deployment backed by a Sealos ObjectStorage bucket, while still exposing the same public HTTPS endpoint and `/v2/` API behavior.

The deployment enables basic auth and access-control policies by default, configures health probes (`/livez`, `/readyz`, `/startupz`), and publishes the service through Sealos-managed ingress with TLS.

## Common Use Cases

- **Private Team Registry**: Host internal base images and application images for development and production pipelines.
- **CI/CD Artifact Distribution**: Push build outputs from CI jobs and pull them in deployment stages.
- **Edge and Homelab Registry**: Run a lightweight OCI registry for distributed or resource-constrained environments.
- **Air-Gapped or Controlled Environments**: Mirror and serve approved images from a controlled registry endpoint.
- **OCI Artifact Hub**: Store not only images but also OCI-compatible artifacts for platform tooling.

## Dependencies for Zot Registry Hosting

The Sealos template includes all required dependencies for Zot runtime:

- Zot core service (`ghcr.io/project-zot/zot:v2.1.14`)
- Service + Ingress with HTTPS exposure
- Built-in basic authentication and repository access-control policy
- Optional Sealos ObjectStorage bucket (when `zot_storage_backend=objectstorage`)
- Persistent volume claim (when `zot_storage_backend=filesystem`)

### Deployment Dependencies

- [Zot Official Website](https://zotregistry.dev/) - Project overview and docs entry
- [Zot GitHub Repository](https://github.com/project-zot/zot) - Source code and releases
- [Zot Examples](https://github.com/project-zot/zot/tree/main/examples) - Reference configuration files
- [Sealos Documentation](https://sealos.io/docs) - Platform usage and operations

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Zot Workload**:
  - `StatefulSet` in `filesystem` mode
  - `Deployment` in `objectstorage` mode
- **Service**: Exposes port `5000` for Zot API and UI
- **Ingress**: Public HTTPS endpoint with Sealos-managed TLS
- **ObjectStorageBucket** (optional): Created only in object storage mode
- **ConfigMap** (object storage mode): Stores Zot config and htpasswd content

**Configuration:**

- Default generated values:
  - `app_name`, `app_host`
- Runtime storage mode:
  - `filesystem`: persistent local registry data (`1Gi` PVC)
  - `objectstorage`: S3-compatible backend with Sealos ObjectStorage credentials
- Authentication:
  - Basic auth is enabled by default
  - Admin policy grants `read/create/update/delete` to configured admin user
- Public entrypoint:
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- API endpoint:
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`

**License Information:**

Zot is licensed under the [Apache License 2.0](https://github.com/project-zot/zot/blob/main/LICENSE).

## Why Deploy Zot Registry on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes, designed to simplify app delivery and operations. By deploying Zot on Sealos, you get:

- **One-Click Deployment**: Launch a production-ready private registry without writing Kubernetes manifests.
- **Kubernetes-Native Runtime**: Use proven primitives (Service, Ingress, StatefulSet/Deployment) with managed networking.
- **Flexible Storage Choices**: Choose persistent local storage or S3-compatible object storage based on workload needs.
- **Managed HTTPS Access**: Get a public domain and TLS certificates automatically.
- **Easy Day-2 Operations**: Tune resources and behavior from Canvas via AI dialog and resource cards.
- **Pay-as-You-Go Efficiency**: Start small and scale resource usage according to actual traffic.

Deploy Zot on Sealos and focus on shipping artifacts instead of managing infrastructure.

## Deployment Guide

1. Open the [Zot template](https://sealos.io/products/app-store/zot) and click **Deploy Now**.
2. Configure parameters in the popup dialog:
   - `zot_storage_backend`: `filesystem` or `objectstorage`
   - `zot_admin_user`
   - If `filesystem`: set `zot_admin_password`
   - If `objectstorage`: set `zot_admin_htpasswd_hash` and optional `zot_s3_region`
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas. For later changes, describe requirements in the AI dialog or edit resources via resource cards.
4. Access Zot:
   - **Web UI**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/`
   - **Registry API**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`
5. Authenticate registry operations with your configured admin credentials.

## Configuration

After deployment, you can configure Zot through:

- **AI Dialog**: Describe required changes and let AI apply updates.
- **Resource Cards**: Modify workload resources, ingress behavior, and storage profile.
- **Registry Clients**: Use Docker/Podman/Skopeo login and push/pull workflows against the generated domain.

### Template Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| `zot_storage_backend` | Storage backend (`filesystem` or `objectstorage`) | Yes |
| `zot_admin_user` | Admin username for basic auth | Yes |
| `zot_admin_password` | Admin password (filesystem mode only) | Conditional |
| `zot_admin_htpasswd_hash` | Admin htpasswd hash, not plain password (objectstorage mode only) | Conditional |
| `zot_s3_region` | S3 region for object storage mode | Conditional |

## Scaling

To scale Zot resources:

1. Open your deployment in Canvas.
2. Select the Zot workload resource card (StatefulSet or Deployment).
3. Adjust CPU/Memory resources and apply changes.
4. For object storage mode, scale the Deployment replica count as needed and validate client behavior.

## Troubleshooting

### Common Issues

**Issue: Pod restarts immediately in object storage mode**
- Cause: Incompatible storage extension settings or invalid object storage configuration.
- Solution: Ensure object storage mode uses compatible search settings and valid S3 parameters from template defaults/inputs.

**Issue: `UNAUTHORIZED` when calling `/v2/`**
- Cause: Missing/incorrect basic auth credentials.
- Solution: Verify admin credentials and re-run registry login from your client.

**Issue: Auth works in filesystem mode but not in object storage mode**
- Cause: `zot_admin_htpasswd_hash` was provided as plain text instead of hash.
- Solution: Provide a bcrypt or SHA-crypt htpasswd hash (for example, generated by `htpasswd -nB <user>`).

**Issue: Push fails for large layers**
- Cause: Client-side limits or workload resource constraints.
- Solution: Increase workload resources in Canvas and retry push.

### Getting Help

- [Zot Documentation](https://zotregistry.dev/)
- [Zot GitHub Issues](https://github.com/project-zot/zot/issues)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Zot Configuration Examples](https://github.com/project-zot/zot/tree/main/examples)
- [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec)
- [Skopeo Documentation](https://github.com/containers/skopeo)

## License

This Sealos template follows the templates repository license policy. Zot itself is licensed under the [Apache License 2.0](https://github.com/project-zot/zot/blob/main/LICENSE).
