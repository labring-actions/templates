# Deploy and Host ToolJet on Sealos

ToolJet is an open-source low-code platform for building internal tools, dashboards, business applications, and workflow interfaces. This template deploys ToolJet CE on Sealos Cloud with PostgreSQL, Redis, PostgREST, database initialization jobs, and a public HTTPS endpoint.

## About Hosting ToolJet

ToolJet runs as a web-based application builder. Teams can connect databases and APIs, design internal admin panels, build dashboards, and automate operational workflows from a browser.

This Sealos template provisions the services ToolJet needs for a production-style single-instance deployment. PostgreSQL stores ToolJet metadata and the ToolJet database, Redis supports realtime and background features, and PostgREST exposes the ToolJet database API required by ToolJet.

The template also runs initialization and migration jobs before the web application starts. This avoids first-boot schema errors and ensures the setup page is ready when the public URL becomes available.

## Common Use Cases

- **Internal admin panels**: Build CRUD interfaces for operations, support, finance, or business teams.
- **Dashboards and reporting**: Connect data sources and create lightweight dashboards for internal users.
- **Workflow tools**: Build approval flows, ticket triage tools, and operational workflows.
- **Database-backed apps**: Use PostgreSQL, REST APIs, and other data sources to build secure internal applications.
- **Prototype business apps**: Validate internal tools quickly before investing in custom development.

## Dependencies for ToolJet Hosting

The Sealos template includes the required runtime and services:

- **ToolJet CE**: `tooljet/tooljet-ce:v3.20.170-lts`
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4.0, 1 Gi storage
- **Redis**: KubeBlocks Redis with Sentinel, 2 Gi total storage
- **PostgREST**: PostgREST v12.0.2 for ToolJet database APIs
- **Initialization jobs**: PostgreSQL database creation and ToolJet schema migrations

### Deployment Dependencies

- [ToolJet Documentation](https://docs.tooljet.ai/) - Official ToolJet documentation
- [ToolJet GitHub Repository](https://github.com/ToolJet/ToolJet) - Source code and releases
- [Sealos Documentation](https://sealos.io/docs) - Sealos deployment and operations guide

## Implementation Details

### Architecture Components

This template deploys the following components:

- **ToolJet web application**: Serves the frontend and backend API on port `3000`.
- **PostgreSQL cluster**: Stores `tooljet_production` and `tooljet_db` databases.
- **Redis cluster**: Provides cache and realtime coordination used by ToolJet.
- **PostgREST deployment**: Provides the internal REST endpoint for ToolJet DB features.
- **Database init job**: Creates the two required PostgreSQL databases before migrations.
- **Migration job**: Runs ToolJet production database and data migrations.
- **Ingress and Service**: Exposes ToolJet through a Sealos-managed HTTPS URL.

### Resource Profile

The template is tuned from live Sealos testing for a minimal working single-instance deployment:

- ToolJet app: `500m` CPU, `1536Mi` memory
- Migration job: `1` CPU, `2Gi` memory
- PostgreSQL: `200m` CPU, `256Mi` memory, `1Gi` storage
- Redis: two `200m` CPU / `256Mi` memory components, `1Gi` storage each
- PostgREST: `200m` CPU, `256Mi` memory

ToolJet opens multiple database connections at runtime. The template starts the main app through the PostgreSQL pooler port while keeping ToolJet DB operations on the direct PostgreSQL port, because ToolJet passes `statement_timeout` for the ToolJet DB connection.

### Configuration

The template generates the required ToolJet secrets automatically:

- `LOCKBOX_MASTER_KEY`
- `SECRET_KEY_BASE`
- `PGRST_JWT_SECRET`

The `admin_email` input is used as the default sender email for first-run guidance. ToolJet still asks you to create the first admin account in the browser during setup.

### License Information

ToolJet is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This Sealos template follows the templates repository license.

## Why Deploy ToolJet on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and operations. By deploying ToolJet on Sealos, you get:

- **One-click deployment**: Deploy ToolJet and all required services from a single template.
- **Managed public access**: Get an automatic HTTPS URL without manual ingress setup.
- **Persistent storage**: Keep PostgreSQL and Redis data across restarts.
- **Integrated operations**: Adjust resources and inspect logs from the Sealos Canvas.
- **Kubernetes without complexity**: Run ToolJet on Kubernetes without writing manifests yourself.

## Deployment Guide

1. Open the [ToolJet template](https://sealos.io/products/app-store/tooljet) and click **Deploy Now**.
2. Review the `admin_email` parameter. The default value is enough for testing, and you can enter your own email for production guidance.
3. Click **Deploy** and wait for the PostgreSQL, Redis, PostgREST, migration job, and ToolJet app to become ready. First deployment can take several minutes because ToolJet runs database migrations.
4. Open the application URL generated by Sealos, for example `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`.

## First-Run Setup and Login

ToolJet requires a browser-based first-run setup:

1. Open the Sealos application URL.
2. On **Set up your admin account**, enter your name, work email, and password, then click **Sign up**.
3. On **Set up your workspace**, keep the suggested workspace name or enter your own name, then click **Continue**.
4. After setup, ToolJet opens the workspace dashboard. You can click **Create an app** or **Create new application** to start building.
5. For later access, open `/login` on the same app URL and sign in with the email and password created during setup.

The template sets `SMTP_DISABLED=true` by default, so first-run registration does not require email verification. Configure SMTP after deployment if you need invitation emails, password reset emails, or production email delivery.

## Configuration

After deployment, you can configure ToolJet through:

- **ToolJet workspace settings**: Manage users, apps, data sources, and workspace preferences.
- **Sealos Canvas**: Inspect pods, logs, and resources for ToolJet, PostgreSQL, Redis, and PostgREST.
- **Resource cards**: Adjust CPU, memory, or storage if your workspace grows beyond the default single-instance profile.

## Scaling

To scale or tune the deployment:

1. Open the Canvas for your ToolJet deployment.
2. Click the ToolJet application resource card to adjust CPU or memory.
3. Click the PostgreSQL or Redis resource cards to adjust database resources or storage.
4. Apply changes and wait for the affected resources to restart.

For active production use, increase PostgreSQL and ToolJet resources before adding many users, heavy dashboards, or large numbers of data sources.

## Troubleshooting

### Setup page does not appear

Wait until the migration job has completed and the ToolJet deployment is ready. The template blocks the web app startup until required database tables exist.

### Cannot create apps or database requests fail

Check the PostgreSQL and ToolJet logs in Sealos Canvas. ToolJet needs PostgreSQL, Redis, and PostgREST to be running. If the workspace grows, increase PostgreSQL and ToolJet resources.

### Email invitations or password reset do not send

SMTP is disabled by default. Configure SMTP-related ToolJet environment variables before relying on invitation or password reset email delivery.

### Getting Help

- [ToolJet Documentation](https://docs.tooljet.ai/)
- [ToolJet GitHub Issues](https://github.com/ToolJet/ToolJet/issues)
- [Sealos Documentation](https://sealos.io/docs)

## Additional Resources

- [ToolJet Website](https://www.tooljet.ai/)
- [ToolJet Documentation](https://docs.tooljet.ai/)
- [ToolJet GitHub Repository](https://github.com/ToolJet/ToolJet)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the templates repository license. ToolJet itself is licensed under AGPL-3.0.
