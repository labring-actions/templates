# Deploy and Host Odysseus on Sealos

Odysseus is a self-hosted AI workspace with chat, deep research, memory, tools, calendar, notes, and document workflows. This template deploys Odysseus with Chroma and SearXNG side services on Sealos Cloud.

![Odysseus Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odysseus/website-screenshot.webp)

## About Hosting Odysseus

Odysseus runs as a web application backed by local SQLite data, persistent file storage, Chroma vector memory, and SearXNG search. The template provisions separate StatefulSets for Odysseus, Chroma, and SearXNG, plus persistent volumes for application data, logs, SSH state, Hugging Face cache, local cache, Chroma data, and SearXNG cache.

The template creates an initial admin user from the deployment form. Optional OpenAI API key support is included for cloud model access, and local model endpoints can be configured later in the Odysseus settings UI.

## Common Use Cases

- **Self-hosted AI workspace**: Chat, tools, notes, documents, and calendar in one interface.
- **Deep research**: Run multi-step research flows with search and synthesis.
- **Persistent memory**: Store and retrieve knowledge with Chroma-backed vector memory.
- **Private productivity hub**: Keep workspace artifacts in your own Sealos deployment.

## Dependencies for Odysseus Hosting

The Sealos template includes the Odysseus app image, Chroma vector database, SearXNG search service, persistent storage, and public HTTPS ingress.

### Deployment Dependencies

- [GitHub Repository](https://github.com/pewdiepie-archdaemon/odysseus) - Source code
- [Chroma](https://www.trychroma.com/) - Vector memory service
- [SearXNG](https://docs.searxng.org/) - Search service

## Implementation Details

**Architecture Components:**

- **Odysseus**: Main web UI and API server.
- **Chroma**: Vector memory service on the internal cluster network.
- **SearXNG**: Internal metasearch service for web research.
- **Persistent Storage**: Volumes for data, logs, SSH state, Hugging Face cache, local cache, Chroma data, and SearXNG cache.

**Configuration:**

- `admin_user` and `admin_password` create the initial admin account.
- `openai_api_key` is optional.
- SQLite is stored under `/app/data` through the upstream `ODYSSEUS_DATA_DIR` setting.

**License Information:**

Odysseus is licensed under AGPL-3.0-or-later.

## Why Deploy Odysseus on Sealos?

Sealos provides automatic HTTPS, persistent storage, internal service discovery, and one-click deployment for Odysseus plus its required Chroma and SearXNG services.

## Deployment Guide

1. Open the [Odysseus template](https://sealos.io/products/app-store/odysseus) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. Set the initial admin username and password.
3. Wait for deployment to complete, typically 3-5 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated application URL and log in with the configured admin credentials.

## Configuration

After login, configure model providers, local model endpoints, search settings, memory, and workspace tools from the Odysseus UI. Use the Sealos Canvas resource cards to adjust storage and resource limits.

## Additional Resources

- [Odysseus GitHub](https://github.com/pewdiepie-archdaemon/odysseus)
- [GitHub Issues](https://github.com/pewdiepie-archdaemon/odysseus/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This template follows the upstream Odysseus AGPL-3.0-or-later License.
