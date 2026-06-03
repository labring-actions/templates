# Deploy and Host Postiz on Sealos

Postiz is an open source social media scheduling and management platform for planning, publishing, and tracking social posts. This template deploys Postiz with PostgreSQL, Redis, Temporal, Elasticsearch, and persistent storage on Sealos Cloud.

![Postiz Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/postiz/website-screenshot.webp)

## About Hosting Postiz

Postiz provides a self-hosted workspace for social media teams to schedule posts, manage channels, and coordinate publishing workflows. The Sealos template runs Postiz `v2.21.8` with the bundled frontend, backend API, orchestrator, and Nginx gateway in the main application container.

The deployment also provisions PostgreSQL for application and Temporal metadata, Redis for queue and cache services, Temporal for workflow execution, Elasticsearch for Temporal visibility, and persistent volumes for uploads and runtime configuration. Sealos creates the public HTTPS endpoint, service discovery, database resources, and storage resources automatically.

This template is configured for the simplest first-run setup: local email-and-password registration is enabled by default. OAuth providers, Resend, email verification, and password reset email delivery are not required for creating the first account.

## Common Use Cases

- **Social media scheduling**: Plan and publish posts across connected social channels from one self-hosted dashboard.
- **Team content operations**: Coordinate content calendars, drafts, and publishing workflows in a private workspace.
- **Agency publishing workflows**: Manage multiple client social accounts while keeping data in your own Sealos workspace.
- **Self-hosted social tooling**: Run Postiz without depending on a hosted SaaS account or external identity provider for first login.

## Dependencies for Postiz Hosting

The Sealos template includes all required runtime dependencies: the Postiz application image, PostgreSQL 16.4, Redis 7.2, Temporal 1.28, Elasticsearch 7.17, persistent upload storage, and persistent configuration storage.

### Deployment Dependencies

- [Postiz Website](https://postiz.com/) - Product website and overview
- [Postiz Documentation](https://docs.postiz.com/introduction) - Official documentation and setup guides
- [Postiz Source Repository](https://github.com/gitroomhq/postiz-app) - Source code and issue tracker
- [Sealos Documentation](https://sealos.io/docs) - Sealos Cloud documentation

## Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Postiz application**: Runs `ghcr.io/gitroomhq/postiz-app:v2.21.8` and serves the web UI, API, Nginx gateway, and orchestrator through port `5000`.
- **PostgreSQL 16.4**: Stores Postiz application data and the Temporal metadata databases. A setup job creates the `postiz` database before the app starts.
- **Redis 7.2**: Provides cache and queue backing services for Postiz.
- **Temporal 1.28**: Runs workflow processing required by Postiz background jobs.
- **Temporal Elasticsearch 7.17**: Stores Temporal visibility data with a 256 MiB heap.
- **Persistent volumes**: Store uploads at `/uploads` and application configuration at `/config`.

**Configuration:**

The template automatically generates the app name, public hostname, and JWT secret. The app uses local storage by default and sets `DISABLE_REGISTRATION=false`, so the first user can register with an email address and password immediately after deployment.

Default service-to-service connections are configured through Kubernetes DNS and Sealos-provisioned database credentials. PostgreSQL connection limits are set conservatively so Postiz and Temporal can share the default database baseline.

**Resource Profile:**

| Component | CPU limit | Memory limit | Notes |
| --- | ---: | ---: | --- |
| Postiz app | `500m` | `4096Mi` | Covers Nginx, frontend, backend, and orchestrator in one container; 4 GiB is required for cold-start workflow bundle generation. |
| PostgreSQL | `500m` | `512Mi` | Uses the Sealos PostgreSQL database baseline. |
| Redis | `500m` | `512Mi` | Uses the Sealos Redis and Sentinel database baseline. |
| Temporal | `500m` | `512Mi` | Runs the Temporal service and default namespace setup. |
| Temporal Elasticsearch | `500m` | `1024Mi` | Runs Elasticsearch with a 256 MiB heap for Temporal visibility. |

**License Information:**

This Sealos template is provided as part of the Sealos templates repository. Postiz itself is licensed under the GNU Affero General Public License v3.0.

## Why Deploy Postiz on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is well suited for running modern SaaS tools, workflow systems, and multi-service applications. By deploying Postiz on Sealos, you get:

- **One-Click Deployment**: Deploy Postiz, PostgreSQL, Redis, Temporal, Elasticsearch, ingress, and storage from one template.
- **Kubernetes Without Operational Overhead**: Use Kubernetes-backed workloads, service discovery, persistent storage, and health checks without writing YAML by hand.
- **Instant Public Access**: Sealos provisions a public HTTPS URL for the Postiz web interface.
- **Easy Customization**: Adjust environment variables, resources, and storage through the Canvas, AI dialog, or resource cards.
- **Persistent Storage Included**: Uploaded media and application configuration survive restarts and redeployments.
- **Pay-As-You-Go Resources**: Tune CPU, memory, and storage to match your actual workload.
- **Operational Visibility**: Inspect logs, workload status, and resource usage from the Sealos dashboard.

Deploy Postiz on Sealos and focus on social publishing workflows instead of managing the underlying infrastructure.

## Deployment Guide

1. Open the [Postiz template](https://sealos.io/products/app-store/postiz) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. For the simplest setup, keep the default values.
3. Wait for deployment to complete. It typically takes 2-3 minutes, but the first startup can take longer because PostgreSQL, Redis, Temporal, Elasticsearch, and Postiz all need to initialize. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog to let Sealos apply updates, or click the relevant resource cards to modify settings.
4. Access Postiz through the generated public URL and create the first local account.

## First Login and Registration

Postiz is a web application that requires a user account. This template enables local registration by default, so the first account can be created with only an email address and password.

1. Open the generated Postiz URL after deployment.
2. A new deployment opens the local sign-up page at `/auth`. If you land on the login page instead, open `/auth` manually or use the sign-up option in the UI.
3. Ignore OAuth buttons for the first account and use the local registration form below the separator.
4. Enter an email address, a password, and the workspace or company name, then click **Create Account**.
5. The account is activated immediately because the default template does not configure an email provider or email verification.
6. If Postiz asks you to sign in after registration, open `/auth/login` and use the same email address and password.

Use an email address as the username. A direct login attempt returns `Invalid user name or password` until that email has been registered in the current deployment. The registration page is `/auth`; `/auth/register` is not a Postiz route. GitHub OAuth, Google OAuth, X/Twitter API credentials, Resend, and email verification are optional later integrations, not requirements for the first login.

## Configuration

After deployment, you can configure Postiz through:

- **AI Dialog**: Describe the changes you want and let Sealos apply updates.
- **Resource Cards**: Click the StatefulSet, Deployment, database, cache, ingress, or storage cards to modify settings.
- **Postiz UI**: Connect social channels and configure publishing integrations from inside Postiz.
- **Environment Variables**: Add OAuth, email, or social provider credentials only when you are ready to enable those integrations.

Important default environment settings:

| Setting | Default | Purpose |
| --- | --- | --- |
| `DISABLE_REGISTRATION` | `false` | Allows local user registration. |
| `IS_GENERAL` | `true` | Enables the general self-hosted Postiz experience. |
| `STORAGE_PROVIDER` | `local` | Stores uploads on the mounted `/uploads` volume. |
| `TEMPORAL_NAMESPACE` | `default` | Uses the default Temporal namespace created during deployment. |

## Scaling

To scale or tune Postiz:

1. Open the Canvas for your deployment.
2. Click the relevant resource card, such as the Postiz StatefulSet, Temporal Deployment, PostgreSQL cluster, Redis cluster, or Elasticsearch StatefulSet.
3. Adjust CPU, memory, storage, or replica settings according to your workload.
4. Apply the changes in the dialog and monitor workload readiness from the Sealos dashboard.

For small self-hosted workspaces, keep the default single-replica topology. Increase resources before connecting many channels, processing large media uploads, or running high-volume publishing workflows.

## Troubleshooting

### The page is not ready immediately after deployment

Wait for all components to become Running. Temporal and Elasticsearch may take longer than the main web container during cold start.

### Login says `Invalid user name or password`

Create the account first on `/auth`. Direct login only works after the email address exists in the current Postiz deployment.

### Registration asks for email activation

Check whether an email provider or verification setting was added after deployment. With the default template configuration, local users are activated immediately.

### Social posting fails

Confirm that the relevant social provider credentials are configured and that the channel has been connected from the Postiz UI.

### Uploads fail

Check the `/uploads` persistent volume and available storage capacity.

### Getting Help

- [Postiz Documentation](https://docs.postiz.com/introduction)
- [Postiz GitHub Issues](https://github.com/gitroomhq/postiz-app/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Postiz Website](https://postiz.com/)
- [Postiz Source Repository](https://github.com/gitroomhq/postiz-app)
- [Sealos App Store](https://sealos.io/products/app-store)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided as part of the Sealos templates repository. Postiz itself is licensed under the [GNU Affero General Public License v3.0](https://github.com/gitroomhq/postiz-app/blob/main/LICENSE).
