# Refly

## Overview

Refly is an open-source AI-native creation engine powered by 13+ leading AI models.

This Sealos template deploys **Refly** as the `refly` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `EMBEDDINGS_MODEL_NAME` | The embedding model name to use, e.g., text-embedding-ada-002 | `true` | `text-embedding-ada-002` |
| `OPENAI_API_KEY` | OpenAI API Key | `true` | `<redacted>` |
| `OPENAI_BASE_URL` | OpenAI endpoint base URL | `true` | `https://api.openai.com/v1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://refly.ai/
- Source repository: https://github.com/refly-ai/refly
