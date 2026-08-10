# Deploy and Host Ollama on Sealos

Ollama runs open models behind a native REST API and an OpenAI-compatible API. This Sealos template deploys the official CPU image with persistent model storage and a generated HTTPS endpoint.

![Ollama Website](website-screenshot.webp)

## About Hosting Ollama

Ollama packages model downloads, runtime management, and generation APIs into one service. Teams can pull models from the Ollama library, keep them on a persistent volume, and call the same endpoint from internal tools, agents, notebooks, or OpenAI-compatible clients.

This template runs `ollama/ollama:0.32.5` as a single StatefulSet. Sealos creates the Service, Ingress, persistent model volume, and App entry so the API is reachable from the generated HTTPS URL.

## Common Use Cases

- **Local model APIs**: Serve compact open models through a private API endpoint.
- **OpenAI-compatible testing**: Point compatible SDKs at the generated `/v1` base URL.
- **Agent backends**: Provide text-generation capabilities to tools and workflows running on Sealos.
- **Model evaluation**: Pull small models, compare responses, and keep model files across Pod restarts.
- **Prototype deployments**: Start with a CPU-only profile before sizing larger model-serving infrastructure.

## Dependencies for Ollama Hosting

The template includes the Kubernetes resources needed to run the Ollama API on Sealos.

### Deployment Dependencies

- [Ollama documentation](https://docs.ollama.com) - Product and runtime documentation
- [Ollama API documentation](https://docs.ollama.com/api/introduction) - Native REST API reference
- [Ollama model library](https://ollama.com/library) - Available model names and tags
- [Ollama source repository](https://github.com/ollama/ollama) - Source code and release history

### Implementation Details

**Configuration:**

- Uses the official `ollama/ollama:0.32.5` image.
- Exposes port `11434` through a Sealos-managed HTTPS Ingress.
- Stores downloaded models and metadata in `/root/.ollama`.
- Mounts a `1Gi` `openebs-backup` persistent volume for the model store.
- Uses `/api/version` for startup, readiness, and liveness probes.
- Starts with an empty model store so users can choose the model that fits their workload.

**License Information:**

Ollama is available under the MIT License.

## Why Deploy Ollama on Sealos?

- **One-click API endpoint**: Create the StatefulSet, Service, Ingress, PVC, and App entry from one template.
- **Persistent model cache**: Keep downloaded models on durable storage across Pod restarts.
- **OpenAI-compatible access**: Reuse clients that support an OpenAI-compatible base URL.
- **Simple operations**: Inspect logs, resource usage, health checks, and networking from Sealos Canvas.
- **CPU-friendly baseline**: Begin with a compact validated profile and scale resources when models require more capacity.

## Deployment Guide

1. Open the [Ollama template](https://sealos.io/products/app-store/ollama) and click **Deploy Now**.
2. Review the generated application name and hostname, then start the deployment.
3. Wait for the application resources to become Ready. Sealos typically creates the StatefulSet, Service, Ingress, App, and PVC in 2-3 minutes; the first Ollama image pull can add a few minutes.
4. Open the generated App URL or copy it from the Sealos application details.
5. Pull a model through the API before sending the first generation request.

The App URL points to the Ollama API. A browser request to `/` returns `Ollama is running`.

## Use the API

Set the generated HTTPS endpoint:

```bash
export OLLAMA_URL="https://<your-app>.usw-1.sealos.app"
```

Check the deployed version and available models:

```bash
curl "$OLLAMA_URL/api/version"
curl "$OLLAMA_URL/api/tags"
```

Pull the compact model used for template validation:

```bash
curl "$OLLAMA_URL/api/pull" \
  -H "Content-Type: application/json" \
  -d '{"model":"smollm2:135m","stream":false}'
```

Generate a response:

```bash
curl "$OLLAMA_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2:135m",
    "prompt": "What is 2 + 2?",
    "stream": false
  }'
```

OpenAI-compatible clients can use `$OLLAMA_URL/v1` as their base URL.

## Default Resources

| Resource | Default |
| --- | --- |
| CPU limit | `500m` |
| Memory limit | `512Mi` |
| Model storage | `1Gi` |
| Replicas | `1` |

The defaults were validated on Sealos with `smollm2:135m`, whose stored model is about 271 MB. Larger models need enough memory for their weights and working buffers, plus a larger persistent volume when their files exceed the available model storage.

## Storage and Lifecycle

The StatefulSet stores downloaded models and metadata in the `openebs-backup` volume mounted at `/root/.ollama`. Pod replacements keep this data available. Deleting the template instance and its PVC removes the stored models.

## Security

The public HTTPS endpoint reaches the Ollama API directly. Treat the generated host as a sensitive service endpoint and place an authenticated gateway, allowlist, or private network boundary in front of shared deployments.

## Troubleshooting

### The App URL only returns `Ollama is running`

That response means the API process is available. Pull a model through `/api/pull`, then call `/api/generate` or the OpenAI-compatible `/v1` endpoints.

### Model pull is slow

Large model files take longer to download and write to the persistent volume. Start with compact models such as `smollm2:135m`, then increase storage and memory before pulling larger models.

### Generation fails after pulling a larger model

Increase memory for the StatefulSet. Model weights and runtime buffers must fit inside the selected memory limit.

### Getting Help

- [Ollama documentation](https://docs.ollama.com)
- [Ollama API documentation](https://docs.ollama.com/api/introduction)
- [Ollama GitHub issues](https://github.com/ollama/ollama/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Ollama website](https://ollama.com)
- [Ollama model library](https://ollama.com/library)
- [Source code](https://github.com/ollama/ollama)

## License

This template follows the upstream [MIT License](https://github.com/ollama/ollama/blob/main/LICENSE).
