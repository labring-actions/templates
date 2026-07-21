# Deploy and Host Gitea on Sealos

Gitea is a lightweight, self-hosted Git service for source code, issues, pull requests, packages, releases, and automation. This template deploys Gitea 1.27.0 on Sealos with persistent repositories, HTTPS ingress, and optional managed MySQL and S3-compatible object storage.

![Gitea Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gitea/website-screenshot.webp)

## About Hosting Gitea

Gitea runs as a single stateful application with persistent volumes for `/var/lib/gitea` and `/etc/gitea`. The default deployment provisions a KubeBlocks MySQL 8 cluster for application metadata. A SQLite option is available for smaller personal installations.

Repository data stays on the persistent volume. The optional Sealos object storage branch stores Gitea attachments, avatars, LFS objects, packages, release assets, and Actions artifacts in a private S3-compatible bucket while Gitea serves authorized downloads through the application.

## Common Use Cases

- **Private Git hosting**: Host personal, team, or internal repositories.
- **Code collaboration**: Manage issues, pull requests, milestones, and releases.
- **Package distribution**: Publish packages and release attachments from the same service.
- **Automation**: Run Gitea Actions workflows with separately configured runners.

## Dependencies for Gitea Hosting

- **Gitea**: `docker.gitea.com/gitea:1.27.0-rootless`
- **Database**: KubeBlocks MySQL `ac-mysql-8.0.30-1` by default, or embedded SQLite
- **Persistent storage**: Separate volumes for Gitea data and configuration
- **Optional object storage**: Private Sealos S3-compatible bucket
- **Network entry**: Service, HTTPS Ingress, and Sealos App resource

### Deployment Dependencies

- [Gitea Documentation](https://docs.gitea.com/) - Official administration and configuration guides
- [Gitea Installation with Docker](https://docs.gitea.com/installation/install-with-docker-rootless) - Official rootless container guidance
- [Gitea GitHub Repository](https://github.com/go-gitea/gitea) - Source code and releases
- [Sealos Documentation](https://sealos.io/docs) - Platform deployment and operations guides

### Implementation Details

The template uses the upstream rootless image as UID/GID `1000:1000`, prepares both persistent volumes with the matching ownership, and exposes HTTP on port `3000`. Health checks use Gitea's official `/api/healthz` endpoint.

The tested application baseline is `100m` CPU and `256Mi` memory. A fresh SQLite installation exceeded a 128Mi limit, and an 80Mi cold start was OOM-killed. The template therefore keeps 256Mi for reliable first-run installation across both database branches. The managed MySQL component uses `500m` CPU and `512Mi` memory.

Gitea is licensed under the MIT License.

## Why Deploy Gitea on Sealos?

- **One-click stack**: Create Gitea, storage, networking, and the selected database branch from one template.
- **Persistent repositories**: Keep repositories and configuration across pod restarts.
- **Managed database option**: Use KubeBlocks MySQL without manual credential wiring.
- **Private object storage option**: Store upload-heavy features in a Sealos bucket with application-controlled delivery.
- **Instant HTTPS access**: Receive a generated public domain and TLS endpoint.
- **Canvas operations**: Adjust resources and storage from Sealos after deployment.

## Deployment Guide

1. Open the [Gitea template](https://sealos.io/products/app-store/gitea) and click **Deploy Now**.
2. Choose the deployment options:
   - **Use managed MySQL** (`use_external_database`): Enabled by default and recommended for shared or long-lived installations. Disable it to use SQLite.
   - **Enable S3-compatible object storage** (`enable_s3_storage`): Creates a private Sealos object storage bucket for Gitea upload data.
3. Wait for the Gitea workload and the selected database resources to become ready.
4. Open the generated HTTPS URL. A new instance displays the Gitea installation page.
5. Keep the prefilled database and server values. Expand **Optional Settings**, enter an administrator username, email, and strong password, then click **Install Gitea**.
6. After installation, Gitea signs in to the new administrator account. Create a repository to confirm the instance is ready.

## First Login and Registration

The first visitor completes instance setup and creates the initial administrator:

1. Open the generated Gitea URL.
2. Review the prefilled database type, database path or MySQL connection, domain, and root URL.
3. Expand **Optional Settings** and complete the administrator account fields.
4. Submit the installation form and wait for Gitea to redirect to the signed-in dashboard.

Later administrator and user sign-in is available at `https://<your-gitea-domain>/user/login`. User registration remains available according to the instance settings under **Site Administration**.

## Configuration

- **Database branch**: Managed MySQL is the default. SQLite stores its database at `/var/lib/gitea/data/gitea.db` on the persistent volume.
- **Object storage branch**: S3 mode applies to Gitea-managed upload data. Git repositories and the application configuration remain on persistent volumes.
- **SSH access**: The container listens on port `2222`; expose an additional TCP entry when SSH cloning is required. HTTPS cloning works through the generated domain.
- **Email**: SMTP is configured later in Gitea settings or environment variables for account confirmation and notifications.
- **Actions**: Gitea Actions runners are separate workloads and are added after the server deployment.

## Scaling

This template keeps one Gitea replica because the repository and configuration volumes use `ReadWriteOnce`. Scale CPU, memory, and PVC capacity vertically from Canvas as repository count, package usage, and concurrent traffic grow. A multi-replica design requires shared repository storage and a reviewed Gitea high-availability architecture.

## Troubleshooting

**The installation page cannot connect to MySQL**

Wait for the KubeBlocks MySQL cluster to report `Running`, then reload the page. Keep the database values prefilled by the template.

**The pod restarts during setup**

Keep the default 256Mi application memory limit. First-run database initialization needs more memory than an already configured idle instance.

**Uploads fail in S3 mode**

Confirm the ObjectStorageBucket is ready and that the Gitea StatefulSet received the generated bucket credentials. Keep the bucket private; downloads are served by Gitea.

**SSH cloning cannot connect**

Use HTTPS cloning, or add a Sealos TCP entry that forwards to the Gitea service on port `2222`.

## Additional Resources

- [Gitea Configuration Cheat Sheet](https://docs.gitea.com/administration/config-cheat-sheet)
- [Gitea Administrator Guide](https://docs.gitea.com/administration/)
- [Gitea API Documentation](https://docs.gitea.com/api/1.27/)

## License

This Sealos template follows the repository license. Gitea is distributed under the MIT License.
