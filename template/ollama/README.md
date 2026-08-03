# Ollama

Ollama runs open models behind a REST API and an OpenAI-compatible API. This Sealos template deploys the official CPU image with persistent model storage and a public HTTPS endpoint.

![Ollama website](website-screenshot.webp)

## Features

- Official `ollama/ollama:0.32.5` image
- Native Ollama API and OpenAI-compatible endpoints
- Persistent model storage at `/root/.ollama`
- Health checks through `/api/version`
- CPU-only default deployment

## Deploy on Sealos

1. Open the [Ollama template](https://sealos.io/products/app-store/ollama).
2. Click **Deploy Now**.
3. Wait for the StatefulSet to become Ready. The first image pull can take several minutes.
4. Open the generated App URL or copy it from the Sealos application details.

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

OpenAI-compatible clients can use `$OLLAMA_URL/v1` as their base URL. See the [Ollama API documentation](https://docs.ollama.com/api/introduction) for the complete endpoint reference.

## Default resources

| Resource | Default |
| --- | --- |
| CPU limit | `500m` |
| Memory limit | `512Mi` |
| Model storage | `1Gi` |
| Replicas | `1` |

The defaults were validated on Sealos with `smollm2:135m`, whose stored model is about 271 MB. Larger models need enough memory for their weights and working buffers, plus a larger persistent volume when their files exceed the available model storage.

## Persistence

The StatefulSet stores downloaded models and metadata in the `openebs-backup` volume mounted at `/root/.ollama`. Redeploying the Pod keeps this data. Deleting the template instance and its PVC removes the stored models.

## Access control

Ollama serves its local API without built-in authentication. The Sealos Ingress publishes the generated HTTPS endpoint to the internet. Treat the URL as sensitive and add an authenticated gateway or network access policy before sharing it with untrusted clients.

## Links

- [Ollama website](https://ollama.com)
- [Ollama documentation](https://docs.ollama.com)
- [Source code](https://github.com/ollama/ollama)
- [MIT License](https://github.com/ollama/ollama/blob/main/LICENSE)
