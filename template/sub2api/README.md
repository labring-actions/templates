# Deploy and Host Sub2API on Sealos

Sub2API is an AI API gateway platform for distributing and managing subscription quota across upstream AI services. This template deploys Sub2API with PostgreSQL, Redis, persistent storage, and public HTTPS access on Sealos Cloud.

## About Hosting Sub2API

Sub2API gives you a self-hosted control plane for routing AI traffic, issuing and managing API keys, enforcing quota policies, and operating billing or scheduling workflows across upstream providers. The Sealos template packages the application into a ready-to-run deployment so you can launch the gateway without wiring database credentials, Redis access, storage, or ingress rules by hand.

The deployment uses PostgreSQL for persistent application data, Redis for fast in-memory state and coordination, and a dedicated persistent volume for `/app/data`. Sealos also provisions an HTTPS endpoint, generated runtime secrets for JWT and TOTP encryption, and the application URL in the Sealos dashboard so the instance is ready for first-time setup as soon as the pods become healthy.

## Common Use Cases

- **Centralized AI Gateway**: Route requests from internal tools or customer apps through a single endpoint instead of exposing multiple upstream provider credentials.
- **Quota and Spend Governance**: Track subscription usage, distribute quotas across teams, and control how shared upstream capacity is consumed.
- **Multi-Account Operations**: Connect multiple upstream AI accounts and manage allocation, failover, and key distribution from one admin plane.
- **Secure Team Access**: Give operators or internal customers controlled access to a web console for account management and billing workflows.
- **Provider-Specific Integrations**: Configure Gemini OAuth-related settings and policy controls for providers that require additional authorization flows.

## Dependencies for Sub2API Hosting

The Sealos template includes all required components: Sub2API `0.1.104`, PostgreSQL `16.4.0`, Redis `7.2.7`, persistent volumes, HTTPS ingress, and an application record in Sealos Canvas.

### Deployment Dependencies

- [Sub2API GitHub Repository](https://github.com/Wei-Shaw/sub2api) - Upstream source code and project information
- [Sub2API Demo](https://demo.sub2api.org/) - Public demo environment
- [Sub2API Issues](https://github.com/Wei-Shaw/sub2api/issues) - Bug reports and feature discussions
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - PostgreSQL reference
- [Redis Documentation](https://redis.io/docs/latest/) - Redis reference
- [Sealos Documentation](https://sealos.io/docs) - Platform documentation
- [Sealos Discord](https://discord.gg/wdUn538zVP) - Community support

## Implementation Details

### Architecture Components

This template deploys the following services:

- **Sub2API Application**: A `StatefulSet` running `weishaw/sub2api:0.1.104`, exposing HTTP on port `8080` and storing runtime files in `/app/data`.
- **PostgreSQL**: A KubeBlocks PostgreSQL `16.4.0` cluster with a `1Gi` persistent volume for durable application data.
- **PostgreSQL Init Job**: An initialization job that waits for PostgreSQL readiness and creates the `sub2api` database if it does not already exist.
- **Redis**: A KubeBlocks Redis `7.2.7` deployment with replication topology and Sentinel support for high-availability coordination inside the cluster.
- **Ingress and App Resource**: A public HTTPS endpoint backed by Sealos-managed ingress plus an `App` resource that surfaces the application URL in Canvas.

### Configuration

The most important runtime settings are exposed as Sealos form inputs:

- `admin_email`: Initial administrator email address
- `admin_password`: Initial administrator password; leave empty to auto-generate a password on first startup
- `timezone`: Application timezone, defaulting to `Asia/Shanghai`
- `run_mode`: `standard` or `simple`
- `gemini_oauth_client_id`, `gemini_oauth_client_secret`, `gemini_oauth_scopes`, `gemini_quota_policy`
- `gemini_cli_oauth_client_secret`, `antigravity_oauth_client_secret`
- `security_url_allowlist_enabled`, `security_url_allowlist_allow_insecure_http`, `security_url_allowlist_allow_private_hosts`, `security_url_allowlist_upstream_hosts`
- `update_proxy_url`: Optional outbound proxy for update checks and GitHub access

The template also generates the following secrets automatically:

- `JWT_SECRET`
- `TOTP_ENCRYPTION_KEY`

### Operational Characteristics

- Health checks use `GET /health` on port `8080`.
- The application runs with `AUTO_SETUP=true` for first-start bootstrap.
- Database connection details are injected from the KubeBlocks PostgreSQL connection secret.
- Redis credentials are injected from the KubeBlocks Redis secret.
- Public access is served from `https://<app-host>.<your-sealos-domain>`.

### License Information

Sub2API is distributed under the license defined by the upstream project. Review the license file in the upstream repository before production use or redistribution.

## Why Deploy Sub2API on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies deployment and operations for modern applications. By deploying Sub2API on Sealos, you get:

- **One-Click Deployment**: Launch the gateway, PostgreSQL, Redis, storage, and ingress together without writing Kubernetes manifests.
- **Built-In Infrastructure Services**: Databases, secrets, storage, networking, and SSL are provisioned as part of the template.
- **Easy Post-Deployment Changes**: Update configuration through the AI dialog or resource cards in Canvas instead of editing manifests manually.
- **Persistent Storage Included**: Application data, PostgreSQL data, and Redis data survive restarts and routine maintenance.
- **Public HTTPS Access**: Every deployment gets a public URL with managed TLS.
- **Pay-As-You-Go Efficiency**: Resource-based billing makes it easy to start small and scale when traffic increases.
- **Kubernetes Reliability Without the Overhead**: You get the scheduling and lifecycle benefits of Kubernetes without having to operate the platform yourself.

Deploy Sub2API on Sealos and focus on API governance and service integrations instead of infrastructure assembly.

## Deployment Guide

1. Open the [Sub2API template](https://sealos.io/products/app-store/sub2api) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
   - Set `admin_email` for the first administrator account.
   - Optionally set `admin_password`, or leave it empty to let Sub2API generate a one-time password during first startup.
   - Choose the `timezone` and `run_mode`.
   - Fill in Gemini OAuth and allowlist settings only if your deployment requires them.
   - Set `update_proxy_url` if outbound access to GitHub or update endpoints must go through a proxy.
3. Wait for deployment to complete, which typically takes 2-3 minutes. After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Access your application via the provided URL.
   - **Admin UI**: Open `https://<app-host>.<your-sealos-domain>` and sign in with the configured administrator credentials.
   - **Gateway Endpoint**: Use the same public base URL for API access according to your Sub2API routing configuration.

If `admin_password` is empty, check the application logs after first startup to retrieve the generated administrator password.

## Configuration

After deployment, you can manage Sub2API through:

- **AI Dialog**: Describe the change you want, such as updating environment variables or adjusting resources.
- **Resource Cards**: Open the Sub2API, PostgreSQL, Redis, Job, or Ingress cards in Canvas to inspect or update resources.
- **Application Settings**: Use the Sub2API web console to manage upstream accounts, quotas, billing logic, routing rules, and API key distribution after sign-in.

## Scaling

This template is configured with a single Sub2API application replica by default. For most deployments, scaling should start with CPU, memory, and storage adjustments through Canvas:

1. Open the deployment in Canvas.
2. Click the `StatefulSet`, PostgreSQL, or Redis resource card that you want to scale.
3. Increase CPU, memory, or storage based on observed traffic and usage.
4. Apply the changes in the dialog and monitor health status after the update.

If you plan to run multiple application replicas, validate Sub2API's session, storage, and coordination behavior in your environment before changing replica count.

## Troubleshooting

### Common Issues

**Issue 1: The login page does not open after deployment**
- Cause: One of the dependent resources is not ready yet.
- Solution: Check whether the PostgreSQL init job completed successfully and confirm the Sub2API `StatefulSet`, PostgreSQL cluster, and Redis cluster are all healthy in Canvas.

**Issue 2: I left `admin_password` empty and cannot sign in**
- Cause: The password was auto-generated during first startup.
- Solution: Open the Sub2API container logs and search for the generated administrator password emitted during initialization.

**Issue 3: Upstream API requests are blocked**
- Cause: URL allowlist restrictions do not match your environment.
- Solution: Review `security_url_allowlist_enabled`, `security_url_allowlist_allow_insecure_http`, `security_url_allowlist_allow_private_hosts`, and `security_url_allowlist_upstream_hosts`.

**Issue 4: Online update checks cannot reach GitHub**
- Cause: Your environment requires an outbound proxy.
- Solution: Set `update_proxy_url` and redeploy or update the application environment variables.

**Issue 5: The application stays unhealthy during startup**
- Cause: PostgreSQL or Redis may not be ready yet, or the initialization process is still running.
- Solution: Wait for the dependency pods and the PostgreSQL init job to complete, then recheck the `/health` endpoint through the application status in Canvas.

### Getting Help

- [Sub2API GitHub Repository](https://github.com/Wei-Shaw/sub2api)
- [Sub2API Issues](https://github.com/Wei-Shaw/sub2api/issues)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided as part of the templates repository. Sub2API itself is licensed by its upstream project; refer to the upstream repository for the current license terms.
