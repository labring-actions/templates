# Deploy and Host Directus on Sealos

Directus is a composable data platform and headless CMS that adds an admin application, REST and GraphQL APIs, authentication, permissions, files, and automation to a SQL database. This template deploys Directus 12 with Redis and lets you choose the database and file-storage topology at deployment time.

![Directus collection backed by PostgreSQL and Sealos S3](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/directus/website-screenshot.webp)

## What This Template Deploys

- **Directus `12.1.1`** as a single-replica StatefulSet on port `8055`
- **Redis `7.2.7`** through KubeBlocks for cache and rate limiting
- **Managed PostgreSQL `16.4.0`** by default, with embedded SQLite as a lightweight option
- **Persistent local uploads** by default, with private Sealos S3-compatible object storage as an option
- **Persistent extensions storage** at `/directus/extensions`
- **Public HTTPS** through a Sealos-managed Service and Ingress
- **Startup, readiness, and liveness probes** on `/server/ping`

The template keeps PostgreSQL and object storage independent. You can use any of these combinations:

| Database | File storage | Recommended use |
| --- | --- | --- |
| PostgreSQL | Local persistent volume | General single-replica deployment |
| PostgreSQL | Sealos S3 | Production-oriented file storage and future horizontal scaling |
| SQLite | Local persistent volume | Evaluation and small single-replica projects |
| SQLite | Sealos S3 | Lightweight database with durable object storage |

## Common Use Cases

- Headless CMS for websites and applications
- Internal data administration and operational tools
- REST or GraphQL backend with authentication and permissions
- Structured content, user, and file management
- Low-code workflows and dashboards

## Deployment

1. Open the [Directus template in the Sealos App Store](https://sealos.io/products/app-store/directus).
2. Enter a strong initial administrator email and password.
3. Choose the database and file-storage options.
4. Click **Deploy** and wait for the Directus workload to become ready. A first deployment with managed PostgreSQL usually takes several minutes while KubeBlocks provisions the database.
5. Open the HTTPS address shown by Sealos.

### Deployment Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `admin_email` | Required | Email for the first Directus administrator |
| `admin_password` | Required | Password for the first Directus administrator |
| `use_postgresql` | `true` | Creates managed PostgreSQL; `false` uses SQLite at `/directus/database/data.db` |
| `use_object_storage` | `false` | Creates a private Sealos S3 bucket; `false` uses `/directus/uploads` |

Administrator credentials are applied when Directus initializes a new database. Changing these values later does not reset an administrator stored in an existing database.

## First Login

1. Open the deployed Directus URL.
2. Sign in with the configured `admin_email` and `admin_password`.
3. On the first-run license screen, choose **Core plan** for the free, keyless tier or enter a license key for another eligible plan.
4. Complete or skip the optional usage survey.
5. Set the project owner or choose **Remind Later**.

The admin application opens at `/admin`. The same public host serves the APIs:

- REST API: `/items`, `/users`, `/files`, and other resource paths
- GraphQL API: `/graphql`
- Unauthenticated health probe: `/server/ping`

Directus 12 restricts `/server/health`; use `/server/ping` for external uptime checks.

## Database Options

### Managed PostgreSQL

This is the default. The template creates a KubeBlocks PostgreSQL cluster and an idempotent initialization Job for the `directus` database. Directus reads the generated host, port, username, and password from Kubernetes Secrets.

Choose PostgreSQL for production workloads, larger datasets, and deployments that may later use multiple Directus replicas.

### Embedded SQLite

Disable `use_postgresql` to store the database at `/directus/database/data.db` on a dedicated `1Gi` persistent volume. SQLite reduces the deployment footprint and works well for evaluation and small single-replica projects.

Keep SQLite deployments at one Directus replica because the database file lives on a ReadWriteOnce volume.

## File Storage Options

### Local Persistent Storage

With `use_object_storage` disabled, uploaded files are stored at `/directus/uploads` on a dedicated `1Gi` persistent volume.

### Sealos S3 Object Storage

Enable `use_object_storage` to create a private `ObjectStorageBucket`. Directus uses the S3-compatible `sealos` storage location and stores objects under the `uploads` prefix. Bucket credentials are injected from Sealos-managed Secrets.

Private objects return `403` when requested directly. Users access files through Directus, where authentication and permissions are enforced.

## Persistence

| Path or service | Purpose | Provisioned when |
| --- | --- | --- |
| PostgreSQL volume | Directus system and application data | `use_postgresql=true` |
| `/directus/database` | SQLite database file | `use_postgresql=false` |
| `/directus/uploads` | Local uploaded files | `use_object_storage=false` |
| Sealos S3 bucket | Object-backed uploaded files | `use_object_storage=true` |
| `/directus/extensions` | Directus extensions | Always |
| Redis volumes | Cache and rate-limiter data | Always |

## Resource Defaults

The Directus container uses the official minimum memory requirement and the nearest Sealos CPU tier:

| Component | CPU limit | Memory limit | CPU request | Memory request |
| --- | ---: | ---: | ---: | ---: |
| Directus | `500m` | `512Mi` | `50m` | `51Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis Sentinel | `500m` | `512Mi` | `50m` | `51Mi` |
| Startup and initialization containers | `100m` | `128Mi` | `10m` | `12Mi` |

Increase Directus memory for large schemas, heavy API traffic, transformations, or extension workloads.

## Scaling

The template starts with one Directus replica. Before horizontal scaling:

1. Use managed PostgreSQL.
2. Enable Sealos S3 object storage so every replica shares the same file backend.
3. Distribute the same extensions to every replica.
4. Keep Redis enabled for shared cache and rate-limiter state.
5. Adjust the StatefulSet replica and resource settings in Sealos Canvas.

## Troubleshooting

### The application is still starting

Open the Directus, PostgreSQL, and Redis resource cards in Sealos Canvas. On the first deployment, the wait containers hold Directus until the backing services are ready. PostgreSQL provisioning can take several minutes.

### The initial administrator cannot sign in

Use the email and password entered during deployment. These values create the first administrator only when the database is initialized. An existing database keeps its stored users and passwords.

### An S3 file returns `403`

This is expected for the private bucket. Access the file through the Directus `/assets/{id}` endpoint with a user or token that has permission.

### Geometry support warning appears

The managed PostgreSQL image does not include PostGIS, and SQLite does not include SpatiaLite. Standard CMS and API features continue to work. Use a compatible spatial database when the project requires geometry fields and spatial queries.

### Extensions disappear after customization

Place persistent extensions under `/directus/extensions`. When using multiple replicas, make the same extension set available to every replica.

## Documentation

- [Directus Docker Guide](https://docs.directus.io/self-hosted/docker-guide)
- [Directus Configuration Options](https://docs.directus.io/self-hosted/config-options)
- [Directus API Reference](https://directus.io/docs/api)
- [Directus GitHub Repository](https://github.com/directus/directus)
- [Sealos App Store](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

Directus 12 is distributed under the [Monospace Sustainable Core License 1.0 with a GPL future license (MSCL-1.0-GPL)](https://github.com/directus/directus/blob/v12.1.1/license). Review the license and the [Directus pricing page](https://directus.io/pricing) before production use. This repository provides the Sealos deployment template and does not change the Directus license.
