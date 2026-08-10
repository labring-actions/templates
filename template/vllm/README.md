# Deploy and Host vLLM on Sealos

vLLM is an inference and serving engine for language models. This Sealos template runs the official CPU image with a compact instruction model, a persistent Hugging Face cache, and an OpenAI-compatible HTTPS API.

![vLLM Website](website-screenshot.webp)

## About Hosting vLLM

vLLM provides an OpenAI-compatible server for chat completions, text completions, model listing, health checks, and interactive API documentation. It is useful when teams want a familiar API surface for testing model-serving workflows on self-managed infrastructure.

This template serves `HuggingFaceTB/SmolLM2-135M-Instruct` as `smollm2-135m`. Sealos creates the StatefulSet, Service, Ingress, Hugging Face cache volume, and App entry so users can open `/docs` from the generated HTTPS URL.

## Common Use Cases

- **OpenAI-compatible model serving**: Test chat and completion clients against a self-hosted endpoint.
- **Agent backend prototyping**: Provide a small instruction model for agents and workflow tests.
- **Inference smoke testing**: Validate deployment, health, and request flow before moving to larger models.
- **CPU-only experimentation**: Run a compact model on a low-cost baseline profile.
- **Persistent model cache**: Keep Hugging Face snapshots across Pod restarts.

## Dependencies for vLLM Hosting

The template includes the runtime and Kubernetes resources required for the selected CPU model-serving profile.

### Deployment Dependencies

- [vLLM documentation](https://docs.vllm.ai) - Product and serving documentation
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) - API behavior and request formats
- [vLLM CPU installation guide](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/) - CPU runtime notes
- [SmolLM2 model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) - Default model information
- [vLLM source repository](https://github.com/vllm-project/vllm) - Source code and releases

### Implementation Details

**Configuration:**

- Uses `vllm/vllm-openai-cpu:v0.26.0`.
- Starts vLLM with `HuggingFaceTB/SmolLM2-135M-Instruct`.
- Publishes the OpenAI-compatible API on port `8000`.
- Opens the generated App URL at `/docs`.
- Stores Hugging Face model files in `/root/.cache/huggingface`.
- Mounts a `1Gi` `openebs-backup` persistent volume for the model cache.
- Sets `--served-model-name smollm2-135m`, `--max-model-len 512`, `--max-num-seqs 1`, and `--enforce-eager`.
- Uses `/health` for startup, readiness, and liveness probes.

**License Information:**

vLLM is available under the Apache License 2.0.

## Why Deploy vLLM on Sealos?

- **One-click serving stack**: Create the StatefulSet, Service, Ingress, cache volume, and App entry from one template.
- **Familiar API surface**: Use OpenAI-compatible chat, completion, and model-listing endpoints.
- **Persistent model cache**: Keep downloaded model snapshots across Pod restarts.
- **Visual operations**: Inspect logs, health, networking, and resource usage from Sealos Canvas.
- **Validated low-load baseline**: Start from a tested CPU profile and scale resources as latency requirements grow.

## Deployment Guide

1. Open the [vLLM template](https://sealos.io/products/app-store/vllm) and click **Deploy Now**.
2. Review the generated application name and hostname, then start the deployment.
3. Wait for the application resources to become Ready. Sealos typically creates the StatefulSet, Service, Ingress, App, and PVC in 2-3 minutes; vLLM then pulls the CPU image and model, and the validated low-CPU startup can take up to 10 minutes.
4. Open the generated App URL to view the interactive API documentation at `/docs`.
5. Use the generated hostname as the base URL for OpenAI-compatible clients.

The template downloads `HuggingFaceTB/SmolLM2-135M-Instruct` and serves it as `smollm2-135m`.

## Use the API

Set the generated HTTPS endpoint:

```bash
export VLLM_URL="https://<your-app>.usw-1.sealos.app"
```

Check service health and the served model:

```bash
curl "$VLLM_URL/health"
curl "$VLLM_URL/v1/models"
```

Create a chat completion:

```bash
curl "$VLLM_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2-135m",
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
    ],
    "max_tokens": 32,
    "temperature": 0
  }'
```

Create a text completion:

```bash
curl "$VLLM_URL/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2-135m",
    "prompt": "The capital of France is",
    "max_tokens": 16,
    "temperature": 0
  }'
```

## Default Resources

| Resource | Default |
| --- | --- |
| CPU limit | `100m` |
| Memory limit | `4096Mi` |
| Model cache | `1Gi` |
| CPU KV cache | `1Gi` |
| Maximum model length | `512` tokens |
| Maximum concurrent sequences | `1` |

This is the lowest Sealos CPU ladder tier. Live validation measured about 8.5 minutes for a cached cold start and about 55 seconds for an 8-token first completion at `100m`. Increase the CPU limit to `500m` or `1` for substantially lower startup and response latency, and keep the CPU request at 10% of the selected limit. The adjacent `2048Mi` memory tier produced an OOM termination, so `4096Mi` is the validated memory minimum for this model and 1Gi KV cache.

## Storage and Lifecycle

The StatefulSet mounts an `openebs-backup` volume at `/root/.cache/huggingface`. Model snapshots stay available across Pod restarts. Deleting the template instance and its PVC removes the cached model.

## Security

The public HTTPS endpoint reaches the vLLM OpenAI-compatible API directly. Treat the generated host as a sensitive inference endpoint and place an authenticated gateway, allowlist, or private network boundary in front of shared deployments.

## Troubleshooting

### The public URL returns 502 during deployment

vLLM still needs to pull the image, download the model, and load the CPU runtime. Keep the deployment running while the Pod remains inside its startup-probe window.

### `/v1/models` returns an empty or delayed response

Wait until the readiness probe passes and the model has finished loading. The default low-CPU profile favors low cost over fast startup.

### Completion requests are slow

Increase CPU to `500m`, `1`, or higher for faster token generation. Keep the CPU request at about 10% of the selected limit.

### The Pod exits with OOM

Use at least the validated `4096Mi` memory limit for the default model and 1Gi CPU KV cache. Larger models require a larger memory tier and model cache volume.

### Getting Help

- [vLLM documentation](https://docs.vllm.ai)
- [vLLM GitHub issues](https://github.com/vllm-project/vllm/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [vLLM website](https://vllm.ai)
- [CPU installation guide](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/)
- [Default model](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)
- [Source code](https://github.com/vllm-project/vllm)

## License

This template follows the upstream [Apache License 2.0](https://github.com/vllm-project/vllm/blob/main/LICENSE).
