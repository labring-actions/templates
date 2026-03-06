# Deploy and Host Openclaw on Sealos

Openclaw is an AI agent gateway with multi-channel support including WhatsApp, Telegram, and Discord integration. This template deploys a production-ready Openclaw instance with persistent storage on Sealos Cloud.

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

- [Official Website](https://clawd.bot) - Official Openclaw website
- [GitHub Repository](https://github.com/moltbot/moltbot) - Source code and documentation
- [Getting Started Guide](https://clawd.bot) - Quick start guide and configuration instructions

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Openclaw Gateway**: Main AI agent gateway service running on port 18789
- **Persistent Storage**: Two persistent volumes are automatically provisioned:
  - Configuration storage (1Gi): Stores agent configurations, model settings, and channel credentials
  - Workspace storage (1Gi): Stores agent workspace data and generated files

**Configuration:**

The Openclaw gateway is configured through environment variables and a configuration file generated during initialization:

- **Base URL**: OpenAI-compatible API endpoint (default: Sealos AI Proxy)
- **API Key**: Authentication key for your AI model provider
- **Model**: Default AI model to use (e.g., claude-opus-4-5-20251101)
- **Gateway Token**: Authentication token for accessing the gateway control UI
- **Channel Tokens**: Optional tokens for Discord, Telegram, WhatsApp, and Slack

The control UI is enabled by default and accessible through the gateway URL with the gateway token parameter. The UI allows you to manage agents, configure channels, and monitor activity without modifying configuration files.

**Channel Support:**

- **Telegram**: Fully supported, enabled by default
- **Discord**: Add your Discord bot token to enable
- **WhatsApp**: Session data stored in persistent storage
- **Slack**: Configure with bot token and app token

**License Information:**

Openclaw is open-source software. Check the [GitHub repository](https://github.com/moltbot/moltbot) for specific licensing terms.

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

1. Visit [Sealos Cloud](https://os.sealos.io)
2. Click on "App Store" in the desktop
3. Search for "Openclaw" in the App Store
4. Click "Deploy App" and configure the following parameters:
   - **Base URL**: Your OpenAI-compatible API endpoint (default: https://aiproxy.usw-1.sealos.io/v1)
   - **API Key**: Your API key for the AI model provider
   - **Model**: The default model ID to use (e.g., claude-opus-4-5-20251101)
   - **Auth Token**: JWT secret key for gateway authentication (auto-generated by default)
5. Wait for deployment to complete (typically 1-3 minutes)
6. Access your Openclaw gateway via the provided URL

## Configuration

After deployment, you can configure Openclaw through multiple methods:

### Control UI

Access the control UI at:
```
https://[your-app-url]/?token=[gateway-token]
```

The gateway token is automatically generated and displayed in the App Launchpad after deployment. The UI provides a web-based interface for:
- Managing AI agents
- Configuring messaging channels (Telegram, Discord, WhatsApp, Slack)
- Monitoring agent activity
- Adjusting model settings

### Environment Variables

Modify application settings in the App Launchpad by updating the deployment:

- **DISCORD_BOT_TOKEN**: Your Discord bot token
- **TELEGRAM_BOT_TOKEN**: Your Telegram bot token
- **SLACK_BOT_TOKEN**: Your Slack bot token
- **SLACK_APP_TOKEN**: Your Slack app token (for socket mode)

### Channel Setup

Each messaging platform requires specific setup:

**Telegram:**
1. Create a bot via [@BotFather](https://t.me/botfather) on Telegram
2. Copy the bot token
3. Add the token to the TELEGRAM_BOT_TOKEN environment variable or via the control UI
4. Start a conversation with your bot

**Discord:**
1. Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a bot user and copy the token
3. Add the token to the DISCORD_BOT_TOKEN environment variable or via the control UI
4. Invite the bot to your server

**WhatsApp:**
1. WhatsApp session data is stored in persistent storage at `/home/openclaw/.openclaw/whatsapp`
2. Follow the WhatsApp Web QR code authentication process through the control UI
3. Session data persists across container restarts

**Slack:**
1. Create a Slack app at [Slack API](https://api.slack.com/apps)
2. Enable bot scopes and install the app to your workspace
4. Add bot token and app token (for socket mode) via environment variables or control UI

## Scaling

To scale your Openclaw deployment:

1. Open App Launchpad
2. Select your Openclaw deployment
3. Adjust CPU/Memory resources:
   - Minimum: 100m CPU, 204Mi memory
   - Maximum: 1000m CPU, 2Gi memory
4. Increase replica count if needed (currently set to 1)
5. Click "Update" to apply changes

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
- Solution: Copy the gateway token from the App Launchpad and access the URL with `?token=[gateway-token]` parameter

### Getting Help

- [Official Documentation](https://clawd.bot)
- [GitHub Issues](https://github.com/moltbot/moltbot/issues)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [Openclaw Website](https://clawd.bot) - Official website and documentation
- [GitHub Repository](https://github.com/moltbot/moltbot) - Source code, issues, and contributions
- [Sealos Documentation](https://sealos.io/docs) - Learn more about deploying applications on Sealos
- [AI Proxy Configuration](https://aiproxy.usw-1.sealos.io) - Sealos AI Proxy for accessing OpenAI-compatible models

## License

This Sealos template is provided under the same license as Openclaw. Please refer to the [Openclaw GitHub repository](https://github.com/moltbot/moltbot) for specific licensing terms.
