# Deploy and Host LibreDB Studio on Sealos

## Overview

LibreDB Studio is an open-source, self-hosted SQL IDE. It provides a web-based client to browse, query, and manage your SQL databases from a single interface.

This Sealos template deploys **LibreDB Studio** as the `libredb-studio` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain. Sign in with the admin email and password you set during deployment.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_email` | Admin user email for the first login | `true` | `` |
| `admin_password` | Admin user password (minimum 8 characters) | `true` | `` (set at deploy) |
| `jwt_secret` | Secret used to sign session tokens (minimum 32 characters) | `false` | `${{ random(48) }}` |
| `volume_size` | Persistent storage size for the database (GiB) | `false` | `1` |

Data is stored in an embedded SQLite database at `/app/data/libredb-storage.db`, kept on a persistent volume so it survives restarts and redeploys.

Both admin_password and jwt_secret are stored as Sealos-managed inputs, so leave them to the generated defaults or set them at deploy time rather than hardcoding them.

## Official Links

- Official website: https://libredb.org
- Source repository: https://github.com/libredb/libredb-studio
