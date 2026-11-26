# Deploy and Host Logto on Sealos

[Logto](https://logto.io/) is an open-source identity platform for application authentication, user management, and authorization. This template deploys Logto 1.42.0 with a dedicated PostgreSQL database on Sealos Cloud.

![Logto Admin Console](website-screenshot.webp)

## About Hosting Logto

Logto provides sign-in and sign-up experiences, OIDC/OAuth 2.0, SAML, multi-tenancy, role-based access control, and user management from one administration console. Applications connect to the Core/Auth endpoint, while operators manage identity settings through the separate Admin Console endpoint.

The template provisions PostgreSQL 16.4, creates the `logto` database, applies the Logto schema and seed data, and exposes both endpoints through HTTPS. Sealos manages service discovery, certificates, persistent database storage, health checks, and application lifecycle operations.

## Common Use Cases

- **Customer authentication**: Add secure sign-in and registration to web, mobile, and SaaS products.
- **OIDC and OAuth provider**: Issue identities and tokens for first-party and third-party applications.
- **Enterprise identity**: Configure SAML, enterprise SSO, MFA, and organization-aware access.
- **Authorization management**: Manage API resources, roles, permissions, and organization roles.
- **Self-hosted identity control plane**: Keep identity configuration and user data in your own Sealos workspace.

## Dependencies for Logto Hosting

The template includes the Logto 1.42.0 runtime, PostgreSQL 16.4, database initialization jobs, persistent storage, Services, Ingress, and automatic TLS.

### Deployment Dependencies

- [Logto documentation](https://docs.logto.io/) - Product and integration documentation
- [Logto quick starts](https://docs.logto.io/quick-starts) - Framework integration guides
- [Logto GitHub repository](https://github.com/logto-io/logto) - Source code and issue tracker

### Implementation Details

**Architecture Components:**

- **Logto**: Runs `svhd/logto:1.42.0` and serves the Core/Auth endpoint on port 3001 and Admin Console on port 3002.
- **PostgreSQL**: A single PostgreSQL 16.4 instance stores Logto configuration, identities, applications, and audit data.
- **Database initialization**: An idempotent job creates the `logto` database. A Logto init container waits for PostgreSQL, seeds the schema, and applies pending alterations.
- **Public networking**: The Admin Console is the primary Sealos application URL. The Core/Auth endpoint remains publicly available for application integrations.

**Default Resource Limits:**

| Component | CPU | Memory | Storage |
| --- | ---: | ---: | ---: |
| Logto | 100m | 256Mi | - |
| Logto database initializer | 100m | 128Mi | - |
| PostgreSQL | 500m | 512Mi | 1Gi |

The default topology uses one Logto replica and one PostgreSQL replica. Increase resources before adding production traffic, connectors, or high-volume audit workloads.

**License Information:**

Logto is licensed under the Mozilla Public License 2.0.

## Why Deploy Logto on Sealos?

Sealos provides a Kubernetes-based application platform that manages the full deployment lifecycle. Deploying Logto on Sealos provides:

- **One-click deployment**: Provision Logto, PostgreSQL, initialization jobs, networking, and TLS from one template.
- **Integrated persistence**: Keep identity data on managed persistent storage across application restarts.
- **Instant HTTPS endpoints**: Receive separate secure URLs for the Admin Console and authentication traffic.
- **Observable resources**: Inspect workloads, logs, database status, and resource usage from the Canvas.
- **Straightforward customization**: Adjust environment variables, CPU, memory, storage, and replica settings through Sealos.

Deploy Logto on Sealos and manage the identity layer alongside the applications that use it.

## Deployment Guide

1. Open the [Logto template](https://sealos.io/products/app-store/logto) and click **Deploy Now**.
2. Review the generated application name and domains, then start the deployment.
3. Wait for deployment to complete, typically 2-3 minutes. PostgreSQL and schema initialization must finish before Logto becomes ready. After deployment, Sealos opens the Canvas for the application.
4. Open the **Admin Console** URL from the Logto application card.
5. Keep the **Core/Auth endpoint** from the networking details for OIDC/OAuth integrations.

## First Registration and Login

A fresh deployment opens the Logto welcome page:

1. Click **Create account**.
2. Enter the username for the initial administrator and continue.
3. Enter and confirm a strong password, then click **Save password**.
4. Logto opens the authenticated Admin Console. Verify access by opening **Dashboard** and **Applications**.

The first successful registration creates the initial administrator. Later visits use **Sign in** with that username and password. Store the credentials in a password manager because the template does not generate or display them.

Logto exposes two HTTPS endpoints:

- **Admin Console**: `https://<generated-host>-admin.<sealos-cloud-domain>`
- **Core/Auth endpoint**: `https://<generated-host>.<sealos-cloud-domain>`

Use the Core/Auth endpoint as the base issuer URL when configuring applications and SDKs.

## Configuration

After signing in, use the Admin Console to create applications, set redirect URIs, configure sign-in methods, add connectors, define API resources, and manage users. Sealos also provides:

- **AI Dialog**: Describe infrastructure changes and let Sealos apply them.
- **Resource Cards**: Adjust workload resources and inspect runtime settings from the Canvas.
- **Database Card**: Review PostgreSQL status, connection details, storage, and backups.

## Scaling

Start with the tested default resources for evaluation and light workloads. For production use, monitor CPU and memory in Sealos, increase the Logto and PostgreSQL limits as traffic grows, expand database storage before capacity is reached, and plan PostgreSQL availability according to your recovery objectives.

## Troubleshooting

### The Admin Console is still loading after deployment

PostgreSQL startup and Logto schema initialization complete before the readiness check passes. Wait for both the PostgreSQL cluster and Logto workload to show a running state in the Canvas, then reload the Admin Console.

### An application cannot complete OIDC/OAuth redirects

Confirm that the application uses the Core/Auth endpoint as its issuer and that every redirect URI exactly matches the value registered in **Applications**.

### Getting Help

- [Logto documentation](https://docs.logto.io/)
- [Logto GitHub issues](https://github.com/logto-io/logto/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Logto SDKs](https://docs.logto.io/quick-starts)
- [Logto concepts](https://docs.logto.io/end-user-flows)
- [Sealos documentation](https://sealos.io/docs/)

## License

This template follows the license of the Sealos templates repository. Logto is licensed under the [Mozilla Public License 2.0](https://github.com/logto-io/logto/blob/master/LICENSE).
