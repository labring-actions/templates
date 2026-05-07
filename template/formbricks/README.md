# Formbricks

## Overview

Formbricks provides a free and open source surveying platform. Gather feedback at every point in the user journey with beautiful in-app, website, link and email surveys.

This Sealos template deploys **Formbricks** as the `formbricks` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `IMPRINT_URL` | URL for your imprint page | `false` | `https://www.formbricks.com/imprint` |
| `PRIVACY_URL` | URL for your privacy policy page | `false` | `https://www.formbricks.com/privacy` |
| `TERMS_URL` | URL for your terms of service page | `false` | `https://www.formbricks.com/terms` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://formbricks.com
- Source repository: https://github.com/formbricks/formbricks
