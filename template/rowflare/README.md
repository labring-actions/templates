# Deploy and Host Rowflare on Sealos

Rowflare is an open-source Airtable alternative with grid, kanban, calendar, timeline, gallery and form views, formulas, automations, a REST API and an MCP server. This template deploys the official Rowflare Docker image on Sealos Cloud with persistent storage and a public HTTPS address.

![Rowflare website](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rowflare/website-screenshot.webp)

## About Hosting Rowflare

Rowflare is a spreadsheet-style database: each base holds linked tables with typed fields, formulas in the Airtable formula language, rollups and lookups, and several views of the same records. Teams collaborate in real time, and integrations use a REST API modeled on the Airtable Web API or the built-in MCP server for AI clients.

The Docker image runs the same Worker code as Rowflare's Cloudflare deployment inside workerd, Cloudflare's open-source Workers runtime. Accounts, one SQLite database per base, and attachments are all stored under `/data`, so this template runs a single StatefulSet with a persistent volume and needs no external database or object storage.

The screenshot above shows the official product website. After deployment, the App address opens the Rowflare sign-in page.

## Common Use Cases

- **Project and task tracking**: Plan work in grid, kanban, calendar and timeline views with rollups for progress.
- **Lightweight CRM**: Track companies, contacts and deals with linked records and formula fields.
- **Airtable migration**: Import bases from Airtable or CSV and keep the data in your own workspace.
- **Internal data collection**: Publish forms and collect submissions straight into a table.
- **Automation and AI workflows**: Trigger automations on record changes, call the REST API, or connect AI clients through MCP.

## Dependencies for Rowflare Hosting

The official image includes the web app, the API server and the storage engine. No database cluster, cache or object storage is required.

### Deployment Dependencies

- [Rowflare website](https://rowflare.com) - Product overview
- [Rowflare GitHub repository](https://github.com/rowflare/rowflare) - Source code and issues
- [Self-hosting guide](https://github.com/rowflare/rowflare/blob/main/docs/self-hosting.md) - Docker image, settings and backups
- [REST API reference](https://github.com/rowflare/rowflare/blob/main/docs/api.md) - API for scripts and integrations

### Implementation Details

- **Image**: `rowflare/rowflare:0.1.0`, pinned by its multi-arch index digest.
- **Runtime**: One StatefulSet replica listening on port `8787`, a Service, an HTTPS Ingress and a Sealos App entry.
- **Storage**: A 1 GiB persistent volume at `/data` holds the accounts database, every base and all attachments. Expand it from the resource card when your data grows.
- **Settings**: `MODE=selfhost` and `ALLOW_SIGNUP=false`, so the first account becomes the owner and later users join by invite. `SECRET_KEY` is generated at deploy time and encrypts the AI service keys and SMTP or Resend credentials that workspace owners save. `APP_URL` is set to the generated HTTPS address for absolute links in emails and automations.
- **Health checks**: Startup, readiness and liveness probes call `/api/config`.
- **Security**: The container runs as user and group `1000` with all Linux capabilities dropped and service-account token mounting disabled.
- **Resources**: `500m` CPU and `512Mi` memory limits with `50m` CPU and `51Mi` memory requests.

## Why Deploy Rowflare on Sealos?

Sealos runs Rowflare on Kubernetes with one-click deployment, so you get a working instance without writing manifests or configuring a reverse proxy.

- **One-click deployment**: The template creates the workload, persistent volume, Service, Ingress and App entry together.
- **Kubernetes foundation**: Health checks restart the container if it stops responding.
- **Pay-as-you-go resources**: You pay for the CPU, memory and storage the instance uses.
- **Persistent storage**: Bases and attachments survive restarts and redeployments.
- **Public HTTPS**: Sealos issues the domain and TLS certificate automatically.
- **Canvas and AI dialog**: After deployment, use the Canvas AI dialog to describe configuration changes, or open the StatefulSet, Service and Ingress resource cards to adjust settings such as resources, storage or environment variables.

## Deployment Guide

1. Open the [Rowflare template](https://sealos.io/products/app-store/rowflare) and click **Deploy Now**.
2. Review the generated application name and resource settings, then start deployment.
3. Wait for deployment to complete, typically **2-3 minutes**. Sealos then opens the Canvas for your deployment.
4. Open the Rowflare App address and click **Sign up** right away. The first account becomes the owner of the instance; after that, sign-up closes.
5. Create a base from a template such as **Project tracker**, or import a CSV file or an Airtable base.
6. Invite teammates from the workspace settings. Each invite link works for 7 days.

## Configuration

Change these environment variables on the StatefulSet resource card. The container restarts with the new values.

- `ALLOW_SIGNUP`: Set to `true` to let anyone who can reach the instance create an account.
- `MAIL_PROVIDER`, `MAIL_FROM`, `RESEND_API_KEY` or `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURITY`, `SMTP_USERNAME`, `SMTP_PASSWORD`: Enable account emails such as address confirmation and password reset.
- `AUTOMATION_MONTHLY_RUNS`: Automation runs per base per month (default `10000`, `0` for no limit).
- `APP_URL`: Update it when you bind a custom domain.

Keep `SECRET_KEY` unchanged. Changing it makes saved AI and email credentials unreadable, and owners must enter them again.

## Troubleshooting

- **Sign-up says it is invite-only**: The first account already exists. Ask the owner for an invite link, or set `ALLOW_SIGNUP=true`.
- **Forgot the owner password**: Without account email settings there is no reset link. Configure `MAIL_PROVIDER` first, then use **Forgot password?** on the sign-in page.
- **Storage is full**: Expand the `/data` volume from the StatefulSet resource card.

## License

Rowflare is available under the [AGPL-3.0 license](https://github.com/rowflare/rowflare/blob/main/LICENSE).
