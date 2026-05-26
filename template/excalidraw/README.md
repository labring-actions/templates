# Deploy and Host Excalidraw on Sealos

Excalidraw is an open source virtual whiteboard for sketching hand-drawn diagrams, workflows, and visual notes. This template deploys Excalidraw as a lightweight single-service web application on Sealos Cloud.

![Excalidraw Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/excalidraw/website-screenshot.webp)

## About Hosting Excalidraw

Excalidraw runs as a stateless web service that serves the browser-based drawing interface over HTTP. The application stores drawings primarily in the browser or in user-managed export files, so this template does not provision a database or persistent volume.

The Sealos template creates a Deployment, Service, Ingress, and App entry for Excalidraw. Sealos automatically provides the public HTTPS endpoint, TLS certificate integration, Kubernetes scheduling, and resource management through the Canvas.

This deployment is suitable for teams that need a quick shared diagramming surface without managing servers, reverse proxies, or Kubernetes manifests manually.

## Common Use Cases

- **Architecture Sketching**: Draw system diagrams, deployment flows, and service relationships during planning sessions.
- **Product and UX Ideation**: Capture wireframes, user flows, and interface ideas in a hand-drawn style.
- **Meeting Whiteboards**: Use a browser-based canvas for workshops, standups, and remote collaboration.
- **Documentation Diagrams**: Export diagrams for README files, design docs, and engineering proposals.
- **Teaching and Explainers**: Build simple visual explanations for technical or non-technical audiences.

## Dependencies for Excalidraw Hosting

The Sealos template includes the Excalidraw web container and the Kubernetes resources needed to expose it publicly. It does not require PostgreSQL, MySQL, Redis, object storage, or persistent volumes.

### Deployment Dependencies

- [Official Website](https://excalidraw.com/) - Hosted Excalidraw editor and product information
- [Source Repository](https://github.com/excalidraw/excalidraw) - Application source code and release activity
- [Excalidraw Documentation](https://docs.excalidraw.com/) - Product and developer documentation
- [GitHub Issues](https://github.com/excalidraw/excalidraw/issues) - Community support and issue tracking

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Excalidraw Web App**: A single container serving the Excalidraw browser application on port 80.
- **Service**: Routes internal cluster traffic to the Excalidraw container.
- **Ingress**: Provides the public HTTPS endpoint through the Sealos-managed domain.
- **App Entry**: Adds a clickable Excalidraw link in the Sealos dashboard.

**Configuration:**

The template uses generated defaults for `app_name` and `app_host`, so each deployment receives a unique application name and public hostname. No extra user inputs are required during deployment.

The workload uses health probes on `/`, disables automatic service account token mounting, and uses minimal resource settings appropriate for a lightweight static web application.

**License Information:**

Excalidraw is licensed under the MIT License. This Sealos template is provided as part of the Sealos templates repository.

## Why Deploy Excalidraw on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle, from deployment to ongoing operations. By deploying Excalidraw on Sealos, you get:

- **One-Click Deployment**: Open the template page, click **Deploy Now**, and let Sealos create the required Kubernetes resources.
- **Instant Public Access**: Each deployment receives an HTTPS URL with certificate handling built in.
- **Zero Kubernetes Expertise Required**: Run Excalidraw on Kubernetes without writing or maintaining manifests yourself.
- **Resource Efficiency**: Use pay-as-you-go cloud resources with lightweight CPU and memory settings.
- **Easy Customization**: After deployment, use the Canvas, AI dialog, or resource cards to adjust resources and runtime settings.
- **Built-In Operations View**: Inspect the Deployment, Service, Ingress, and App entry from the Sealos dashboard.

Deploy Excalidraw on Sealos and focus on drawing ideas instead of managing infrastructure.

## Deployment Guide

1. Open the [Excalidraw template](https://sealos.io/products/app-store/excalidraw) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. The default values are enough for a standard deployment.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **Excalidraw Web UI**: Open the generated HTTPS endpoint and start drawing in your browser.

## Configuration

After deployment, you can configure Excalidraw through:

- **AI Dialog**: Describe changes such as resource adjustments and let AI apply updates.
- **Resource Cards**: Click the Deployment, Service, or Ingress cards to inspect and modify settings.
- **Application URL**: Use the generated Sealos HTTPS URL to access the whiteboard.

Excalidraw itself does not require an admin account or database configuration for the default web editor experience.

## Scaling

To scale or resize the deployment:

1. Open the Canvas for your Excalidraw deployment.
2. Click the Deployment resource card.
3. Adjust CPU, memory, or replica count based on your expected traffic.
4. Apply the changes in the dialog.

For most small teams and personal workspaces, the default single-replica deployment is sufficient.

## Troubleshooting

### The Excalidraw page does not open after deployment

- Cause: The container or Ingress may still be starting.
- Solution: Wait until the Deployment is ready in the Canvas, then reopen the application URL.

### Browser data is not shared across users

- Cause: The default Excalidraw web app is primarily browser-based and does not provision a backend database in this template.
- Solution: Export diagrams as files or use Excalidraw's supported sharing features when needed.

### Getting Help

- [Excalidraw Documentation](https://docs.excalidraw.com/)
- [Excalidraw GitHub Issues](https://github.com/excalidraw/excalidraw/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Excalidraw Official Website](https://excalidraw.com/)
- [Excalidraw Source Repository](https://github.com/excalidraw/excalidraw)
- [Excalidraw Blog](https://plus.excalidraw.com/blog)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided as part of the Sealos templates repository. Excalidraw itself is licensed under the [MIT License](https://github.com/excalidraw/excalidraw/blob/master/LICENSE).
