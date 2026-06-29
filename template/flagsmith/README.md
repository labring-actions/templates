# Deploy and Host Flagsmith on Sealos

Flagsmith is an open-source feature flag and remote configuration platform. This template deploys Flagsmith with a KubeBlocks PostgreSQL database and a background task processor on Sealos Cloud.

![Flagsmith Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/flagsmith/website-screenshot.webp)

## About Hosting Flagsmith

Flagsmith provides a dashboard and API for managing feature flags, remote configuration, identity-based targeting, and experimentation workflows. The combined web/API service serves the user interface and REST API from one public endpoint.

The template provisions PostgreSQL for application and analytics data, runs database migrations during startup, and starts a private task processor for asynchronous jobs. Sealos provides HTTPS ingress, Kubernetes orchestration, persistent database storage, and operational controls through Canvas.

## Common Use Cases

- **Feature Rollouts**: Release functionality gradually by environment, segment, or identity.
- **Remote Configuration**: Change application behavior without redeploying code.
- **Experimentation**: Manage A/B tests and feature variants from one dashboard.
- **SDK Management**: Serve feature flag values to web, mobile, and backend SDKs.

## Dependencies for Flagsmith Hosting

The Sealos template includes the Flagsmith web/API service, the Flagsmith task processor, and KubeBlocks PostgreSQL.

### Deployment Dependencies

- [Flagsmith Documentation](https://docs.flagsmith.com/) - Official documentation
- [Docker Hosting Guide](https://docs.flagsmith.com/deployment-self-hosting/hosting-guides/docker) - Official Docker runtime layout
- [Environment Variables](https://docs.flagsmith.com/deployment-self-hosting/core-configuration/environment-variables) - Configuration reference
- [GitHub Repository](https://github.com/Flagsmith/flagsmith) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys three services:

- **Flagsmith Web/API**: Combined dashboard and REST API on port 8000.
- **Task Processor**: Private background worker for asynchronous task execution.
- **PostgreSQL**: KubeBlocks-managed database for core data and analytics.

**Configuration:**

Flagsmith connects to PostgreSQL through KubeBlocks credentials using `DATABASE_URL`. The public domain is injected through `FLAGSMITH_DOMAIN`, registration is enabled for first-time setup, and task execution uses the dedicated task processor. Official documentation also supports external object storage for selected enterprise and import/export workflows; this template keeps storage local to PostgreSQL unless you intentionally add S3 configuration after deployment.

**License Information:**

Flagsmith is licensed under the BSD-3-Clause License. This Sealos template is provided under the repository license.

## Why Deploy Flagsmith on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operations, and scaling. By deploying Flagsmith on Sealos, you get:

- **One-Click Deployment**: Deploy the dashboard, API, task processor, and database from one template.
- **Managed PostgreSQL**: Use KubeBlocks-managed PostgreSQL with persistent storage.
- **Instant HTTPS Access**: Receive a public HTTPS URL for the Flagsmith dashboard and API.
- **Canvas Operations**: Tune resources, inspect logs, and apply changes through Canvas, AI dialog, and resource cards.
- **Pay-as-You-Go Resources**: Run Flagsmith with practical resource limits and adjust them as adoption grows.

## Deployment Guide

1. Open the [Flagsmith template](https://sealos.io/products/app-store/flagsmith) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **Flagsmith Dashboard**: Open the URL and create your first account from `/signup`.
   - **Flagsmith API**: Use the same base URL for SDK and REST API access.

## Configuration

After deployment, you can configure Flagsmith through:

- **Dashboard**: Create organisations, projects, environments, feature flags, and segments.
- **SDK Settings**: Copy client and server-side environment keys for application integration.
- **AI Dialog**: Describe changes such as resource updates or environment variable changes.
- **Resource Cards**: Modify web/API, task processor, ingress, and database resources.

## Scaling

To scale Flagsmith:

1. Open the Canvas for your deployment.
2. Click the web/API, task processor, or PostgreSQL resource card.
3. Adjust CPU, memory, storage, or replica settings.
4. Apply the changes in the dialog.

## Troubleshooting

### Signup page is unavailable

- Cause: Registration settings or startup migrations are still settling.
- Solution: Wait for the web/API service to become ready, then open `/signup` again.

### SDK clients cannot connect

- Cause: SDKs are pointing at the hosted Flagsmith cloud endpoint.
- Solution: Configure SDK base URLs to the Sealos-provided Flagsmith URL.

### Background tasks do not run

- Cause: The task processor is unhealthy or cannot reach PostgreSQL.
- Solution: Check the task processor resource card logs and verify PostgreSQL is running.

## Additional Resources

- [Flagsmith SDK API](https://docs.flagsmith.com/sdk-api/)
- [Self-Hosting Overview](https://docs.flagsmith.com/deployment-self-hosting/)
- [Sealos](https://sealos.io)

## License

This Sealos template is provided under the repository license. Flagsmith itself is licensed under the BSD-3-Clause License.
