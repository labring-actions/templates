# Deploy and Host Appwrite on Sealos

Appwrite is an open-source backend platform for building applications with authentication, databases, storage, functions, and APIs. This template deploys Appwrite 1.9.0 with MongoDB, Redis, persistent storage, optional S3-compatible object storage, and HTTPS ingress on Sealos Cloud.

![Appwrite Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/appwrite/website-screenshot.webp)

## About Hosting Appwrite

Appwrite provides a self-hosted backend console and API for projects that need user authentication, document databases, file storage, serverless-style functions, and platform services behind a single API surface.

This Sealos template provisions the core Appwrite web/API service, a KubeBlocks MongoDB database, a lightweight Redis service, persistent `/storage`, and a public HTTPS URL. The template also includes an optional Sealos S3-compatible object storage bucket for user uploads.

## Common Use Cases

- **Application Backends**: Build web or mobile backends with authentication, database APIs, and file uploads.
- **Self-Hosted BaaS**: Keep backend platform control inside your own Sealos workspace.
- **Prototype APIs**: Create project APIs quickly from the Appwrite Console.
- **Team Development**: Centralize projects, users, collections, and storage buckets for small teams.

## Dependencies for Appwrite Hosting

The Sealos template includes Appwrite, MongoDB, Redis, persistent storage, optional object storage, a Service, an Ingress, and an App launcher entry.

### Deployment Dependencies

- [Appwrite Documentation](https://appwrite.io/docs) - Official product documentation
- [Self-hosting Installation](https://appwrite.io/docs/advanced/self-hosting/installation) - Official Docker Compose installation guide
- [Appwrite GitHub Repository](https://github.com/appwrite/appwrite) - Source code and releases

## Implementation Details

### Architecture Components

- **Appwrite**: Runs the Console and API on port `80`
- **MongoDB**: Default Appwrite 1.9 database backend
- **Redis**: Cache and queue dependency
- **Persistent Storage**: Stores local Appwrite runtime files at `/storage`
- **Optional Object Storage**: Enables S3-compatible storage for uploaded files

### Resource Allocation

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Appwrite | 20m | 200m | 25Mi | 256Mi |
| MongoDB | 50m | 500m | 51Mi | 512Mi |
| Redis | 20m | 200m | 25Mi | 256Mi |

### Configuration

Sealos generates the public hostname, application name, OpenSSL key, and executor secret automatically. MongoDB credentials are injected from KubeBlocks-managed secrets, and the bundled Redis service is wired through an internal Kubernetes Service. Appwrite router protection is disabled so both Sealos ingress traffic and internal Kubernetes health checks can reach the service.

### License Information

Appwrite is licensed under the [BSD 3-Clause License](https://github.com/appwrite/appwrite/blob/master/LICENSE). This template follows the licensing terms of the Sealos templates repository.

## Why Deploy Appwrite on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies the full deployment lifecycle. By deploying Appwrite on Sealos, you get:

- **One-Click Deployment**: Launch Appwrite with MongoDB, Redis, storage, and HTTPS from one template page.
- **Managed Runtime Dependencies**: Use KubeBlocks-managed MongoDB and an internal Redis service without wiring them by hand.
- **Persistent Data**: Keep Appwrite storage and database data across restarts.
- **Public HTTPS Access**: Open the Appwrite Console from an automatically generated secure URL.
- **Simple Operations**: Use the Sealos Canvas and resource cards to adjust resources after deployment.

## Deployment Guide

1. Open the [Appwrite template](https://sealos.io/products/app-store/appwrite) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. Enable object storage when uploaded files should use Sealos S3-compatible storage.
3. Wait for deployment to complete, which typically takes several minutes because MongoDB must initialize before Appwrite starts.
4. Open the generated Appwrite URL and create the first root account from the sign-up screen.
5. Sign in to the Appwrite Console, create a project, and create a collection or storage bucket.

## Configuration

After deployment, use the Sealos Canvas to adjust CPU, memory, storage, or the public hostname. Use the Appwrite Console for project-level configuration, authentication providers, database collections, storage buckets, API keys, and platform settings.

## Scaling

This template is optimized for a single Appwrite web/API instance. Scale vertically first by increasing CPU and memory on the Appwrite StatefulSet. Increase MongoDB, Redis, or storage capacity as project data grows.

## Troubleshooting

**Issue: Appwrite takes several minutes to become ready**
- Cause: MongoDB needs to initialize before Appwrite can connect.
- Solution: Wait for the database pods to become ready, then check the Appwrite StatefulSet logs.

**Issue: Uploads should use object storage**
- Cause: The default deployment stores files locally.
- Solution: Enable the object storage option at deployment time.

## Additional Resources

- [Appwrite Self-Hosting](https://appwrite.io/docs/advanced/self-hosting)
- [Appwrite API Reference](https://appwrite.io/docs/references)
- [Appwrite GitHub Issues](https://github.com/appwrite/appwrite/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing policy of the templates repository. Appwrite itself is licensed under the BSD 3-Clause License.
