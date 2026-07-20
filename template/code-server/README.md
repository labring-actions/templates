# Deploy and Host code-server on Sealos

code-server runs VS Code in the browser with a persistent workspace volume. This template deploys code-server 4.128.0 with password authentication, persistent home storage, and HTTPS access on Sealos Cloud.

![code-server Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/code-server/website-screenshot.webp)

## About Hosting code-server

code-server serves the VS Code web UI on port `8080`. The Sealos template creates a single-replica Deployment with a `Recreate` update strategy, persistent `/home/coder` volume, Service, Ingress, and App entry.

Authentication is password-based. After deployment, open the generated HTTPS URL and enter the `PASSWORD` value from the deployment form.

## Common Use Cases

- **Browser IDE**: Edit files, use terminals, and run development commands from a browser.
- **Remote Workspace**: Keep project files and VS Code settings on the persistent Sealos volume.
- **Lightweight Admin Console**: Run quick maintenance commands from a secured web IDE.
- **Teaching and Demos**: Provide a ready-to-use coding surface with one URL and one password.

## Deployment Guide

1. Open the [code-server template](https://sealos.io/products/app-store/code-server) and click **Deploy Now**.
2. Set `PASSWORD` to a strong value.
3. Wait for the Deployment to become ready, then open the generated HTTPS URL from Sealos Canvas.
4. Enter `PASSWORD` on the sign-in screen.
5. Save projects under `/home/coder` to keep them on persistent storage.

## Configuration

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `PASSWORD` | Password used on the code-server sign-in screen. | `true` | None |

Store the password in Sealos-managed inputs and rotate it from Canvas when access needs to change.

## Scaling

The template starts with `200m` CPU and `512Mi` memory for a small interactive IDE session. Keep one replica while using the ReadWriteOnce volume, and increase resources from Sealos Canvas for language servers, dependency installation, or heavier terminal workloads.

## Troubleshooting

### Password is rejected

Confirm the current `PASSWORD` value in the Deployment input, update it from Canvas if needed, and restart the Deployment.

### Terminal or language server is slow

Increase CPU and memory on the code-server Deployment. Large repositories and language servers can use more memory than the base editor.

### Workspace files disappear

Confirm that files are saved under `/home/coder`. That path is backed by persistent storage.

## Additional Resources

- [code-server Documentation](https://coder.com/docs/code-server)
- [code-server Source Code](https://github.com/coder/code-server)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. code-server is licensed by its upstream project.
