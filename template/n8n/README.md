# N8N

## Overview

n8n is a workflow automation platform that gives technical teams the flexibility of code with the speed of no-code.

This Sealos template deploys **N8N** as the `n8n` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `timezone` | The n8n instance timezone. Important for schedule nodes (such as Cron) | `false` | `America/New_York` |
| `use_postgresql` | Use PostgreSQL database for production workloads (recommended for better performance and data persistence) | `false` | `false` |
| `use_queue_mode` | Enable queue mode with Redis and workers for improved scalability and parallel execution (requires PostgreSQL) | `false` | `false` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://n8n.io/
- Source repository: https://github.com/n8n-io/n8n
