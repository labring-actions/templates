# Deploy and Host Casdoor on Sealos

[Casdoor](https://casdoor.org/) is an open-source identity and access management platform with OAuth 2.0, OpenID Connect, SAML, CAS, LDAP, MFA, and user-management capabilities. This template deploys Casdoor 3.141.0 with a selectable SQLite, MySQL, or PostgreSQL datastore on Sealos Cloud.

![Casdoor Dashboard](website-screenshot.webp)

## About Hosting Casdoor

Casdoor provides a web administration console and standards-based identity endpoints for applications. Teams can manage users, organizations, applications, providers, roles, permissions, sessions, and audit data from one service.

The default deployment stores Casdoor data in SQLite on a persistent volume. The MySQL and PostgreSQL options provision a dedicated Sealos-managed database, create the `casdoor` database, and hold the Casdoor workload behind a readiness initializer until the database is usable.

## Common Use Cases

- **Single sign-on**: Add OIDC, OAuth 2.0, SAML, or CAS authentication to internal and customer-facing applications.
- **Central user management**: Manage users, organizations, invitations, verification, and profile attributes.
- **External identity providers**: Connect social, enterprise, email, SMS, and custom authentication providers.
- **Authorization**: Define roles and permissions for applications and APIs.
- **Self-hosted identity control plane**: Operate authentication data and configuration in your Sealos workspace.

## Dependencies for Casdoor Hosting

The template includes Casdoor 3.141.0, HTTPS networking, a persistent volume for SQLite deployments, and optional MySQL 8.0.30 or PostgreSQL 16.4 database resources.

### Deployment Dependencies

- [Casdoor documentation](https://casdoor.org/docs/overview) - Product and integration documentation
- [Casdoor server installation guide](https://casdoor.org/docs/basic/server-installation) - Self-hosted setup guidance
- [Casdoor GitHub repository](https://github.com/casdoor/casdoor) - Source code and issue tracker

### Implementation Details

**Architecture Components:**

- **Casdoor**: Runs `casbin/casdoor:3.141.0` on port 8000.
- **SQLite mode**: Uses a StatefulSet and a 1Gi persistent volume mounted at `/home`.
- **MySQL mode**: Provisions MySQL 8.0.30, creates the `casdoor` database, and deploys a stateless Casdoor workload.
- **PostgreSQL mode**: Provisions PostgreSQL 16.4, creates the `casdoor` database, and deploys a stateless Casdoor workload.
- **Startup gates**: Database jobs and workload initializers guarantee that the selected managed database is ready before Casdoor starts.
- **Administrator bootstrap**: A one-time Job reads the required password from a Kubernetes Secret and replaces the upstream bootstrap password before the public Service selects the Casdoor Pod.
- **Public networking**: A Sealos-managed HTTPS endpoint opens the Casdoor console and identity APIs.

**Database Selection:**

| `driver_name` | Data storage | Recommended use |
| --- | --- | --- |
| `sqlite` | SQLite on the Casdoor persistent volume | Evaluation and compact deployments |
| `mysql` | Dedicated Sealos-managed MySQL cluster | Independent database operations and backups |
| `postgres` | Dedicated Sealos-managed PostgreSQL cluster | Independent database operations and backups |

**Default Resource Limits:**

| Component | CPU | Memory | Storage |
| --- | ---: | ---: | ---: |
| Casdoor | 100m | 128Mi | 1Gi in SQLite mode |
| Database initializer | 100m | 128Mi | - |
| MySQL or PostgreSQL readiness initializer | 100m | 128Mi | - |
| Administrator bootstrap Job | 100m | 128Mi | - |
| Optional MySQL or PostgreSQL | 500m | 512Mi | 1Gi |

The tested topology uses one Casdoor replica. SQLite mode preserves a stable workload identity and local persistent storage. Managed-database modes keep application compute and database persistence as separate resources.

**License Information:**

Casdoor is licensed under the Apache License 2.0.

## Why Deploy Casdoor on Sealos?

Sealos manages the Kubernetes resources, database lifecycle, networking, and TLS required by Casdoor:

- **One-click deployment**: Create Casdoor and the selected storage architecture from one form.
- **Database choice**: Start with persistent SQLite or provision a managed MySQL or PostgreSQL cluster.
- **Instant HTTPS access**: Receive a secure public URL for the console and identity endpoints.
- **Integrated operations**: Inspect workloads, logs, storage, networking, and database status from the Canvas.
- **Persistent identity data**: Keep users, organizations, applications, and provider settings across restarts.

Deploy Casdoor on Sealos and place identity management beside the applications that consume it.

## Deployment Guide

1. Open the [Casdoor template](https://sealos.io/products/app-store/casdoor) and click **Deploy Now**.
2. Enter a unique administrator password with at least 8 characters and no spaces. Store it in a password manager.
3. Select a database driver:
   - Choose **sqlite** for a compact deployment with a persistent application volume.
   - Choose **mysql** for a dedicated Sealos-managed MySQL cluster.
   - Choose **postgres** for a dedicated Sealos-managed PostgreSQL cluster.
4. Start the deployment. SQLite usually becomes ready within one minute. Managed databases usually take 2-3 minutes during their first initialization.
5. Open the Casdoor application URL from the application card.

## First Login

A fresh Casdoor deployment creates the built-in administrator with the password entered in the deployment form:

- **Account**: `built-in/admin`
- **Password**: the required `admin_password` value

Enter `admin` in the username field when the login page already shows the **Built-in Organization**. The bootstrap Job verifies the configured credential and marks the workload ready before the public endpoint receives traffic.

Confirm authenticated access by opening **Dashboard** and **Apps**. Then configure the applications, redirect URLs, providers, organizations, roles, and permissions required by your identity flow.

## Configuration

Use the Casdoor console to create applications, copy OAuth/OIDC client credentials, register redirect URLs, configure identity providers, invite users, and define authorization rules. Sealos also provides:

- **AI Dialog**: Describe infrastructure changes and let Sealos apply them.
- **Resource Cards**: Adjust Casdoor CPU and memory from the Canvas.
- **Database Card**: Manage connection information, storage, and backups for MySQL or PostgreSQL deployments.

## Scaling

The tested defaults support evaluation and light workloads. Monitor CPU, memory, request latency, and database usage in Sealos as traffic grows. Increase Casdoor resources before sustained login traffic, expand database storage before capacity is reached, and plan database availability according to your recovery objectives.

SQLite mode uses one Casdoor replica because the database file resides on its attached volume. MySQL and PostgreSQL modes separate database persistence from the Casdoor workload and provide the clearer base for production operations.

## Troubleshooting

### Casdoor is still starting

Open the Canvas and check the Casdoor workload and the `admin-bootstrap` Job. With MySQL or PostgreSQL selected, confirm that the database cluster and initialization job are ready. The public Service receives an endpoint after the administrator password is configured and verified.

### The bootstrap administrator cannot sign in

Confirm that the organization is **built-in**, the username is `admin`, and the password matches the `admin_password` deployment input. Use the full account form `built-in/admin` when an integration asks for an organization-qualified identity. Inspect the bootstrap Job logs when the workload remains pending; short passwords, spaces, and the upstream default value are rejected.

### An OAuth or OIDC redirect fails

Open **Apps**, select the application, and confirm that every redirect URI exactly matches the calling application's scheme, host, port, and path.

### Getting Help

- [Casdoor documentation](https://casdoor.org/docs/overview)
- [Casdoor GitHub issues](https://github.com/casdoor/casdoor/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Casdoor application configuration](https://casdoor.org/docs/application/config)
- [Casdoor OIDC integration](https://casdoor.org/docs/how-to-connect/oidc-client)
- [Sealos documentation](https://sealos.io/docs/)

## License

This template follows the license of the Sealos templates repository. Casdoor is licensed under the [Apache License 2.0](https://github.com/casdoor/casdoor/blob/master/LICENSE).
