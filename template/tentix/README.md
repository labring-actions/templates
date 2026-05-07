# tentix

## Overview

A FastGPT-powered AI customer service platform with 10x accelerated resolution.

This Sealos template deploys **tentix** as the `tentix` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API Key | `true` | `<redacted>` |
| `OPENAI_BASE_URL` | OpenAI endpoint base URL | `true` | `https://api.openai.com/v1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/labring/tentix
- Source repository: https://github.com/labring/tentix
