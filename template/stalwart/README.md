# Deploy and Host Stalwart on Sealos

Stalwart is an open-source mail and collaboration server with SMTP, IMAP, JMAP, CalDAV, CardDAV, WebDAV, spam filtering, and a web administration console. This template deploys Stalwart 0.16.16 as a single persistent server on Sealos Cloud.

![Stalwart Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/stalwart/website-screenshot.webp)

## About Hosting Stalwart

Stalwart combines mail transfer, mailbox access, calendars, contacts, shared files, and security controls in one server. The template automates Stalwart's official bootstrap flow, creates the primary domain and permanent administrator, applies the password supplied in the deployment form, and starts the normal server configuration.

The database and blob store are independent choices. PostgreSQL 16 is the default managed DataStore, while SQLite provides a compact persistent single-node option. Message bodies and other blobs can use the selected DataStore or a private Sealos Object Storage bucket.

## Common Use Cases

- **Business Mail Hosting**: Serve mailboxes and message delivery for an organization domain
- **Collaboration Server**: Provide calendars, contacts, shared files, and standards-based synchronization
- **Mail Transfer Agent**: Process inbound and outbound SMTP with built-in spam and phishing controls
- **JMAP Backend**: Support modern mail and collaboration clients through a unified API
- **Self-Hosted Mail Lab**: Evaluate mail clients, DNS records, policies, and delivery workflows

## Dependencies for Stalwart Hosting

The template includes a digest-pinned Stalwart 0.16.16 image, a 1Gi persistent application volume, an HTTPS Ingress, and optional managed PostgreSQL and Object Storage resources.

### Deployment Dependencies

- [Stalwart Documentation](https://stalw.art/docs/) - Installation, management, and protocol documentation
- [Bootstrap Mode](https://stalw.art/docs/configuration/bootstrap-mode/) - Official initial configuration workflow
- [Kubernetes Deployment Guide](https://stalw.art/docs/cluster/orchestration/kubernetes/) - Official Kubernetes runtime guidance
- [PostgreSQL Backend](https://stalw.art/docs/storage/backends/postgresql/) - PostgreSQL DataStore configuration
- [SQLite Backend](https://stalw.art/docs/storage/backends/sqlite/) - SQLite DataStore configuration
- [S3-Compatible Backend](https://stalw.art/docs/storage/backends/s3/) - S3 BlobStore configuration
- [Stalwart Releases](https://github.com/stalwartlabs/stalwart/releases) - Source and release history

## Implementation Details

### Architecture Components

- **Stalwart StatefulSet**: Runs one replica of `stalwartlabs/stalwart:v0.16.16` from an immutable image digest
- **Bootstrap Init Container**: Uses Stalwart's management API to configure the domain, stores, permanent administrator, password, and safe listener defaults
- **Application Storage**: Mounts a 1Gi persistent volume at `/var/lib/stalwart` for `config.json`, SQLite data, logs, and bootstrap state
- **PostgreSQL 16**: Provisions an independent KubeBlocks cluster and database initialization Job when enabled
- **Sealos Object Storage**: Provisions a private bucket and connects it as Stalwart's S3 BlobStore when enabled
- **Ingress and Service**: Publishes the web interface over HTTPS and defines internal SMTP, submission, IMAP, POP3, ManageSieve, HTTP, and HTTPS ports

### Configuration Choices

| Input | Default | Result |
| --- | --- | --- |
| `default_domain` | User supplied | Creates the primary mail domain and administrator identity |
| `admin_password` | User supplied | Sets the permanent administrator password |
| `use_postgresql` | `true` | Uses an independent managed PostgreSQL 16 DataStore |
| `use_postgresql` | `false` | Uses SQLite at `/var/lib/stalwart/stalwart.db` |
| `enable_s3_storage` | `false` | Stores blobs in the selected DataStore |
| `enable_s3_storage` | `true` | Stores blobs in a private Sealos Object Storage bucket |

The bootstrap process writes `/var/lib/stalwart/config.json` using Stalwart's current object-based configuration model. PostgreSQL credentials and S3 credentials are read from Sealos-managed Kubernetes Secrets. S3 writes use `verifyAfterWrite` so Stalwart confirms that each uploaded object is readable.

### Network Ports

| Port | Protocol | Purpose |
| --- | --- | --- |
| `25` | SMTP | Server-to-server mail delivery |
| `465` | Submissions over TLS | Authenticated mail submission |
| `993` | IMAPS | Mailbox access over TLS |
| `995` | POP3S | POP3 mailbox access over TLS |
| `4190` | ManageSieve | Sieve script management |
| `8080` | HTTP | Health checks and the Ingress backend |
| `443` | HTTPS | Stalwart's native HTTPS listener |

Sealos Ingress publishes the HTTP listener through the generated HTTPS application URL. Production mail traffic requires public L4 mappings for the selected mail protocol ports, along with suitable provider policies and reverse DNS.

## Why Deploy Stalwart on Sealos?

Sealos is a Kubernetes-based cloud operating system that manages application resources through a visual Canvas and AI-assisted operations. This Stalwart deployment provides:

- **One-Click Bootstrap**: Create the domain, administrator, database, and selected blob storage from one form
- **Persistent State**: Keep configuration and local data across pod restarts
- **Managed Storage Choices**: Select PostgreSQL or SQLite independently from local or S3 blob storage
- **Secure Web Access**: Receive an HTTPS administration endpoint and managed certificate
- **Resource Control**: Adjust CPU, memory, and storage through the Canvas
- **Pay-as-You-Go Resources**: Provision only the database and object storage selected for the workload

## Deployment Guide

1. Open the [Stalwart template](https://sealos.io/products/app-store/stalwart) and click **Deploy Now**.
2. Enter the primary mail domain, such as `example.com`.
3. Enter a strong administrator password with at least eight characters.
4. Keep PostgreSQL enabled for a managed database, or clear it for persistent SQLite.
5. Enable S3 storage for a private blob bucket, or keep blobs in the selected DataStore.
6. Submit the form and wait for the Stalwart StatefulSet to become Ready. PostgreSQL deployments can take several minutes while the database cluster starts.
7. Open the application URL at `/admin` and sign in with `admin@<default_domain>` and the password from the deployment form.

## Login and First Setup

The template creates the permanent administrator during bootstrap. For a domain input of `example.com`, use `admin@example.com` as the username. New mail users are created after sign-in under **Directory > Accounts**.

After the first login:

1. Open **Management > Directory > Domains** and select the primary domain.
2. Review the generated DNS records and DKIM public key.
3. Create mail accounts under **Directory > Accounts**.
4. Configure public L4 access for the mail protocol ports required by your clients.
5. Publish MX, SPF, DKIM, DMARC, MTA-STS, and reverse DNS records before production delivery.

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| `/admin` | Open the web administration console |
| `/jmap/session` | Discover the authenticated JMAP session |
| `/jmap` | Send JMAP and Stalwart management requests |
| `/healthz/live` | Check process liveness |
| `/healthz/ready` | Check service readiness |

Use the Sealos Canvas AI dialog or resource cards for later resource changes. Keep one Stalwart replica for this template because its persistent application volume and bootstrap state are designed for a single server.

## Troubleshooting

### Administrator Login Fails

Use the full administrator address `admin@<default_domain>` and the exact password entered in the deployment form. Confirm that the StatefulSet is Ready before signing in.

### PostgreSQL Startup Takes Several Minutes

Wait for the KubeBlocks PostgreSQL cluster and the `pg-init` Job to complete. The Stalwart init containers gate bootstrap until the `stalwart` database accepts queries.

### S3 Blob Uploads Fail

Confirm that the ObjectStorageBucket and its generated bucket Secret are ready. Stalwart validates the S3 endpoint during bootstrap and verifies every successful object write.

### Mail Clients Cannot Connect

Create public L4 mappings for the required mail protocol ports and configure matching DNS records. The generated application URL covers the web administration endpoint.

### Getting Help

- [Stalwart Documentation](https://stalw.art/docs/)
- [Stalwart GitHub Issues](https://github.com/stalwartlabs/stalwart/issues)
- [Stalwart Support](https://stalw.art/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the repository license. Stalwart Community Edition is available under the AGPL-3.0 license; see the [Stalwart license](https://github.com/stalwartlabs/stalwart/blob/main/LICENSES/AGPL-3.0-only.txt) for details.
