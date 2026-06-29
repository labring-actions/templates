# Deploy and Host linkding on Sealos

linkding is a minimal, fast, self-hosted bookmark manager for collecting, tagging, searching, and sharing links. This template deploys linkding with PostgreSQL and persistent data storage on Sealos.

![linkding Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/linkding/website-screenshot.webp)

## About Hosting linkding

linkding runs as a Django-based web application on port `9090`. The template uses the official container image, provisions KubeBlocks PostgreSQL for the application database, and mounts persistent storage at `/etc/linkding/data`.

The first administrator is created from deployment inputs through linkding's documented `LD_SUPERUSER_NAME` and `LD_SUPERUSER_PASSWORD` environment variables. After deployment, sign in with those credentials from the App URL.

## Common Use Cases

- **Personal Bookmark Library**: Save links with tags, descriptions, notes, and archive metadata.
- **Team Link Collection**: Share curated links across a small team.
- **Read-Later Workflow**: Store pages for later triage and search.
- **Browser Extension Backend**: Use linkding as the sync target for its browser integrations.

## Dependencies for linkding Hosting

The Sealos template includes all required dependencies: linkding, KubeBlocks PostgreSQL `postgresql-16.4.0`, an initialization Job for the `linkding` database, persistent storage, Service, Ingress, and App entry.

### Deployment Dependencies

- [Official Repository](https://github.com/sissbruecker/linkding) - Source code and setup instructions
- [Docker Compose](https://github.com/sissbruecker/linkding/blob/master/docker-compose.yml) - Official container deployment baseline
- [Environment Sample](https://github.com/sissbruecker/linkding/blob/master/.env.sample) - Environment variable reference
- [Sealos](https://sealos.io) - Kubernetes-based application hosting

### Implementation Details

**Architecture Components:**

- **linkding Web Service**: Runs `sissbruecker/linkding:1.45.0` and serves the UI on port `9090`.
- **PostgreSQL**: KubeBlocks-managed `postgresql-16.4.0` stores application data.
- **Persistent Data Volume**: Mounted at `/etc/linkding/data` for application data files.
- **Service and Ingress**: Expose the web UI through HTTPS.

**Configuration:**

The template sets `LD_DB_ENGINE=postgres` and injects database fields from the KubeBlocks connection secret. It also sets `LD_CSRF_TRUSTED_ORIGINS` to the generated Sealos HTTPS URL.

**License Information:**

This Sealos template is provided under the repository license. linkding is licensed under the MIT License.

## Why Deploy linkding on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, public access, and operations. By deploying linkding on Sealos, you get:

- **One-Click Deployment**: Launch a complete bookmark manager from the App Store.
- **Managed PostgreSQL**: Store bookmarks in a KubeBlocks database.
- **Persistent Storage**: Keep linkding data across restarts.
- **Instant Public Access**: Sealos creates an HTTPS URL automatically.

## Deployment Guide

1. Open the [linkding template](https://sealos.io/products/app-store/linkding) and click **Deploy Now**.
2. Configure the initial administrator username and password.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access linkding through the provided App URL and log in with the administrator credentials from step 2.

## Configuration

After deployment, manage bookmarks, tags, users, and integrations from the linkding web UI. For resource changes or environment updates, use the Sealos Canvas, AI dialog, or workload resource card.

## Additional Resources

- [linkding README](https://github.com/sissbruecker/linkding)
- [Environment Sample](https://github.com/sissbruecker/linkding/blob/master/.env.sample)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the repository license. linkding is licensed under the MIT License.
