# Deploy and Host LLMIO on Sealos

LLMIO is a Go-based LLM gateway that puts weighted load balancing, protocol translation, usage analytics, and cost tracking in front of your upstream model providers. This template deploys the official LLMIO v0.9.4 image with its web console and persistent SQLite storage on Sealos Cloud.

![LLMIO console](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/llmio/website-screenshot.webp)

## About Hosting LLMIO

LLMIO is a single Go binary that serves both the gateway and its embedded React console from port 7070, so one public address covers the console and every API surface. Clients can speak OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, or Gemini native format; when the client protocol differs from the upstream protocol, LLMIO bridges OpenAI and Anthropic in both directions, streaming events included. Provider availability, quotas, and charges stay governed by each upstream's own terms.

Providers, models, and model-provider associations are configured in the console, and every association carries its own weight. Requests then distribute across the bound upstreams either by weighted lottery or by weight-ordered rotation. Each request is recorded with a trace ID, latency breakdown, TPS, token usage, and an optional cost figure, and the analytics views break that down by time range, provider, model, and API key.

The console is protected by the access token set at deploy time. The same token authenticates API calls with full model access, while narrower per-client keys — each with its own enable state, expiry, model allow-list, and IO-logging switch — are issued under **API Keys**.

Sealos provisions one application replica, a 1 GiB persistent volume, and a public HTTPS address. The SQLite database holding configuration, access keys, and request logs lives on that volume, so it survives Pod restarts.

## Common Use Cases

- **One address for many clients:** Point Claude Code, Codex, Gemini CLI, Cherry Studio, Open WebUI, and other tools at the same gateway.
- **Weighted routing and failover:** Spread traffic across several upstream accounts or providers and shift the weights without touching client configuration.
- **Cost and usage visibility:** Track token usage, cache hit rate, first-byte latency, and per-request cost per provider and per key.
- **Protocol translation:** Keep an Anthropic-protocol client on an OpenAI-protocol upstream, or the reverse, without changing the client.
- **Per-client credentials:** Issue separate keys with their own expiry and model allow-list instead of sharing one credential.

## Dependencies for LLMIO Hosting

The template includes the gateway binary, the embedded console, SQLite, and persistent storage. Upstream provider credentials are configured inside LLMIO after deployment.

### Deployment Dependencies

- [Source repository](https://github.com/atopos31/llmio)
- [Docker Compose deployment](https://github.com/atopos31/llmio/blob/v0.9.4/docker-compose.yml)
- [Environment variable reference](https://github.com/atopos31/llmio/blob/v0.9.4/README.md#environment-variables)
- [Support and issues](https://github.com/atopos31/llmio/issues)

### Implementation Details

**Architecture Components:**

- **Application:** One StatefulSet running `atopos31/llmio:0.9.4`, serving the console and all gateway endpoints on port 7070.
- **Storage:** One 1 GiB persistent volume mounted at `/app/db`, holding `llmio.db` and the quota configuration.
- **Networking:** A Service on port 7070 and Sealos Ingress with automatic HTTPS. The console and the API prefixes share that single address.

**Configuration:**

| Item | Template setting |
| --- | --- |
| Application replicas | 1 |
| Container limits / requests | 1000m CPU, 1024Mi memory / 100m CPU, 128Mi memory |
| Listening port | 7070, pinned with `LLMIO_SERVER_PORT` |
| Database path | `/app/db/llmio.db`, pinned with `LLMIO_DB_PATH` |
| Credential | `TOKEN`, taken from the deploy-time token input |
| Quota configuration | `/app/db/quota.config.json` |
| Probe path | `/`, the console shell |
| Ingress proxy timeouts | 300s read and send |
| Runtime identity | Image default (root), as in the upstream Docker Compose setup |

Keep one replica. SQLite is a single-writer database and the background log-compression and space-reclamation tasks assume a single process; raise CPU and memory instead of adding replicas.

Request and response bodies are stored in the log database, and new rows are compressed by default. A long-running gateway therefore grows the volume: raise the storage size at deploy time, set a retention window under **System Config**, or use the compression and space-reclamation controls there. Back up `llmio.db` from the volume if you need the history elsewhere.

Keep the token non-empty. LLMIO skips authentication entirely when `TOKEN` is unset, which would leave an internet-facing gateway open to anyone; the template generates a random token by default.

**License Information:** LLMIO is licensed under the MIT License.

## Why Deploy LLMIO on Sealos?

[Sealos](https://sealos.io) is built on Kubernetes and provides application management through Canvas, resource cards, and an AI dialog.

- **One-click deployment:** Provision the application, persistent storage, and HTTPS endpoint from one template.
- **Resource efficiency:** Pay-as-you-go resources start from a small single-replica configuration, sized for personal and small-team gateway traffic.
- **Persistent state:** Keep providers, models, API keys, and request logs across restarts.
- **Operational visibility:** Inspect logs and resource usage from the application's Canvas resource card.

## Deployment Guide

1. Open the [LLMIO template](https://sealos.io/products/app-store/llmio) and click **Deploy Now**.
2. Keep the generated access token or replace it, choose the storage size, and confirm. Provider credentials are added inside LLMIO after it starts.
3. Wait for deployment to finish, typically **1-2 minutes**. Sealos opens the Canvas; the application resource card provides logs, configuration, and the public HTTPS address.
4. Open the application address and log in with the access token. A fresh deployment starts with an empty console.
5. Open **Providers** and add each upstream — provider type, base URL, and API key — then open **Models** to create models and bind them to providers, giving every binding a weight.
6. Open **API Keys** and create a key for each client. Restrict a key to specific models or give it an expiry when it is meant for a single tool.
7. Open **Developer Quickstart** to select an API format, choose a model and key, and copy a ready-made request example, or use the base URLs below directly.

### Gateway Base URLs

| Client protocol | Base URL |
| --- | --- |
| OpenAI Chat Completions / Responses | `https://<your-app-address>/openai/v1` |
| OpenAI-compatible alias | `https://<your-app-address>/v1` |
| Anthropic Messages | `https://<your-app-address>/anthropic/v1` |
| Google Generative | `https://<your-app-address>/gemini/v1beta` |

Send the key as `Authorization: Bearer <key>` on the OpenAI-style prefixes, as `x-api-key: <key>` on `/anthropic` (a Bearer token is accepted there as well), and as `x-goog-api-key: <key>` on `/gemini`.

## Configuration and Scaling

Manage providers, models, weights, keys, and retention inside LLMIO. For infrastructure changes, open Canvas and describe the change in the AI dialog or edit the application resource card. Increase CPU and memory for heavier concurrent traffic while keeping the single application replica.

The gateway proxies long streaming responses, so the Ingress sets 300-second read and send timeouts. A single generation that streams for longer than that will be cut off; raise the timeouts on the Ingress if your workloads need it.

## Troubleshooting

**The console rejects the token:** Use the `TOKEN` value shown in the application resource card. If the value was changed after the Pod started, the Pod must restart to pick it up.

**A client gets 401 Invalid token:** Check where the key is sent — `Authorization: Bearer` for `/openai` and `/v1`, `x-api-key` for `/anthropic`, `x-goog-api-key` for `/gemini`. A key restricted to a model allow-list also rejects models outside that list, so use a full-access key while testing.

**Provider connectivity tests fail:** Test connectivity from the console's provider page. A wrong base URL, a revoked upstream key, or an upstream that is unreachable from the cluster all show up there first.

**A request fails with a protocol error:** Check the request log detail view. It shows the client protocol, the upstream protocol actually selected, and any field-level notes the bridge recorded.

**The volume fills up:** Request bodies dominate the log database. Lower the retention window, run the compression and space-reclamation actions under **System Config**, or grow the volume.

## License

This Sealos template is provided under the template repository's license. LLMIO itself is distributed under the [MIT License](https://github.com/atopos31/llmio/blob/v0.9.4/LICENSE).
