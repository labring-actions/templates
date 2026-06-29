# Deploy and Host OpenGist on Sealos

OpenGist is a self-hosted pastebin powered by Git. This template deploys OpenGist with KubeBlocks PostgreSQL and persistent Git data storage on Sealos Cloud.

![OpenGist Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/opengist/website-screenshot.webp)

## About Hosting OpenGist

OpenGist stores snippets as Git repositories, so users can create, edit, clone, pull, and push snippets through the web interface or Git tooling. It supports public, private, and unlisted snippets, syntax highlighting, search, likes, forks, and revision history.

This Sealos template runs the pinned `ghcr.io/thomiceli/opengist:1.9.1` image on port `6157`. Sealos provisions a KubeBlocks PostgreSQL `postgresql-16.4.0` database, a persistent `/opengist` volume, an internal Service, an HTTPS Ingress, and a Sealos App entry.

## Common Use Cases

- **Private code snippets**: Host internal notes, scripts, and examples with ownership control.
- **Git-backed pastebin**: Keep snippet history in Git repositories.
- **Team knowledge sharing**: Share public or unlisted snippets across engineering teams.
- **Self-hosted Gist alternative**: Run a lightweight open-source replacement for GitHub Gist.

## Dependencies for OpenGist Hosting

The Sealos template includes the OpenGist application container, KubeBlocks PostgreSQL, persistent storage, Service, Ingress, and App resource.

### Deployment Dependencies

- [OpenGist Documentation](https://opengist.io/docs) - Official documentation
- [OpenGist GitHub Repository](https://github.com/thomiceli/opengist) - Source code and releases
- [OpenGist Container Image](https://github.com/thomiceli/opengist/pkgs/container/opengist) - Official GHCR image

### Implementation Details

**Architecture Components:**

- **OpenGist**: Web application and Git-over-HTTP service on port `6157`
- **PostgreSQL**: KubeBlocks-managed `postgresql-16.4.0` database for application metadata
- **Persistent storage**: `1Gi` volume mounted at `/opengist` for Git repositories and indexes
- **Ingress**: Sealos-managed HTTPS public endpoint

**Configuration:**

- `OG_EXTERNAL_URL` is set to the generated Sealos HTTPS URL.
- `OG_DB_URI` is assembled from the KubeBlocks PostgreSQL connection secret.
- `OG_SSH_GIT_ENABLED=false` keeps the public template focused on HTTPS access.
- The first registered user becomes the initial account for the instance.

**License Information:**

OpenGist is licensed under AGPL-3.0.

## Why Deploy OpenGist on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, networking, storage, and operations. By deploying OpenGist on Sealos, you get:

- **One-Click Deployment**: Deploy OpenGist, PostgreSQL, storage, Service, Ingress, and App entry from one template.
- **Managed Database**: Use a KubeBlocks PostgreSQL cluster without manual database operations.
- **Persistent Git Data**: Store repositories and indexes on durable volume storage.
- **Instant Public Access**: Open the generated HTTPS URL after deployment.
- **Easy Customization**: Adjust resources and environment variables through Sealos resource cards or the AI dialog.

## Deployment Guide

1. Open the [OpenGist template](https://sealos.io/products/app-store/opengist) and click **Deploy Now**.
2. Configure the parameters in the popup dialog, or keep the generated defaults.
3. Wait for deployment to complete, typically 2-4 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated OpenGist URL from the App card.
5. Register the first user account. OpenGist uses the first registration as the initial account for the instance.

## Configuration

After deployment, you can configure OpenGist through:

- **OpenGist UI**: Manage users, snippets, OAuth providers, and visibility settings.
- **AI Dialog**: Describe resource changes for Sealos to apply.
- **Resource Cards**: Click the StatefulSet, PostgreSQL cluster, Service, Ingress, or PVC cards to adjust settings.

## Scaling

OpenGist is deployed as a single-replica StatefulSet with persistent Git data. Review upstream OpenGist guidance before changing replica count.

## Troubleshooting

### Registration page is unavailable

Wait until the OpenGist StatefulSet and PostgreSQL cluster show Ready in the Sealos Canvas. First cold start includes database creation and repository storage initialization.

### Snippets are missing after restart

Confirm that the `/opengist` volume remains attached to the StatefulSet. The template stores Git repositories and indexes on that persistent volume.

### Getting Help

- [OpenGist Documentation](https://opengist.io/docs)
- [OpenGist GitHub Issues](https://github.com/thomiceli/opengist/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [OpenGist Website](https://opengist.io/)
- [OpenGist Configuration](https://opengist.io/docs/configuration/configure.html)
- [OpenGist Demo](https://demo.opengist.io/)

## License

This Sealos template is provided under the repository license. OpenGist itself is licensed under AGPL-3.0.
