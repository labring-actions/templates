# 雾锁王国私服

## Overview

该私服默认可容纳 4~8 个玩家流畅玩耍

This Sealos template deploys **雾锁王国私服** as the `enshrouded` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `SERVER_NAME` | 私服名称 | `false` | `` |
| `SERVER_PASSWORD` | 私服密码 | `false` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/mornedhels/enshrouded-server
- Source repository: https://github.com/mornedhels/enshrouded-server
