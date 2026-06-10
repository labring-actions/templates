# Deploy and Host Joplin Server on Sealos

Joplin Server is the open-source synchronization backend for Joplin notes, users, sharing, and publishing. This template deploys Joplin Server 3.7.1 with PostgreSQL and HTTPS ingress on Sealos Cloud.

![Joplin Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/joplin/website-screenshot.webp)

## About Hosting Joplin Server

Joplin Server stores note metadata, note contents, attachments, users, sessions, shares, and publishing state for Joplin desktop and mobile clients. It provides the admin web UI and sync API on the same HTTP service.

This Sealos template provisions a PostgreSQL cluster, a database initialization job that creates the `joplin` database, the Joplin Server container, HTTPS ingress, and an App launcher entry. The template follows the official server profile from the Joplin Docker Compose example and uses an external PostgreSQL database.

## Common Use Cases

- **Personal Note Sync**: Sync notes and resources across Joplin desktop and mobile clients.
- **Team Note Hosting**: Create users and manage team note synchronization from one server.
- **Self-Hosted Publishing**: Host shared notes and published content from your own workspace.
- **Private Knowledge Base**: Keep note data inside a controlled Sealos environment.

## Dependencies for Joplin Server Hosting

The Sealos template includes all required runtime dependencies: Joplin Server, PostgreSQL, a database init job, Service, Ingress, and App launcher entry.

### Deployment Dependencies

- [Joplin Server Documentation](https://github.com/laurent22/joplin/blob/dev/packages/server/README.md) - Official server setup guide
- [Joplin Docker Compose Example](https://raw.githubusercontent.com/laurent22/joplin/dev/docker-compose.server.yml) - Official Compose topology
- [Joplin GitHub Repository](https://github.com/laurent22/joplin) - Source code and releases

## Implementation Details

### Architecture Components

- **Joplin Server**: Runs the web UI and sync API on port `22300`
- **PostgreSQL**: Stores users, notes, item metadata, sessions, and sync state
- **Database Init Job**: Creates the `joplin` database before the app starts
- **Ingress**: Exposes the server over HTTPS with `APP_BASE_URL` aligned to the Sealos URL

### Resource Allocation

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Joplin Server | 20m | 200m | 25Mi | 256Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### Configuration

Joplin Server is configured with `DB_CLIENT=pg`, the Sealos public `APP_BASE_URL`, and PostgreSQL credentials from KubeBlocks-managed secrets. The container health probes use TCP checks because Joplin enforces origin checks on HTTP requests.

### License Information

Joplin is licensed under the [AGPL-3.0 License](https://github.com/laurent22/joplin/blob/dev/LICENSE). This template follows the licensing policy of the Sealos templates repository.

## Why Deploy Joplin Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies deployment and operations. By deploying Joplin Server on Sealos, you get:

- **One-Click Deployment**: Launch Joplin Server with PostgreSQL and HTTPS from one template page.
- **Managed PostgreSQL**: Store note sync data in a managed KubeBlocks PostgreSQL cluster.
- **Public Sync URL**: Use the generated HTTPS URL as the Joplin sync target.
- **Simple Operations**: Adjust resources and inspect logs from the Sealos Canvas.

## Deployment Guide

1. Open the [Joplin template](https://sealos.io/products/app-store/joplin) and click **Deploy Now**.
2. Review the generated parameters in the popup dialog and deploy.
3. Wait for PostgreSQL, the init job, and Joplin Server to become ready.
4. Open the generated URL and sign in with the default admin account:
   - Email: `admin@localhost`
   - Password: `admin`
5. Open the profile menu and change the admin password. Then create a sync user for regular Joplin clients.

## Configuration

Use the Joplin admin UI to create users and manage accounts. Use Sealos Canvas to adjust CPU, memory, hostname, or database storage.

In a Joplin client, set the sync target to **Joplin Server** and use the generated Sealos HTTPS URL.

## Scaling

This template is designed for a single Joplin Server instance. Start by increasing CPU and memory on the Deployment when sync traffic grows. Increase PostgreSQL storage as note data and attachments grow.

## Troubleshooting

**Issue: Login uses default credentials**
- Cause: Joplin Server creates `admin@localhost` / `admin` on first launch.
- Solution: Sign in once and immediately change the admin password.

**Issue: Sync client cannot connect**
- Cause: The client sync URL or user credentials are incorrect.
- Solution: Set the sync URL to the generated Sealos HTTPS URL and use a created Joplin user account.

## Additional Resources

- [Joplin Server README](https://github.com/laurent22/joplin/blob/dev/packages/server/README.md)
- [Joplin Help](https://joplinapp.org/help/)
- [Joplin GitHub Issues](https://github.com/laurent22/joplin/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing policy of the templates repository. Joplin itself is licensed under AGPL-3.0.
