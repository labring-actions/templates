# Deploy and Host OmniRoute on Sealos

OmniRoute is a self-hosted OpenAI-compatible AI gateway with model routing, provider fallback, API keys, and an administration dashboard.

![OmniRoute dashboard](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/omniroute/website-screenshot.webp)

## About Hosting OmniRoute

This template runs OmniRoute as a StatefulSet with a 1 GiB persistent volume for `/app/data` and a dedicated KubeBlocks Redis Cluster for runtime state. The dashboard password is supplied during deployment, and gateway requests require an API key.

Open the public URL and sign in with the initial password. From the dashboard, add provider credentials, define model routes and fallbacks, and create API keys for clients. The OpenAI-compatible endpoint is served from the same host.

## Architecture Components

- **OmniRoute StatefulSet**: runs the dashboard, routing engine, and OpenAI-compatible API.
- **KubeBlocks Redis Cluster**: provides a one-replica Redis service for runtime state and caching.
- **Persistent volume**: stores OmniRoute configuration, provider metadata, and API keys.
- **Service and Ingress**: publish the dashboard and API over public HTTPS.

## Common Use Cases

- Put one OpenAI-compatible endpoint in front of multiple model providers.
- Route requests by model, cost, or availability with automatic fallback.
- Centralize provider credentials and issue scoped API keys to applications.
- Track usage across assistants, agents, and internal tools.
- Prototype multi-provider AI routing before production rollout.

## Dependencies for OmniRoute Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A KubeBlocks Redis Cluster provisioned by this template.
- At least one upstream AI provider account and API key.
- An initial dashboard password supplied through the template input.
- Outbound HTTPS access to the configured model providers.

## Why Deploy OmniRoute on Sealos?

- One-click deployment of the gateway and its Redis dependency.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent storage for routes, provider settings, and API keys.
- Pay-as-you-go resource cards sized for gateway workloads.
- Canvas view for the StatefulSet, Redis Cluster, Services, and Ingress.
- AI dialog for deployment guidance in the Sealos desktop.

## Deployment Guide

1. Open the [OmniRoute template](https://sealos.io/products/app-store/omniroute) and click **Deploy Now**.
2. Enter the initial dashboard password, keep the generated application name, and confirm the resource plan.
3. Wait 2-3 minutes for the StatefulSet and Redis Cluster to become ready, then open the public URL from the App card.
4. Sign in with the password from step 2, add a provider credential, and create an API key.
5. Send a test chat completion to the OpenAI-compatible endpoint with that key, then open Canvas to review all resources.

## License

OmniRoute is released under the [MIT License](https://github.com/cheaper-inference/OmniRoute/blob/main/LICENSE).
