# Deploy and Host CowAgent on Sealos

CowAgent is an open-source super AI assistant with a browser console, tools, skills, memory, knowledge management, scheduling, and multi-channel integrations. This template deploys CowAgent with persistent user data, a password-protected web console, and public HTTPS access on Sealos Cloud.

![CowAgent Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cowagent/website-screenshot.webp)

## About Hosting CowAgent

CowAgent runs as a single stateful web console service on port 9899. The Sealos template configures the Web channel, binds the console to `0.0.0.0`, stores runtime data under `/home/agent/cow`, and protects the public console with the deployment password.

The web console is the main entry point for chatting with the agent, configuring model providers, managing skills, browsing memory and knowledge, connecting channels, and inspecting logs.

## Common Use Cases

- **Personal AI Assistant**: Run a persistent AI assistant with browser access.
- **Skill-Based Automation**: Install and use reusable skills for files, tools, media, and workflows.
- **Knowledge and Memory Hub**: Maintain long-term memory and a personal knowledge base.
- **Multi-Channel Operations**: Connect Web, Telegram, Slack, Discord, WeChat, Feishu, DingTalk, and other supported channels.

## Dependencies for CowAgent Hosting

The Sealos template includes the CowAgent container image, persistent data storage, a ClusterIP service, HTTPS ingress, and the Sealos App link.

### Deployment Dependencies

- [Official Website](https://cowagent.ai/) - Product website
- [Documentation](https://docs.cowagent.ai/intro/index) - Official documentation
- [GitHub Repository](https://github.com/zhayujie/CowAgent) - Source code and releases
- [Skill Hub](https://skills.cowagent.ai/) - CowAgent skill marketplace

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **CowAgent Web Console**: Browser UI and API on port 9899.
- **Persistent Data Volume**: Stores config, logs, conversation data, memory, knowledge, browser profile data, and installed assets under `/home/agent/cow`.
- **Sealos Ingress**: Publishes the web console over HTTPS on your generated Sealos domain.

**Configuration:**

The template sets `CHANNEL_TYPE=web`, `WEB_HOST=0.0.0.0`, and `WEB_PASSWORD` from the deployment input. Model providers can be configured after login from the web console.

**License Information:**

CowAgent is licensed under the MIT License. This Sealos template is provided under the repository license for Sealos templates.

## Why Deploy CowAgent on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and ongoing operations. By deploying CowAgent on Sealos, you get:

- **One-Click Deployment**: Launch CowAgent from the App Store with a generated public console URL.
- **Persistent Agent Data**: Keep configuration, memory, knowledge, logs, and user data across restarts.
- **Password-Protected Access**: Use the deployment password to protect the public web console.
- **Canvas Operations**: Tune resources, inspect logs, and change runtime settings through Canvas, AI dialog, and resource cards.
- **Provider Flexibility**: Configure OpenAI-compatible, Claude, Gemini, DeepSeek, Qwen, and other providers in the console.
- **Pay-as-You-Go Hosting**: Start with a single persistent instance and scale resources when needed.

## Deployment Guide

1. Open the [CowAgent template](https://sealos.io/products/app-store/cowagent) and click **Deploy Now**.
2. Configure the web console password in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access CowAgent via the provided URL.
5. Enter the web console password from the deployment form.
6. Open **Model Management** in the console and configure at least one model provider before running chat or agent tasks.

## Login and Registration

CowAgent uses password login for the Web console. There is no separate registration step in this template.

Use the `web_password` value from the deployment form. After login, the session is stored in the browser cookie, and you can update the password later from the console configuration page.

## Configuration

After deployment, you can configure CowAgent through:

- **Web Console**: Configure models, channels, tools, skills, memory, knowledge, scheduled tasks, and logs.
- **Canvas Resource Cards**: Adjust CPU, memory, storage, or environment values.
- **AI Dialog**: Describe operational changes and let Sealos update the resources.

## Scaling

To scale CowAgent resources:

1. Open the Canvas for your deployment.
2. Click the CowAgent StatefulSet resource card.
3. Increase CPU or memory for heavier browser automation, tool execution, or multi-channel use.
4. Apply the change and monitor logs.

## Troubleshooting

### Login page rejects the password

- Cause: The entered value differs from the `web_password` deployment input.
- Solution: Check the deployment parameters or update `WEB_PASSWORD` from the Canvas resource card.

### Chat returns provider errors

- Cause: No model provider is configured, or the provider key/base URL is invalid.
- Solution: Log in to the console, open **Model Management**, and configure a valid provider.

### Browser automation is unstable

- Cause: Browser-based tools may need more memory for heavier tasks.
- Solution: Increase the CowAgent StatefulSet memory from the Canvas.

## Additional Resources

- [CowAgent Documentation](https://docs.cowagent.ai/intro/index)
- [Web Console Guide](https://docs.cowagent.ai/channels/web)
- [Skill Hub](https://skills.cowagent.ai/)
- [GitHub Releases](https://github.com/zhayujie/CowAgent/releases)

## License

This Sealos template is provided under the Sealos templates repository license. CowAgent itself is licensed under the MIT License.
