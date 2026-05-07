# Tianji

## Overview

Tianji: Insight into everything, Website Analytics + Uptime Monitor + Server Status. not only another GA alternatives

This Sealos template deploys **Tianji** as the `tianji` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ALLOW_OPENAPI` | whether allow open openapi | `false` | `true` |
| `ALLOW_REGISTER` | whether allow register account | `false` | `false` |
| `JWT_SECRET` | replace me with a random string | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://tianji.msgbyte.com/
- Source repository: https://github.com/msgbyte/tianji
