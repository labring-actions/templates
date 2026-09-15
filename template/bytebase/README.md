# Deploy and Host Bytebase on Sealos

[Bytebase](https://www.bytebase.com/) is a database DevOps and GitOps platform for developers, DBAs, and platform teams. This template deploys Bytebase 3.21.0 with persistent metadata storage and an optional dedicated Sealos-managed PostgreSQL cluster.

![Bytebase Workspace](website-screenshot.webp)

## About Hosting Bytebase

Bytebase centralizes database inventory, schema changes, SQL review, access control, audit logs, and CI/CD workflows in one web console. Teams connect existing database instances, organize them into projects and environments, and route changes through reviewable issues and rollout plans.

Bytebase 3.21.0 includes an embedded PostgreSQL datastore for its own metadata. The default template keeps that datastore on a persistent volume. A deployment option provisions a separate PostgreSQL 16.4 cluster and configures Bytebase to use it, which gives the metadata database an independent lifecycle and database resource card in Sealos.

## Common Use Cases

- **Database change management**: Review, approve, and roll out schema or data changes through tracked issues.
- **Database inventory**: Register database instances and organize databases by project and environment.
- **SQL governance**: Apply SQL review rules and keep an auditable record of changes.
- **Data access workflows**: Manage access requests, grants, and masking exemptions.
- **GitOps delivery**: Connect repositories and CI/CD processes to database releases.

## Dependencies for Bytebase Hosting

The template includes Bytebase 3.21.0, a persistent 1Gi application volume, HTTPS networking, and health checks. The optional managed-storage mode also includes PostgreSQL 16.4, a 1Gi database volume, and a startup gate that waits for the database before Bytebase starts.

### Deployment Dependencies

- [Bytebase documentation](https://docs.bytebase.com/) - Product and administration documentation
- [Bytebase getting started guide](https://docs.bytebase.com/get-started/self-host/) - Self-hosted setup concepts
- [Bytebase GitHub repository](https://github.com/bytebase/bytebase) - Source code and issue tracker

### Implementation Details

**Architecture Components:**

- **Bytebase**: A single StatefulSet running `bytebase/bytebase:3.21.0` on port 8080.
- **Persistent application volume**: Stores Bytebase runtime data under `/var/opt/bytebase`.
- **Embedded PostgreSQL**: The default metadata datastore, persisted on the application volume.
- **Managed PostgreSQL**: An optional PostgreSQL 16.4 cluster selected with `enable_managed_postgres`.
- **Public networking**: A Sealos-managed HTTPS endpoint opens the Bytebase web console.

**Storage Selection:**

| `enable_managed_postgres` | Metadata storage | Recommended use |
| --- | --- | --- |
| `false` | Embedded PostgreSQL on the Bytebase volume | Evaluation and compact deployments |
| `true` | Dedicated Sealos-managed PostgreSQL cluster | Independent database operations and backups |

**Default Resource Limits:**

| Component | CPU | Memory | Storage |
| --- | ---: | ---: | ---: |
| Bytebase | 100m | 512Mi | 1Gi |
| PostgreSQL readiness initializer | 100m | 128Mi | - |
| Optional managed PostgreSQL | 500m | 512Mi | 1Gi |

The template preserves the single-replica Bytebase topology and uses a StatefulSet for stable storage identity.

**License Information:**

Bytebase community source is available under the MIT license, while enterprise-specific code and feature controls use the Bytebase enterprise license.

## Why Deploy Bytebase on Sealos?

Sealos provides a Kubernetes-based application platform that manages the deployment lifecycle. Deploying Bytebase on Sealos provides:

- **One-click deployment**: Create Bytebase, storage, networking, and the selected metadata database architecture from one form.
- **Persistent metadata**: Keep workspace configuration, users, projects, and audit data across restarts.
- **Optional managed database**: Add a dedicated PostgreSQL cluster through one deployment switch.
- **Instant HTTPS access**: Receive a secure public URL for the Bytebase console.
- **Integrated operations**: Inspect workloads, logs, storage, networking, and PostgreSQL from the Canvas.

Deploy Bytebase on Sealos and place database delivery workflows beside the infrastructure they govern.

## Deployment Guide

1. Open the [Bytebase template](https://sealos.io/products/app-store/bytebase) and click **Deploy Now**.
2. Choose the metadata storage mode:
   - Keep **Managed PostgreSQL** disabled to use Bytebase's embedded PostgreSQL datastore.
   - Enable **Managed PostgreSQL** to provision a dedicated Sealos PostgreSQL cluster.
3. Start the deployment and wait for completion, typically 2-3 minutes. The managed PostgreSQL option can add a short database startup wait. Sealos opens the Canvas when the resources are created.
4. Open the Bytebase application URL from the application card.

## First Registration and Login

A fresh deployment opens the administrator registration page:

1. Enter the administrator email address.
2. Enter and confirm a password that satisfies the policy shown on the page.
3. Enter the administrator display name.
4. Accept the Bytebase Terms of Service and Privacy Policy, then click **Sign up as admin**.
5. Complete or skip the onboarding questionnaire. Open **Projects** and **Instances** to confirm authenticated access.

The first successful registration creates the workspace administrator. Later visits use that email address and password on the sign-in page. Keep the credentials in a password manager.

## Configuration

After signing in, use Bytebase to connect database instances, create projects, define environments, configure SQL review policies, invite members, and set up GitOps integrations. Sealos also provides:

- **AI Dialog**: Describe infrastructure changes and let Sealos apply them.
- **Resource Cards**: Adjust CPU, memory, and storage from the Canvas.
- **Database Card**: Manage the optional PostgreSQL cluster, connection information, and backups.

## Scaling

The tested topology uses one Bytebase replica. Scale CPU, memory, and storage according to connected database count, concurrent users, and audit volume. The managed PostgreSQL option is the clearer operational boundary for production metadata backups and database lifecycle management.

## Troubleshooting

### Bytebase remains on the startup screen

Open the Canvas and confirm the Bytebase StatefulSet is ready. With managed PostgreSQL enabled, confirm that the PostgreSQL cluster is running and that the `wait-for-postgres` initializer has completed.

### The administrator registration page no longer appears

The first registration creates the workspace administrator. Open the sign-in page and use the administrator email and password created during initial setup.

### Getting Help

- [Bytebase documentation](https://docs.bytebase.com/)
- [Bytebase GitHub issues](https://github.com/bytebase/bytebase/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Bytebase concepts](https://docs.bytebase.com/get-started/concepts/)
- [Database change workflow](https://docs.bytebase.com/change-database/overview/)
- [Sealos documentation](https://sealos.io/docs/)

## License

This template follows the license of the Sealos templates repository. See the [Bytebase license](https://github.com/bytebase/bytebase/blob/main/LICENSE) and [enterprise license](https://github.com/bytebase/bytebase/blob/main/LICENSE.enterprise) for the upstream licensing terms.
