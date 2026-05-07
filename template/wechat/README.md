# 微信

## Overview

Linux 版微信。该项目允许用户通过网页或 VNC 访问微信，从而在不同的操作系统和环境中使用微信，无需直接在本地安装。

This Sealos template deploys **微信** as the `wechat` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `STORAGE_SIZE` | 给微信分配的存储空间大小(单位:GB) | `true` | `` |
| `VNC_PASSWORD` | 连接到应用程序GUI所需的密码 | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/RICwang/docker-wechat
- Source repository: https://github.com/RICwang/docker-wechat
