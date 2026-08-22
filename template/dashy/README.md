# Deploy and Host Dashy on Sealos

Dashy is a self-hostable personal dashboard with widgets, status checks, themes, icon packs, and a built-in UI editor. This template deploys Dashy with persistent user-data storage on Sealos Cloud.

![Dashy Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/dashy/website-screenshot.webp)

## About Hosting Dashy

Dashy runs a Node.js web server on port 8080 and reads dashboard configuration from `/app/user-data/conf.yml`. The Sealos template provisions the container, a starter configuration file, persistent storage, service, HTTPS ingress, and App entry automatically.

The deployment follows the official Docker runtime model and pins `lissy93/dashy:4.3.11`. A starter Sealos section is included so the first launch has a valid dashboard configuration.

## Common Use Cases

- **Personal dashboard**: Collect tools, bookmarks, notes, and links in one page.
- **Service status page**: Monitor internal apps and public endpoints with Dashy status checks.
- **Homelab launchpad**: Group self-hosted applications and infrastructure links.
- **Team navigation hub**: Publish a curated dashboard for operations, support, or engineering teams.

## Dependencies for Dashy Hosting

The Sealos template includes Dashy, persistent user-data storage, starter configuration, a public HTTPS ingress, and the dashboard App entry.

### Deployment Dependencies

- [Official Website](https://dashy.to) - Product homepage
- [Deployment Documentation](https://dashy.to/docs/deployment) - Official deployment guide
- [GitHub Repository](https://github.com/Lissy93/dashy) - Source code and releases
- [Docker Image](https://hub.docker.com/r/lissy93/dashy) - Official container image

### Implementation Details

**Architecture Components:**

- **Dashy web app**: Browser-facing dashboard served on port 8080.
- **Starter config**: ConfigMap-mounted `conf.yml` for first launch.
- **Persistent user data**: Volume mounted at `/app/user-data` for custom config and assets.

**Configuration:**

- The template creates a starter `conf.yml` with a Sealos section.
- Dashy can be customized through the UI editor or by editing `/app/user-data/conf.yml`.
- Health probes use the official `node /app/services/healthcheck.js` command.

**License Information:**

Dashy is licensed under the MIT License. This Sealos template is provided under the repository license.

## Why Deploy Dashy on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Dashy on Sealos, you get:

- **One-Click Deployment**: Launch Dashy from the App Store in minutes.
- **Persistent User Data**: Keep configuration and dashboard assets across restarts.
- **Instant Public Access**: Open Dashy through an automatically generated HTTPS URL.
- **Easy Customization**: Edit resources, storage, and configuration from Sealos.
- **Integrated Operations**: Inspect rollout state, logs, ingress, and storage from one Canvas.

## Deployment Guide

1. Open the [Dashy template](https://sealos.io/products/app-store/dashy) and click **Deploy Now**.
2. Confirm the deployment parameters in the popup dialog.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Access Dashy through the provided App URL.

## Login and Access Guidance

Dashy starts without a login account by default. The App URL opens the dashboard directly, and you can add authentication later from Dashy configuration if you need a private dashboard.

After first launch, use the UI editor or update `/app/user-data/conf.yml` to add sections, items, icons, widgets, and status checks.

## Configuration

After deployment, configure Dashy through:

- **Dashy UI editor**: Update dashboard content from the browser.
- **Configuration file**: Edit `/app/user-data/conf.yml` for versioned dashboard settings.
- **AI Dialog**: Describe resource or environment changes in Sealos.
- **Resource Cards**: Open the StatefulSet or storage card for direct edits.

## Scaling

Dashy stores configuration on a single persistent volume. Keep one replica for normal use, and increase CPU or memory from the StatefulSet card if widgets or status checks become heavy.

## Troubleshooting

### Dashboard shows a configuration error

- Cause: `conf.yml` may contain invalid YAML or unsupported fields.
- Solution: Validate the file against the Dashy configuration documentation and restart the StatefulSet.

### UI editor changes disappear

- Cause: The dashboard may still be using the starter ConfigMap-mounted file.
- Solution: Save changes into `/app/user-data/conf.yml` and keep the persistent volume attached.

## Additional Resources

- [Dashy Documentation](https://dashy.to/docs)
- [Configuration Guide](https://dashy.to/docs/configuring)
- [Management Guide](https://dashy.to/docs/management)
- [GitHub Issues](https://github.com/Lissy93/dashy/issues)

## License

This Sealos template is provided under the repository license. Dashy itself is licensed under the MIT License.
