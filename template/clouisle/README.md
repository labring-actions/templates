# Deploy and Host Clouisle on Sealos

Clouisle is an open-source AI agent platform for visual workflows, RAG knowledge bases, tools, and team administration. This template deploys Clouisle `v0.3.0-beta.4` with PostgreSQL, Redis, Qdrant, background workers, an optional sandbox worker, and optional Sealos S3-compatible object storage.

![Clouisle Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/clouisle/website-screenshot.webp)

## About Hosting Clouisle

Clouisle combines a React web interface with a FastAPI backend, Celery workers, PostgreSQL metadata and lexical search, Redis queues, and Qdrant vector search. The default deployment provides the core knowledge-base and agent platform. An optional sandbox worker runs code and command jobs separately from the API process.

The template preserves the official single-instance Compose topology and replaces the Compose database containers with KubeBlocks-managed PostgreSQL and Redis. Uploads use a shared persistent volume by default; enabling S3 storage provisions a private Sealos ObjectStorageBucket and configures Clouisle after its database migration completes.

## Common Use Cases

- **AI Agent Workspaces**: Create team-scoped agents and connect approved model providers and tools.
- **Visual Workflow Automation**: Combine LLM, tool, condition, and HTTP nodes; an enabled sandbox worker adds isolated code and command execution.
- **RAG Knowledge Bases**: Upload documents and use lexical, vector, or hybrid retrieval.
- **Multi-Team Administration**: Manage users, roles, model access, quotas, audit logs, and site settings.

## Dependencies for Clouisle Hosting

The template includes every runtime dependency used by the selected official release:

- Clouisle frontend, API, worker, and beat scheduler `0.3.0-beta.4`, plus the optional matching sandbox worker
- KubeBlocks PostgreSQL 16.4.0 with `pg_search` 0.24.3 and `pg_stat_statements`
- KubeBlocks Redis 7.2.7 with Sentinel
- Qdrant 1.18.3 with persistent storage
- A shared 1 GiB upload volume or a private Sealos ObjectStorageBucket
- Sealos Services, HTTPS Ingress, and an App entry

### Deployment Dependencies

- [Clouisle Website](https://clouisle.asia/) - Official product website
- [Clouisle GitHub Repository](https://github.com/clouisle/clouisle) - Source code and releases
- [Clouisle v0.3.0-beta.4](https://github.com/clouisle/clouisle/releases/tag/v0.3.0-beta.4) - Version deployed by this template
- [Clouisle User Guide](https://github.com/clouisle/clouisle/tree/v0.3.0-beta.4/docs/guide) - Product and administration guides

### Implementation Details

**Architecture Components:**

- **Frontend**: Serves the browser interface on port `3000`.
- **API**: Runs the FastAPI application, database migrations, authenticated upload proxy, and public API on port `8000`.
- **Worker and Beat**: Execute Celery background tasks and scheduled work.
- **Sandbox Worker**: Conditionally runs isolated code and artifact jobs through rootless Bubblewrap.
- **PostgreSQL**: Stores accounts, teams, agents, workflows, knowledge metadata, site settings, and BM25 lexical indexes.
- **Redis and Sentinel**: Provide queues, cache, and coordination.
- **Qdrant**: Stores vector embeddings for semantic and hybrid retrieval.
- **Upload Storage**: Uses either a shared local PVC or a private S3-compatible bucket selected during deployment.

KubeBlocks currently supplies PostgreSQL 16.4.0. The template installs the official ParadeDB PostgreSQL 16 package for `pg_search` 0.24.3, verifies its SHA-256 digest, adds `pg_search` and `pg_stat_statements` to `shared_preload_libraries`, creates both extensions, and waits for the Clouisle BM25 migration. This compatibility boundary was validated with Clouisle `v0.3.0-beta.4`, including the `knowledge_lexical_chunks_bm25_idx` index.

The S3 branch validates the private bucket before writing Clouisle's storage settings. The local branch mounts the same persistent upload claim in the API and worker, plus the sandbox worker when enabled, and pins those consumers to the API volume's node.

The Sealos HTTP Ingress contract uses a `32m` request-body envelope. This template initializes Clouisle's knowledge-base document limit to 31 MiB so multipart requests reach the application limit cleanly. Upstream Helm uses `100m`; the narrower ceiling is a deliberate Sealos platform-contract boundary.

**License Information:**

Clouisle is released under the [GNU General Public License v3.0](https://github.com/clouisle/clouisle/blob/v0.3.0-beta.4/LICENSE).

## Why Deploy Clouisle on Sealos?

Sealos combines Kubernetes application orchestration, managed databases, object storage, HTTPS networking, and lifecycle controls in one Canvas. This template turns the official multi-service topology into one configurable deployment while keeping each service visible as its own resource card.

- **One-Click Topology**: Create the full Clouisle stack from one App Store form.
- **Storage Choice**: Select a persistent local volume or private Sealos object storage.
- **Managed Data Services**: Operate PostgreSQL and Redis through KubeBlocks resource cards.
- **Immediate HTTPS Access**: Open the generated public URL after the readiness checks complete.
- **AI-Assisted Operations**: Describe configuration changes in the Canvas dialog or edit individual resource cards.

## Deployment Guide

1. Open the [Clouisle template](https://sealos.io/products/app-store/clouisle) and click **Deploy Now**.
2. Choose **Enable S3 Storage** for a private Sealos ObjectStorageBucket, or keep the default local persistent upload volume.
3. Keep **Enable Sandbox** cleared in a standard Sealos workspace. Enable it only in a workspace that permits `Unconfined` seccomp or supplies an equivalent installed `Localhost` profile for Bubblewrap.
4. Wait for the resources to become ready. Core resources typically appear in 2-3 minutes; the first PostgreSQL `pg_search` initialization can add several minutes.
5. Open the generated Clouisle HTTPS URL from the Canvas.

## Register and Log In

This template uses Clouisle's bootstrap registration flow. You create the initial credentials in the browser:

1. Open the generated Clouisle URL and select **Register**.
2. Enter a unique username, email address, and password. The release defaults require at least 8 characters, one uppercase letter, and one digit. Special characters are optional under the default policy.
3. Submit the form. The first registered account becomes active, email-verified, and receives the **Super Admin** role automatically.
4. Log in with the same username or email and password.
5. Create a team, then open **Knowledge Bases** or **Workflows** to begin using the application.

Later registrations follow the approval, email-verification, CAPTCHA, default-team, and role settings managed by the first administrator. Model-backed agent runs and vector embeddings require provider credentials configured under the administration model settings.

## Configuration

- **AI Dialog**: Describe resource or environment changes in the Canvas.
- **Resource Cards**: Adjust individual workloads, storage, network settings, or database resources.
- **Upload Storage**: Select the storage backend during the initial deployment. Preserve the selected bucket or upload PVC during upgrades.
- **Upload Size**: Knowledge-base documents are limited to 31 MiB within the Sealos `32m` Ingress envelope.
- **Code and Command Sandbox**: Enable the sandbox input only where the workspace security policy supports rootless Bubblewrap namespace and mount isolation.
- **Model Providers**: Sign in as Super Admin, open the model administration page, add provider credentials, test the connection, and grant models to the intended team.
- **Site Security**: Configure registration approval, email verification, CAPTCHA, password policy, and SSO from Clouisle site settings.

## Resource Sizing

The default deployment's core roles passed cold startup, registration, team and knowledge-base creation, file upload and download, search, and a 60-second stable window with zero active failures. The optional sandbox-worker tier is retained for compatible workspaces:

| Component | CPU | Memory |
| --- | ---: | ---: |
| API | `100m` | `1024Mi` |
| Worker | `100m` | `1024Mi` |
| Sandbox worker | `100m` | `256Mi` |
| Beat scheduler | `100m` | `256Mi` |
| Frontend | `100m` | `128Mi` |
| Qdrant | `100m` | `128Mi` |
| PostgreSQL | `500m` | `512Mi` |
| Redis | `500m` | `512Mi` |
| Redis Sentinel | `500m` | `512Mi` |

Observed steady-state memory was approximately 297 MiB for API, 607 MiB for worker, 212 MiB for the sandbox worker process, 212 MiB for beat, 70 MiB for frontend, and 16 MiB for Qdrant. The API's 512 MiB candidate was OOM-killed while receiving an oversized 40 MiB regression request, so 1024 MiB is the minimum stable tier for the documented upload boundary. The next lower memory tier also falls below the observed workload for worker and beat. The sandbox tier reflects worker-process measurement; live Bubblewrap execution requires a compatible workspace and remains outside this baseline workspace's admission policy. PostgreSQL and Redis retain the KubeBlocks database resource contract.

## Troubleshooting

### First Deployment Takes Longer

The PostgreSQL bootstrap downloads and verifies the pinned `pg_search` package, updates the managed PostgreSQL configuration, and waits for the extension and BM25 migration. Keep the PostgreSQL volume so subsequent pod replacements reuse the verified package.

### Registration Is Pending Approval

The first account receives Super Admin access immediately. Later accounts follow the registration and approval policy under **Site Settings → Security**.

### Knowledge Processing Needs a Model

Add an embedding-capable provider under the model administration page, test it, and authorize that model for the knowledge base's team.

### Code or Command Sandbox Tools Stay Queued

Clouisle `v0.3.0-beta.4` launches rootless Bubblewrap with user, PID, IPC, UTS, namespace, and mount isolation. Standard Sealos workspaces enforce PodSecurity `baseline:v1.25`, so this template leaves **Enable Sandbox** cleared by default. Use the enabled branch in a workspace that permits the worker's documented `Unconfined` seccomp profile or provides an equivalent installed `Localhost` profile. The release provides no remote sandbox backend.

### Uploads Fail

Confirm the file is within the 31 MiB knowledge-base limit. For local storage, confirm the API upload PVC is bound and the worker is scheduled with the API volume; check the sandbox worker too when enabled. For S3 storage, confirm the ObjectStorageBucket and the one-time S3 configuration Job are ready.

### Getting Help

- [Clouisle GitHub Issues](https://github.com/clouisle/clouisle/issues)
- [Clouisle Documentation](https://github.com/clouisle/clouisle/tree/v0.3.0-beta.4/docs)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

Clouisle is licensed under GPL-3.0. This template contains deployment metadata and documentation for running the upstream software on Sealos.
