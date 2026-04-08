# Deploy and Host Openclaw on Sealos

Openclaw is an AI agent gateway with multi-channel support including WhatsApp, Telegram, and Discord integration. This template deploys a production-ready Openclaw instance with persistent storage on Sealos Cloud.

This template is aligned with the current OpenClaw Docker gateway flow and pins the official `2026.3.28` container image.

## About Hosting Openclaw

Openclaw runs as a single-node AI agent gateway service that provides a unified interface for deploying and managing AI agents across multiple messaging platforms. The Sealos template automatically provisions persistent storage for your agent configurations, workspace data, and WhatsApp session files, ensuring your data is safely stored and survives restarts.

The gateway architecture allows you to connect OpenAI-compatible AI models (like Claude, GPT-4, etc.) to popular messaging platforms including Telegram, Discord, WhatsApp, and Slack. The deployment includes automatic SSL certificate provisioning, domain management, and integrated monitoring through the Sealos dashboard.

## Common Use Cases

- **Multi-Platform AI Assistant**: Deploy a single AI assistant across Telegram, Discord, WhatsApp, and Slack simultaneously
- **Customer Support Automation**: Build intelligent chatbots that handle customer inquiries across multiple channels
- **Team Collaboration**: Create AI-powered productivity bots for team communication platforms
- **Community Management**: Automate community moderation and engagement with AI agents
- **Personal AI Assistant**: Run your own personal AI assistant accessible from any messaging platform

## Dependencies for Openclaw Hosting

The Sealos template includes all required dependencies: runtime environment, persistent storage volumes for configuration and workspace data.

### Deployment Dependencies

- [Official Website](https://openclaw.ai/) - Official Openclaw website
- [GitHub Repository](https://github.com/openclaw/openclaw) - Source code and documentation
- [Getting Started Guide](https://openclaw.ai/) - Quick start guide and configuration instructions

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Openclaw Gateway**: Main AI agent gateway service running on port 18789
- **Persistent Storage**: A persistent volume is mounted at `/home/node/.openclaw`, which also contains the default workspace path `/home/node/.openclaw/workspace`

**Configuration:**

The Openclaw gateway is configured through environment variables and a configuration file generated during initialization:

- **Base URL**: OpenAI-compatible API endpoint (default: Sealos AI Proxy)
- **API Key**: Authentication key for your AI model provider
- **Model**: Default AI model to use (e.g., claude-opus-4-6)
- **Gateway Token**: Authentication token for accessing the gateway control UI
- **Channel Tokens**: Optional tokens for Discord, Telegram, WhatsApp, and Slack

The control UI is enabled by default and accessible through the gateway URL with a token fragment. The UI allows you to manage agents, configure channels, and monitor activity without modifying configuration files.

**Channel Support:**

- **Telegram**: Fully supported, enabled by default
- **Discord**: Add your Discord bot token to enable
- **WhatsApp**: Session data stored in persistent storage
- **Slack**: Configure with bot token and app token

**License Information:**

Openclaw is open-source software. Check the [GitHub repository](https://github.com/openclaw/openclaw) for specific licensing terms.

## Why Deploy Openclaw on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying Openclaw on Sealos, you get:

- **One-Click Deployment**: Deploy Openclaw with a single click. No YAML configuration, no container orchestration complexity - just point, click, and deploy.
- **Auto-Scaling Built-In**: Your AI agents automatically scale up and down based on demand. Handle traffic spikes from multiple messaging platforms without manual intervention.
- **Easy Customization**: Configure AI models, API keys, and channel connections with intuitive forms. Customize your setup without touching a single line of code.
- **Zero Kubernetes Expertise Required**: Get all the benefits of Kubernetes - high availability, service discovery, and container orchestration - without becoming a Kubernetes expert.
- **Persistent Storage Included**: Built-in persistent storage solutions ensure your agent configurations, workspace data, and WhatsApp sessions are safe and accessible across deployments and scaling events.
- **Instant Public Access**: Each deployment gets an automatic public URL with SSL certificates. Share your AI agent gateway instantly without complex networking setup.
- **Integrated AI Proxy**: Seamlessly connect to Sealos AI Proxy for easy access to Claude, GPT-4, and other OpenAI-compatible models.

Deploy Openclaw on Sealos and focus on building intelligent AI agents instead of managing infrastructure.

## Deployment Guide

1. Open the [OpenClaw template](https://sealos.io/products/app-store/openclaw) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **模型提供商类型**: Select `openai_compat` or `anthropic_compat`. The default is `openai_compat`, which matches the default `/v1` endpoint
   - **模型接口地址**: Compatible provider base URL (default: `https://aiproxy.usw-1.sealos.io/v1`)
   - **API密钥**: Provider API key
   - **登录令牌**: Control UI login token. The form defaults to `sealos2026`, but you can replace it with your own token.
   - **默认模型**: Default model ID (for example `claude-opus-4-6` or `gpt-5.2`)
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click resource cards to modify settings.
4. Access your application via the provided URLs:
   - **Control UI**: Open the generated URL from App resources (includes a `#token=...` fragment)
   - **Gateway Endpoint**: Use `https://<your-domain>/` as the OpenClaw gateway base endpoint

Security note: OpenClaw's Control UI is an admin surface. This template is designed for convenient self-hosting on a Sealos HTTPS domain, so keep the generated token private and rotate it if you ever suspect exposure.

## Configuration

After deployment, you can configure Openclaw through multiple methods:

### Control UI

Access the control UI at:
```
https://[your-app-url]/#token=[gateway-token]
```

The gateway token comes from the deployment form and is included in the App access URL shown on the Canvas App card after deployment. The form defaults to `sealos2026`, and the token is passed in the URL fragment so it is not sent to the server. The UI provides a web-based interface for:
- Managing AI agents
- Configuring messaging channels (Telegram, Discord, WhatsApp, Slack)
- Monitoring agent activity
- Adjusting model settings

### Environment Variables

Modify application settings after deployment through Canvas: use the AI dialog for intent-based changes, or open the StatefulSet resource card to edit environment variables directly:

- **DISCORD_BOT_TOKEN**: Your Discord bot token
- **TELEGRAM_BOT_TOKEN**: Your Telegram bot token
- **SLACK_BOT_TOKEN**: Your Slack bot token
- **SLACK_APP_TOKEN**: Your Slack app token (for socket mode)

### Channel Setup

Each messaging platform requires specific setup:

**Telegram:**
1. Create a bot via [@BotFather](https://t.me/botfather) on Telegram
2. Copy the bot token
3. Add the token to the TELEGRAM_BOT_TOKEN environment variable via Canvas resource card or via the control UI
4. Start a conversation with your bot

**Discord:**
1. Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a bot user and copy the token
3. Add the token to the DISCORD_BOT_TOKEN environment variable via Canvas resource card or via the control UI
4. Invite the bot to your server

**WhatsApp:**
1. WhatsApp session data is stored in persistent storage under `/home/node/.openclaw`
2. Follow the WhatsApp Web QR code authentication process through the control UI
3. Session data persists across container restarts

**Slack:**
1. Create a Slack app at [Slack API](https://api.slack.com/apps)
2. Enable bot scopes and install the app to your workspace
4. Add bot token and app token (for socket mode) via environment variables or control UI

## Scaling

To scale your Openclaw deployment:

1. Open the Canvas for your Openclaw deployment
2. Open the StatefulSet resource card
3. Adjust CPU/Memory resources:
   - Minimum: 100m CPU, 256Mi memory
   - Maximum: 1000m CPU, 2Gi memory
4. Increase replica count if needed (currently set to 1)
5. Apply the changes in the dialog

**Note:** Openclaw uses StatefulSet for deployment. For production use with high traffic, consider deploying multiple instances behind a load balancer.

## Troubleshooting

### Common Issues

**Issue: Agents not responding on messaging platforms**
- Cause: Missing or incorrect bot tokens for the platform
- Solution: Verify that the correct bot token is configured in environment variables or via the control UI

**Issue: AI model errors**
- Cause: Invalid API key, incorrect base URL, or model name
- Solution: Check that your API key is valid, the base URL is correct, and the model ID is supported by your provider

**Issue: WhatsApp session lost after restart**
- Cause: Session data not persisted properly
- Solution: The template includes persistent storage for WhatsApp sessions. Ensure the storage volume is mounted correctly

**Issue: Cannot access control UI**
- Cause: Incorrect gateway token or URL
- Solution: Use the App URL from the Canvas App card (it already includes the token fragment), or append `#token=[gateway-token]` to your gateway URL manually

### Getting Help

- [Official Documentation](https://openclaw.ai/)
- [GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Openclaw Website](https://openclaw.ai/) - Official website and documentation
- [GitHub Repository](https://github.com/openclaw/openclaw) - Source code, issues, and contributions
- [Sealos Documentation](https://sealos.io/docs) - Learn more about deploying applications on Sealos
- [AI Proxy Configuration](https://aiproxy.usw-1.sealos.io) - Sealos AI Proxy for accessing OpenAI-compatible models

## License

This Sealos template is provided under the same license as Openclaw. Please refer to the [Openclaw GitHub repository](https://github.com/openclaw/openclaw) for specific licensing terms.
