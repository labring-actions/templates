# Deploy and Host OpenList on Sealos

OpenList is a community-driven file list and storage aggregation platform with WebDAV, offline downloads, and a browser-based administration interface. This template deploys OpenList `v4.2.2-aria2` with a ready-to-use local storage mount, optional managed PostgreSQL, and optional private Sealos S3 storage.

![OpenList with Sealos S3 storage](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openlist/website-screenshot.webp)

## About Hosting OpenList

OpenList presents multiple storage providers through one web interface and WebDAV endpoint. Administrators can add storage drivers, manage users and permissions, create shares, configure metadata, and run offline download tasks.

The Sealos template runs one OpenList StatefulSet with a `1Gi` persistent volume. A storage initialization Job automatically mounts the persistent volume at `/local` or creates `/sealos-s3` from a private Sealos Object Storage bucket. Startup, readiness, and liveness probes use OpenList's public `/ping` endpoint.

Database and file storage choices are independent:

| Database | File storage | Recommended use |
| --- | --- | --- |
| SQLite | Local persistent volume | Evaluation, personal use, and compact deployments |
| SQLite | Sealos S3 | Compact metadata storage with object-backed files |
| PostgreSQL | Local persistent volume | Larger metadata sets with local files |
| PostgreSQL | Sealos S3 | Production-oriented metadata and object storage |

## Common Use Cases

- **Unified storage portal**: Present cloud drives and S3-compatible providers through one file browser.
- **Private file service**: Upload, organize, preview, and share files from a self-hosted interface.
- **WebDAV gateway**: Connect desktop, mobile, backup, and media applications through WebDAV.
- **S3-backed file access**: Store files in a private Sealos bucket and serve them through OpenList authorization.
- **Offline downloads**: Use the included Aria2 integration for supported transfer workflows.

## Dependencies for OpenList Hosting

The template includes the OpenList container, persistent storage, a Kubernetes Service, an HTTPS Ingress, a Sealos App entry, and an idempotent storage initialization Job. Optional branches add a KubeBlocks PostgreSQL cluster or a private Sealos `ObjectStorageBucket`.

### Deployment Dependencies

- [OpenList Website](https://oplist.org/) - Product website
- [OpenList Documentation](https://doc.oplist.org/) - Installation and administration guides
- [Docker Installation Guide](https://doc.oplist.org/guide/installation/docker) - Official container deployment guidance
- [S3 Driver Guide](https://doc.oplist.org/guide/drivers/s3) - S3-compatible storage configuration
- [OpenList GitHub Repository](https://github.com/OpenListTeam/OpenList) - Source code and issue tracker

### Implementation Details

**Architecture Components:**

- **OpenList Web Service**: Runs `openlistteam/openlist:v4.2.2-aria2` on port `5244`.
- **Persistent Volume**: Stores OpenList configuration, SQLite data, and local files under `/opt/openlist/data`.
- **Storage Initialization Job**: Authenticates with the initial admin account and creates the selected `/local` or `/sealos-s3` mount.
- **Optional PostgreSQL**: A KubeBlocks PostgreSQL `16.4.0` cluster stores OpenList metadata.
- **Optional Object Storage**: A private Sealos S3-compatible bucket stores files mounted at `/sealos-s3`.
- **Public Entry**: A Service, Ingress, and Sealos App expose the web interface through HTTPS.

**License Information:**

OpenList is licensed under the GNU Affero General Public License v3.0. This repository provides deployment configuration and preserves the upstream license.

## Why Deploy OpenList on Sealos?

Sealos is a Cloud Operating System built on Kubernetes that combines application deployment and resource operations in one workspace. OpenList deployments gain:

- **One-Click Deployment**: Create the application, networking, persistent storage, and selected managed services from one form.
- **Ready-to-Use Storage**: OpenList starts with a functional local or Sealos S3 mount.
- **Managed Database Option**: Provision PostgreSQL with generated connection credentials.
- **Instant HTTPS Access**: Receive a public URL and managed TLS configuration.
- **Persistent Data**: Keep configuration, database data, and local files across Pod restarts.
- **Pay-As-You-Go Resources**: Start with the smallest validated OpenList resource tier.
- **Canvas and AI Operations**: Inspect resources and describe later changes from the Sealos Canvas.

## Deployment Guide

1. Open the [OpenList template](https://sealos.io/products/app-store/openlist) and click **Deploy Now**.
2. Enter a strong `admin_password` and record it in a password manager.
3. Choose the database:
   - Keep `enable_postgresql` disabled for SQLite on the persistent volume.
   - Enable `enable_postgresql` for a dedicated PostgreSQL cluster.
4. Choose the file storage:
   - Keep `enable_s3_storage` disabled for the `/local` persistent-volume mount.
   - Enable `enable_s3_storage` for a private Sealos bucket mounted at `/sealos-s3`.
5. Wait for deployment to complete, typically 2-3 minutes for SQLite and several minutes for PostgreSQL provisioning.
6. Open the generated OpenList URL from the Sealos App entry.

### Deployment Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `admin_password` | Required | Initial password for the built-in `admin` account |
| `enable_postgresql` | `false` | Creates managed PostgreSQL; `false` uses SQLite at `/opt/openlist/data/data.db` |
| `enable_s3_storage` | `false` | Creates a private Sealos bucket at `/sealos-s3`; `false` creates `/local` on the persistent volume |

## First Login and User Setup

1. Open the generated application URL. OpenList redirects to its login page.
2. Enter `admin` as the username.
3. Enter the `admin_password` configured during deployment.
4. Open **Manage** to configure storage, settings, shares, and indexing.
5. Open **Manage > Users** and click **Add** to create accounts for other users.
6. Assign each user a base path and the minimum permissions required for their workflow.

The configured password initializes the `admin` account when OpenList creates a new database. Existing SQLite or PostgreSQL data keeps the stored administrator password across application updates.

## Storage Options

### Local Persistent Storage

With `enable_s3_storage=false`, the initialization Job creates a Local driver mounted at `/local`. Files live under `/opt/openlist/data/storage` on the StatefulSet's `1Gi` persistent volume and survive Pod replacement.

### Sealos S3 Object Storage

With `enable_s3_storage=true`, Sealos creates a private `ObjectStorageBucket`. The initialization Job registers OpenList's official S3 driver at `/sealos-s3` with path-style addressing and credentials from Sealos-managed Secrets.

Private bucket objects return `403` to anonymous raw requests. Authenticated users upload and download through OpenList or WebDAV, where OpenList permissions remain in effect.

## Database Options

### Embedded SQLite

SQLite is the default and stores metadata at `/opt/openlist/data/data.db`. It provides the smallest deployment footprint and fits personal or compact single-replica installations.

### Managed PostgreSQL

Enabling `enable_postgresql` creates a PostgreSQL cluster and an idempotent database initialization Job. OpenList reads the generated host, port, username, and password from Kubernetes Secrets.

## Persistence

| Path or service | Purpose | Provisioned when |
| --- | --- | --- |
| `/opt/openlist/data/config.json` | OpenList runtime configuration | Always |
| `/opt/openlist/data/data.db` | SQLite metadata | `enable_postgresql=false` |
| `/opt/openlist/data/storage` | Files mounted at `/local` | `enable_s3_storage=false` |
| PostgreSQL volume | Users, settings, storage definitions, shares, and metadata | `enable_postgresql=true` |
| Sealos S3 bucket | Files mounted at `/sealos-s3` | `enable_s3_storage=true` |

## Resource Defaults

Live deployment tests covered admin login, management navigation, file upload and download, storage persistence after Pod replacement, PostgreSQL persistence, and private S3 access controls.

| Component | CPU limit | Memory limit | CPU request | Memory request |
| --- | ---: | ---: | ---: | ---: |
| OpenList | `100m` | `128Mi` | `10m` | `12Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| Initialization containers and Jobs | `100m` | `128Mi` | `10m` | `12Mi` |

Increase OpenList resources for concurrent transfers, media previews, indexing, or sustained API traffic.

## Scaling

The template preserves OpenList's single-instance StatefulSet topology. SQLite and the local file mount use a ReadWriteOnce volume, so this mode remains at one replica.

For larger workloads, select PostgreSQL and Sealos S3, increase CPU and memory through the StatefulSet resource card, and review OpenList's multi-instance requirements before changing replica count.

## Troubleshooting

### The application is still starting

Open the OpenList resource card in Sealos Canvas and inspect Pod readiness. PostgreSQL deployments wait for the database and storage initialization Jobs before the full workflow becomes available.

### Administrator login fails

Use the username `admin` and the password entered during the first deployment of the current database. An existing database preserves its stored password.

### The storage mount is missing

Inspect the `<generated-app-name>-storage-init` Job in Canvas. A successful Job reports `Local storage mounted at /local` or `S3 storage mounted at /sealos-s3`.

### S3 files return `403`

The Sealos bucket uses a private policy. Access files through OpenList or WebDAV with an authorized account.

### Getting Help

- [OpenList Documentation](https://doc.oplist.org/)
- [OpenList GitHub Issues](https://github.com/OpenListTeam/OpenList/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the repository license. OpenList is licensed under the [GNU Affero General Public License v3.0](https://github.com/OpenListTeam/OpenList/blob/v4.2.2/LICENSE).
