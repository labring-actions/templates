# midjourney-ui

## Overview

Midjourney UI is an open source txt2img UI for AI draw.

This Sealos template deploys **midjourney-ui** as the `midjourney-ui` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `CHANNEL_ID` | CHANNEL_ID | `false` | `` |
| `HUGGINGFACE_TOKEN` | HUGGINGFACE_TOKEN | `false` | `<redacted>` |
| `SALAI_TOKEN` | SALAI_TOKEN | `false` | `<redacted>` |
| `SERVER_ID` | SERVER_ID | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/topics/midjourney-ui
- Source repository: https://github.com/erictik/midjourney-ui
