# Deploy and Host Kuvasz on Sealos

Kuvasz is an open-source, self-hosted uptime and SSL monitoring service with status pages. This template deploys Kuvasz with a Kubeblocks PostgreSQL database and a public HTTPS endpoint on Sealos Cloud.

![Kuvasz Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/kuvasz/website-screenshot.webp)

## About Hosting Kuvasz

Kuvasz monitors websites and services with HTTP, SSL, push, and ICMP checks. It provides a web dashboard, REST API, notification integrations, metrics exporters, and status pages for publishing service health.

This Sealos template runs the official Kuvasz container as a single web service on port `8080`. Sealos provisions PostgreSQL `postgresql-16.4.0`, creates the `kuvasz` database, mounts `/config/kuvasz.yml` from a ConfigMap, and exposes the dashboard through an HTTPS Ingress.

Authentication is enabled by default. The template asks for an initial admin username, admin password, and API key, with secure generated defaults for the password and API key.

## Common Use Cases

- **Website uptime monitoring**: Track public websites and APIs with HTTP status checks.
- **SSL certificate monitoring**: Detect invalid or expiring certificates before users are affected.
- **Status pages**: Publish service availability for teams, customers, or internal systems.
- **API-driven monitoring**: Create, update, and export monitors through the Kuvasz REST API.
- **Notification workflows**: Connect email, Discord, Slack, Telegram, PagerDuty, and webhook alerts.

## Dependencies for Kuvasz Hosting

The Sealos template includes the required runtime components: the Kuvasz container image, a PostgreSQL database, a database initialization Job, a ConfigMap for `/config/kuvasz.yml`, a Kubernetes Service, an Ingress, and a Sealos App entry.

### Deployment Dependencies

- [Kuvasz Website](https://kuvasz-uptime.dev/) - Official documentation and product overview
- [Kuvasz GitHub Repository](https://github.com/kuvasz-uptime/kuvasz) - Source code and release notes
- [Kuvasz Deployment Guide](https://kuvasz-uptime.dev/setup/installation/) - Official Docker and Helm deployment guidance
- [Kuvasz API Documentation](https://api-docs.kuvasz-uptime.dev/) - REST API reference

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Kuvasz Web Service**: Runs `kuvaszmonitoring/kuvasz:3.11.0` on port `8080` and serves the dashboard, REST API, health endpoint, and monitoring scheduler.
- **PostgreSQL**: Kubeblocks-managed PostgreSQL `postgresql-16.4.0` stores monitors, events, status pages, integrations, and application metadata.
- **PostgreSQL Init Job**: Creates the `kuvasz` database idempotently after PostgreSQL is ready.
- **ConfigMap**: Mounts `/config/kuvasz.yml` for optional integrations, YAML-managed monitors, status pages, and SMTP settings.
- **Ingress and App Entry**: Sealos exposes Kuvasz through an HTTPS domain and creates a dashboard entry for direct access.

**Configuration:**

The template configures:

- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, and `DATABASE_PASSWORD` from the Kubeblocks PostgreSQL connection Secret.
- `DATABASE_NAME=kuvasz` for the application database.
- `ENABLE_AUTH=true` with the configured admin username, password, and API key.
- `APP_LANGUAGE=en` and `TZ=UTC`.

After deployment, log in to the web UI with the configured admin username and password. Use the configured API key in the `X-API-KEY` header or as a Bearer token for REST API calls.

**License Information:**

Kuvasz is distributed under the Apache License 2.0. This Sealos template is provided as deployment configuration for Kuvasz and keeps the upstream application license unchanged.

## Why Deploy Kuvasz on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operations, and resource management. By deploying Kuvasz on Sealos, you get:

- **One-Click Deployment**: Deploy Kuvasz, PostgreSQL, networking, and the dashboard entry from one template.
- **Kubernetes Foundation**: Run on Kubernetes-backed scheduling, service discovery, health checks, and rolling updates.
- **Persistent Database Included**: Keep monitors, incidents, and status page data across restarts.
- **Instant Public Access**: Each deployment receives an HTTPS URL for the dashboard, API, and status pages.
- **Easy Customization**: Adjust environment variables, resources, and mounted configuration through Canvas, AI dialog, or resource cards.
- **Pay-As-You-Go Resources**: Start with a compact resource profile and scale when monitoring volume grows.

Deploy Kuvasz on Sealos and focus on service reliability operations.

## Deployment Guide

1. Open the [Kuvasz template](https://sealos.io/products/app-store/kuvasz) and click **Deploy Now**.
2. Configure the admin username, admin password, and API key in the popup dialog. The generated defaults are suitable for a first deployment.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Open the generated Kuvasz URL from the App entry.
5. Log in with the configured admin username and password.
6. Create your first monitor from the dashboard, or call the REST API with the configured `X-API-KEY` value.

## Configuration

After deployment, you can configure Kuvasz through:

- **Kuvasz Web UI**: Create HTTP, SSL, push, and ICMP monitors; manage status pages; and configure supported integrations.
- **REST API**: Send requests with `X-API-KEY: <your-api-key>` to manage monitors and read stats.
- **ConfigMap**: Edit `/config/kuvasz.yml` through the Canvas resource card for YAML-managed monitors, SMTP settings, integrations, and status pages.
- **Sealos AI Dialog**: Describe environment, resource, or configuration changes and let AI apply updates.
- **Resource Cards**: Click the Deployment, PostgreSQL, ConfigMap, Ingress, or Service cards in Canvas to inspect and adjust settings.

When monitors are defined in `/config/kuvasz.yml`, Kuvasz treats that YAML file as the source of truth for those monitor types. Use the web UI or API for day-to-day edits when the YAML file leaves monitor sections empty.

## Scaling

To scale Kuvasz on Sealos:

1. Open the Canvas for your Kuvasz deployment.
2. Click the Kuvasz Deployment resource card.
3. Increase CPU or memory when monitor count, check frequency, API traffic, or integrations require more capacity.
4. Apply the change and wait for the pod to become ready.

The default template uses `50m` CPU and `384Mi` memory requests with `500m` CPU and `512Mi` memory limits for the Kuvasz container. PostgreSQL uses `50m` CPU and `51Mi` memory requests with `500m` CPU and `512Mi` memory limits.

## Troubleshooting

### The app opens the login page

This is the expected first screen for a fresh deployment. Log in with the admin username and password configured during deployment.

### API requests return unauthorized

Pass the API key as `X-API-KEY: <your-api-key>` or `Authorization: Bearer <your-api-key>`. The health endpoint `/api/v2/health` is public.

### Monitor changes appear read-only

Kuvasz enables read-only mode for monitor types that are managed through `/config/kuvasz.yml`. Remove YAML-managed monitor sections or edit the ConfigMap when you want YAML to remain the operational source.

### Getting Help

- [Kuvasz Documentation](https://kuvasz-uptime.dev/)
- [Kuvasz GitHub Issues](https://github.com/kuvasz-uptime/kuvasz/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Kuvasz Configuration Reference](https://kuvasz-uptime.dev/setup/configuration/)
- [Kuvasz API Guide](https://kuvasz-uptime.dev/features/api/)
- [Kuvasz Docker Image](https://hub.docker.com/r/kuvaszmonitoring/kuvasz)
- [Kuvasz GitHub Releases](https://github.com/kuvasz-uptime/kuvasz/releases)

## License

This Sealos template is provided under the repository's template license. Kuvasz itself is licensed under the Apache License 2.0.
