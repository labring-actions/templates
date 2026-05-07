# Coze Studio

## Overview

An open-source AI agent development platform with integrated workflow, knowledge, memory, plugin, and chat capabilities.

This Sealos template deploys **Coze Studio** as the `coze-studio` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `api_key` | the API Key for Ark API Key | `false` | `<redacted>` |
| `model_id` | the Model ID or Endpoint ID of Ark | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/coze-dev/coze-studio
- Source repository: https://github.com/coze-dev/coze-studio
