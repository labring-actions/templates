# Deploy and Host Sunshine on Sealos

Sunshine is a self-hosted game stream host for Moonlight with a browser-based configuration UI and client pairing workflow. This template deploys Sunshine with persistent configuration storage on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/sunshine/website-screenshot.webp)

## About Hosting Sunshine

Sunshine runs from the official LizardByte container image and exposes the Web UI on port `47990`, matching the upstream documentation. The Sealos template persists Sunshine configuration and cache directories so account setup, pairing state, and application settings survive restarts.

This template is best suited for Web UI configuration testing and Moonlight pairing workflows in cloud environments. Real game streaming depends on host GPU, encoder, networking, and client connectivity constraints.

## Common Use Cases

- **Moonlight Host Configuration**: Manage Sunshine settings from a browser.
- **Client Pairing Tests**: Validate Web UI setup and PIN pairing workflows.
- **Remote Streaming Lab**: Experiment with Sunshine configuration in a disposable cloud workspace.
- **Documentation and Demo Environment**: Show the Sunshine UI without installing a desktop host locally.

## Dependencies for Sunshine Hosting

The Sealos template includes the Sunshine application container and persistent storage for user configuration.

### Deployment Dependencies

- [Sunshine Documentation](https://docs.lizardbyte.dev/projects/sunshine/latest/) - Official documentation
- [Getting Started Guide](https://docs.lizardbyte.dev/projects/sunshine/latest/md_docs_2getting__started.html) - Web UI and configuration flow
- [Moonlight](https://moonlight-stream.org/) - Client application ecosystem

### Implementation Details

**Architecture Components:**

This template deploys one service:

- **Sunshine**: Web UI exposed through Sealos Ingress on port `47990`
- **Persistent Configuration**: Volumes mounted at `/home/lizard/.config/sunshine` and `/home/lizard/.cache/sunshine`

**Configuration:**

- On first launch, open the Web UI and create the Sunshine username and password.
- Save the username and password created during first-run setup.
- Use the Web UI to pair Moonlight clients and manage applications.
- Sunshine's upstream Web UI uses HTTPS internally with a self-signed certificate; the template routes it through Sealos HTTPS Ingress.

**License Information:**

Sunshine is licensed under the GNU General Public License v3.0.

## Why Deploy Sunshine on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and day-2 operations. By deploying Sunshine on Sealos, you get:

- **One-Click Deployment**: Launch Sunshine from the App Store with persistent configuration.
- **Instant Public Access**: Open the Web UI through a generated HTTPS URL.
- **Persistent Settings**: Keep first-run account setup and configuration across restarts.
- **AI-Assisted Operations**: Use the Canvas AI dialog to tune resources and networking.
- **Pay-as-You-Go Efficiency**: Test Sunshine workflows with cloud resources sized for the current workload.

## Deployment Guide

1. Open the [Sunshine template](https://sealos.io/products/app-store/sunshine) and click **Deploy Now**.
2. Review the deployment settings in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Sunshine through the provided URL. On the first visit, create the Web UI username and password, then save them for future logins.

## Configuration

After deployment, you can configure Sunshine through:

- **Sunshine Web UI**: Create the first user, pair clients, and manage applications.
- **AI Dialog**: Ask Sealos to adjust CPU, memory, or storage.
- **Resource Cards**: Modify the StatefulSet, Service, Ingress, and storage settings from the Canvas.

## Scaling

Sunshine streaming workloads can need more CPU and memory than the default template. Open the Canvas, click the Sunshine StatefulSet resource card, adjust CPU or memory, and apply the change.

## Troubleshooting

**First-run setup appears**

Create a username and password on the first visit. Save them because Sunshine uses those credentials for later Web UI logins.

**Moonlight cannot connect**

Check client reachability, required streaming ports, and host encoder availability. The Web UI may be reachable while full game streaming still needs additional networking and hardware support.

## Additional Resources

- [Sunshine Documentation](https://docs.lizardbyte.dev/projects/sunshine/latest/)
- [Sunshine GitHub Repository](https://github.com/LizardByte/Sunshine)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. Sunshine itself is licensed under the GNU General Public License v3.0.
