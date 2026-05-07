# Nakama Server

## Overview

Nakama is an open-source game server for real-time multiplayer, social features, and live ops.

This Sealos template deploys **Nakama Server** as the `nakama` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `console_password` | Nakama Console admin password (set for initial login) | `true` | `<redacted>` |
| `console_username` | Nakama Console admin username (overrides the default) | `true` | `admin` |
| `enable_grpc` | Expose gRPC ports 7348/7349 publicly | `false` | `false` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://heroiclabs.com/nakama/
- Source repository: https://github.com/heroiclabs/nakama
