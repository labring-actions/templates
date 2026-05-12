# Deploy and Host EdgeQuake on Sealos

EdgeQuake is a high-performance Graph-RAG platform written in Rust for transforming documents into knowledge graphs and querying them with vector and graph retrieval. This template deploys EdgeQuake with a Rust API, a React/Next.js Web UI, and PostgreSQL with pgvector and Apache AGE-compatible graph storage on Sealos Cloud.

## About Hosting EdgeQuake

EdgeQuake combines document ingestion, entity extraction, relationship mapping, vector search, and graph traversal into a Graph-RAG system. Instead of relying only on vector similarity, it stores entities and relationships so users can ask multi-hop, thematic, and relationship-oriented questions across their documents.

This Sealos template deploys a multi-service architecture. The frontend provides the browser UI for uploads, workspace configuration, querying, and graph visualization, while the API serves the Graph-RAG backend, health endpoints, and REST interface. Sealos automatically provisions PostgreSQL 16.4.0 with persistent storage, initializes the `edgequake` database, enables `uuid-ossp` and `vector`, and attempts to enable Apache AGE with a compatible fallback layer when AGE is unavailable.

Sealos also provisions public HTTPS access for both the Web UI and API, service discovery between components, resource controls, and post-deployment management through the Canvas.

## Common Use Cases

- **Document Knowledge Bases**: Upload documents and query them with graph-aware retrieval instead of simple keyword or vector search.
- **Research and Analysis Workspaces**: Explore entities, relationships, themes, and cross-document connections in technical, legal, financial, or research material.
- **AI Agent Knowledge Tools**: Use EdgeQuake as a structured retrieval backend for agents that need document-grounded answers.
- **Graph Visualization**: Inspect generated knowledge graphs through the React UI and understand how concepts connect.
- **RAG API Prototyping**: Build applications against the EdgeQuake REST API and streaming endpoints.

## Dependencies for EdgeQuake Hosting

The Sealos template includes all required deployment components: EdgeQuake API, EdgeQuake frontend, PostgreSQL, pgvector, database initialization, service discovery, and HTTPS ingress.

### Deployment Dependencies

- [EdgeQuake GitHub Repository](https://github.com/raphaelmansuy/edgequake) - Source code and project documentation
- [Docker Quick Start](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/DOCKER_QUICK_START.md) - Upstream Docker deployment reference
- [EdgeQuake Issues](https://github.com/raphaelmansuy/edgequake/issues) - Bug reports and community discussion
- [Sealos App Store](https://sealos.io/products/app-store/edgequake) - EdgeQuake template page

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Web UI**: React/Next.js frontend exposed through the primary public URL.
- **API Service**: Rust EdgeQuake backend serving REST, health, ingestion, query, and graph endpoints on port `8080`.
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4.0 cluster with persistent `1Gi` storage.
- **Database Init Job**: Initializes the `edgequake` database, required extensions, and Apache AGE-compatible fallback graph views when needed.
- **Ingress Resources**: Public HTTPS routes for both the frontend and API endpoint.

**Configuration:**

The template exposes the following deployment parameters:

- `EDGEQUAKE_LLM_PROVIDER`: Select `openai`, `mistral`, `anthropic`, `gemini`, `ollama`, or `mock`.
- `OPENAI_API_KEY`: API key used when the OpenAI provider is selected.
- `OPENAI_BASE_URL`: Optional OpenAI-compatible base URL for compatible providers or proxies.
- `RUST_LOG`: Rust log filter for the API container.

The frontend receives the generated API URL at runtime, so the browser connects to the public Sealos API endpoint instead of a local development address.

**License Information:**

EdgeQuake is licensed under the [Apache License 2.0](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/LICENSE).

## Why Deploy EdgeQuake on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is well suited for AI applications, SaaS platforms, and multi-service architectures. By deploying EdgeQuake on Sealos, you get:

- **One-Click Deployment**: Deploy EdgeQuake without writing Kubernetes manifests or manually wiring services.
- **Managed Multi-Service Setup**: Run the API, frontend, database, initialization job, services, and ingresses as one template.
- **Persistent Storage Included**: Store PostgreSQL data on persistent volumes that survive restarts.
- **Instant Public Access**: Get HTTPS URLs for the Web UI and API endpoint automatically.
- **Easy Customization**: Configure provider, API key, base URL, logging, resources, and deployment settings from the Sealos UI.
- **Canvas + AI Ops**: After deployment, use the Canvas, AI dialog, and resource cards to inspect or modify resources.
- **Pay-as-You-Go Efficiency**: Start with compact resource defaults and scale only when your workload requires it.
- **Kubernetes Foundation**: Benefit from Kubernetes service discovery, health checks, rollout management, and workload isolation without operating Kubernetes directly.

Deploy EdgeQuake on Sealos and focus on building document intelligence workflows instead of managing infrastructure.

## Deployment Guide

1. Open the [EdgeQuake template](https://sealos.io/products/app-store/edgequake) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - Choose `EDGEQUAKE_LLM_PROVIDER`.
   - Set `OPENAI_API_KEY` when using OpenAI.
   - Optionally set `OPENAI_BASE_URL` for OpenAI-compatible gateways.
   - Keep `RUST_LOG` as `info` unless you need more verbose API logs.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your deployment through the generated URLs:
   - **Web UI**: Open the EdgeQuake app URL from the App resource.
   - **API Endpoint**: Use the generated API URL for REST access, health checks, SDK integration, and `/swagger-ui` if enabled by the application image.

## Configuration

After deployment, you can configure EdgeQuake through:

- **AI Dialog**: Describe changes such as updating environment variables, scaling replicas, or tuning resources.
- **Resource Cards**: Click the Deployment, Service, Ingress, Job, or PostgreSQL cards to inspect and modify settings.
- **Web UI**: Configure workspaces, upload documents, and interact with generated graphs from the browser.
- **API Endpoint**: Integrate external tools through the EdgeQuake REST API.

## Scaling

To scale EdgeQuake:

1. Open the Canvas for your deployment.
2. Click the API or Web UI Deployment resource card.
3. Adjust CPU, memory, or replica count according to your workload.
4. Apply the changes in the dialog and monitor rollout status.

For larger document ingestion workloads, scale the API first and monitor PostgreSQL usage. Keep database storage and backup needs in mind as document and graph data grow.

## Troubleshooting

### Common Issues

**The Web UI cannot connect to the API**
- Cause: The frontend must use the generated public API URL.
- Solution: Confirm the frontend Deployment has `EDGEQUAKE_API_URL` set to the API ingress URL and restart the frontend if you changed ingress settings.

**Graph queries fail because Apache AGE is unavailable**
- Cause: Some PostgreSQL environments may not provide the Apache AGE extension.
- Solution: This template installs fallback AGE-compatible views after EdgeQuake creates its base tables. If graph queries fail during first startup, wait for initialization to complete and check the `pgsql-init` Job logs.

**LLM requests fail**
- Cause: Missing or invalid provider credentials.
- Solution: Confirm `EDGEQUAKE_LLM_PROVIDER`, `OPENAI_API_KEY`, and `OPENAI_BASE_URL` match your provider setup.

### Getting Help

- [EdgeQuake GitHub Repository](https://github.com/raphaelmansuy/edgequake)
- [EdgeQuake Issues](https://github.com/raphaelmansuy/edgequake/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [EdgeQuake README](https://github.com/raphaelmansuy/edgequake)
- [Docker Quick Start](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/DOCKER_QUICK_START.md)
- [Apache AGE](https://age.apache.org/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Sealos](https://sealos.io)

## License

This Sealos template is provided under the repository license for Sealos templates. EdgeQuake itself is licensed under the [Apache License 2.0](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/LICENSE).
