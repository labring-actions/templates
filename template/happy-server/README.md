# Happy Server

## Overview

Minimal backend for open-source end-to-end encrypted Claude Code clients.

This Sealos template deploys **Happy Server** as the `happy-server` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `node_env` | Node environment | `true` | `production` |
| `seed` | Seed for token generation | `true` | `${{ random(32) }}` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/slopus/happy/tree/main/packages/happy-server
- Source repository: https://github.com/slopus/happy/tree/main/packages/happy-server
