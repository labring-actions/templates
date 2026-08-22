# Deploy and Host Homepage on Sealos

Homepage is a highly customizable self-hosted startpage and application dashboard with service API integrations. This template deploys Homepage with persistent configuration storage on Sealos Cloud.

![Homepage Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/homepage/website-screenshot.webp)

## About Hosting Homepage

Homepage runs as a Next.js application on port 3000 and reads configuration files from `/app/config`. The Sealos template provisions the container, persistent config volume, service, HTTPS ingress, and App entry automatically.

The deployment follows the official Docker runtime model and pins `ghcr.io/gethomepage/homepage:v1.13.2`. The template sets `HOMEPAGE_ALLOWED_HOSTS` to the generated Sealos domain so Homepage accepts requests through the public App URL.

## Common Use Cases

- **Personal startpage**: Organize bookmarks, internal tools, and services in one dashboard.
- **Homelab dashboard**: Display service cards, widgets, and health signals for self-hosted systems.
- **Team launchpad**: Share links to dashboards, runbooks, docs, and tools.
- **API-integrated overview**: Use Homepage widgets to surface data from supported services.

## Dependencies for Homepage Hosting

The Sealos template includes Homepage, persistent configuration storage, an internal service, and a public HTTPS ingress.

### Deployment Dependencies

- [Official Website](https://gethomepage.dev) - Product homepage
- [Docker Installation Guide](https://gethomepage.dev/installation/docker/) - Official Docker documentation
- [GitHub Repository](https://github.com/gethomepage/homepage) - Source code and releases
- [Container Image](https://github.com/gethomepage/homepage/pkgs/container/homepage) - Official GHCR image

### Implementation Details

**Architecture Components:**

- **Homepage web app**: Browser-facing dashboard served on port 3000.
- **Configuration storage**: Persistent volume mounted at `/app/config`.
- **Sealos ingress**: HTTPS public access using the generated App host.

**Configuration:**

- `HOMEPAGE_ALLOWED_HOSTS` is set to the generated Sealos host.
- The Docker socket integration is omitted for cloud-safe default deployment.
- Config files can be edited by opening the storage and workload resources from Sealos Canvas.

**License Information:**

Homepage is licensed under the GNU General Public License v3.0. This Sealos template is provided under the repository license.

## Why Deploy Homepage on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Homepage on Sealos, you get:

- **One-Click Deployment**: Deploy a ready Homepage instance from the App Store.
- **Persistent Configuration**: Keep dashboard settings and service definitions on durable storage.
- **Instant Public Access**: Open the dashboard through an automatically generated HTTPS URL.
- **Easy Customization**: Adjust resources, environment variables, and files from Sealos.
- **Integrated Monitoring**: Inspect rollout state, logs, ingress, and storage from the Canvas.

## Deployment Guide

1. Open the [Homepage template](https://sealos.io/products/app-store/homepage) and click **Deploy Now**.
2. Confirm the deployment parameters in the popup dialog.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Access Homepage through the provided App URL.

## Login and Access Guidance

Homepage does not create a login account by default. The first page opens directly to the dashboard, and access control should be added through your preferred ingress, identity, or network policy workflow if the deployment contains private links.

After the first launch, customize the dashboard by editing Homepage configuration files under `/app/config`.

## Configuration

After deployment, configure Homepage through:

- **Configuration files**: Edit files in `/app/config` to define services, bookmarks, widgets, and layouts.
- **AI Dialog**: Describe environment or resource changes in Sealos.
- **Resource Cards**: Open the StatefulSet or storage card for direct edits.

## Scaling

Homepage stores configuration on a single persistent volume. Keep one replica for normal use, and increase CPU or memory from the StatefulSet card if dashboard integrations become heavy.

## Troubleshooting

### Public URL returns an allowed-host error

- Cause: Homepage requires `HOMEPAGE_ALLOWED_HOSTS` to match the request host.
- Solution: Confirm the environment variable matches the generated Sealos App host.

### Dashboard is empty after first launch

- Cause: Homepage starts with default or empty configuration.
- Solution: Add services, bookmarks, and widgets in `/app/config` following the official configuration documentation.

## Additional Resources

- [Homepage Documentation](https://gethomepage.dev)
- [Configuration Guide](https://gethomepage.dev/configs/)
- [Widgets](https://gethomepage.dev/widgets/)
- [GitHub Discussions](https://github.com/gethomepage/homepage/discussions)

## License

This Sealos template is provided under the repository license. Homepage itself is licensed under the GNU General Public License v3.0.
