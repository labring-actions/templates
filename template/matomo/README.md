# Deploy and Host Matomo on Sealos

Matomo is an open source web analytics platform for tracking visitor behavior, conversions, campaigns, and site performance. This template deploys Matomo with the official Apache/PHP runtime, persistent application storage, and a Sealos-managed MySQL database on Sealos Cloud.

## About Hosting Matomo

Matomo runs as a single Apache/PHP application container, which avoids sidecar configuration drift during restarts and provides the public HTTP entry point directly. Sealos provisions a MySQL database through KubeBlocks and persistent storage for `/var/www/html`, so application files and generated configuration survive restarts.

On first access, Matomo opens its installation wizard. The template preconfigures the database host, database username, password, database name, table prefix, and trusted host through Matomo-supported environment variables, so you can proceed through the wizard and create the first superuser account from the browser.

## Common Use Cases

- **Privacy-focused web analytics**: Track website traffic while keeping analytics data under your control.
- **Campaign and conversion tracking**: Measure marketing campaigns, goals, funnels, and ecommerce events.
- **Product usage analytics**: Monitor how users navigate product documentation, portals, or SaaS dashboards.
- **Self-hosted reporting**: Provide teams with analytics dashboards without relying on third-party hosted analytics.

## Dependencies for Matomo Hosting

The Sealos template includes the required runtime services: Matomo Apache/PHP runtime, persistent storage, and a MySQL database.

### Deployment Dependencies

- [Matomo Official Website](https://matomo.org/) - Product overview and documentation
- [Matomo Installation Guide](https://matomo.org/faq/on-premise/installing-matomo/) - First-run installation flow
- [Matomo Docker Image](https://hub.docker.com/_/matomo) - Official container image
- [Matomo GitHub Repository](https://github.com/matomo-org/matomo) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Matomo Application**: Runs Matomo 5.10.0 with the official Apache/PHP image and serves the web UI on port 80.
- **MySQL**: A Sealos-managed KubeBlocks MySQL cluster stores analytics data and application settings.
- **Persistent Storage**: A 1 GiB volume stores Matomo application files and generated configuration under `/var/www/html`.

**Configuration:**

- The public endpoint is exposed through Sealos Ingress with automatic HTTPS.
- Database connection values use Matomo-supported `MATOMO_DATABASE_*` environment variables and are sourced from the Sealos-managed MySQL credential secret.
- The first Matomo administrator is created in the browser during the installation wizard.
- Keep the generated public URL stable after installation because Matomo records it as a trusted host.

**License Information:**

Matomo is licensed under GPL-3.0. This Sealos template is provided under the repository license.

## Why Deploy Matomo on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and operations. By deploying Matomo on Sealos, you get:

- **One-Click Deployment**: Deploy Matomo and MySQL from a ready-made template without writing Kubernetes YAML.
- **Managed Public Access**: Sealos creates an HTTPS endpoint for the Matomo web UI.
- **Persistent Data**: Application files and database data are stored on persistent volumes.
- **Easy Operations**: Use the Canvas, AI dialog, and resource cards to adjust resources or inspect runtime state.
- **Pay-as-you-go Resources**: Start with a small footprint and scale resources when analytics volume grows.

## Deployment Guide

1. Open the [Matomo template](https://sealos.io/products/app-store/matomo) and click **Deploy Now**.
2. Keep the default parameters or adjust the generated app name and host in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
4. Open the provided Matomo URL.
5. Complete the Matomo installation wizard:
   - Confirm the system check.
   - Use the prefilled database settings when shown.
   - Create the first superuser account.
   - Add your first website and copy the tracking code into the site you want to measure.
   - On the final congratulations page, click **Continue to Matomo** to reach the sign-in page.
6. Sign in with the superuser username and password you created in the wizard.

## Configuration

After deployment, configure Matomo through:

- **Installation Wizard**: Create the first administrator and website when you open the app for the first time.
- **Matomo Admin Panel**: Manage users, websites, privacy settings, plugins, and tracking code after installation.
- **AI Dialog**: Describe resource or configuration changes in the Sealos Canvas.
- **Resource Cards**: Open the StatefulSet, MySQL, Ingress, or storage cards to inspect and adjust runtime settings.

## Scaling

The template uses a validated 512 MiB memory limit so the installation wizard can finish without PHP/Apache being OOMKilled. As traffic grows:

1. Open the Canvas for your deployment.
2. Click the Matomo StatefulSet resource card.
3. Increase CPU or memory using the allowed Sealos resource options if dashboards or archiving become slow.
4. Apply the change and verify the Matomo dashboard remains available.

For high-traffic installations, also configure Matomo archiving through cron according to the official Matomo documentation.

## Troubleshooting

### Installation wizard cannot connect to the database

- Cause: MySQL may still be starting or credentials may not be ready yet.
- Solution: Wait until the MySQL pod and the Matomo pod are running, then reload the wizard.

### Browser shows a trusted host or HTTPS warning

- Cause: Matomo validates the host it is accessed through.
- Solution: Use the Sealos-provided public URL and avoid changing the app host after completing installation.

### Setup stops midway or the pod restarts

- Cause: Matomo can exceed a 256 MiB container limit while creating tables, plugins, and the first admin account.
- Solution: Keep the template memory limit at 512 MiB or higher during setup. The current template already uses this validated limit.

### Analytics reports are slow on larger sites

- Cause: Browser-triggered archiving can become slow with more traffic.
- Solution: Follow Matomo's cron archiving guide and increase application resources if needed.

### Getting Help

- [Matomo Documentation](https://matomo.org/help/)
- [Matomo Community Forum](https://forum.matomo.org/)
- [Matomo GitHub Issues](https://github.com/matomo-org/matomo/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Tracking Code Guide](https://matomo.org/faq/new-to-piwik/how-to-install-the-javascript-tracking-code/)
- [Privacy Features](https://matomo.org/privacy/)
- [Developer Documentation](https://developer.matomo.org/)

## License

This Sealos template is provided under the repository license. Matomo itself is licensed under GPL-3.0.
