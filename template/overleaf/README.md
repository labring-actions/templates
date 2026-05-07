# Overleaf

## Overview

Overleaf is an open-source online real-time collaborative LaTeX editor.

This Sealos template deploys **Overleaf** as the `overleaf` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `EMAIL_CONFIRMATION_DISABLED` | Disables email confirmation requirementk | `false` | `true` |
| `ENABLED_LINKED_FILE_TYPES` | - | `false` | `project_file,project_output_file` |
| `ENABLE_CONVERSIONS` | Enables Thumbnail generation using ImageMagick | `false` | `true` |
| `OVERLEAF_APP_NAME` | - | `false` | `Overleaf Community Edition` |
| `OVERLEAF_SITE_LANGUAGE` | Set language | `false` | `zh-CN` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/overleaf/overleaf
- Source repository: https://github.com/overleaf/overleaf
