# Deploy and Host Directus on Sealos

Directus is an open-source data platform and headless CMS for managing SQL databases with APIs, authentication, file management, and an admin application. This template deploys Directus with PostgreSQL, Redis, persistent volumes, and optional S3-compatible object storage on Sealos Cloud.

## About Hosting Directus

Directus provides a no-code admin interface, REST API, GraphQL API, authentication, permissions, file management, and automation tools on top of a SQL database. It is commonly used to turn existing or new databases into a managed content and data platform without building a custom backend from scratch.

The Sealos template provisions Directus as a Kubernetes StatefulSet backed by PostgreSQL for application data and Redis for cache, rate limiting, and runtime coordination. It also creates persistent volumes for local uploads and extensions, and can optionally provision S3-compatible object storage for uploaded files.

Sealos handles public HTTPS access, service discovery, persistent storage, resource configuration, and database provisioning so you can deploy Directus without writing Kubernetes manifests manually.

## Common Use Cases

- **Headless CMS**: Manage content models, media files, users, roles, and API access for websites and applications.
- **Database Admin App**: Provide a polished admin interface for PostgreSQL-backed internal tools.
- **API Backend**: Expose REST and GraphQL APIs with authentication and permissions from a managed SQL schema.
- **Low-Code Data Platform**: Build data workflows, dashboards, and operational tools around structured business data.
- **Media and File Management**: Store uploaded files locally or in S3-compatible object storage for production-friendly deployments.

## Dependencies for Directus Hosting

The Sealos template includes the required runtime dependencies for Directus:

- Directus `11.17.4`
- PostgreSQL `16.4.0` through KubeBlocks
- Redis `7.2.7` through KubeBlocks
- Persistent storage for uploads and extensions
- Optional S3-compatible object storage for uploaded files
- HTTPS Ingress and Sealos App entry

### Deployment Dependencies

- [Directus Documentation](https://directus.io/docs/) - Official Directus documentation
- [Directus Self-Hosting Guide](https://directus.io/docs/self-hosting/overview) - Runtime and deployment reference
- [Directus GitHub Repository](https://github.com/directus/directus) - Source code, releases, and issues
- [Directus Community](https://community.directus.io/) - Community support and discussions

## Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Directus StatefulSet**: Runs the Directus web application and API on port `8055` using `directus/directus:11.17.4`.
- **PostgreSQL Cluster**: Stores Directus system tables, users, roles, permissions, collections, and application data.
- **PostgreSQL Init Job**: Waits for PostgreSQL readiness and creates the `directus` database idempotently.
- **Redis Cluster**: Provides Redis for Directus cache, rate limiter storage, and runtime coordination.
- **Persistent Uploads Volume**: Stores local uploaded files at `/directus/uploads` when object storage is not enabled.
- **Persistent Extensions Volume**: Stores Directus extensions at `/directus/extensions`.
- **Optional ObjectStorageBucket**: Creates S3-compatible storage and configures Directus storage under the `sealos` location when `use_object_storage` is enabled.
- **Service and Ingress**: Exposes Directus through a public HTTPS URL managed by Sealos.
- **Sealos App Resource**: Adds the deployed Directus instance to the Sealos application interface.

**Configuration:**

The template asks for an initial administrator email and password. It generates the Directus `SECRET`, public host, and application name automatically.

Directus connects to PostgreSQL through KubeBlocks connection secrets and to Redis through the Sealos cluster service DNS name. Startup containers wait for PostgreSQL and Redis before the main Directus container starts.

File storage can run in two modes:

- **Local storage**: Default mode. Directus stores uploaded files in the persistent `/directus/uploads` volume.
- **Object storage**: Optional mode. When `use_object_storage` is enabled, the template provisions an S3-compatible bucket and configures Directus with `STORAGE_SEALOS_*` environment variables.

**Resource Defaults:**

The template uses conservative default resources for Directus, init containers, and database components:

- CPU limit: `200m`
- Memory limit: `256Mi`
- CPU request: `20m`
- Memory request: `25Mi`

**Health Checks:**

Directus uses `/server/health` for startup, readiness, and liveness probes. This keeps the application out of service until the database, Redis, and file storage are ready.

**License Information:**

Directus is distributed under the Business Source License 1.1, with a change license to GNU GPL v3 after the applicable change date. Review the [Directus license](https://github.com/directus/directus/blob/main/license) and [Directus pricing](https://directus.io/pricing) pages for production usage terms.

## Why Deploy Directus on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle, from cloud development environments to production deployment and operations. By deploying Directus on Sealos, you get:

- **One-Click Deployment**: Deploy Directus with PostgreSQL, Redis, storage, and HTTPS access from one template.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed infrastructure without writing manifests or managing cluster internals.
- **Built-In Persistent Storage**: Keep database data, uploads, and extensions available across restarts.
- **Optional Object Storage**: Choose S3-compatible storage during deployment when you want a more production-friendly file storage path.
- **Instant Public Access**: Sealos provisions a public HTTPS URL for the Directus admin app and APIs.
- **Easy Customization**: Adjust environment variables, resources, storage, and service settings from the Sealos Canvas after deployment.
- **AI-Assisted Operations**: Describe changes in the Sealos AI dialog or edit resource cards directly for post-deployment updates.
- **Pay-As-You-Go Efficiency**: Start with lightweight resources and increase them only when your workload needs more capacity.

Deploy Directus on Sealos and focus on modeling data, managing content, and building APIs instead of managing infrastructure.

## Deployment Guide

1. Open the [Directus template](https://sealos.io/products/app-store/directus) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **admin_email**: Initial Directus administrator email address.
   - **admin_password**: Initial Directus administrator password.
   - **use_object_storage**: Enable this option if you want uploaded files stored in S3-compatible object storage instead of the local persistent volume.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URLs:
   - **Directus Admin App**: Log in with the configured administrator email and password.
   - **Directus API**: Use the same public URL for REST and GraphQL API access.

## Configuration

After deployment, you can configure Directus through:

- **Directus Admin App**: Manage collections, fields, roles, permissions, users, files, flows, and settings.
- **AI Dialog**: Describe configuration changes in Sealos and let AI apply updates to resources.
- **Resource Cards**: Open the StatefulSet, database, Redis, storage, or Ingress cards in the Canvas to adjust settings.
- **Environment Variables**: Modify Directus runtime settings such as storage, cache, public URL, and security options from the workload resource.
- **Extensions Volume**: Use `/directus/extensions` for Directus extensions that need persistent storage.

For production deployments with multiple replicas or high file-upload volume, enable object storage so uploaded files are not tied to a single local volume.

## Scaling

To scale your deployment:

1. Open the Canvas for your Directus deployment.
2. Click the Directus StatefulSet resource card.
3. Adjust CPU, memory, or replica settings in the dialog.
4. Apply the changes and wait for the workload to roll out.

Directus uses PostgreSQL and Redis as shared backing services. If you increase Directus replicas, prefer object storage for uploaded files so all replicas can access the same file backend.

## Troubleshooting

### Directus does not become ready

- **Cause**: PostgreSQL, Redis, or file storage is not ready yet.
- **Solution**: Check the Directus StatefulSet logs and the PostgreSQL and Redis resource cards. The template includes startup wait containers and `/server/health` probes, so readiness may take a few minutes during first deployment.

### Login fails with the initial administrator account

- **Cause**: The wrong administrator email or password was entered during deployment.
- **Solution**: Use the values configured in the deployment dialog. If they were entered incorrectly, update the deployment or recreate the application with the intended credentials.

### File uploads fail

- **Cause**: The local uploads volume is not writable, or object storage credentials are not available when object storage mode is enabled.
- **Solution**: Keep the template's volume permission init container and `fsGroup` settings when customizing the workload. If object storage is enabled, verify that the ObjectStorageBucket and related secrets were created.

### Extensions are not available after restart

- **Cause**: Extensions were not placed in the persistent extensions path.
- **Solution**: Store extensions under `/directus/extensions`, which is backed by a persistent volume in this template.

### Getting Help

- [Directus Documentation](https://directus.io/docs/)
- [Directus GitHub Issues](https://github.com/directus/directus/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Directus API Reference](https://directus.io/docs/api)
- [Directus Configuration Reference](https://directus.io/docs/configuration)
- [Directus Self-Hosting Overview](https://directus.io/docs/self-hosting/overview)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template provides deployment configuration for running Directus on Sealos. Directus itself is distributed under the Business Source License 1.1, with a change license to GNU GPL v3 after the applicable change date. Review the Directus license before using it in production.
