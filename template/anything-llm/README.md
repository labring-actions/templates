# Deploy and Host AnythingLLM on Sealos

AnythingLLM is an all-in-one AI application for private chat, document ingestion, agents, and workspace knowledge bases. This template deploys AnythingLLM with persistent application storage on Sealos Cloud.

![AnythingLLM Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/anything-llm/website-screenshot.webp)

## About Hosting AnythingLLM

AnythingLLM runs as a single web service that includes the application server, document ingestion pipeline, local workspace storage, and vector storage configuration. The template provisions persistent volumes for `/app/server/storage`, `/app/collector/hotdir`, and `/app/collector/outputs` so uploaded files, workspace metadata, and processed outputs survive restarts.

The default vector backend is LanceDB in the application storage volume. For an external PGVector deployment, set **Vector Database** to `pgvector` and fill the PostgreSQL connection string plus table name.

## Common Use Cases

- **Private AI chat**: Create workspace-based assistants with your own model providers.
- **Document Q&A**: Upload files and query them through workspace knowledge bases.
- **Agent workflows**: Run tools and agent actions from a browser UI.
- **Team knowledge hub**: Keep project context, documents, and chats in one self-hosted interface.

## Dependencies for AnythingLLM Hosting

The Sealos template includes the AnythingLLM container image, persistent storage, public HTTPS ingress, and optional PGVector connection parameters.

### Deployment Dependencies

- [Official Website](https://anythingllm.com/) - Product website
- [GitHub Repository](https://github.com/Mintplex-Labs/anything-llm) - Source code
- [Docker Guide](https://github.com/Mintplex-Labs/anything-llm/tree/master/docker) - Upstream container deployment notes

## Implementation Details

**Architecture Components:**

- **AnythingLLM**: Web UI, API server, workspace management, document ingestion, and vector backend client.
- **Persistent Storage**: Volumes for server storage, collector hotdir, and collector outputs.
- **Optional PGVector**: External PostgreSQL with pgvector extension for vector storage.

**Configuration:**

- `auth_token` sets the single-user password.
- `openai_api_key` is available during onboarding and later model setup.
- `vector_database` defaults to `lancedb`; choose `pgvector` and fill the PGVector fields for external vector storage.

**License Information:**

AnythingLLM is licensed under the MIT License.

## Why Deploy AnythingLLM on Sealos?

Sealos provides one-click deployment, automatic HTTPS, persistent storage, and Kubernetes-backed lifecycle management. You get a public AnythingLLM URL with configurable storage and model-provider settings from the App Store form.

## Deployment Guide

1. Open the [AnythingLLM template](https://sealos.io/products/app-store/anything-llm) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. Set **Single-user password** for first login. Keep **Vector Database** as `lancedb` for built-in storage, or choose `pgvector` and fill the external PGVector fields.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated application URL and log in with the single-user password you configured.

## Configuration

After deployment, configure model providers, embedding providers, workspaces, and document upload settings in the AnythingLLM UI. Resource and environment changes can be made from the Sealos Canvas resource cards.

## Additional Resources

- [AnythingLLM Documentation](https://docs.anythingllm.com/)
- [GitHub Issues](https://github.com/Mintplex-Labs/anything-llm/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This template follows the upstream AnythingLLM MIT License.
