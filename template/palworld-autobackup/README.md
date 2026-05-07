# 帕鲁私服定时存档

## Overview

定时存档帕鲁私服数据

This Sealos template deploys **帕鲁私服定时存档** as the `palworld-autobackup` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `APP_NAME` | 帕鲁私服应用名称 | `true` | `` |
| `INTERVAL` | 每隔多少小时备份一次？单位是小时 | `true` | `3` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/yangchuansheng/templates-palworld
- Source repository: https://github.com/yangchuansheng/templates-palworld
