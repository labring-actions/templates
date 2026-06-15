# Deploy and Host OpenDesign on Sealos

OpenDesign is a local-first, open-source AI design workspace for generating prototypes, dashboards, decks, images, videos, and design-system-driven artifacts. This template deploys the official OpenDesign Docker runtime as a single persistent service on Sealos.

![OpenDesign Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/opendesign/website-screenshot.webp)

## About Hosting OpenDesign

OpenDesign provides a browser-based workspace backed by a local daemon. The daemon serves the web UI, API routes, project files, plugin data, and generated artifacts from one container. On Sealos, this template persists the OpenDesign workspace under `/app/.od` so projects, conversations, media configuration, and generated outputs survive restarts.

The upstream Docker deployment exposes port `7456`, stores runtime data in `/app/.od`, and requires an API token when the daemon binds to a public interface. This Sealos template follows the upstream cloud pattern by running an Nginx proxy in front of OpenDesign. The proxy exposes port `8080`, forwards traffic to the OpenDesign service on port `7456`, and injects the internal bearer token for `/api` routes.

## Common Use Cases

- **AI design workspace**: Generate web, desktop, and mobile prototypes from prompts and design-system context.
- **Presentation and artifact generation**: Produce decks, live dashboards, HTML artifacts, PDFs, and exportable design outputs.
- **Design-system experimentation**: Try design systems, plugins, and reusable workflows in a persistent workspace.
- **Agent-assisted design handoff**: Use OpenDesign as a visual workspace before handing artifacts to coding agents or editors.

## Dependencies for OpenDesign Hosting

The Sealos template includes all runtime dependencies in the OpenDesign Docker image and provisions persistent storage for workspace data.

### Deployment Dependencies

- [Official Website](https://open-design.ai/) - Product website and download links
- [Source Repository](https://github.com/nexu-io/open-design) - OpenDesign source code
- [Docker Deployment Guide](https://github.com/nexu-io/open-design/blob/main/deploy/README.md) - Upstream Docker deployment notes
- [Docker Image](https://hub.docker.com/r/vanjayak/open-design) - Published OpenDesign container image

### Implementation Details

**Architecture Components:**

- **OpenDesign Runtime**: Container serving the web UI and daemon API on port `7456`
- **Nginx Proxy**: Public entry point on port `8080`, forwarding API requests with the generated bearer token
- **Persistent Workspace Volume**: Stores `/app/.od`, including projects, conversations, generated artifacts, and local configuration
- **Ingress and App Link**: Exposes the OpenDesign web interface through the generated Sealos domain

**Configuration:**

- The image is pinned by digest to avoid mutable `latest` drift.
- `OD_BIND_HOST=0.0.0.0`, `OD_PORT=7456`, `OD_WEB_PORT=7456`, and a generated `OD_API_TOKEN` match the upstream cloud runtime requirements.
- `OD_ALLOWED_ORIGINS` is set to the generated Sealos HTTPS domain so OpenDesign accepts same-origin browser requests behind Ingress.
- Nginx forwards `/api/` with `Authorization: Bearer <generated token>` so browser API calls work through the public Sealos domain.
- The proxy preserves the browser-facing Host and forwarded headers so same-origin browser requests can reach the daemon through the Sealos domain.
- OpenDesign's upstream Docker guide warns that remote deployments should sit behind an authenticated reverse proxy, SSH tunnel, VPN, or equivalent access layer. This template protects the daemon API token internally, but it does not add end-user login in front of the web UI. Do not treat it as a hardened multi-user public service without adding an access-control layer.

**License Information:**

OpenDesign is licensed under Apache-2.0.

## Why Deploy OpenDesign on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying OpenDesign on Sealos, you get:

- **One-Click Deployment**: Deploy OpenDesign without manually writing Kubernetes YAML.
- **Persistent Storage Included**: Workspace files and generated artifacts survive container restarts.
- **Instant Public Access**: Each deployment gets a generated HTTPS endpoint.
- **Easy Customization**: Configure allowed origins, resources, storage, and networking from Sealos.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed hosting without managing cluster primitives directly.

## Deployment Guide

1. Open the [OpenDesign template](https://sealos.io/products/app-store/opendesign) and click **Deploy Now**.
2. Review the default resource and storage settings.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the OpenDesign app link from the Canvas or App list.

OpenDesign does not create a template-managed admin account or login page. The deployed app opens directly into the workspace, where you can configure BYOK providers, plugins, design systems, and local workspace settings.

The template was tested with a minimum runtime footprint of `20m` CPU and `128Mi` memory request for the OpenDesign container, `20m` CPU and `25Mi` memory request for the proxy container, and a `1Gi` persistent workspace volume. Increase memory or storage if you generate large media assets or keep many projects in one workspace.

## Configuration

After deployment, you can configure OpenDesign through:

- **AI Dialog**: Describe changes such as larger storage, more memory, or access-control adjustments.
- **Resource Cards**: Modify the StatefulSet, Service, Ingress, or persistent volume from the Canvas.
- **OpenDesign UI**: Configure BYOK providers, plugins, design systems, and workspace settings inside OpenDesign.

## Scaling

OpenDesign stores local workspace state on a single persistent volume, so keep the application at one replica unless you have validated a multi-replica storage and session strategy for your own deployment.

To increase capacity:

1. Open the Canvas for your deployment.
2. Click the OpenDesign StatefulSet resource card.
3. Increase CPU, memory, or persistent storage.
4. Apply the change.

## Troubleshooting

### The app starts but API calls fail

This template uses an Nginx proxy to inject the generated API token for `/api/` routes. If API calls fail, confirm the proxy Deployment is running and still has the generated Nginx configuration mounted.

### Generated files disappear after restart

Confirm the StatefulSet still mounts the persistent volume at `/app/.od`. Workspace data is stored there.

### Getting Help

- [OpenDesign GitHub Issues](https://github.com/nexu-io/open-design/issues)
- [OpenDesign Discussions](https://github.com/nexu-io/open-design/discussions)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [OpenDesign README](https://github.com/nexu-io/open-design/blob/main/README.md)
- [OpenDesign Docker Deployment](https://github.com/nexu-io/open-design/blob/main/deploy/README.md)
- [OpenDesign Releases](https://github.com/nexu-io/open-design/releases)

## License

OpenDesign is distributed under the Apache-2.0 license. Review the upstream repository for the latest license and third-party notices.
