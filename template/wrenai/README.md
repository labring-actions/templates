# Deploy and Host WrenAI on Sealos

WrenAI is an open-source GenBI agent that turns conversations with data into Text-to-SQL, charts, spreadsheets, reports, and BI insights. This template deploys the WrenAI `0.29.3` AI service, `0.24.6` engine, `0.25.0` Ibis server, `0.32.2` UI, Qdrant `v1.18.2`, and PostgreSQL on Sealos Cloud.

![WrenAI Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/wrenai/website-screenshot.webp)

## About Hosting WrenAI

The template runs the WrenAI runtime bundle as one Sealos application. The UI provides the public HTTPS entry, the AI service handles model and embedding calls, the Wren engine and Ibis server execute SQL, Qdrant stores embeddings, and PostgreSQL stores project and configuration data.

The AI service reads the generated configuration from a mounted ConfigMap. The deployment uses OpenAI models and requires separate keys for text generation and embeddings. All internal services use cluster DNS names, so the bundle stays self-contained inside the Sealos namespace.

## Common Use Cases

- **Natural-language analytics**: Let teams ask questions about a connected data source in plain language.
- **SQL acceleration**: Generate, explain, and correct SQL during analysis work.
- **Semantic modeling**: Index schemas and business descriptions for repeatable answers.
- **Self-hosted BI experiments**: Keep metadata and vector indexes in a Sealos workspace.

## Architecture and Dependencies

- **Wren UI `0.32.2`**: Browser application on port `3000`, published through the HTTPS Ingress and App entry.
- **Wren AI service `0.29.3`**: Model and embedding gateway on port `5555`.
- **Wren engine `0.24.6`**: SQL and semantic execution service on ports `8080` and `7432`, with a bootstrap init container.
- **Wren Ibis server `0.25.0`**: Ibis query service on port `8000`.
- **Qdrant `v1.18.2`**: Persistent vector store with storage, snapshots, and initialization volumes.
- **PostgreSQL `16.4.0`**: KubeBlocks-managed database for the `wrenai` application database.
- **PostgreSQL init Job**: Waits for the database and creates `wrenai` idempotently.

## Why Deploy WrenAI on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes. It brings the WrenAI services, managed PostgreSQL, persistent vector storage, TLS, and service discovery into one repeatable deployment.

- **One-click GenBI stack**: Provision UI, model gateway, SQL services, vector search, and PostgreSQL together.
- **Managed operations**: Use Canvas resource cards and the AI dialog for environment updates.
- **Persistent analytics state**: Keep schemas, embeddings, projects, and query metadata across restarts.
- **Pay-as-you-go resources**: Increase capacity for the services that handle larger datasets or query volume.

## Configuration

Provide both credentials in the deployment dialog:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `openai_api_key` | OpenAI key for WrenAI text generation. | Yes | None |
| `embedder_openai_api_key` | OpenAI key for `text-embedding-3-large`. | Yes | None |
| `openai_api_base` | OpenAI-compatible base URL for text generation. | No | `https://api.openai.com/v1` |
| `embedder_openai_api_base` | OpenAI-compatible base URL for embeddings. | No | `https://api.openai.com/v1` |
| `generation_model` | Default chat model name used by WrenAI. | No | `gpt-4.1-nano-2025-04-14` |

The template generates the application name, host, and user telemetry identifier. Keep API keys in Sealos-managed inputs and rotate them through the workload configuration when required.

## Deployment Guide

1. Open the [WrenAI template](https://sealos.io/products/app-store/wrenai) and click **Deploy Now**.
2. Enter `openai_api_key` and `embedder_openai_api_key` in the parameter dialog.
3. Keep the default API bases for the public OpenAI API, or set both API base inputs for an OpenAI-compatible provider. Set `generation_model` to a model supported by that provider.
4. Wait for PostgreSQL, the init Job, AI service, engine, Ibis server, Qdrant, and UI to become Ready. Typical Sealos deployments take 2-3 minutes; this runtime bundle can take longer while the database and vector store initialize. After deployment, Canvas exposes the AI dialog and resource cards for follow-up changes.
5. Open the generated URL from the Sealos App entry.
6. Complete WrenAI's first-run UI setup at `/setup/connection`, then add a data source or choose the built-in E-commerce sample.
7. WrenAI OSS opens this setup flow directly and has no email/password registration or login page in this template. Sealos App access and workspace permissions provide the access boundary.
8. After the sample data finishes indexing, open Modeling or Home and run a sample question. A working text-generation endpoint and a working embedding endpoint are both required for semantic indexing and question answering.

## Storage and Operations

Qdrant uses persistent volumes for vectors, snapshots, and its initialization marker. Wren engine uses a persistent `/app/data` volume for bootstrap data, and PostgreSQL uses a 1 GiB managed volume. Sealos is built on Kubernetes and uses pay-as-you-go resources. Expand the relevant Canvas resource card when datasets or query history grow, and use the Canvas AI dialog for environment changes.

WrenAI sends model and embedding requests to the configured OpenAI-compatible endpoints using the supplied keys. Review provider quotas and network egress policy before importing a large schema.

## Troubleshooting

### The UI loads but data queries fail

Check the AI service, engine, and Ibis server logs. Confirm both OpenAI keys are present and that the UI can reach the internal service DNS names.

### Vector indexing fails

Inspect Qdrant readiness and the AI service logs. Confirm the Qdrant storage and snapshots volumes are bound and that the embedding key has access to `text-embedding-3-large`.

### The question stays on "Understanding question"

Check the AI service logs for the provider response from the configured embedding endpoint. A `503` from `/embeddings` means the selected OpenAI-compatible provider does not expose the configured embedding model; switch to a provider and model that support embeddings, then restart the AI service configuration.

### PostgreSQL initialization is pending

Wait for the PostgreSQL Cluster to reach Ready and for the `wrenai-pg-init` Job to complete. The UI has a startup gate that waits for the `wrenai` database before accepting requests.

### Getting Help

- [WrenAI Documentation](https://docs.getwren.ai/)
- [WrenAI GitHub Issues](https://github.com/Canner/WrenAI/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Official Links

- [WrenAI website](https://getwren.ai/)
- [WrenAI source repository](https://github.com/Canner/WrenAI)

## Additional Resources

- [WrenAI OSS documentation](https://docs.getwren.ai/oss/introduction)
- [WrenAI deployment guide](https://docs.getwren.ai/oss/deployment)

## License

This Sealos template is provided under the templates repository license. WrenAI and its bundled components remain subject to their respective upstream licenses.
