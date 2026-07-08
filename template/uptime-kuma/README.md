# Deploy and Host Uptime Kuma on Sealos

Uptime Kuma is an easy-to-use self-hosted monitoring tool for websites, APIs, TCP ports, ping checks, and status pages. This template deploys Uptime Kuma on Sealos Cloud with Uptime Kuma v2, a default independent MySQL-compatible database, and persistent `/app/data` runtime storage.

![Uptime Kuma Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/uptime-kuma/website-screenshot.webp)

## About Hosting Uptime Kuma

Uptime Kuma runs a web dashboard on port `3001`. The Sealos template uses Uptime Kuma v2 with an independent MySQL-compatible database by default, and also keeps a persistent `/app/data` volume for runtime files.

Set `USE_MARIADB=false` only when you want the smaller SQLite-backed mode. The SQLite path still uses the `/app/data` persistent volume and is best for lightweight single-node installs.

## Common Use Cases

- **Website uptime monitoring**: Track public websites and receive alerts when checks fail.
- **API health checks**: Monitor HTTP endpoints, JSON responses, and latency.
- **Internal service checks**: Watch TCP ports, DNS, ping, and keyword-based monitors.
- **Public status pages**: Publish service status pages for users or internal teams.
- **Notification routing**: Send alerts to Slack, Discord, Telegram, email, webhooks, and other supported channels.

## Dependencies for Uptime Kuma Hosting

The Sealos template includes all required runtime resources:

- **Uptime Kuma StatefulSet**: Runs the dashboard and monitoring worker.
- **Independent MySQL-compatible database**: Stores monitor data, users, status pages, incidents, and notification settings when `USE_MARIADB=true`.
- **Persistent `/app/data` volume**: Stores runtime files and the SQLite database when `USE_MARIADB=false`.
- **Service and Ingress**: Exposes the dashboard over HTTPS through the Sealos gateway.
- **App entry**: Adds a clickable Uptime Kuma entry in the Sealos desktop.

### Deployment Dependencies

- [Official Website](https://uptime.kuma.pet/) - Product homepage
- [Official Installation Guide](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install) - Docker installation and storage notes
- [Docker Tags Guide](https://github.com/louislam/uptime-kuma/wiki/Docker-Tags) - Image tag and v2 storage backend notes
- [GitHub Repository](https://github.com/louislam/uptime-kuma) - Source code and issue tracker

## Implementation Details

**Architecture Components:**

This template deploys one application component:

- **Uptime Kuma**: A Node.js-based monitoring dashboard listening on port `3001`.
- **MySQL-compatible database**: Provisioned through Kubeblocks when `USE_MARIADB=true`.
- **Persistent Volume**: Mounted at `/app/data` for runtime files and SQLite mode.
- **Ingress**: Publishes the dashboard at `https://<app-host>.<your-sealos-domain>` with Sealos-managed TLS.

**Configuration:**

- The app host is generated with the `uptime-kuma-` prefix.
- The runtime uses the pinned `louislam/uptime-kuma:2.4.0-slim` image.
- `USE_MARIADB=true` provisions an independent MySQL-compatible database and injects `UPTIME_KUMA_DB_TYPE=mariadb` plus the generated connection credentials.
- `USE_MARIADB=false` keeps the SQLite file database on persistent storage.

**License Information:**

Uptime Kuma is licensed under the MIT License. This Sealos template is provided under the license terms of the templates repository.

## First-Run Setup

After deployment, open the Uptime Kuma URL from the Sealos App entry or generated Ingress URL.

1. On the first screen, create the first administrator account with a username and password.
2. After account creation, sign in with that administrator account.
3. Click **Add New Monitor**.
4. Choose a monitor type such as **HTTP(s)**, **Ping**, or **TCP Port**.
5. Enter the target URL or host, set the heartbeat interval, and click **Save**.
6. Open **Settings** to configure notification channels, language, status pages, and other instance options.

## Why Deploy Uptime Kuma on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and operations. By deploying Uptime Kuma on Sealos, you get:

- **One-Click Deployment**: Deploy from the App Store without writing Kubernetes manifests.
- **Persistent Storage Included**: Keep monitor data and user settings across restarts.
- **Instant Public Access**: Get an HTTPS URL with Sealos-managed certificates.
- **Pay-as-you-go Resources**: Start with a small resource profile and adjust from the Canvas when needed.
- **AI Ops and Resource Cards**: Use the Canvas AI dialog or resource cards to update CPU, memory, storage, and runtime settings.

## Deployment Guide

1. Open the [Uptime Kuma template](https://sealos.io/products/app-store/uptime-kuma) and click **Deploy Now**.
2. Review the generated application name and host values.
   - Keep `USE_MARIADB=true` for the default independent database deployment.
   - Set `USE_MARIADB=false` for SQLite-backed single-node mode.
3. Wait for deployment to complete, typically within 2-3 minutes. After deployment, Sealos redirects you to the Canvas.
4. Access your application:
   - **Uptime Kuma Dashboard**: Open the App entry or generated public URL.
   - **First-run setup**: Create the first administrator account, sign in, and add your first monitor.

## Scaling

To adjust resources after deployment:

1. Open the Canvas for your Uptime Kuma deployment.
2. Click the StatefulSet resource card.
3. Adjust CPU, memory, or storage based on monitor count and check frequency.
4. Apply the changes in the dialog.

## Troubleshooting

### First-run page keeps returning after account creation

- Cause: The application data directory is missing persistence or cannot write correctly.
- Solution: Confirm the StatefulSet has the `/app/data` persistent volume mounted and the pod is running without storage errors.

### SQLite storage warnings

- Cause: SQLite requires filesystem support for POSIX file locks.
- Solution: Keep `/app/data` on the Sealos persistent volume and avoid replacing it with shared filesystems that break file locking.

### WebSocket or dashboard updates feel stale

- Cause: Reverse proxy settings can affect realtime updates.
- Solution: Keep the template Ingress annotations and access Uptime Kuma through the generated HTTPS URL.

## Additional Resources

- [Uptime Kuma Documentation Wiki](https://github.com/louislam/uptime-kuma/wiki)
- [Reverse Proxy Notes](https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy)
- [Uptime Kuma Releases](https://github.com/louislam/uptime-kuma/releases)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the templates repository license. Uptime Kuma itself is licensed under the MIT License.
