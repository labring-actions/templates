# Deploy and Host Harbor on Sealos

Harbor is an open-source OCI artifact registry that helps secure software supply chains with access control, image signing, and vulnerability scanning. This template deploys Harbor v2.14.0 with managed PostgreSQL, managed Redis, and object storage integration on Sealos Cloud.

![Harbor Logo](logo.png)

## About Hosting Harbor

Harbor provides a private container registry for storing and distributing OCI images and artifacts, with role-based access control, project isolation, and policy-driven governance. It also includes built-in vulnerability scanning and replication features to support production software delivery workflows.

This Sealos template deploys Harbor as a multi-component application: `core`, `portal`, `jobservice`, `registry`, `registryctl`, and `trivy`. The platform provisions PostgreSQL and Redis through KubeBlocks, creates an ObjectStorage bucket for registry backend storage, and exposes Harbor over HTTPS ingress.

The deployment uses path-based routing on one public domain, where UI traffic goes to the portal and API/registry paths are routed to Harbor core. You can continue day-2 operations in Canvas through AI dialog and resource cards.

## Common Use Cases

- **Private Container Registry**: Host internal images and OCI artifacts for development and production pipelines.
- **Supply Chain Security**: Scan images with Trivy and apply project policies before promotion.
- **Multi-Team Governance**: Isolate projects and enforce role-based access across engineering teams.
- **Registry Replication**: Replicate artifacts between Harbor instances or external registries for hybrid/multi-region delivery.
- **SBOM and Signature Workflows**: Store and manage signed artifacts in a centralized registry platform.

## Dependencies for Harbor Hosting

The Sealos template includes all required dependencies for a production-ready Harbor deployment:

- Harbor component services (`core`, `portal`, `jobservice`, `registry`, `registryctl`, `trivy`)
- KubeBlocks-managed PostgreSQL `16.4.0`
- KubeBlocks-managed Redis `7.2.7` (replication + sentinel topology)
- Sealos ObjectStorage bucket and credentials wiring for registry blob storage
- Kubernetes ingress, services, and persistent volumes

### Deployment Dependencies

- [Harbor Official Website](https://goharbor.io/) - Product overview and project links
- [Harbor Documentation](https://goharbor.io/docs/) - Installation, administration, and operations
- [Harbor GitHub Repository](https://github.com/goharbor/harbor) - Source code and issue tracking
- [Sealos Documentation](https://sealos.io/docs) - Platform usage and operations

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Harbor Core** (`goharbor/harbor-core:v2.14.0`): API, auth, token service, and control-plane logic
- **Harbor Portal** (`goharbor/harbor-portal:v2.14.0`): Web UI frontend
- **Harbor Jobservice** (`goharbor/harbor-jobservice:v2.14.0`): Background jobs (replication, scans, GC-related workflows)
- **Harbor Registry** (`goharbor/registry-photon:v2.14.0`): OCI registry service with S3-compatible backend
- **Harbor Registry Controller** (`goharbor/harbor-registryctl:v2.14.0`): Registry control-plane helper
- **Harbor Trivy Adapter** (`goharbor/trivy-adapter-photon:v2.14.0`): Vulnerability scanning service
- **PostgreSQL Cluster**: Metadata and Harbor application data storage
- **Redis Cluster + Sentinel**: Job queue/cache and coordination
- **Object Storage Bucket**: Durable blob storage for image layers/artifacts

**Configuration:**

- Required deployment input:
  - `harbor_admin_password`: Initial password for Harbor `admin` user
- Auto-generated defaults:
  - `app_name`, `app_host`, and internal Harbor/registry secret values
- Public entrypoint:
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- Path routing:
  - `/` routes to Harbor portal
  - `/api/`, `/service/`, `/v2/`, `/c/` route to Harbor core

**License Information:**

Harbor is licensed under the [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE).

## Why Deploy Harbor on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies the full lifecycle from deployment to day-2 operations. By deploying Harbor on Sealos, you get:

- **One-Click Deployment**: Launch a multi-service Harbor stack without writing Kubernetes manifests manually.
- **Kubernetes-Native Reliability**: Run Harbor on proven Kubernetes primitives with managed ingress and service discovery.
- **Built-In Persistent Storage**: Keep metadata, queue state, job logs, and scanner cache durable across restarts.
- **Managed HTTPS Access**: Get a public URL with TLS certificates automatically handled by the platform.
- **Easy Day-2 Operations**: Update resources from Canvas via AI dialog or resource cards.
- **Cost Efficiency**: Use pay-as-you-go resources and scale based on actual registry workload.

Deploy Harbor on Sealos and focus on artifact governance instead of infrastructure management.

## Deployment Guide

1. Open the [Harbor template](https://sealos.io/products/app-store/harbor) and click **Deploy Now**.
2. Configure the required parameter in the popup dialog:
   - `harbor_admin_password` (used for the initial `admin` login)
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas. For later changes, describe requirements in the AI dialog or edit specific resources via resource cards.
4. Access Harbor:
   - **Web UI**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
   - **Registry API**: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`
5. Sign in with:
   - Username: `admin`
   - Password: value provided in `harbor_admin_password`

## Configuration

After deployment, you can configure Harbor through:

- **AI Dialog**: Describe required changes and let AI apply updates.
- **Resource Cards**: Modify Deployments/StatefulSets, services, ingress, and storage settings.
- **Harbor Admin UI**: Manage projects, users, robot accounts, retention, and replication rules.

### Template Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| `harbor_admin_password` | Initial password for Harbor `admin` user | Yes |

## Scaling

To scale Harbor resources:

1. Open your deployment in Canvas.
2. Adjust resources on relevant component cards (for example: `core`, `jobservice`, `registry`, `trivy`).
3. Apply changes and monitor rollout status.
4. For higher throughput, increase CPU/memory for `registry` and `jobservice` first, then tune `core` and `redis`/`postgresql` capacity as needed.

## Troubleshooting

### Common Issues

**Issue: Cannot log in as `admin` after deployment**
- Cause: Incorrect initial password entry or forgotten configured value.
- Solution: Verify the `harbor_admin_password` value used during deployment and reset admin credentials through Harbor recovery procedures if required.

**Issue: Image push fails with payload/proxy size errors**
- Cause: Large layers exceed default ingress body-size settings for your use case.
- Solution: Update ingress/body-size related settings from Canvas resource cards and retry push.

**Issue: Vulnerability scan jobs are delayed or stuck**
- Cause: Trivy database sync or scanner backlog under limited resources.
- Solution: Check `trivy` pod logs, verify outbound network access, and increase scanner resources if needed.

**Issue: Harbor URL is not reachable immediately**
- Cause: Ingress provisioning or DNS propagation is still completing.
- Solution: Wait a few minutes, then refresh the URL from Canvas.

### Getting Help

- [Harbor Documentation](https://goharbor.io/docs/)
- [Harbor GitHub Issues](https://github.com/goharbor/harbor/issues)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Harbor Installation and Configuration](https://goharbor.io/docs/main/install-config/)
- [Harbor Administration Guide](https://goharbor.io/docs/main/administration/)
- [Harbor Artifact Replication](https://goharbor.io/docs/main/administration/configuring-replication/)
- [Harbor Vulnerability Scanning](https://goharbor.io/docs/main/administration/vulnerability-scanning/)

## License

This Sealos template follows the templates repository license policy. Harbor itself is licensed under the [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE).
