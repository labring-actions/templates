# Deploy and Host drawDB on Sealos

drawDB is a browser-based database entity relationship diagram editor and SQL generator. This template deploys the drawDB static web app on Sealos Cloud with automatic HTTPS access.

![drawDB editor screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/drawdb/website-screenshot.webp)

## About Hosting drawDB

drawDB runs as a single web service served by NGINX. Users open the editor, choose a database dialect, build ER diagrams, import SQL, export diagrams, and generate SQL without creating an account.

The template deploys the core drawDB editor. Diagram data is stored in the browser through drawDB's client-side storage and can be exported or imported by users when they need portable files.

drawDB also offers an optional sharing backend through [drawdb-server](https://github.com/drawdb-io/drawdb-server). That backend requires external email and GitHub token configuration, so this template keeps the default account-free editor flow.

## Common Use Cases

- **Database schema design**: Create ER diagrams for new database projects.
- **SQL review**: Import SQL scripts and inspect table relationships visually.
- **Migration planning**: Generate SQL and compare schema changes before implementation.
- **Team documentation**: Export diagrams as files or images for architecture notes.
- **Learning databases**: Explore MySQL, PostgreSQL, SQLite, MariaDB, MSSQL, Oracle SQL, and generic schema models.

## Dependencies for drawDB Hosting

The Sealos template includes the drawDB web container, a Kubernetes Deployment, Service, Ingress, App link, and a small NGINX configuration that opens the editor route directly.

### Deployment Dependencies

- [Official Website](https://drawdb.app/) - Hosted drawDB product site
- [GitHub Repository](https://github.com/drawdb-io/drawdb) - Source code and Docker instructions
- [Official Documentation](https://drawdb-io.github.io/docs) - drawDB usage documentation
- [Optional Sharing Backend](https://github.com/drawdb-io/drawdb-server) - Separate server for sharing support

## Implementation Details

**Architecture Components:**

This template deploys one service:

- **drawDB Web App**: Static React application served by NGINX on port 80.

**Configuration:**

- The App link opens `/editor` so users land on the working editor.
- The NGINX configuration redirects `/` to `/editor`.
- The deployment uses the official `ghcr.io/drawdb-io/drawdb:v1.5.0` container image.
- Resource requests and limits follow the docker-to-sealos baseline for lightweight web services.
- No database, persistent volume, or object storage is required for the default editor flow.

**License Information:**

drawDB is licensed under the [AGPL-3.0 license](https://github.com/drawdb-io/drawdb/blob/main/LICENSE). This Sealos template follows the same application distribution terms.

## Why Deploy drawDB on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to operations. By deploying drawDB on Sealos, you get:

- **One-Click Deployment**: Deploy drawDB from the App Store template page without writing Kubernetes YAML.
- **Automatic HTTPS**: Every deployment receives a public URL with managed TLS.
- **Simple Operations**: Use Canvas, the AI dialog, and resource cards for post-deployment changes.
- **Pay-as-You-Go Efficiency**: Run a lightweight editor with small baseline resources.
- **Kubernetes Foundation**: Keep the portability and resilience of Kubernetes while using a simpler interface.

## Deployment Guide

1. Open the [drawDB template](https://sealos.io/products/app-store/drawdb) and click **Deploy Now**.
2. Configure the app name and public host in the popup dialog.
3. Wait for deployment to complete, usually 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
4. Access drawDB from the App link. The app opens the `/editor` route.
5. Choose a database dialect such as MySQL or PostgreSQL, then start adding tables and relationships.

## Configuration

The default deployment works without setup steps. To enable sharing features, deploy [drawdb-server](https://github.com/drawdb-io/drawdb-server) separately, configure its email and GitHub token settings, and provide its URL to the drawDB frontend through `VITE_BACKEND_URL` in a custom build.

## Scaling

drawDB is a static editor and usually runs well as a single replica. To adjust resources:

1. Open the Canvas for your deployment.
2. Click the drawDB Deployment resource card.
3. Adjust CPU, memory, or replica count.
4. Apply the change in the dialog.

## Troubleshooting

### The editor opens with an empty diagram

Choose a database dialect from the startup dialog, then add tables from the editor toolbar.

### Sharing options need server configuration

Use the optional [drawdb-server](https://github.com/drawdb-io/drawdb-server) project and connect a custom frontend build to that backend.

### Getting Help

- [Official Documentation](https://drawdb-io.github.io/docs)
- [GitHub Issues](https://github.com/drawdb-io/drawdb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [drawDB Website](https://drawdb.app/)
- [drawDB GitHub Repository](https://github.com/drawdb-io/drawdb)
- [drawDB Server](https://github.com/drawdb-io/drawdb-server)

## License

This Sealos template is provided for deploying drawDB on Sealos. drawDB itself is licensed under the [AGPL-3.0 license](https://github.com/drawdb-io/drawdb/blob/main/LICENSE).
