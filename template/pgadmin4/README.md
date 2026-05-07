# pgadmin4

## Overview

pgAdmin 4 is a rewrite of the popular pgAdmin3 management tool for the PostgreSQL database.

This Sealos template deploys **pgadmin4** as the `pgadmin4` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `PGADMIN_DEFAULT_EMAIL` | login page account email | `false` | `admin@sealos.io` |
| `PGADMIN_DEFAULT_PASSWORD` | login page account password | `false` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.pgadmin.org/
- Source repository: https://github.com/pgadmin-org/pgadmin4
