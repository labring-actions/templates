# NetBird

## Overview

基于 WireGuard 的零信任网络平台，支持自托管管理、信令与中继。

This Sealos template deploys **NetBird** as the `netbird` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `disable_default_policy` | Disable default all-to-all policy | `true` | `false` |
| `external_turn_host` | External TURN host and port (example: turn.example.com:3478) | `false` | `` |
| `external_turn_password` | External TURN password (required when external TURN is used) | `false` | `<redacted>` |
| `external_turn_username` | External TURN username (required when external TURN is used) | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://netbird.io/
- Source repository: https://github.com/netbirdio/netbird
