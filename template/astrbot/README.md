# Deploy and Host AstrBot on Sealos

AstrBot is an AI agent assistant and chatbot framework with a WebUI, plugin marketplace, messaging platform adapters, and LLM integrations. This template deploys AstrBot as a persistent single-node service on Sealos Cloud.

![AstrBot Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/astrbot/website-screenshot.webp)

## About Hosting AstrBot

AstrBot runs a web management console on port 6185 and stores runtime data, plugins, provider settings, and bot configuration in persistent storage. The Sealos template provisions the container, persistent volume, service, HTTPS ingress, and dashboard App entry automatically.

The deployment follows the official Docker runtime model and pins `soulter/astrbot:v4.26.2`. AstrBot can connect to messaging platforms such as Telegram, Discord, QQ, Lark, DingTalk, WeCom, and OneBot-compatible gateways after you configure adapters in the WebUI.

## Common Use Cases

- **AI chatbot operations**: Run one bot framework for multiple messaging channels.
- **LLM provider orchestration**: Configure OpenAI-compatible, Gemini, Ollama, and other model providers from the WebUI.
- **Plugin-based automation**: Install AstrBot plugins for workflows, commands, search, sandboxing, and integrations.
- **Agent experimentation**: Test agent runners, MCP tools, and web search features in a hosted environment.

## Dependencies for AstrBot Hosting

The Sealos template includes AstrBot, persistent storage, public HTTPS access, and the optional OneBot WebSocket service inside the same workload.

### Deployment Dependencies

- [Official Website](https://astrbot.app) - Product homepage
- [Docker Deployment Guide](https://docs.astrbot.app/en/deploy/astrbot/docker.html) - Official Docker deployment documentation
- [GitHub Repository](https://github.com/AstrBotDevs/AstrBot) - Source code and releases
- [Docker Image](https://hub.docker.com/r/soulter/astrbot) - Official container image

### Implementation Details

**Architecture Components:**

- **AstrBot WebUI**: Browser-facing management console served on port 6185.
- **OneBot WebSocket port**: Internal service port 6199 for OneBot-compatible adapters.
- **Persistent storage**: Mounted at `/AstrBot/data` for plugins, settings, and runtime state.

**Configuration:**

- The App URL opens the AstrBot WebUI directly.
- The template keeps `/AstrBot/data` on a persistent volume so configuration survives restarts.
- Messaging adapters and model providers are configured after deployment inside the WebUI.

**License Information:**

AstrBot is licensed under the GNU Affero General Public License v3.0. This Sealos template is provided under the repository license.

## Why Deploy AstrBot on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying AstrBot on Sealos, you get:

- **One-Click Deployment**: Deploy AstrBot from the App Store without writing Kubernetes manifests.
- **Persistent Storage Included**: Keep AstrBot plugins, provider settings, and bot data across restarts.
- **Instant Public Access**: Get an HTTPS App URL for the WebUI automatically.
- **Easy Customization**: Adjust resources and environment variables from the Sealos Canvas.
- **Integrated Operations**: Monitor rollout state, logs, storage, and ingress from one dashboard.

## Deployment Guide

1. Open the [AstrBot template](https://sealos.io/products/app-store/astrbot) and click **Deploy Now**.
2. Confirm the deployment parameters in the popup dialog.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the AstrBot App URL from the Canvas.
5. Use the first-run WebUI flow shown by AstrBot. If the page asks for credentials, inspect the AstrBot workload logs in Sealos and use the generated initial login information printed by the application.

## Login and First-Run Guidance

AstrBot exposes its WebUI at the App URL. On first launch, complete the setup or login screen shown by AstrBot, then configure model providers, messaging adapters, and plugins from the console.

Keep the generated credentials in a password manager if AstrBot prints initial login information in the container logs. Rotate credentials from the WebUI after the first successful login.

## Configuration

After deployment, configure AstrBot through:

- **AstrBot WebUI**: Add LLM providers, messaging platforms, plugins, and bot behavior.
- **AI Dialog**: Describe desired resource or environment changes in Sealos.
- **Resource Cards**: Open the StatefulSet, Service, Ingress, or storage card for direct edits.

## Scaling

AstrBot stores state on a single persistent volume, so keep replicas at one unless you have validated an external state strategy. Increase CPU or memory from the StatefulSet card when plugin load or model-provider traffic grows.

## Troubleshooting

### WebUI does not show the login or setup page

- Cause: AstrBot may still be initializing plugins and runtime data.
- Solution: Wait for the StatefulSet to become ready, then inspect workload logs from the Sealos Canvas.

### Adapter cannot connect back to AstrBot

- Cause: Messaging platform callbacks or OneBot gateway settings may point to the wrong public URL or port.
- Solution: Use the HTTPS App URL for browser-facing callbacks and configure OneBot-compatible integrations with the documented AstrBot adapter settings.

## Additional Resources

- [AstrBot Documentation](https://docs.astrbot.app/en/what-is-astrbot.html)
- [Plugin Usage](https://docs.astrbot.app/en/use/plugin.html)
- [HTTP API](https://docs.astrbot.app/scalar.html)
- [Community](https://docs.astrbot.app/en/community.html)

## License

This Sealos template is provided under the repository license. AstrBot itself is licensed under the GNU Affero General Public License v3.0.
