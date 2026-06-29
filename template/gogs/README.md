# Deploy and Host Gogs on Sealos

Gogs is a lightweight self-hosted Git service for repositories, users, organizations, issues, and project collaboration. This template deploys Gogs with a KubeBlocks PostgreSQL database, persistent Git data, public HTTPS access, and first-run registration on Sealos Cloud.

![Gogs Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gogs/website-screenshot.webp)

## About Hosting Gogs

Gogs runs as a single web service backed by PostgreSQL for application metadata and persistent storage for repositories, SSH keys, logs, and custom configuration. The template generates a production `app.ini` before startup, sets the public root URL to your Sealos domain, disables in-container SSH exposure, and keeps HTTP traffic behind Sealos Ingress.

Sealos provisions the PostgreSQL database, persistent volume, HTTPS ingress, and App Store entry. Gogs handles user accounts, repositories, organizations, issues, and web-based Git collaboration from the browser.

## Common Use Cases

- **Personal Git Hosting**: Host private repositories with a compact Git service.
- **Team Code Collaboration**: Manage users, organizations, repositories, issues, and pull requests.
- **Internal Tooling**: Run a private Git service close to self-hosted CI, automation, or deployment workflows.
- **Education and Labs**: Provide isolated Git hosting for classes, workshops, and small teams.

## Dependencies for Gogs Hosting

The Sealos template includes all required dependencies: the Gogs web application, KubeBlocks PostgreSQL, persistent repository storage, a ClusterIP service, HTTPS ingress, and the Sealos App link.

### Deployment Dependencies

- [Official Website](https://gogs.io/) - Gogs product website
- [GitHub Repository](https://github.com/gogs/gogs) - Source code and releases
- [Docker Documentation](https://github.com/gogs/gogs/tree/main/docker) - Official container guidance
- [Configuration Primer](https://gogs.io/fine-tuning/configuration-primer) - Gogs configuration reference

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Gogs Web Service**: Serves the web UI, Git HTTP endpoints, registration, login, and repository workflows.
- **PostgreSQL**: Stores Gogs users, repositories metadata, issues, organizations, and settings.
- **Persistent Storage**: Stores Git repositories, custom configuration, logs, and runtime data under `/data`.
- **Sealos Ingress**: Publishes the web service over HTTPS on your generated Sealos domain.

**Configuration:**

The template writes `/data/gogs/conf/app.ini` from a ConfigMap and injects PostgreSQL credentials from the KubeBlocks connection secret. Registration captcha is disabled for first-run setup, and the first user who registers in a new deployment becomes the administrator.

**License Information:**

Gogs is licensed under the MIT License. This Sealos template is provided under the repository license for Sealos templates.

## Why Deploy Gogs on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to ongoing management. By deploying Gogs on Sealos, you get:

- **One-Click Deployment**: Launch Gogs from the App Store without writing Kubernetes YAML.
- **Managed Database Provisioning**: PostgreSQL is created with KubeBlocks and wired into the app automatically.
- **Persistent Storage**: Repository and application data survive restarts and upgrades.
- **Instant HTTPS Access**: Sealos provides a public domain and TLS certificate for the Gogs web UI.
- **Canvas Operations**: Adjust resources, inspect logs, or update settings through the Canvas, AI dialog, and resource cards.
- **Pay-as-You-Go Efficiency**: Start with lightweight resources and scale as your repository usage grows.

## Deployment Guide

1. Open the [Gogs template](https://sealos.io/products/app-store/gogs) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Gogs via the provided URL and click **Register**.
5. Create the first account. Gogs grants administrator privileges to the first registered user in a fresh deployment.
6. Sign in with that account and create your first repository.

## Login and Registration

Gogs enables self-registration on a fresh deployment and disables registration captcha for the initial setup flow. The first registered user becomes the administrator, so create that account before sharing the URL with other users.

After the administrator exists, additional users can register from the same login page unless you disable registration in the Gogs admin settings.

## Configuration

After deployment, you can configure Gogs through:

- **Gogs Admin Panel**: Manage users, organizations, repositories, authentication sources, and application settings.
- **Canvas Resource Cards**: Change CPU, memory, storage, or environment values.
- **AI Dialog**: Describe operational changes and let Sealos apply them to the template resources.

## Scaling

To scale the deployment:

1. Open the Canvas for your deployment.
2. Click the Gogs StatefulSet or PostgreSQL resource card.
3. Adjust CPU, memory, storage, or replica-related settings.
4. Apply the change and monitor rollout status.

## Troubleshooting

### Registration page is unavailable

- Cause: The app is still starting or PostgreSQL is finishing initialization.
- Solution: Wait for the Gogs StatefulSet and PostgreSQL Cluster to become ready, then reload the App URL.

### Login succeeds but repository operations fail

- Cause: The persistent volume or database may still be warming up after startup.
- Solution: Check the Gogs pod logs and PostgreSQL status from the Canvas.

### Getting Help

- [Gogs Documentation](https://gogs.io/docs)
- [GitHub Issues](https://github.com/gogs/gogs/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Gogs Configuration Primer](https://gogs.io/fine-tuning/configuration-primer)
- [Gogs Docker Guide](https://github.com/gogs/gogs/tree/main/docker)
- [Gogs Releases](https://github.com/gogs/gogs/releases)

## License

This Sealos template is provided under the Sealos templates repository license. Gogs itself is licensed under the MIT License.
