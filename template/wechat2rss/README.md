# Wechat2RSS

## Overview

自建微信公众号RSS服务

This Sealos template deploys **Wechat2RSS** as the `wechat2rss` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `LIC_CODE` | 激活码 | `true` | `` |
| `LIC_EMAIL` | 邮箱 | `true` | `` |
| `RSS_HOST` | 服务域名 | `true` | `${{ defaults.app_host + '.' + SEALOS_CLOUD_DOMAIN }}` |
| `RSS_HTTPS` | 开启HTTPS | `false` | `1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://wechat2rss.xlab.app/
- Source repository: https://github.com/ttttmr/Wechat2RSS
