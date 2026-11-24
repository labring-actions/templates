# Deploy and Host Gogs on Sealos

Gogs is a lightweight self-hosted Git service with repositories, issues, pull requests, webhooks, and a clean web interface.

![Gogs documentation](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gogs/website-screenshot.webp)

## About Hosting Gogs

This template runs Gogs as a single StatefulSet with SQLite storage and a 1 GiB persistent volume mounted at `/data`. The installer is locked, so the service starts directly with the bundled production configuration and a generated secret key.

Open the public URL and register the first account. Gogs grants administrator rights to that account, which can then manage users, repositories, and site settings. Repository data and the SQLite database persist across pod restarts.

## Common Use Cases

- Host private Git repositories for a small team or personal projects.
- Review code with issues, pull requests, and inline comments.
- Run lightweight CI hooks through repository webhooks.
- Mirror repositories inside a private network.
- Provide a self-contained Git forge for labs and demos.

## Dependencies for Gogs Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A 1 GiB persistent volume for repositories and the SQLite database.
- A modern browser for the web interface.
- Git clients that use HTTPS remotes; SSH access is disabled in this template.

## Why Deploy Gogs on Sealos?

- One-click deployment with a public HTTPS Git endpoint.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent storage for repositories, users, issues, and attachments.
- Pay-as-you-go resource cards that keep a small forge affordable.
- Canvas view for inspecting the StatefulSet, Service, Ingress, and PVC.
- AI dialog for deployment guidance in the Sealos desktop.

## Deployment Guide

1. Open the [Gogs template](https://sealos.io/products/app-store/gogs) and click **Deploy Now**.
2. Keep the generated application name or set your own, confirm the 1 GiB storage plan, and submit the deployment.
3. Wait 2-3 minutes for the StatefulSet to become ready, then open the public URL from the App card.
4. Register the first account; Gogs makes this account the site administrator.
5. Create a repository, then open Canvas to review the StatefulSet, Service, Ingress, and persistent volume.

## License

Gogs is released under the [MIT License](https://github.com/gogs/gogs/blob/main/LICENSE).
