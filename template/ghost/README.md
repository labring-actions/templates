# Deploy and Host Ghost on Sealos

Ghost is an open-source publishing, newsletter, membership, and subscription platform. This template deploys Ghost with KubeBlocks MySQL and persistent content storage on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/ghost/website-screenshot.webp)

## About Hosting Ghost

Ghost runs as a Node.js application serving the public site and Ghost Admin from the same URL. The Sealos template provisions an external MySQL database because Ghost production mode requires MySQL 8, and it mounts persistent storage at `/var/lib/ghost/content` for themes, images, and local content files.

The deployment includes a public HTTPS URL, an NGINX ingress, a KubeBlocks MySQL cluster, database initialization, and a stateful Ghost workload.

## Common Use Cases

- **Independent publishing**: Run a professional blog or publication with Ghost Admin.
- **Newsletter operations**: Manage posts, members, and newsletters from one CMS.
- **Membership sites**: Build gated content and subscription workflows.
- **Team editorial workflow**: Give authors and editors a shared publishing backend.

## Dependencies for Ghost Hosting

The Sealos template includes Ghost, KubeBlocks MySQL, persistent storage, HTTPS ingress, and automatic database creation.

### Deployment Dependencies

- [Ghost Documentation](https://ghost.org/docs/) - Official Ghost documentation
- [Ghost Docker Image](https://hub.docker.com/_/ghost) - Official Docker image documentation
- [Ghost GitHub Repository](https://github.com/TryGhost/Ghost) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Ghost**: Main publishing and admin application using `ghost:6.44.1-alpine`
- **MySQL**: KubeBlocks MySQL `ac-mysql-8.0.30-1`
- **Persistent Storage**: Mounted at `/var/lib/ghost/content`
- **Ingress**: HTTPS public access on the Sealos domain

**Configuration:**

The template sets `NODE_ENV=production`, configures `url` to the generated HTTPS URL, and connects Ghost to the provisioned MySQL database. Ghost serves the public site at `/` and the admin interface at `/ghost`.

**License Information:**

Ghost is licensed under the MIT License.

## Why Deploy Ghost on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Ghost on Sealos, you get:

- **One-Click Deployment**: Deploy Ghost, MySQL, storage, ingress, and SSL with a single click.
- **Persistent Storage Included**: Keep uploaded content and themes across restarts.
- **Managed Database**: Run Ghost with a KubeBlocks MySQL database.
- **Instant Public Access**: Use the generated HTTPS URL immediately after deployment.
- **Easy Customization**: Adjust resources and environment variables from the Sealos Canvas.

Deploy Ghost on Sealos and focus on publishing instead of operating infrastructure.

## Deployment Guide

1. Open the [Ghost template](https://sealos.io/products/app-store/ghost) and click **Deploy Now**.
2. Configure the deployment parameters:
   - **use_s3_storage**: Enable this option when you want Ghost media and uploads to use S3-compatible object storage.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Ghost via the provided URL:
   - **Public Site**: Use the generated HTTPS URL from Sealos.
   - **Admin Setup**: Open `/ghost` on the same URL and create the first owner account.

## Configuration

Ghost Admin is available at `https://[your-app-url]/ghost`. The first visit starts the owner account setup flow where you create the administrator email and password. After setup, use the same `/ghost` path for normal administrator login.

The template disables staff-device email verification during first setup so the owner account can be created before SMTP is configured. Configure SMTP from Ghost Admin before sending newsletters or inviting staff users.

Social Web and Ghost Explore pings are disabled by default for a clean single-node deployment. Enable those features from Ghost Admin after adding the supporting services and public configuration you want to use.

This template uses local persistent content storage by default. The **Use S3-compatible object storage through the Ghost storage adapter configuration** switch creates a Sealos object storage bucket, installs the Ghost S3 storage adapter into `/var/lib/ghost/content/adapters/storage/s3` during startup, and injects the S3 adapter configuration variables.

## Scaling

To scale Ghost resources:

1. Open the Canvas for your deployment.
2. Click the Ghost StatefulSet resource card.
3. Adjust CPU, memory, or storage.
4. Apply the changes in the dialog.

## Troubleshooting

**Admin setup page does not load**

- Cause: Ghost may still be initializing or waiting for MySQL.
- Solution: Wait for the Ghost workload to become ready, then open `/ghost` again.

**Images or themes disappear after restart**

- Cause: The content volume was modified or removed.
- Solution: Keep `/var/lib/ghost/content` mounted to persistent storage.

## Additional Resources

- [Ghost Configuration](https://ghost.org/docs/config/)
- [Ghost Admin](https://ghost.org/docs/admin/)
- [Ghost Docker Image](https://hub.docker.com/_/ghost)

## License

This Sealos template is provided under the repository license. Ghost itself is licensed under the MIT License.
