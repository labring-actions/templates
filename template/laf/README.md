# Laf

## Overview

Laf 是开源的云开发平台，提供云函数、云数据库、云存储等开箱即用的应用资源。让开发者专注于业务开发，无需折腾服务器，快速释放创意。

This Sealos template deploys **Laf** as the `laf` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `domain` | the domain of laf | `true` | `laf-${{ random(8) }}` |
| `minio_storage` | Storage size for minio in Gi | `true` | `5` |
| `prometheus_storage` | Storage size for Prometheus in Gi | `true` | `10` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://laf.run/
- Source repository: https://github.com/labring/laf
