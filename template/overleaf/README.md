# Deploy and Host Overleaf on Sealos

Overleaf is an open-source, real-time collaborative LaTeX editor. This template deploys Overleaf Community Edition 6.1.2 with KubeBlocks MongoDB, KubeBlocks Redis, persistent project storage, and an HTTPS public endpoint on Sealos Cloud.

## About Hosting Overleaf

Overleaf provides a browser-based LaTeX workspace for writing papers, technical reports, books, and teaching materials. It combines source editing, project management, and PDF compilation in one web application, so teams can collaborate without installing a local TeX environment.

This Sealos template provisions the Overleaf web application, MongoDB for application metadata, Redis for realtime/session coordination, and persistent storage at `/var/lib/overleaf` for user data. Sealos manages the Kubernetes resources, public ingress, TLS certificate, and the App launch entry.

## Common Use Cases

- **Academic writing**: Write and compile LaTeX papers, theses, and reports in a browser.
- **Team collaboration**: Let trusted users edit shared LaTeX projects in one workspace.
- **Teaching environments**: Provide students with a ready-to-use LaTeX editor without local setup.
- **Technical documentation**: Maintain structured LaTeX documents with persistent project storage.

## Dependencies for Overleaf Hosting

The Sealos template includes all required runtime dependencies: Overleaf Community Edition, KubeBlocks MongoDB, KubeBlocks Redis, persistent storage, Service, Ingress, and Sealos App metadata.

### Deployment Dependencies

- [Overleaf Community Edition](https://github.com/overleaf/overleaf) - Source repository
- [Overleaf Toolkit Quick Start](https://github.com/overleaf/toolkit/blob/master/doc/quick-start-guide.md) - Official first-admin and usage flow
- [Sealos](https://sealos.io) - Cloud application platform

### Implementation Details

**Architecture Components:**

- **Overleaf web service**: Runs `sharelatex/sharelatex:6.1.2` and exposes the web UI on port 80.
- **MongoDB**: Stores users, projects, and Overleaf application metadata through KubeBlocks MongoDB 8.0.4.
- **Redis**: Provides Overleaf cache/realtime coordination through KubeBlocks Redis 7.2.7.
- **Persistent project storage**: Stores Overleaf data under `/var/lib/overleaf` on a 1 GiB volume.
- **Ingress and App entry**: Publishes the HTTPS URL and integrates the deployment into the Sealos App launcher.

**Configuration:**

The template sets `OVERLEAF_SITE_URL` from the generated Sealos hostname, enables proxy-aware behavior, and keeps email confirmation disabled by default for first-run Community Edition setup. Overleaf Community Edition is intended for trusted users; isolated/sandboxed compiles are a Server Pro feature, not part of this template.

**License Information:**

This Sealos template is provided under the repository license. Overleaf Community Edition is distributed by the Overleaf project; review the upstream repository for application licensing details.

## Why Deploy Overleaf on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to operation. By deploying Overleaf on Sealos, you get:

- **One-Click Deployment**: Create the Overleaf app, databases, storage, ingress, and App launcher entry from one template.
- **Managed Dependencies**: Use KubeBlocks MongoDB and Redis without hand-writing Kubernetes manifests.
- **Persistent Storage Included**: Keep Overleaf project data across restarts through the mounted data volume.
- **Instant Public Access**: Get an HTTPS URL managed by Sealos Ingress and certificates.
- **Easy Resource Tuning**: Adjust CPU, memory, and storage from Sealos resource cards as usage grows.
- **Zero Kubernetes Expertise Required**: Operate Overleaf from the Sealos UI while retaining Kubernetes-backed reliability.

## Deployment Guide

1. Open the [Overleaf template](https://sealos.io/products/app-store/overleaf) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. The defaults are enough for a first test deployment.
3. Wait for deployment to complete. The first cold start can take several minutes because Overleaf initializes MongoDB indexes and runs migrations.
4. Open the generated Overleaf URL from the Sealos App entry.
5. Open `/register` to confirm public self-signup. Overleaf Community Edition normally shows **Please contact to create an account** until an administrator creates users.
6. Create the first administrator or user from the container console, then sign in from `/login` and continue to `/project` to start using Overleaf.

## Configuration

Deployment parameters:

| Name | Description | Default |
|------|-------------|---------|
| `OVERLEAF_SITE_LANGUAGE` | Set the Overleaf interface language. | `zh-CN` |
| `OVERLEAF_APP_NAME` | Set the displayed Overleaf site name. | `Overleaf Community Edition` |
| `ENABLED_LINKED_FILE_TYPES` | Comma-separated linked file types enabled for projects. | `project_file,project_output_file` |
| `ENABLE_CONVERSIONS` | Enable thumbnail generation with ImageMagick. | `true` |
| `EMAIL_CONFIRMATION_DISABLED` | Disable email confirmation for first-run local account setup. | `true` |

After deployment, create the initial account from the Overleaf container console or import an existing data set, then sign in from `/login`. The live validation for this template confirmed that `/login` is reachable and `/register` returns the expected Community Edition message, **Please contact to create an account**, when public self-signup is not enabled.

## Scaling

The template is tuned for a small Community Edition deployment. The minimum tested app allocation is 1 vCPU and 2 GiB memory for the Overleaf container, plus KubeBlocks MongoDB and Redis at 500 mCPU and 512 MiB memory per database component. Increase memory first if cold starts, migrations, or PDF compilation workloads become slow.

To scale resources, open the deployment Canvas, click the relevant resource card, adjust CPU, memory, storage, or replicas, and apply the change in the dialog.

## Troubleshooting

### First start takes several minutes

Overleaf runs database migrations on an empty MongoDB database. Wait until the Overleaf pod is Ready before opening the site.

### `/register` says “Please contact to create an account”

This is the expected Community Edition behavior when public self-signup is not enabled. Create or invite users from the administrator context, then sign in from `/login`.

### Login succeeds but projects are slow to open

Check the Overleaf pod memory and database health in Sealos. Increase the Overleaf memory limit if the instance is used for larger documents or heavier compilation workloads.

### Getting Help

- [Overleaf Toolkit documentation](https://github.com/overleaf/toolkit/tree/master/doc)
- [Overleaf GitHub Issues](https://github.com/overleaf/overleaf/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Overleaf website](https://www.overleaf.com/)
- [Overleaf source repository](https://github.com/overleaf/overleaf)
- [Overleaf Toolkit](https://github.com/overleaf/toolkit)

## License

This Sealos template is provided under the templates repository license. Overleaf Community Edition is licensed by the Overleaf project; review the upstream repository for current application license terms.
