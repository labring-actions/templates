# Deploy and Host Dify on Sealos

Dify is an open-source LLM application development platform for building AI agents, workflows, chatbots, and RAG applications. This template deploys Dify with PostgreSQL, Redis, Weaviate, object storage, sandbox execution, and the plugin daemon on Sealos Cloud.

![Dify Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/dify/website-screenshot.webp)

## About Hosting Dify

Dify runs as a multi-service AI application platform. The web service serves the console and public app UI, the API service handles backend requests, workers process asynchronous jobs, and the worker beat container schedules periodic tasks. Dify Sandbox isolates code execution, while the plugin daemon installs and runs marketplace plugins.

The template provisions PostgreSQL for application and plugin metadata, Redis for Celery queues, Weaviate for vector search, and an optional Sealos ObjectStorage bucket for uploaded files and plugin packages. Sealos also manages the public HTTPS endpoint through Ingress and exposes Dify as a dashboard App entry.

## Common Use Cases

- **AI agents and chatbots**: Build hosted assistants with model providers, tools, and memory.
- **RAG applications**: Upload documents, index them in Weaviate, and serve grounded answers.
- **Workflow automation**: Run multi-step LLM workflows with background worker processing.
- **Plugin-based extensions**: Install Dify plugins through the plugin daemon and marketplace.
- **Internal AI portals**: Host a shared console for teams building and testing AI apps.

## Dependencies for Dify Hosting

The Sealos template includes all required runtime services: Dify Web, Dify API, Celery worker, Celery beat, Dify Sandbox, Dify Plugin Daemon, PostgreSQL, Redis, Weaviate, and optional Sealos ObjectStorage.

### Deployment Dependencies

- [Dify Documentation](https://docs.dify.ai/) - Product and self-hosting documentation
- [Docker Compose Deployment](https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose) - Official self-hosted topology
- [Dify GitHub Repository](https://github.com/langgenius/dify) - Source code and releases
- [Sealos App Store](https://sealos.io/products/app-store/dify) - Dify template page

### Implementation Details

**Architecture Components:**

- **Web**: Serves the Dify console and public application pages.
- **API**: Handles console APIs, app APIs, file routes, MCP routes, migrations, and first setup.
- **Worker**: Processes Celery queues for datasets, workflows, mail, and asynchronous jobs.
- **Worker Beat**: Schedules periodic background tasks.
- **Sandbox**: Runs isolated code execution through an internal service endpoint.
- **Plugin Daemon**: Manages plugin installation, execution, and remote plugin debugging endpoints.
- **PostgreSQL**: Stores Dify application metadata and a separate plugin database.
- **Redis**: Provides queue and cache services for the API, workers, and plugin daemon.
- **Weaviate**: Provides the default vector database for knowledge indexing.
- **Object Storage**: Stores uploaded files and plugin packages when `use_sealos_objectstorage` is enabled.

**Configuration:**

- `init_password` sets the initial administrator password used on the first setup screen.
- `use_sealos_objectstorage` provisions a Sealos ObjectStorage bucket and injects S3-compatible credentials.
- Dify URLs are configured to `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}` for console, API, app, and service endpoints.
- PostgreSQL and Redis credentials are sourced from Sealos-managed KubeBlocks secrets.

**License Information:**

Dify is licensed under the Dify Open Source License. This Sealos template is provided under the repository license for Sealos application templates.

## Why Deploy Dify on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and operations. By deploying Dify on Sealos, you get:

- **One-Click Deployment**: Deploy the full Dify stack from the App Store.
- **Managed Dependencies**: Provision PostgreSQL, Redis, Weaviate, storage, and public routing with the template.
- **Instant HTTPS Access**: Receive a public URL with SSL after deployment.
- **Canvas Operations**: Use the Canvas, AI dialog, and resource cards for post-deployment changes.
- **Pay-As-You-Go Resources**: Adjust CPU, memory, and replicas as usage grows.

## Deployment Guide

1. Open the [Dify template](https://sealos.io/products/app-store/dify) and click **Deploy Now**.
2. Configure the deployment parameters:
   - `init_password`: Enter the password for the first Dify administrator.
   - `use_sealos_objectstorage`: Keep `true` for Sealos-managed S3-compatible storage.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, Sealos redirects you to the Canvas.
4. Open the Dify App entry or the public URL shown by Sealos.
5. On the first setup screen, create the initial administrator account. Use any valid administrator email and the `init_password` value entered during deployment.
6. Log in with the administrator email and password.

## First Login Checks

After login, verify two core interactions:

1. Open **Studio** and create a Chatflow or Chatbot app.
2. Open **Knowledge** and create a knowledge base to confirm the API, worker, Redis queue, Weaviate, and storage path are connected.

Model providers are configured inside Dify after login. Add your provider API key in Dify settings before running model-backed chats or workflows.

## Configuration

After deployment, you can configure Dify through:

- **Dify Console**: Add model providers, create apps, configure tools, and manage knowledge bases.
- **AI Dialog**: Describe infrastructure changes in the Sealos Canvas dialog.
- **Resource Cards**: Adjust Deployment, StatefulSet, database, storage, and Ingress resources.
- **Environment Variables**: Update Dify runtime settings from the relevant workload cards.

## Scaling

To scale Dify:

1. Open the Canvas for your deployment.
2. Click the Web, API, Worker, Sandbox, Plugin Daemon, PostgreSQL, Redis, or Weaviate resource card.
3. Adjust CPU, memory, storage, or replica settings.
4. Apply the changes in the dialog and wait for the rollout to finish.

The template assigns the `1G` memory tier to the API, worker, and beat containers. Live startup validation showed the beat process can exceed `256Mi` during scheduler boot. The Web container uses TCP probes so the first-init redirect and login flow complete in the browser.

For larger workloads, scale the API and worker containers first, then increase PostgreSQL, Redis, and Weaviate resources based on observed bottlenecks.

## Troubleshooting

### First setup screen loops

- Cause: The API service is waiting for PostgreSQL migrations or Redis connectivity.
- Solution: Check the API and worker logs from the Canvas, then confirm PostgreSQL and Redis resource cards are healthy.

### Knowledge base indexing stalls

- Cause: Worker, Redis, Weaviate, or object storage connectivity is delayed.
- Solution: Check worker logs, Redis status, and Weaviate readiness. Confirm `use_sealos_objectstorage` stayed enabled for persistent uploads.

### Plugin installation fails

- Cause: Plugin daemon storage or internal API credentials are unavailable.
- Solution: Check plugin daemon logs and confirm the API service is reachable from the plugin daemon resource.

### Getting Help

- [Dify Documentation](https://docs.dify.ai/)
- [Dify GitHub Issues](https://github.com/langgenius/dify/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Dify Self-Hosted Guide](https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose)
- [Dify Plugins](https://docs.dify.ai/plugins)
- [Dify API Reference](https://docs.dify.ai/api-reference)

## License

This Sealos template is provided under the repository license for Sealos templates. Dify itself is licensed under the Dify Open Source License.
