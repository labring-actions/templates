# Deploy and Host Immich on Sealos

Immich is a self-hosted photo and video management platform for backing up, organizing, searching, and sharing personal media. This template deploys Immich with PostgreSQL, Redis, persistent media storage, and optional machine learning on Sealos Cloud.

![Immich Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/immich/website-screenshot.webp)

## About Hosting Immich

Immich runs as a web application that provides a browser UI, mobile app sync endpoints, background media processing, and smart library features. The Sealos template provisions the application server, PostgreSQL 16.4 with pgvector, Redis 7.2.7, persistent upload storage, and an optional machine learning service.

The application server stores photos and videos on a persistent volume mounted at `/usr/src/app/upload`. PostgreSQL stores metadata, users, albums, jobs, and vector indexes, while Redis coordinates background jobs and cache data. When machine learning is enabled, a separate Immich ML service provides face recognition, object detection, and smart search support.

## Common Use Cases

- **Personal Photo Backup**: Sync photos and videos from mobile devices to a private server.
- **Family Media Library**: Organize shared albums, people, places, and timelines in one web UI.
- **Private Smart Search**: Use local machine learning for face recognition and semantic media search.
- **Self-Hosted Google Photos Alternative**: Keep media and metadata under your own Sealos-managed deployment.

## Dependencies for Immich Hosting

The Sealos template includes all required runtime dependencies for a single-node Immich deployment:

- **Immich Server v2.7.5**: Web UI, API, background processing, and mobile sync endpoint.
- **Immich Machine Learning v2.7.5**: Optional ML service for face recognition and smart search.
- **PostgreSQL 16.4**: KubeBlocks-managed PostgreSQL with the pgvector extension enabled.
- **Redis 7.2.7**: KubeBlocks-managed Redis for queue and cache coordination.
- **Persistent Volumes**: Media upload storage, ML cache storage, PostgreSQL data, and Redis data.

### Deployment Dependencies

- [Immich Documentation](https://immich.app/docs/) - Official documentation
- [Immich Post Installation Guide](https://immich.app/docs/install/post-install/) - First user and admin setup
- [Immich GitHub Repository](https://github.com/immich-app/immich) - Source code and release notes

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Immich Server**: StatefulSet serving the web UI and API on port `2283`.
- **Immich Machine Learning**: Optional StatefulSet serving ML requests on port `3003`.
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4 cluster with the `immich` database and vector extensions.
- **Redis**: KubeBlocks Redis 7.2.7 cluster used by Immich job queues and cache.
- **Ingress and App Link**: Sealos-managed HTTPS endpoint for browser and mobile app access.

**Configuration:**

- `enable_machine_learning` controls whether the Immich ML service is deployed.
- The server uses `IMMICH_MACHINE_LEARNING_URL` to reach the ML service when ML is enabled.
- PostgreSQL is initialized idempotently with the `immich` database and required extensions.
- Uploaded media persists on `/usr/src/app/upload`; back up this volume together with PostgreSQL.

**License Information:**

Immich is distributed under the GNU Affero General Public License v3.0. This Sealos template follows the license of the templates repository.

## Why Deploy Immich on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, networking, storage, and lifecycle management. By deploying Immich on Sealos, you get:

- **One-Click Deployment**: Deploy Immich, PostgreSQL, Redis, storage, and HTTPS routing from one template.
- **Persistent Storage Included**: Keep media uploads, model cache, database data, and Redis data across restarts.
- **Kubernetes Foundation**: Run Immich on managed Kubernetes without writing Kubernetes manifests by hand.
- **Easy Customization**: Adjust resources, storage, environment variables, and scaling from Canvas resource cards or the AI dialog.
- **Instant Public Access**: Get a Sealos-managed HTTPS URL after deployment completes.
- **Pay-as-You-Go Resources**: Start with tested resource limits and scale as your media library grows.

## Deployment Guide

1. Open the [Immich template](https://sealos.io/products/app-store/immich) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - `enable_machine_learning`: keep `true` for face recognition and smart search, or set `false` for a lighter deployment.
3. Wait for deployment to complete. The full stack usually needs several minutes because PostgreSQL, Redis, and the app server must initialize in order.
4. Access your application via the provided URL:
   - **Immich Web UI**: open the generated Sealos URL, for example `https://<your-app-host>.<your-sealos-domain>`.
5. For later changes, open the deployment Canvas and describe your requirements in the AI dialog, or click the relevant resource cards to modify resources, storage, or environment variables.

## First Login and Registration

Immich does not ship with a default username or password. On a fresh deployment, open the web UI and complete the **Getting Started** flow; the first user you register becomes the administrator.

After the admin account is created, sign in with that email and password. Additional users can be invited or created from the Immich administration settings according to your access policy.

## Configuration

After deployment, you can configure Immich through:

- **Immich Administration UI**: Manage users, libraries, jobs, storage template settings, and server preferences.
- **Sealos AI Dialog**: Describe desired changes such as resource increases or environment-variable updates.
- **Sealos Resource Cards**: Adjust StatefulSet resources, storage size, Ingress settings, or database resources.
- **Mobile Apps**: Use the generated Sealos URL as the server endpoint in the official Immich mobile app.

## Scaling

Start with the template defaults, then scale based on library size and feature usage:

1. Open the Canvas for your Immich deployment.
2. Click the Immich server, ML service, PostgreSQL, or Redis resource card.
3. Increase CPU, memory, storage, or replica settings as needed.
4. Apply the changes and wait for the resources to roll out.

Large libraries and ML-heavy workloads need more memory and storage. Always back up PostgreSQL and the upload volume before major upgrades or storage changes.

## Troubleshooting

### The web page is not ready immediately

Immich depends on PostgreSQL and Redis. If the page is temporarily unavailable right after deployment, wait until the PostgreSQL, Redis, and Immich server pods are ready, then refresh the generated URL.

### First login asks for account creation

This is expected for a fresh Immich deployment. Register the first account in the Getting Started flow; that account becomes the administrator.

### Uploads or machine learning jobs are slow

Increase Immich server or ML service CPU and memory from the Sealos Canvas. Large video uploads, thumbnail generation, face recognition, and smart search indexing can be resource-intensive.

### Getting Help

- [Immich Documentation](https://immich.app/docs/)
- [Immich GitHub Issues](https://github.com/immich-app/immich/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Immich Mobile App Documentation](https://immich.app/docs/features/mobile-app/)
- [Immich Backup and Restore Guide](https://immich.app/docs/administration/backup-and-restore/)
- [Immich Release Notes](https://github.com/immich-app/immich/releases)

## License

This Sealos template is provided under the templates repository license. Immich itself is licensed under the GNU Affero General Public License v3.0.
