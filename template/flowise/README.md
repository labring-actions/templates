# Flowise

## Overview

Drag & drop UI to build your customized LLM flow.

This Sealos template deploys **Flowise** as the `flowise` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `USE_POSTGRESQL` | Use PostgreSQL database instead of local SQLite | `false` | `false` |
| `USE_S3_STORAGE` | Use S3 object storage for file uploads | `false` | `false` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://flowiseai.com/
- Source repository: https://github.com/FlowiseAI/Flowise
