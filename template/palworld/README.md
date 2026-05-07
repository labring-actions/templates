# 幻兽帕鲁私服

## Overview

该私服默认最多可容纳 4~6 个玩家流畅玩耍，如需支撑更多玩家则需要调大 CPU 和内存

This Sealos template deploys **幻兽帕鲁私服** as the `palworld` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ADMIN_PASSWORD` | Secure administration access in the server with a password | `true` | `<redacted>` |
| `SERVER_NAME` | A name for your community server | `false` | `` |
| `SERVER_PASSWORD` | Secure your community server with a password | `false` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/thijsvanloef/palworld-server-docker
- Source repository: https://github.com/thijsvanloef/palworld-server-docker
