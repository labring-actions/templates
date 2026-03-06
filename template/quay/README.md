# Deploy and Host Project Quay on Sealos

Project Quay is an enterprise container registry for storing, securing, and distributing OCI images. This template deploys Quay with PostgreSQL, Redis, persistent storage, and automated initial admin bootstrap on Sealos Cloud.

## About Hosting Project Quay

Project Quay provides a secure private registry with repository management, robot accounts, vulnerability and metadata services, and API-driven automation for CI/CD pipelines. In this template, Quay runs as a StatefulSet with persistent storage mounted at `/datastorage` for image layer and metadata durability.

The deployment also provisions a managed PostgreSQL 16.4.0 cluster (Kubeblocks) and a managed Redis 7.2.7 replication topology with Sentinel for caching and queue-related functions. A PostgreSQL init job enables required extensions, and an admin-init job automatically creates the first Quay administrator account during first deployment.

Sealos automatically provides a public HTTPS domain and ingress routing to the Quay web/API endpoint, so you can start pushing and pulling images without manual ingress or certificate setup.

## Common Use Cases

- **Private Container Registry**: Host internal images for development, staging, and production.
- **CI/CD Image Distribution**: Store build artifacts and integrate with automated pipelines.
- **Multi-Team Repository Governance**: Manage team/org access with controlled permissions.
- **Secure Image Delivery**: Serve images over HTTPS with centralized registry access.
- **Self-Hosted Registry Migration**: Move from ad-hoc registry setups to a managed Kubernetes-native deployment.

## Dependencies for Project Quay Hosting

The Sealos template includes all required dependencies for a production-ready single-instance Quay deployment:

- Project Quay (`quay.io/projectquay/quay:v3.9.8`)
- PostgreSQL 16.4.0 (Kubeblocks cluster)
- Redis 7.2.7 with Sentinel (Kubeblocks cluster)
- Persistent volume for registry data
- Kubernetes Ingress with TLS termination

### Deployment Dependencies

- [Project Quay Documentation](https://docs.projectquay.io/) - Official Quay docs
- [Project Quay GitHub Repository](https://github.com/quay/quay) - Source code and issue tracker
- [OCI Distribution Spec](https://github.com/opencontainers/distribution-spec) - Registry protocol reference
- [Sealos Documentation](https://sealos.io/docs) - Platform and operations guidance

## Implementation Details

### Architecture Components

This template deploys the following components:

- **Quay StatefulSet**: Main registry service (UI + API + registry endpoints) exposed through Ingress.
- **PostgreSQL Cluster**: Metadata and application database backend.
- **PostgreSQL Init Job**: Enables `pg_trgm` extension required by Quay features.
- **Redis Cluster (Replication + Sentinel)**: Cache/event and queue-related backend for Quay runtime services.
- **Admin Initialization Job**: Waits for Quay health endpoint and initializes the first admin user via API.
- **Persistent Storage**: Registry data persisted at `/datastorage/registry` via PVC.

### Configuration

- Quay is configured at runtime by generating `config.yaml` from environment variables and secret references.
- Health probes use HTTP on port `8080` (`/health/instance`, `/health/endtoend`).
- TLS is terminated at Sealos Ingress (`EXTERNAL_TLS_TERMINATION: true`), while backend service traffic stays HTTP.
- Initial admin inputs are provided during deployment:
  - `initial_admin_username`
  - `initial_admin_password`
  - `initial_admin_email`
- The admin-init job is idempotent: if the database is already initialized, the job exits successfully without overwriting existing users.

### License Information

Project Quay is licensed under the Apache License 2.0.

## Why Deploy Project Quay on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment and operations. By deploying Project Quay on Sealos, you get:

- **One-Click Deployment**: Launch Quay and its dependencies in one workflow.
- **Managed Datastores**: PostgreSQL and Redis are provisioned automatically.
- **Persistent Storage**: Registry data survives restarts and updates.
- **Automatic HTTPS Access**: Public domain and TLS-enabled ingress are created for you.
- **Simple Day-2 Operations**: Update resources and settings through Canvas + AI dialog.
- **Pay-as-You-Go Efficiency**: Run only what you need and scale resources when needed.

## Deployment Guide

1. Open the [Project Quay template](https://sealos.io/products/app-store/quay) and click **Deploy Now**.
2. Configure deployment parameters in the popup, especially:
   - `initial_admin_username`
   - `initial_admin_password`
   - `initial_admin_email`
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas, where you can use the AI dialog or resource cards for later adjustments.
4. Access your application via the generated URL:
   - **Quay Web UI**: `https://<your-app-host>`
   - **Registry/API Endpoint**: same domain, used by Docker/OCI clients and automation
5. Log in with the admin credentials you entered in step 2.

## Configuration

After deployment, you can update Quay using:

- **AI Dialog**: Describe desired config or resource changes in plain language.
- **Resource Cards**: Edit StatefulSet resources, storage, jobs, and networking settings.
- **Quay Admin UI**: Create organizations, repositories, robot accounts, and access policies.

## Scaling

This template is optimized for a single Quay registry instance with persistent local registry storage.

1. Open Canvas for your deployment.
2. Click the Quay StatefulSet resource card.
3. Adjust CPU/Memory resources based on traffic and repository size.
4. Apply changes.

If you need multi-replica registry scaling, use an external/shared object storage strategy and adjust Quay storage configuration accordingly.

## Troubleshooting

### Common Issues

**Issue: Cannot log in after deployment**
- Cause: Admin credentials were not set as expected during deployment.
- Solution: Redeploy with explicit `initial_admin_*` values or reset user credentials through Quay admin/database procedures.

**Issue: Admin init job exits with non-empty database message**
- Cause: Quay database already contains users/data.
- Solution: This is expected behavior; initialization is skipped to avoid overwriting existing accounts.

**Issue: Registry storage write errors**
- Cause: Storage mount or permission mismatch in customized deployments.
- Solution: Ensure registry storage path remains `/datastorage/registry` with writable PVC and correct security context.

### Getting Help

- [Project Quay Docs](https://docs.projectquay.io/)
- [Project Quay Issues](https://github.com/quay/quay/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Quay API and Integration Docs](https://docs.projectquay.io/api/)
- [Quay Security Scanner Overview](https://docs.projectquay.io/solution/georep.html)
- [Sealos App Launch and Management](https://sealos.io/docs)

## License

This Sealos template is provided under MIT License. Project Quay itself is licensed under Apache License 2.0.
