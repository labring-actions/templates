# Deploy and Host BunkerWeb on Sealos

BunkerWeb is an open-source Web Application Firewall and reverse proxy built on NGINX. This template deploys BunkerWeb with the scheduler, Web UI, PostgreSQL, Redis, a protected demo backend, and optional S3-compatible backup wiring on Sealos Cloud.

![BunkerWeb Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bunkerweb/website-screenshot.webp)

## About Hosting BunkerWeb

BunkerWeb protects web services through an NGINX-based reverse proxy with security features such as ModSecurity, rate limiting, IP controls, bot protections, custom headers, gzip, cache controls, and centralized configuration. The scheduler computes and pushes configuration to BunkerWeb instances, while the Web UI provides an administrator console for services, instances, jobs, plugins, reports, and settings.

This Sealos template follows the official BunkerWeb multi-container deployment model. It runs BunkerWeb as the traffic gateway, a scheduler as the configuration control plane, and the official Web UI as the admin console. PostgreSQL stores the BunkerWeb configuration database, and Redis supports shared runtime state.

The template also deploys a small protected `whoami` backend behind BunkerWeb so the reverse-proxy path is usable immediately. Replace that backend and the BunkerWeb service settings when you attach your real applications.

## Common Use Cases

- **Web Application Firewall**: Put security controls in front of public web apps.
- **Reverse Proxy Gateway**: Route incoming HTTP traffic to internal services.
- **Security Policy Testing**: Evaluate BunkerWeb rules and plugin behavior before protecting production services.
- **Centralized Admin UI**: Manage services, instances, plugins, jobs, and reports from the BunkerWeb Web UI.
- **Backup-Ready Configuration**: Enable Sealos Object Storage for S3-compatible BunkerWeb PRO backup settings.

## Dependencies for BunkerWeb Hosting

The Sealos template includes all required dependencies for a single-instance BunkerWeb deployment:

- BunkerWeb `1.6.11`
- BunkerWeb Scheduler `1.6.11`
- BunkerWeb Web UI `1.6.11`
- PostgreSQL `16.4.0` through KubeBlocks
- Redis `7.2.7` with Sentinel through KubeBlocks
- A protected demo backend using `traefik/whoami`
- Persistent volumes for scheduler data and Web UI state/logs
- Optional Sealos `ObjectStorageBucket` for S3-compatible backup settings
- Kubernetes Services and HTTPS Ingress routes

### Deployment Dependencies

- [BunkerWeb Website](https://www.bunkerweb.io/) - Product overview
- [BunkerWeb Documentation](https://docs.bunkerweb.io/) - Official documentation
- [BunkerWeb GitHub Repository](https://github.com/bunkerity/bunkerweb) - Source code and issue tracker
- [BunkerWeb Helm Chart](https://github.com/bunkerity/helm-charts) - Official Kubernetes chart
- [Sealos Documentation](https://sealos.io/docs) - Platform and operations guidance

## Implementation Details

### Architecture Components

This template deploys the following services:

- **BunkerWeb Gateway**: Runs `bunkerity/bunkerweb:1.6.11`, exposes HTTP traffic on port `8080`, and exposes the BunkerWeb API on port `5000` for the scheduler.
- **Scheduler**: Runs `bunkerity/bunkerweb-scheduler:1.6.11`, initializes and maintains the BunkerWeb database, saves generated config, and pushes changes to the BunkerWeb API.
- **Web UI**: Runs `bunkerity/bunkerweb-ui:1.6.11`, provides the admin console on port `7000`, and creates the initial administrator from deployment inputs.
- **PostgreSQL Cluster**: Stores BunkerWeb configuration, UI users, services, jobs, plugins, reports, and metadata.
- **Redis Cluster**: Provides shared cache/session/runtime state for BunkerWeb.
- **Protected Demo Backend**: Runs `traefik/whoami` behind BunkerWeb for immediate gateway verification.
- **Optional Object Storage**: Provisions a private Sealos bucket and injects BunkerWeb S3 backup settings when `enable_s3_backup` is selected.

### Configuration

- `admin_username` and `admin_password` create the initial BunkerWeb Web UI administrator.
- `enable_s3_backup` provisions Sealos Object Storage and injects the official BunkerWeb `backup_s3` settings. This feature belongs to BunkerWeb PRO backup functionality.
- The public application URL routes to the protected demo backend through the BunkerWeb gateway.
- The public admin URL routes directly to the Web UI. For production operations, review access controls and protect the admin URL according to your organization policy.
- The scheduler uses `BUNKERWEB_INSTANCES` with the BunkerWeb API service URL and stores service configuration in PostgreSQL.
- Startup gates wait for PostgreSQL, Redis, BunkerWeb API, and initialized database metadata so cold starts converge cleanly.

### Reverse Proxy Caveats

The default protected service is a demo endpoint. To protect a real application, update the service host and reverse-proxy settings in BunkerWeb, then verify the generated policy against your app behavior. Security rules can block unusual headers, request bodies, bots, scanners, or paths, so test login, uploads, APIs, and health checks before routing production traffic.

### License Information

BunkerWeb is licensed under the GNU Affero General Public License v3.0. This Sealos template is deployment configuration for BunkerWeb and follows the repository's template license.

## Why Deploy BunkerWeb on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment and operations. By deploying BunkerWeb on Sealos, you get:

- **One-Click Deployment**: Launch BunkerWeb, scheduler, UI, PostgreSQL, Redis, storage, and ingress in one workflow.
- **Managed Datastores**: PostgreSQL and Redis are provisioned automatically through KubeBlocks.
- **Instant HTTPS Access**: Sealos creates public HTTPS URLs for the protected gateway and admin UI.
- **Persistent Configuration**: BunkerWeb data survives pod restarts through PostgreSQL and persistent volumes.
- **Optional Object Storage**: Create an S3-compatible bucket from the deployment form for backup wiring.
- **AI-Assisted Operations**: Use Canvas and AI dialog to adjust resources, environment values, and networking.

Deploy BunkerWeb on Sealos and manage a security gateway with Kubernetes primitives handled by the platform.

## Deployment Guide

1. Open the [BunkerWeb template](https://sealos.io/products/app-store/bunkerweb) and click **Deploy Now**.
2. Configure the deployment parameters:
   - `admin_username`: BunkerWeb Web UI administrator username.
   - `admin_password`: BunkerWeb Web UI administrator password.
   - `enable_s3_backup`: Provisions Sealos Object Storage and injects S3 backup settings.
3. Wait for deployment to complete. BunkerWeb cold start includes PostgreSQL, Redis, scheduler database initialization, and Web UI startup.
4. Access the generated URLs from the Canvas:
   - **Protected Service URL**: routes through BunkerWeb to the demo backend.
   - **BunkerWeb Web UI URL**: opens the administrator console.
5. Sign in to the Web UI with the configured administrator credentials.
6. Complete any first-login TOTP or recovery-code prompts shown by BunkerWeb, then open the dashboard.
7. Replace the demo backend with your real service configuration before using BunkerWeb for production traffic.

## Configuration

After deployment, configure BunkerWeb through:

- **BunkerWeb Web UI**: Manage services, instances, plugins, jobs, reports, and account settings.
- **Sealos AI Dialog**: Describe resource, environment, storage, or networking changes.
- **Resource Cards**: Open Deployments, StatefulSets, Services, Ingresses, PostgreSQL, Redis, and Object Storage cards from Canvas.

For first production use, review admin URL exposure, BunkerWeb security rules, reverse-proxy host settings, allowed request sizes, bot protections, and backup policy.

## Scaling

This template starts with one BunkerWeb gateway, one scheduler, one Web UI, one PostgreSQL instance, and one Redis replication topology. Scale vertically first by increasing CPU and memory on the BunkerWeb gateway and scheduler cards. Multi-instance gateway scaling requires coordinated BunkerWeb instance registration and traffic testing.

## Troubleshooting

### Admin login prompts for TOTP

BunkerWeb may require first-login two-factor enrollment or recovery-code handling. Complete the prompt in the Web UI and store recovery codes securely.

### Protected service returns a security block page

Review the matched BunkerWeb rule in the Web UI reports/logs and tune the service policy for your application's request patterns.

### Web UI waits during cold start

The Web UI depends on scheduler database initialization. Wait for PostgreSQL, Redis, scheduler, and BunkerWeb pods to become ready, then refresh the Web UI URL.

### S3 backup settings are inactive

Enable `enable_s3_backup` during deployment and confirm the BunkerWeb PRO backup plugin behavior in the Web UI. The template injects Sealos Object Storage credentials for the BunkerWeb `backup_s3` settings.

### Getting Help

- [BunkerWeb Documentation](https://docs.bunkerweb.io/)
- [BunkerWeb GitHub Issues](https://github.com/bunkerity/bunkerweb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [BunkerWeb Quick Start](https://docs.bunkerweb.io/latest/quickstart-guide/)
- [BunkerWeb Integrations](https://docs.bunkerweb.io/latest/integrations/)
- [BunkerWeb Features](https://docs.bunkerweb.io/latest/features/)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository's template license. BunkerWeb itself is licensed under the GNU Affero General Public License v3.0.
