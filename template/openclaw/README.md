# Deploy Managed OpenClaw on Sealos (Updated: March 2026)

OpenClaw is a local-first AI Agent Gateway that unifies channels like WhatsApp, Telegram, Discord, and Slack. With the Sealos template, you can deploy a production-ready OpenClaw instance quickly, including persistent storage for configuration and workspace data.

## About Managed OpenClaw

OpenClaw runs as a single-node AI gateway service (default port `18789`) and provides a unified control plane for multi-channel AI agent operations.

The Sealos template provisions persistent storage for:

- Gateway config and tokens
- Workspace data
- Channel session data (for example, WhatsApp sessions)

This ensures your core state survives restarts and re-deployments.

## Latest Version Info (as of 2026-03-02)

- Latest stable OpenClaw release: `v2026.3.1` (released on 2026-03-02)
- New container/Kubernetes-friendly health endpoints:
  - `/health`
  - `/healthz`
  - `/ready`
  - `/readyz`

These endpoints make liveness/readiness probe configuration straightforward in Sealos/Kubernetes.

## Common Use Cases

- Cross-platform AI assistants (same agent on Telegram/Discord/WhatsApp/Slack)
- Multi-channel customer support automation
- Team productivity bots
- Community moderation and engagement automation
- Personal AI assistants accessible from messaging apps

## Dependencies and Components

The Sealos app template typically includes all runtime dependencies, with these core components:

- OpenClaw gateway service
- Persistent volumes for config and workspace
- Public access entry with managed TLS/domain capabilities

> Note: exact default resources and form fields may vary by Sealos cluster/template version. Always use current App Store form values as source of truth.

## Recommended Deployment Parameters

When deploying from Sealos App Store, verify these key settings:

- **Base URL**: OpenAI-compatible model endpoint
  - Example: `https://aiproxy.usw-1.sealos.io/v1`
- **API Key**: model provider key
- **Model**: default model ID supported by your provider
- **Gateway/Auth Token**: gateway access token (use a strong random value)
- Optional channel tokens:
  - `TELEGRAM_BOT_TOKEN`
  - `DISCORD_BOT_TOKEN`
  - `SLACK_BOT_TOKEN`
  - `SLACK_APP_TOKEN`

## Deployment Guide (Sealos)

1. Open [Sealos Cloud](https://cloud.sealos.run)
2. Go to App Store and search for **OpenClaw**
3. Click deploy and fill in model/auth settings
4. Wait for startup (usually a few minutes)
5. Open the generated public URL and sign in to the control UI

## Control UI and Security Best Practices

Legacy docs often use `/?token=...` for direct UI access.

Current best practice:

- Avoid keeping sensitive tokens in URLs
- Manage sessions in UI after first login
- Rotate gateway tokens regularly
- Apply least-privilege review for third-party skills

## Channel Setup

### Telegram

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Put token into `TELEGRAM_BOT_TOKEN`
3. Configure routing/session policy in control UI

### Discord

1. Create app/bot in [Discord Developer Portal](https://discord.com/developers/applications)
2. Set `DISCORD_BOT_TOKEN`
3. Invite bot to target server with required permissions

### Slack

1. Create app in [Slack API](https://api.slack.com/apps)
2. Configure bot token and app token
3. Set `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`

### WhatsApp

- Store session data on persistent volume
- Complete QR pairing flow from the control UI

## Scaling and Operations

- Scale CPU/memory and replicas by traffic
- Use `/healthz` and `/readyz` for probes
- Back up config/workspace/session data to object storage regularly
- Enable monitoring and alerting for gateway and channels

## Troubleshooting

- **Bot not responding on channels**: check channel tokens and permissions
- **Model invocation errors**: validate Base URL, API key, and model ID
- **Control UI inaccessible**: verify URL/token and ingress/TLS health
- **State lost after restart**: verify PVC binding and mount path

## References

- OpenClaw Website: <https://openclaw.ai>
- OpenClaw Docs: <https://docs.openclaw.ai>
- OpenClaw GitHub: <https://github.com/openclaw/openclaw>
- OpenClaw Releases: <https://github.com/openclaw/openclaw/releases>
- Sealos OpenClaw App Page: <https://sealos.io/products/app-store/openclaw/>
- Sealos Cloud: <https://cloud.sealos.run>
