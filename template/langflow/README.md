# Langflow

## Overview

Langflow is a low-code app builder for RAG and multi-agent AI applications. Build, iterate, and deploy AI workflows with a drag-and-drop interface.

This Sealos template deploys **Langflow** as the `langflow` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `enable_database` | Enable external database (PostgreSQL) for production use | `false` | `false` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.langflow.org/
- Source repository: https://github.com/langflow-ai/langflow
