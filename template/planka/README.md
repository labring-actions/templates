# Deploy and Host PLANKA on Sealos

PLANKA is a real-time Kanban project management tool for teams and individuals. This template deploys PLANKA with a PostgreSQL database, persistent application data, and a public HTTPS endpoint on Sealos Cloud.

## About Hosting PLANKA

PLANKA helps teams organize projects with boards, lists, cards, labels, comments, attachments, and real-time collaboration. It is useful for replacing lightweight Trello-style workflows while keeping the deployment self-hosted.

This Sealos template provisions the PLANKA web application, a KubeBlocks PostgreSQL cluster, a database initialization job, persistent storage for `/app/data`, a Service, an Ingress, and a Sealos App entry. The template also configures `BASE_URL`, `DATABASE_URL`, proxy support, health checks, and initial administrator credentials.

PLANKA requires an administrator account for first access. During deployment, configure the initial admin email, username, password, and display name. After logging in, use the PLANKA administration UI to manage users and workspace settings.

## Common Use Cases

- **Team project tracking**: Manage tasks across projects with shared Kanban boards.
- **Product roadmaps**: Track features, milestones, labels, and ownership in one place.
- **Editorial workflows**: Move articles, issues, or design tasks through review stages.
- **Client workspaces**: Organize deliverables, discussions, and attachments by project.
- **Personal task management**: Keep private boards for individual planning and follow-up.

## Dependencies for PLANKA Hosting

The Sealos template includes all required runtime dependencies:

- **PLANKA 2.1.1**: The web application image `ghcr.io/plankanban/planka:2.1.1`.
- **PostgreSQL 16.4.0**: A KubeBlocks PostgreSQL cluster used by PLANKA.
- **Persistent storage**: 1 GiB for PLANKA application data and 1 GiB for PostgreSQL data.
- **Sealos networking**: Service, Ingress, automatic public URL, and TLS termination.

### Deployment Dependencies

- [PLANKA Documentation](https://docs.planka.cloud/docs/welcome/) - Official documentation.
- [Production Docker Guide](https://docs.planka.cloud/docs/installation/docker/production-version/) - Official production installation reference.
- [Configuration Reference](https://docs.planka.cloud/docs/category/configuration/) - PLANKA configuration options.
- [PLANKA GitHub Repository](https://github.com/plankanban/planka) - Source code and releases.

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **PLANKA StatefulSet**: Runs `ghcr.io/plankanban/planka:2.1.1`, exposes port `1337`, stores uploads and runtime data in `/app/data`, and waits for PostgreSQL before starting.
- **PostgreSQL Cluster**: Uses the Sealos KubeBlocks PostgreSQL 16.4.0 template with one replica and persistent data storage.
- **PostgreSQL Init Job**: Waits for PostgreSQL readiness and creates the `planka` database idempotently.
- **Service and Ingress**: Expose PLANKA through the generated Sealos public HTTPS URL.
- **Sealos App Resource**: Adds a clickable PLANKA entry in the Sealos dashboard.

**Configuration:**

- `BASE_URL` is set to the generated Sealos public URL.
- `DATABASE_URL` is built from the KubeBlocks PostgreSQL connection secret.
- `SECRET_KEY` is generated automatically by the template.
- `TRUST_PROXY` is enabled for Sealos Ingress TLS termination.
- `DEFAULT_ADMIN_EMAIL`, `DEFAULT_ADMIN_USERNAME`, `DEFAULT_ADMIN_PASSWORD`, and `DEFAULT_ADMIN_NAME` come from deployment inputs and create the initial administrator account on first launch.

**Resource Profile:**

- PLANKA application container: `100m` CPU and `128Mi` memory.
- PostgreSQL KubeBlocks component: `500m` CPU and `512Mi` memory.
- PLANKA application storage: `1Gi`.
- PostgreSQL data storage: `1Gi`.

The application resource profile was validated with a fresh Sealos deployment, login smoke test, dashboard access, and basic UI interactions.

**License Information:**

PLANKA is distributed under PLANKA's Fair Use License with Pro and Enterprise licensing options. This Sealos template is provided as part of the Sealos templates repository.

## Why Deploy PLANKA on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and database management. By deploying PLANKA on Sealos, you get:

- **One-Click Deployment**: Deploy the PLANKA application and PostgreSQL database from one template.
- **Easy Customization**: Configure administrator credentials and resource settings through the deployment dialog.
- **Persistent Storage Included**: Keep PLANKA uploads, runtime data, and PostgreSQL data across restarts.
- **Instant Public Access**: Use an automatically generated HTTPS URL after deployment.
- **Kubernetes-Native Runtime**: Run PLANKA with health checks, service discovery, and managed database resources.

## Deployment Guide

1. Open the [PLANKA template](https://sealos.io/products/app-store/planka) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **Initial administrator email address**: Email used for the first admin login.
   - **Initial administrator username**: Username for the first admin account.
   - **Initial administrator password**: Password for the first admin account.
   - **Initial administrator display name**: Display name shown in PLANKA.
3. Wait for deployment to complete. A fresh deployment typically takes a few minutes because PostgreSQL must become ready before PLANKA starts.
4. Access your application via the provided URL:
   - **PLANKA UI**: Open the generated Sealos public URL and log in with the administrator email or username and password configured in Step 2.
5. If PLANKA shows an end-user terms dialog on first login, scroll through it, check the confirmation box, and continue to the dashboard.
6. Create your first project from the dashboard, then add boards, lists, cards, labels, and users as needed.

## Configuration

After deployment, you can configure PLANKA through:

- **PLANKA Admin UI**: Log in with the initial administrator account and open the user/system administration menu.
- **Sealos AI Dialog**: Describe resource or configuration changes and let Sealos apply updates.
- **Resource Cards**: Click the StatefulSet, database, storage, Service, or Ingress cards in the Sealos Canvas to inspect or adjust runtime settings.

Public self-registration is not enabled by this template. Use the configured administrator account for first login, then manage users from PLANKA after setup.

## Scaling

To adjust resources:

1. Open the Canvas for your deployment.
2. Click the PLANKA StatefulSet or PostgreSQL resource card.
3. Adjust CPU, memory, or storage values according to your workload.
4. Apply the changes in the dialog and wait for the deployment to become ready again.

For larger teams, raise PLANKA memory before increasing traffic or upload volume. Keep PostgreSQL resources aligned with the size of your boards, cards, attachments, and activity history.

## Troubleshooting

### Login fails with the configured administrator account

- Cause: The administrator credentials were entered differently during deployment, or an existing database already contains users.
- Solution: Check the values configured during deployment. For a fresh template deployment, use the configured initial admin email or username plus the configured password.

### PLANKA takes several minutes to become available

- Cause: PLANKA waits for the KubeBlocks PostgreSQL service and database initialization job before starting.
- Solution: Wait for the PostgreSQL cluster and PLANKA StatefulSet to report ready in the Sealos Canvas.

### The public URL opens but login or redirects behave unexpectedly

- Cause: PLANKA requires `BASE_URL` to match the public endpoint.
- Solution: This template sets `BASE_URL` from the generated Sealos host. If you customize the domain, update `BASE_URL` accordingly.

### Getting Help

- [PLANKA Documentation](https://docs.planka.cloud/docs/welcome/)
- [PLANKA GitHub Issues](https://github.com/plankanban/planka/issues)
- [PLANKA Community Discord](https://discord.gg/WqqYNd7Jvt)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [PLANKA API Reference](https://plankanban.github.io/planka/swagger-ui/)
- [PLANKA Configuration Docs](https://docs.planka.cloud/docs/category/configuration/)
- [PLANKA Production Docker Guide](https://docs.planka.cloud/docs/installation/docker/production-version/)

## License

This Sealos template is provided as part of the Sealos templates repository. PLANKA itself is distributed under PLANKA's Fair Use License with Pro and Enterprise licensing options.
