# Deploy and Host Evolution API on Sealos

Evolution API is an open-source WhatsApp API platform for Baileys, WhatsApp Cloud API, webhooks, bots, chats, and media integrations. This template deploys Evolution API with PostgreSQL, Redis, persistent instance storage, and optional S3-compatible object storage on Sealos Cloud.

![Evolution API Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/evolution-api/website-screenshot.webp)

## About Hosting Evolution API

Evolution API exposes WhatsApp automation and integration features through HTTP APIs. It can manage WhatsApp instances, QR code pairing, message events, webhooks, chat integrations, and media workflows from a self-hosted backend.

The Sealos template runs Evolution API as a Kubernetes StatefulSet. KubeBlocks provisions PostgreSQL for persistent application data and Redis for cache and instance coordination. A persistent volume stores local WhatsApp instance state, and S3-compatible object storage can be enabled for media files.

Sealos handles public HTTPS access, service discovery, storage, database provisioning, and resource configuration so you can operate Evolution API without writing Kubernetes manifests manually.

## Common Use Cases

- **WhatsApp Automation API**: Create and manage WhatsApp instances for business messaging workflows.
- **Webhook Event Hub**: Receive message, contact, chat, group, and connection events in external systems.
- **Chatbot Integrations**: Connect WhatsApp conversations with bot platforms and automation tools.
- **Media Processing**: Store WhatsApp media locally or in S3-compatible object storage.
- **Customer Communication Backend**: Provide a programmable backend for CRM, support, and notification systems.

## Dependencies for Evolution API Hosting

The Sealos template includes the required runtime dependencies:

- Evolution API `v2.3.7`
- PostgreSQL `16.4.0` through KubeBlocks
- Redis `7.2.7` through KubeBlocks
- Persistent storage for `/evolution/instances`
- Optional S3-compatible object storage for media
- HTTPS Ingress and Sealos App entry

### Deployment Dependencies

- [Evolution API GitHub Repository](https://github.com/evolution-foundation/evolution-api) - Source code and releases
- [Evolution API Documentation](https://doc.evolution-api.com/) - Official documentation
- [Docker Hub Image](https://hub.docker.com/r/evoapicloud/evolution-api) - Published container images

## Implementation Details

**Architecture Components:**

- **Evolution API StatefulSet**: Runs `evoapicloud/evolution-api:v2.3.7` on port `8080`.
- **PostgreSQL Cluster**: Stores instances, messages, contacts, chats, labels, and runtime metadata.
- **PostgreSQL Init Job**: Waits for PostgreSQL readiness and creates the `evolution_db` database idempotently. The application uses the `evolution_api` PostgreSQL schema, matching the upstream example connection URI.
- **Redis Cluster**: Provides cache and instance coordination.
- **Persistent Instance Volume**: Stores WhatsApp instance state at `/evolution/instances`.
- **Optional ObjectStorageBucket**: Enables S3-compatible media storage when `use_object_storage` is enabled.
- **Service, Ingress, and App Resource**: Expose Evolution API through a public HTTPS URL.

**Configuration:**

The template generates the API key automatically as `AUTHENTICATION_API_KEY`. Evolution API has no registration flow in this template; use the generated API key for the Manager UI and HTTP API requests. The API manager is enabled by default and is available at the public application URL.

Object storage has two modes:

- **Local media mode**: Default. Media and instance files stay on the persistent volume.
- **S3 media mode**: Enable `use_object_storage` during deployment to create an S3-compatible bucket and configure `S3_*` environment variables.

**Resource Defaults:**

- App CPU limit: `200m`
- App memory limit: `256Mi`
- Database CPU limit: `500m`
- Database memory limit: `512Mi`

**Health Checks:**

The template probes `/` on port `8080` for startup, readiness, and liveness. Live deployment should also verify logs and one authenticated API request with the generated API key.

**License Information:**

Evolution API is licensed under Apache License 2.0 with additional commercial and attribution conditions in the upstream repository license.

## Why Deploy Evolution API on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and operations. By deploying Evolution API on Sealos, you get:

- **One-Click Deployment**: Deploy Evolution API, PostgreSQL, Redis, storage, and HTTPS access from one template.
- **Built-In Persistence**: Keep database data and WhatsApp instance state across restarts.
- **Optional Object Storage**: Use S3-compatible storage for media-heavy workloads.
- **Instant Public Access**: Sealos provisions a public HTTPS endpoint automatically.
- **Easy Customization**: Adjust environment variables, resources, and storage from the Sealos Canvas.
- **AI-Assisted Operations**: Use the Sealos AI dialog or resource cards for post-deployment changes.

## Deployment Guide

1. Open the [Evolution API template](https://sealos.io/products/app-store/evolution-api) and click **Deploy Now**.
2. Configure the deployment parameters:
   - **use_object_storage**: Enable this option when you want media files stored in S3-compatible object storage.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Evolution API through the provided URL:
   - **Manager UI and API Base URL**: Use the public HTTPS URL from Sealos.
   - **API Authentication**: Open the StatefulSet resource card, read the generated `AUTHENTICATION_API_KEY` value from the workload environment, and use it in the Manager UI or API requests.

## Configuration

After deployment, configure Evolution API through:

- **Manager UI**: Use the generated API key to create and manage WhatsApp instances and QR pairing.
- **HTTP API**: Use the generated API key in requests.
- **Resource Cards**: Modify environment variables such as webhooks, integrations, logging, S3, and proxy settings.
- **Canvas AI Dialog**: Describe the configuration change you want and let Sealos apply it.

## Troubleshooting

### API requests are unauthorized

- **Cause**: Requests are missing the generated `AUTHENTICATION_API_KEY`.
- **Solution**: Read the value from the Evolution API workload environment and include it in API requests according to the Evolution API documentation.

### Instance pairing or media handling fails

- **Cause**: Instance storage is not writable or S3 settings are incomplete.
- **Solution**: Keep the template's persistent volume and permission init container. If object storage is enabled, confirm that the ObjectStorageBucket and object storage secrets exist.

### Startup takes longer than expected

- **Cause**: PostgreSQL and Redis must become ready before the application starts.
- **Solution**: Check the StatefulSet logs plus PostgreSQL and Redis resource cards in Canvas.

## Additional Resources

- [Evolution API Documentation](https://doc.evolution-api.com/)
- [Evolution API GitHub Issues](https://github.com/evolution-foundation/evolution-api/issues)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template provides deployment configuration for running Evolution API on Sealos. Evolution API itself is distributed under Apache License 2.0 with additional conditions in the upstream license file.
