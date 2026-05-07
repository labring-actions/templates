# OpenList

## Overview

OpenList 是一个有韧性、长期治理、社区驱动的 AList 分支，旨在防御基于信任的开源攻击。

This Sealos template deploys **OpenList** as the `openlist` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `PASSWORD` | 默认密码 | `true` | `<redacted>` |
| `USERNAME` | 默认用户名 | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://doc.oplist.org
- Source repository: https://github.com/OpenListTeam/OpenList
