# Deploy and Host MindsDB on Sealos

MindsDB is an open-source AI query engine and automation platform for building controllable AI systems over connected data. This template deploys MindsDB with PostgreSQL-backed metadata storage, persistent application storage, authentication, and optional Sealos Object Storage on Sealos Cloud.

![MindsDB Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mindsdb/website-screenshot.webp)

## About Hosting MindsDB

MindsDB provides a web editor, REST API, MySQL-compatible API, SQL execution layer, data integrations, agents, jobs, and knowledge base workflows. It lets users connect data sources, query them with SQL, and build AI-powered automation over those sources.

This Sealos template runs MindsDB as a StatefulSet and provisions a KubeBlocks PostgreSQL 16 database for MindsDB metadata. The template also creates the `mindsdb` and `kb` databases before the application starts, aligning with the upstream Compose deployment that stores application state and knowledge base vector data in PostgreSQL.

MindsDB authentication is enabled by default through the official `MINDSDB_USERNAME` and `MINDSDB_PASSWORD` environment variables. After deployment, use the configured credentials to sign in to the web UI or call the REST API.

## Common Use Cases

- **AI Query Engine**: Connect business data sources and query them through MindsDB SQL.
- **Automation Agents**: Build agents that answer questions or execute workflows over connected data.
- **Knowledge Bases**: Store and query structured or unstructured content through MindsDB knowledge base APIs.
- **Data Integration Gateway**: Expose connected data systems through a common SQL and REST interface.
- **Self-Hosted AI Platform**: Run MindsDB in your own cloud environment with managed Kubernetes primitives.

## Dependencies for MindsDB Hosting

The Sealos template includes MindsDB, PostgreSQL 16, persistent storage, a Kubernetes Service, an HTTPS Ingress, and a Sealos App entry. Optional Sealos Object Storage can be enabled for MindsDB permanent file storage.

### Deployment Dependencies

- [MindsDB Documentation](https://docs.mindsdb.com/) - Official documentation
- [Docker Deployment Guide](https://docs.mindsdb.com/setup/self-hosted/docker/) - Official Docker deployment guide
- [Environment Variables](https://docs.mindsdb.com/setup/environment-vars) - Official runtime configuration reference
- [Custom Configuration](https://docs.mindsdb.com/setup/custom-config) - Official storage and API configuration guide
- [REST API Query Reference](https://docs.mindsdb.com/rest/sql) - SQL execution API
- [Minds Platform Repository](https://github.com/mindsdb/minds-platform) - Source code and upstream deployment files

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **MindsDB Application**: Runs `mindsdb/mindsdb:v26.1.0` and serves the web UI, REST API, and MySQL-compatible API.
- **PostgreSQL**: KubeBlocks-managed PostgreSQL 16.4 database for MindsDB metadata and knowledge base storage.
- **PostgreSQL Init Job**: Waits for PostgreSQL readiness and idempotently creates the `mindsdb` and `kb` databases.
- **Persistent Volume**: A `1Gi` volume mounted at `/mindsdb/var` for local runtime files, static GUI assets, cache, logs, and uploaded content when local file storage is selected.
- **Optional Object Storage**: A Sealos `ObjectStorageBucket` for MindsDB permanent file storage when `sealos-objectstorage` is selected.
- **Ingress and App Entry**: Sealos exposes MindsDB through an HTTPS URL and creates a dashboard entry for direct access.

**Configuration:**

The template asks for:

- `admin_username`: Administrator username for the web UI and REST API.
- `admin_password`: Administrator password for the web UI and REST API.
- `file_storage`: `local` for persistent-volume file storage, or `sealos-objectstorage` for S3-compatible permanent storage.

MindsDB runs with `MINDSDB_APIS=http,mysql`, so the web UI and REST API are exposed on port `47334`, while the MySQL-compatible API is available inside the cluster on port `47335`. PostgreSQL credentials are injected from the Sealos-managed KubeBlocks connection secret.

When Object Storage is enabled, the container generates a MindsDB configuration file at startup with the Sealos bucket, access key, secret key, and internal S3 endpoint.

**License Information:**

Minds Platform is open source under the upstream repository license. This Sealos template is deployment configuration for running MindsDB on Sealos Cloud.

## Why Deploy MindsDB on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to production operations. By deploying MindsDB on Sealos, you get:

- **One-Click Deployment**: Deploy MindsDB, PostgreSQL, persistent storage, networking, and the App entry from one template.
- **Kubernetes-Native Runtime**: Run MindsDB on managed Kubernetes primitives with internal service discovery.
- **Persistent Storage Included**: Keep application files and metadata available across restarts.
- **Managed Database Setup**: Create PostgreSQL resources and required databases automatically.
- **Optional Object Storage**: Use a Sealos-managed S3-compatible bucket for MindsDB permanent file storage.
- **Instant Public Access**: Get an automatic HTTPS URL for the web editor and REST API.
- **Pay-As-You-Go Resources**: Start with a measured resource profile and scale as workloads grow.

Deploy MindsDB on Sealos to run a self-hosted AI query and automation platform without managing Kubernetes manifests manually.

## Deployment Guide

1. Open the [MindsDB template](https://sealos.io/products/app-store/mindsdb) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - `admin_username`: the username for MindsDB login.
   - `admin_password`: the password for MindsDB login.
   - `file_storage`: choose `local` or `sealos-objectstorage`.
3. Wait for deployment to complete, typically 2-3 minutes. The first cold start can take longer while PostgreSQL initializes, MindsDB applies database migrations, and the web GUI assets are prepared. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **MindsDB Web UI**: Open the generated public URL and sign in with the configured credentials.
   - **REST API**: Use the same public URL for endpoints such as `/api/login`, `/api/status`, and `/api/sql/query`.
   - **MySQL-Compatible API**: Use the internal Service on port `47335` from workloads inside the same namespace.

## Configuration

After deployment, you can configure MindsDB through:

- **MindsDB Web UI**: Sign in with the configured administrator credentials, connect data sources, install integrations, run SQL, and manage knowledge bases.
- **REST API**: Call `/api/login` to obtain a token, then use authenticated endpoints such as `/api/sql/query`.
- **Sealos AI Dialog**: Describe environment, storage, or resource changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, PostgreSQL Cluster, Ingress, Service, persistent volume, or Object Storage cards in Canvas to inspect and adjust settings.

## Scaling

MindsDB is memory-intensive during cold start because it applies migrations, starts multiple APIs, and prepares the web GUI. The template uses a `1Gi` memory limit based on live cold-start testing on Sealos.

1. Open the Canvas for your MindsDB deployment.
2. Click the MindsDB StatefulSet resource card.
3. Increase memory first when startup, integration installation, or query workloads become heavier.
4. Increase CPU when concurrent SQL queries, agents, or API traffic grow.
5. Apply changes through the dialog and monitor readiness from the Canvas.

For production workloads with many integrations, large file uploads, or active knowledge bases, plan additional memory and storage capacity.

## Troubleshooting

### Login fails

- Cause: The entered credentials differ from `admin_username` and `admin_password`.
- Solution: Use the deployment values, or update `MINDSDB_USERNAME` and `MINDSDB_PASSWORD` on the StatefulSet and restart the pod.

### API redirects from `/api/databases` or `/api/projects`

- Cause: MindsDB canonicalizes some collection endpoints with a trailing slash.
- Solution: Use `/api/databases/` and `/api/projects/` when calling these endpoints directly.

### Startup takes several minutes

- Cause: PostgreSQL initialization, database creation, MindsDB migrations, and GUI asset preparation happen during the first cold start.
- Solution: Wait for the StatefulSet pod to become ready. Increase memory when the pod is OOMKilled during startup.

### Knowledge base vector storage

- Cause: Upstream Compose uses pgvector-capable PostgreSQL for `KB_PGVECTOR_URL`.
- Solution: The template provisions PostgreSQL 16.4 and creates the `kb` database. Verify pgvector extension availability in your Sealos PostgreSQL environment before relying on vector-heavy knowledge base workloads.

### Getting Help

- [MindsDB Documentation](https://docs.mindsdb.com/)
- [Minds Platform GitHub Issues](https://github.com/mindsdb/minds-platform/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [MindsDB REST API](https://docs.mindsdb.com/rest/overview)
- [MindsDB SQL Query API](https://docs.mindsdb.com/rest/sql)
- [MindsDB Custom Configuration](https://docs.mindsdb.com/setup/custom-config)
- [MindsDB Docker Image](https://hub.docker.com/r/mindsdb/mindsdb)

## License

This Sealos template is provided under the repository's template license. Minds Platform itself is licensed under the upstream project license.
