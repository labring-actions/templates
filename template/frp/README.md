# frp

## Overview

frp 是一个专注于内网穿透的高性能的反向代理应用

This Sealos template deploys **frp** as the `frp` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ADMIN_PASSWORD` | admin dashboard's password | `true` | `<redacted>` |
| `ADMIN_USER` | admin dashboard's username | `true` | `admin` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/fatedier/frp
- Source repository: https://github.com/fatedier/frp
