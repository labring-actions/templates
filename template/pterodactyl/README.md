# Deploy and Host Pterodactyl Panel on Sealos

Pterodactyl Panel is an open-source game server management panel. This template deploys the Panel with KubeBlocks MySQL, KubeBlocks Redis, persistent application storage, and HTTPS ingress on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pterodactyl/website-screenshot.webp)

## About Hosting Pterodactyl Panel

Pterodactyl Panel is the web control plane for managing game servers through Pterodactyl Wings. The official Docker topology uses a Panel container, MySQL-compatible database, Redis cache, and persistent storage for application state and logs.

The Sealos template provisions MySQL and Redis with KubeBlocks, initializes the Panel database, creates the first administrator account, and exposes the Panel through a Sealos HTTPS URL.

## Common Use Cases

- **Game server control panel**: Manage users, nodes, allocations, and servers.
- **Minecraft and game hosting**: Pair the Panel with Wings nodes to host game servers.
- **Team administration**: Give staff and users controlled access to server operations.
- **Self-hosted infrastructure**: Run the Panel on Kubernetes-managed cloud resources.

## Dependencies for Pterodactyl Panel Hosting

The Sealos template includes the Panel container, KubeBlocks MySQL, KubeBlocks Redis, database bootstrap, administrator bootstrap, persistent storage, and HTTPS ingress.

### Deployment Dependencies

- [Pterodactyl Documentation](https://pterodactyl.io/panel/1.0/getting_started.html) - Official Panel documentation
- [Pterodactyl Docker Compose](https://github.com/pterodactyl/panel/blob/v1.12.4/docker-compose.example.yml) - Official container topology
- [Pterodactyl GitHub Repository](https://github.com/pterodactyl/panel) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Panel**: PHP, nginx, supervisor, and scheduled tasks in `ghcr.io/pterodactyl/panel:v1.12.4`
- **MySQL**: KubeBlocks MySQL `ac-mysql-8.0.30-1`
- **Redis**: KubeBlocks Redis `redis-7.2.7`
- **Bootstrap Job**: Runs migrations, seeds data, and creates the configured administrator
- **Persistent Storage**: Mounted for `/app/var` and `/app/storage/logs`

**Configuration:**

The template sets `APP_URL` to the generated HTTPS URL, uses Redis for cache/session/queue, sets mail delivery to log mode, and creates the initial administrator with the parameters supplied during deployment.

**License Information:**

Pterodactyl Panel is licensed under the MIT License.

## Why Deploy Pterodactyl Panel on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Pterodactyl Panel on Sealos, you get:

- **One-Click Deployment**: Deploy Panel, MySQL, Redis, storage, ingress, and SSL in one flow.
- **Managed Databases**: Use KubeBlocks MySQL and Redis for durable application services.
- **Administrator Bootstrap**: Create the first Panel administrator during deployment.
- **Instant Public Access**: Open the generated HTTPS URL after deployment.
- **Operational Control**: Tune resources and environment variables from the Sealos Canvas.

Deploy Pterodactyl Panel on Sealos and manage the control plane with cloud-native infrastructure.

## Deployment Guide

1. Open the [Pterodactyl Panel template](https://sealos.io/products/app-store/pterodactyl) and click **Deploy Now**.
2. Configure the administrator email, username, name, password, and optional S3 backups in the popup dialog.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access the Panel via the provided URL.
5. Log in with the administrator email and password configured during deployment.

## Configuration

The first administrator account is created by the bootstrap Job using Pterodactyl's `p:user:make` command after migrations and seeders complete. Add Wings nodes from the Panel after deployment to run actual game servers.

S3-compatible backups are available through the **Use S3-compatible object storage for Pterodactyl server backups** switch. When enabled, the template creates a Sealos object storage bucket and configures `APP_BACKUP_DRIVER=s3` with path-style S3 settings. MySQL and Redis are provisioned as external KubeBlocks services.

## Scaling

To scale Pterodactyl Panel resources:

1. Open the Canvas for your deployment.
2. Click the Panel StatefulSet, MySQL, or Redis resource card.
3. Adjust CPU, memory, replicas, or storage.
4. Apply the changes in the dialog.

## Troubleshooting

**Administrator login fails**

- Cause: The bootstrap Job may still be running migrations and user creation.
- Solution: Wait for the bootstrap Job to complete, then log in with the configured administrator email and password.

**Panel loads but queues or sessions fail**

- Cause: Redis may still be initializing.
- Solution: Wait for Redis to become ready and restart the Panel workload from the Canvas.

**Game servers cannot be created**

- Cause: Pterodactyl requires Wings nodes for server execution.
- Solution: Add and configure a Wings node from the Panel after the Panel is deployed.

## Additional Resources

- [Pterodactyl Panel Documentation](https://pterodactyl.io/panel/1.0/getting_started.html)
- [Pterodactyl Wings Documentation](https://pterodactyl.io/wings/1.0/installing.html)
- [Pterodactyl GitHub](https://github.com/pterodactyl/panel)

## License

This Sealos template is provided under the repository license. Pterodactyl Panel itself is licensed under the MIT License.
