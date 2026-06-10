# Deploy and Host OpenHands on Sealos

OpenHands is an AI software development agent web application. This template deploys the OpenHands web UI on Sealos Cloud with persistent workspace and state storage.

![OpenHands Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openhands/website-screenshot.webp)

## About Hosting OpenHands

OpenHands runs as a web application on port `3000` and stores workspace data under `/workspace` and application state under `/root/.openhands-state`. The template exposes the UI through Sealos HTTPS ingress and lets you provide optional LLM settings during deployment.

OpenHands' full Docker sandbox mode normally requires access to a Docker daemon. This Sealos template provides a reachable web deployment path with persistent workspace storage and validates the UI/runtime startup path. Agent execution that requires launching nested sandbox containers depends on platform-level Docker/runtime support.

## Common Use Cases

- **AI coding workspace**: Open a browser-based OpenHands UI for project automation.
- **LLM agent experiments**: Connect an LLM API key and test agent workflows.
- **Persistent task state**: Keep workspace files and OpenHands state across restarts.
- **Cloud development assistant**: Run an assistant-style web app next to other Sealos services.

## Dependencies for OpenHands Hosting

The Sealos template includes the OpenHands web container, persistent workspace storage, persistent state storage, public HTTPS ingress, and optional LLM configuration inputs.

### Deployment Dependencies

- [OpenHands Documentation](https://docs.openhands.dev/) - Official documentation
- [OpenHands Runtime Documentation](https://docs.openhands.dev/openhands/usage/runtimes) - Runtime and sandbox reference
- [OpenHands GitHub Repository](https://github.com/OpenHands/OpenHands) - Source code and releases

### Implementation Details

**Architecture Components:**

- **OpenHands StatefulSet**: Runs `ghcr.io/openhands/openhands:1.8.0` on port `3000`.
- **Workspace volume**: Persists `/workspace`.
- **State volume**: Persists `/root/.openhands-state`.
- **Ingress and App**: Publish the OpenHands web UI through HTTPS.

**Configuration:**

- `llm_api_key` is optional and maps to `LLM_API_KEY`.
- `llm_model` is optional and maps to `LLM_MODEL`.
- `SANDBOX_RUNTIME_CONTAINER_IMAGE` points to the matching OpenHands runtime image on GHCR.
- Full nested-container execution depends on Docker/runtime availability in the Sealos environment.

**License Information:**

OpenHands is licensed under MIT. This Sealos template is provided under the repository license.

## Why Deploy OpenHands on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying OpenHands on Sealos, you get:

- **One-Click Web UI**: Start the OpenHands web app quickly.
- **Persistent Workspace**: Keep workspace and state data across restarts.
- **Optional LLM Setup**: Provide model and API key values during deployment.
- **Instant Public Access**: Access the UI through an HTTPS URL.
- **Integrated Operations**: Inspect logs, restart the app, and adjust resources from the Canvas.

## Deployment Guide

1. Open the [OpenHands template](https://sealos.io/products/app-store/openhands) and click **Deploy Now**.
2. Optionally provide `llm_api_key` and `llm_model`.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the OpenHands URL.
5. Configure the LLM provider in the UI when prompted, then open the main workspace page.

## Configuration

After deployment, configure OpenHands through:

- **OpenHands UI**: Set or confirm the LLM provider and model.
- **AI Dialog**: Describe resource or environment changes and let Sealos apply them.
- **Resource Cards**: Adjust CPU, memory, storage, and environment variables.

## Runtime Notes

The template validates the OpenHands web application path and persistent storage path. Workflows that require starting sandbox runtime containers need Docker-compatible runtime access from the hosting environment. For code editing, UI setup, and state persistence, the deployment works as a normal web app.

## Troubleshooting

### Agent execution cannot start a sandbox

- Cause: The hosting environment does not expose a Docker daemon or compatible nested runtime to the OpenHands container.
- Solution: Use OpenHands UI features that do not require nested runtime containers, or attach a supported runtime service according to OpenHands runtime documentation.

### LLM calls fail

- Cause: Missing or invalid provider credentials.
- Solution: Set `llm_api_key` and `llm_model` during deployment or update them from the StatefulSet environment variables.

## Additional Resources

- [OpenHands Documentation](https://docs.openhands.dev/)
- [OpenHands Runtime Guide](https://docs.openhands.dev/openhands/usage/runtimes)
- [OpenHands GitHub Repository](https://github.com/OpenHands/OpenHands)

## License

This Sealos template is provided under the repository license. OpenHands itself is licensed under MIT.
