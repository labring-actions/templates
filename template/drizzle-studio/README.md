# Drizzle Studio (Gateway)

## Overview

Drizzle Studio (Gateway) is a self-hosted, browser-based interface for exploring and managing your database schema using the Drizzle ORM ecosystem. It acts as a gateway between your database and Drizzle Studio’s frontend, enabling secure connections, schema introspection, and query execution directly from your own infrastructure instead of relying on a public service.

This Sealos template deploys **Drizzle Studio (Gateway)** as the `drizzle-studio` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `masterpass` | Master password used by Drizzle Studio Gateway (optional) | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://gateway.drizzle.team/
- Source repository: https://github.com/drizzle-team/drizzle-orm
