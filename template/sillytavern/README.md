# Deploy and Host SillyTavern on Sealos

SillyTavern is a feature-rich frontend for LLM roleplay, character chats, prompt management, extensions, and multiple AI provider integrations. This template deploys SillyTavern as a single persistent service on Sealos Cloud.

![SillyTavern Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/sillytavern/website-screenshot.webp)

## About Hosting SillyTavern

SillyTavern provides a browser UI for creating characters, configuring prompts, connecting AI APIs, managing chats, and installing extensions. It stores user data, configuration, plugins, and third-party extensions on persistent volumes.

This template uses the pinned `ghcr.io/sillytavern/sillytavern:1.18.0` release image, exposes port 8000 through Sealos HTTPS ingress, and enables Docker-style heartbeat health checks. Basic Auth is enabled by default so the public URL satisfies SillyTavern's remote access safety check.

## Common Use Cases

- **Character chat frontend**: Manage characters, lorebooks, and chat histories.
- **Multi-provider LLM UI**: Connect OpenAI-compatible, Anthropic, OpenRouter, Kobold, and other providers from the UI.
- **Prompt experimentation**: Tune prompts, presets, context templates, and generation settings.
- **Extension workspace**: Use third-party UI extensions and server plugins.

## Dependencies for SillyTavern Hosting

The Sealos template includes SillyTavern, persistent volumes for configuration and user data, public HTTPS ingress, and an App launcher entry.

### Deployment Dependencies

- [SillyTavern Documentation](https://docs.sillytavern.app/) - Official documentation
- [Docker Installation](https://docs.sillytavern.app/installation/docker/) - Container deployment reference
- [Configuration Guide](https://docs.sillytavern.app/administration/config-yaml/) - Runtime configuration
- [GitHub Repository](https://github.com/SillyTavern/SillyTavern) - Source code and releases

### Implementation Details

**Architecture Components:**

- **SillyTavern**: Main web UI and backend server.
- **Persistent Volumes**: Config, data, plugins, and third-party extension directories.
- **Ingress**: Public HTTPS access through Sealos.

**Configuration:**

- `SILLYTAVERN_LISTEN=true` allows the server to accept ingress traffic.
- `SILLYTAVERN_WHITELISTMODE=false` allows public access through the Sealos URL.
- `SILLYTAVERN_HEARTBEATINTERVAL=30` enables the built-in healthcheck mechanism.
- Basic Auth uses `basic_auth_username` and `basic_auth_password` from the deployment dialog.

**License Information:**

SillyTavern is distributed by the upstream project. Review the upstream repository for current license details.

## Why Deploy SillyTavern on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying SillyTavern on Sealos, you get:

- **One-Click Deployment**: Deploy SillyTavern, persistent storage, HTTPS ingress, and App launcher together.
- **Persistent User Data**: Keep characters, chats, settings, plugins, and extensions across restarts.
- **Easy Customization**: Change environment variables, resources, and storage through Canvas.
- **Instant Public Access**: Open SillyTavern from an HTTPS URL after deployment.
- **Zero Kubernetes Expertise Required**: Operate the containerized service from a simple UI.

Deploy SillyTavern on Sealos and focus on your LLM workspace.

## Deployment Guide

1. Open the [SillyTavern template](https://sealos.io/products/app-store/sillytavern) and click **Deploy Now**.
2. Keep Basic Auth enabled for public access, or configure another SillyTavern access-control mode before disabling it. The default username is `user`; the `basic_auth_password` field is prefilled with a generated password and can be replaced before deployment.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Open the SillyTavern App URL from Canvas and log in with `basic_auth_username` and `basic_auth_password`.
5. Start configuring AI provider API keys, characters, prompts, and extensions inside the SillyTavern UI.

## Configuration

After deployment, you can configure SillyTavern through:

- **AI Dialog**: Describe resource, auth, or environment changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, Service, Ingress, or storage cards to modify settings.
- **SillyTavern UI**: Configure AI providers, presets, characters, extensions, and chat settings.
- **Persistent Config Volume**: Advanced configuration is stored under `/home/node/app/config`.

## Scaling

SillyTavern is stateful and stores active user data on local persistent volumes. Keep one replica for the default template. The template uses 512 MiB memory because first boot compiles frontend libraries and initializes default user content. Increase CPU and memory if large context windows, heavy extensions, or many simultaneous users require more capacity.

## Troubleshooting

### The App Opens but Shows an Access Error

- Cause: Basic Auth credentials are required, or whitelist-related settings were changed.
- Solution: Use the configured `basic_auth_username` and `basic_auth_password`, and confirm `SILLYTAVERN_WHITELISTMODE=false`.

### Health Check Fails

- Cause: The heartbeat file is missing or the server did not start.
- Solution: Check container logs and confirm `SILLYTAVERN_HEARTBEATINTERVAL=30`.

### Data Is Missing After Restart

- Cause: Data was written outside the persistent directories.
- Solution: Store config, characters, chats, plugins, and extensions under the mounted SillyTavern directories.

## Additional Resources

- [SillyTavern Docker Guide](https://docs.sillytavern.app/installation/docker/)
- [SillyTavern Configuration](https://docs.sillytavern.app/administration/config-yaml/)
- [SillyTavern Extensions](https://docs.sillytavern.app/extensions/)
- [Sealos Documentation](https://sealos.io/docs)

## License

Review the [upstream repository](https://github.com/SillyTavern/SillyTavern) for the current SillyTavern license and usage terms.
