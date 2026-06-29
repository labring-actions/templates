# Deploy and Host Manim on Sealos

Manim is a community-maintained Python framework for creating precise mathematical animations. This template deploys the official Manim image with a browser-based JupyterLab workspace on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/manim/website-screenshot.webp)

## About Hosting Manim

Manim runs in the official `manimcommunity/manim` container, which includes Python, Manim, graphics libraries, and TeX dependencies required for animation rendering. The Sealos template starts JupyterLab as the browser entry so you can create notebooks, scripts, and rendered media from a web workspace.

The deployment includes persistent storage mounted at `/manim`, so notebooks, Python files, and generated media survive restarts. Access is protected by a generated Jupyter token shown in the template defaults.

## Common Use Cases

- **Math Animation Prototyping**: Create and preview Manim scenes from a browser.
- **Teaching Materials**: Build visual explanations for algebra, geometry, calculus, and physics.
- **Notebook-Based Experiments**: Combine Python notes, code, and rendered outputs.
- **Cloud Rendering Workspace**: Keep Manim projects in persistent cloud storage.

## Dependencies for Manim Hosting

The Sealos template includes the official Manim container and persistent workspace storage.

### Deployment Dependencies

- [Manim Community Website](https://www.manim.community/) - Project homepage
- [Manim Docker Documentation](https://docs.manim.community/en/stable/installation/docker.html) - Official container guidance
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/) - Browser workspace documentation

### Implementation Details

**Architecture Components:**

This template deploys one service:

- **Manim JupyterLab**: Browser workspace running on port `8888`
- **Persistent Workspace**: A volume mounted at `/manim`

**Configuration:**

- JupyterLab starts with a generated token.
- Use the token from the deployment defaults when the Jupyter login page asks for authentication.
- Project files and generated media are stored in `/manim`.
- CPU and memory are set above the baseline because rendering, TeX, and notebook workflows need more room than a static web service.

**License Information:**

Manim Community Edition is licensed under the MIT License.

## Why Deploy Manim on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and day-2 operations. By deploying Manim on Sealos, you get:

- **One-Click Deployment**: Launch a ready-to-use Manim workspace from the App Store.
- **Persistent Workspace Storage**: Keep notebooks, scripts, and rendered media across restarts.
- **Instant HTTPS Access**: Open JupyterLab from the generated public URL.
- **AI-Assisted Operations**: Use the Canvas AI dialog to resize resources or update configuration.
- **Pay-as-You-Go Efficiency**: Start with a modest rendering workspace and scale when scenes become heavier.

## Deployment Guide

1. Open the [Manim template](https://sealos.io/products/app-store/manim) and click **Deploy Now**.
2. Review the generated Jupyter token and save it for login.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access JupyterLab through the provided URL and log in with the generated token.

## Configuration

After deployment, you can configure Manim through:

- **JupyterLab UI**: Create notebooks, Python files, and terminal sessions.
- **AI Dialog**: Ask Sealos to adjust CPU, memory, or storage.
- **Resource Cards**: Modify the StatefulSet and storage resources from the Canvas.

## Scaling

Increase memory for complex scenes, high-resolution renders, or TeX-heavy projects. Open the Canvas, click the Manim StatefulSet resource card, adjust CPU or memory, and apply the change.

## Troubleshooting

**Jupyter asks for a token**

Use the generated token from the template defaults.

**Rendering is slow or fails from memory pressure**

Increase CPU and memory from the StatefulSet resource card.

## Additional Resources

- [Manim Documentation](https://docs.manim.community/)
- [Manim Docker Documentation](https://docs.manim.community/en/stable/installation/docker.html)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. Manim Community Edition itself is licensed under the MIT License.
