# Deploy and Host InsForge on Sealos

InsForge is an agent-native backend platform for building full-stack applications with database, authentication, storage, and function runtime capabilities. This template deploys InsForge as a multi-service stack with PostgreSQL, PostgREST, and Deno runtime on Sealos Cloud.

## About Hosting InsForge

InsForge on Sealos runs as a coordinated backend platform where the main InsForge service provides API, dashboard, and auth endpoints, while PostgREST exposes PostgreSQL as a REST layer and Deno runtime executes function workloads. The template also provisions PostgreSQL with required extensions and roles, so the core backend features work out of the box.

The deployment includes persistent storage for application data, logs, and runtime cache, plus automatic HTTPS ingress and domain management. Sealos manages networking, certificates, and Kubernetes resources so you can focus on application logic instead of infrastructure.

## Common Use Cases

- **Agent-Native SaaS Backends**: Build and operate backend services that AI coding agents can provision and manage.
- **Supabase-Style App Foundations**: Launch projects that need database, auth, and REST APIs with minimal setup.
- **Internal Tools and Automation**: Create internal apps with secure authentication and server-side logic.
- **Rapid MVP Development**: Prototype full-stack products quickly with a ready backend stack.
- **AI Workflow Platforms**: Combine API access and function runtime for AI-assisted product workflows.

## Dependencies for InsForge Hosting

The Sealos template includes all required dependencies: InsForge core service, PostgreSQL, PostgREST, Deno runtime, ingress, and persistent volumes.

### Deployment Dependencies

- [InsForge Official Website](https://insforge.dev) - Product overview and updates
- [InsForge GitHub Repository](https://github.com/insforge/insforge) - Source code and release details
- [InsForge GitHub Issues](https://github.com/insforge/insforge/issues) - Issue tracking and community support
- [Sealos Cloud](https://sealos.io) - Deployment platform

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **InsForge Core (StatefulSet)**: Main service on ports `7130` (API), `7131` (dashboard), and `7132` (auth).
- **PostgreSQL Cluster (KubeBlocks)**: PostgreSQL `16.4.0` with persistent data storage.
- **PostgreSQL Extension Init Job**: Installs and enables `pg_cron`, `http`, and `pgcrypto`, and ensures required roles exist.
- **PostgreSQL Extension Ensure CronJob**: Re-checks extension availability every 5 minutes for operational resilience.
- **PostgREST (Deployment)**: REST gateway on port `3000` with JWT integration.
- **Deno Runtime (StatefulSet)**: Function runtime on port `7133` for backend execution tasks.
- **Ingress + Service Resources**: Public HTTPS endpoint with automatic TLS and internal service discovery.

**Configuration:**

- **Required input**: `admin_password`
- **Optional inputs**: `admin_email`, `openrouter_api_key`, and OAuth credentials for Google, GitHub, Discord, Microsoft, LinkedIn, X, and Apple
- **Security defaults**: Randomized `JWT_SECRET` and `ENCRYPTION_KEY` are generated automatically
- **Storage defaults**:
  - InsForge storage: `/insforge-storage` (103Mi)
  - InsForge logs: `/insforge-logs` (103Mi)
  - Deno runtime cache: `/deno-dir` (103Mi)
  - PostgreSQL data volume: `1Gi`

**License Information:**

InsForge is open-source software. Refer to the upstream repository for the latest license terms and notices.

## Why Deploy InsForge on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies development, deployment, and operations. By deploying InsForge on Sealos, you get:

- **One-Click Deployment**: Launch a multi-service backend stack without manual YAML orchestration.
- **Built-In Kubernetes Reliability**: Use Kubernetes scheduling, service discovery, and restart behavior by default.
- **Easy Configuration**: Manage environment variables and resource settings through Sealos forms and dialogs.
- **Persistent Storage Included**: Keep database and service data durable across restarts.
- **Automatic HTTPS Access**: Receive a public URL with SSL certificate provisioning.
- **Pay-as-You-Go Efficiency**: Allocate only the resources you need and scale when demand grows.
- **AI-Assisted Operations**: Use Canvas and AI dialog workflows for post-deployment changes.

Deploy InsForge on Sealos and focus on shipping product features instead of managing infrastructure.

## Deployment Guide

1. Open the [InsForge template](https://sealos.io/products/app-store/insforge) and click **Deploy Now**.
2. Configure parameters in the popup dialog:
   - **admin_password** (required): Administrator password
   - **admin_email** (optional): Administrator email
   - **openrouter_api_key** (optional): OpenRouter integration key
   - **OAuth client settings** (optional): Google, GitHub, Discord, Microsoft, LinkedIn, X, Apple
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe requirements in the dialog for AI-assisted updates, or click resource cards to adjust settings.
4. Access your application using the generated public URL:
   - **InsForge Web/API Endpoint**: Main entrypoint served through HTTPS ingress

## Configuration

After deployment, you can configure InsForge through:

- **AI Dialog**: Describe desired changes and let AI apply updates
- **Resource Cards**: Edit StatefulSet/Deployment resources and environment variables
- **Admin Credentials**: Update admin email/password and OAuth settings through deployment config
- **Service Connectivity**: Keep internal service endpoints (`postgrest`, `deno`, `postgres`) managed by cluster DNS

## Scaling

To scale your InsForge deployment:

1. Open the Canvas for your InsForge deployment.
2. Select the relevant resource card (`insforge`, `insforge-postgrest`, or `insforge-deno`).
3. Adjust CPU/Memory resources as needed.
4. Apply changes in the dialog.

For higher throughput scenarios, prioritize vertical scaling of PostgreSQL and InsForge core resources before introducing topology changes.

## Troubleshooting

### Common Issues

**Issue: Initial startup takes longer than expected**
- Cause: PostgreSQL extensions and role initialization jobs are still running.
- Solution: Wait for init jobs to complete, then recheck pod readiness.

**Issue: Authentication or JWT-related API errors**
- Cause: Misconfigured `JWT_SECRET` or mismatched auth settings.
- Solution: Verify deployment environment variables and reapply correct values.

**Issue: OAuth login not working**
- Cause: Missing or invalid OAuth client ID/secret configuration.
- Solution: Reconfigure provider credentials in deployment settings and restart affected pods.

**Issue: Runtime function failures**
- Cause: Deno runtime service not ready or internal connectivity issue.
- Solution: Check `insforge-deno` pod status and verify internal service DNS resolution.

### Getting Help

- [InsForge Website](https://insforge.dev)
- [InsForge GitHub Repository](https://github.com/insforge/insforge)
- [InsForge GitHub Issues](https://github.com/insforge/insforge/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [InsForge Source Code](https://github.com/insforge/insforge)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template follows the licensing terms of this templates repository. InsForge itself is licensed under its upstream project license; see the InsForge repository for details.
