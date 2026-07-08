# Deploy and Host OpenClaw on Sealos

OpenClaw is an AI agent gateway for browser-based agent control and chat-channel automation. This template deploys OpenClaw as a single StatefulSet with persistent state on Sealos Cloud.

![OpenClaw Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openclaw/website-screenshot.webp)

## About Hosting OpenClaw

OpenClaw runs a Gateway and Control UI on port `18789`. The Gateway manages agent configuration, model provider access, device pairing, and workspace files for browser-driven agent workflows.

This Sealos template follows the official Docker and Kubernetes runtime model: one OpenClaw container, Gateway token authentication, `/healthz` and `/readyz` probes, and PVC-backed local state. The deployment stores OpenClaw config, workspace data, browser pairing profiles, and package cache across restarts.

## Common Use Cases

- **Personal AI Operator**: Run a browser-based assistant that can use your configured model provider.
- **Team Agent Console**: Host a shared Control UI for agent setup, testing, and operational review.
- **Chat-Channel Automation**: Connect agents to messaging channels after creating the required platform tokens.
- **Workflow Prototyping**: Keep agent workspace files and instructions persistent while iterating on tasks.

## Dependencies for OpenClaw Hosting

The template includes the OpenClaw Gateway image and persistent volumes. You provide a compatible model endpoint, API key, and default model id at deployment time.

### Deployment Dependencies

- [Official Website](https://openclaw.ai/) - Product website
- [Docker Installation](https://docs.openclaw.ai/install/docker) - Official container runtime guide
- [Kubernetes Installation](https://docs.openclaw.ai/install/kubernetes) - Official Kubernetes topology
- [Control UI Guide](https://docs.openclaw.ai/web/control-ui) - Browser access, token, and device pairing
- [Security Guide](https://docs.openclaw.ai/gateway/security) - Token and remote origin guidance

### Implementation Details

**Architecture Components:**

This template deploys one OpenClaw Gateway service:

- **OpenClaw Gateway**: Serves the Control UI, WebSocket Gateway, and health endpoints on port `18789`.
- **State PVC**: Mounts `/home/node/.openclaw` for `openclaw.json`, workspace files, and agent state.
- **Profile PVC**: Mounts `/home/node/.config/openclaw` for browser device pairing profile data.
- **NPM Cache PVC**: Mounts `/home/node/.npm` for package cache used by OpenClaw extensions.

**Configuration:**

At first boot, the template writes `openclaw.json` with:

- Gateway token authentication enabled
- Gateway bind mode set for Sealos ingress access
- Control UI origin restricted to your generated Sealos HTTPS URL
- A default model provider built from `provider_kind`, `base_url`, `api_key`, and `model`
- A default agent workspace at `~/.openclaw/workspace`

Persistence is PVC-backed local state, matching the official Docker and Kubernetes deployment guides.

**License Information:**

OpenClaw is licensed under the MIT License. This Sealos template is provided under the same license terms as the templates repository.

## Why Deploy OpenClaw on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes. By deploying OpenClaw on Sealos, you get:

- **One-Click Deployment**: Open the template page, enter the model provider values, and deploy.
- **Managed HTTPS Access**: Sealos creates the public URL and TLS certificate for the Gateway.
- **Persistent Agent State**: PVCs keep workspace, configuration, profile, and cache data across restarts.
- **Resource Controls**: The template uses the OpenClaw-recommended 2 GB memory class on the Sealos resource ladder.
- **Canvas Operations**: Adjust environment variables, resources, and replica settings from the Sealos Canvas after deployment.

## Deployment Guide

1. Open the [OpenClaw template](https://sealos.io/products/app-store/openclaw) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **provider_kind**: Select `openai_compat` or `anthropic_compat`.
   - **base_url**: Enter the provider base URL, such as an OpenAI-compatible `/v1` endpoint.
   - **api_key**: Enter the provider API key.
   - **model**: Enter the model id, such as `claude-opus-4-6` or `gpt-5.2`.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, Sealos redirects you to the Canvas. For later changes, describe your request in the AI dialog or open the relevant resource card.
4. Open the **OpenClaw** App card URL. The URL includes the generated Gateway token as a fragment.
5. Complete first-device pairing when the Control UI asks for approval:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Run those commands from the OpenClaw container terminal in Canvas. After approval, refresh the Control UI and continue setup.

## Initial Setup and Login

The App URL includes `#token=<gateway-token>`, which lets the Control UI authenticate against the Gateway. Browser device pairing protects remote access: approve the first browser once, then the profile PVC keeps that pairing data across restarts.

After opening the Control UI:

1. Confirm that the default provider and model are listed in model settings.
2. Open the default assistant workspace and send a short prompt.
3. Add messaging-channel credentials from the Control UI or by editing environment variables on the StatefulSet resource card.

## Configuration

You can update OpenClaw after deployment through:

- **Control UI**: Manage agents, model providers, workspace files, and channel setup.
- **Canvas AI Dialog**: Describe configuration changes and let Sealos apply them.
- **StatefulSet Resource Card**: Edit provider values, API keys, and resource limits.

For provider changes, keep the provider protocol aligned with the base URL:

- `openai_compat` for OpenAI-compatible chat-completions endpoints
- `anthropic_compat` for Anthropic Messages-compatible endpoints

## Scaling

OpenClaw keeps local state in PVCs, so the template runs one replica. To adjust resources:

1. Open the Canvas for your OpenClaw deployment.
2. Open the StatefulSet resource card.
3. Adjust CPU or memory using the Sealos resource controls.
4. Apply the update and wait for the Pod to become Ready.

The template starts with `1` CPU and `2G` memory because the official deployment guidance recommends the 2 GB memory class for reliable operation.

## Troubleshooting

### Control UI Shows a Pairing Screen

Open the OpenClaw container terminal from Canvas, run `openclaw devices list`, then approve the shown request id with `openclaw devices approve <requestId>`.

### Model Calls Fail

Confirm that `provider_kind`, `base_url`, `api_key`, and `model` match your provider. For OpenAI-compatible providers, the base URL usually ends with `/v1`.

### Gateway Health Fails

Open the StatefulSet logs and check that the Gateway is listening on port `18789`. The probes call `/healthz` and `/readyz`, matching the official container healthcheck.

## Additional Resources

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the templates repository license. OpenClaw is licensed under the MIT License.
