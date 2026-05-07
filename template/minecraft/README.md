# Minecraft

## Overview

Minecraft 专有版服务器，支持 Forge 和 Fabric。

This Sealos template deploys **Minecraft** as the `minecraft` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `TYPE` | server type | `true` | `PAPER` |
| `VERSION` | minecraft version | `true` | `LATEST` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://docker-minecraft-server.readthedocs.io/en/latest/
- Source repository: https://github.com/itzg/docker-minecraft-server
