# 帕鲁管理器

## Overview

通过图形化界面管理幻兽帕鲁 / PalWorld 专用服务器

This Sealos template deploys **帕鲁管理器** as the `palworld-management` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ADMIN_PASSWORD` | 帕鲁私服管理员密码 | `true` | `<redacted>` |
| `APP_NAME` | 帕鲁私服应用名称 | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/zaigie/palworld-server-tool
- Source repository: https://github.com/zaigie/palworld-server-tool
