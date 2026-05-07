# PocketBase

## Overview

Open source backend consisting of embedded database (SQLite) with realtime subscriptions, built-in auth management, convenient dashboard UI and simple REST-ish API

This Sealos template deploys **PocketBase** as the `pocketbase` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_email` | Admin user email for login | `true` | `` |
| `admin_password` | Admin user password (minimum 8 characters) | `true` | `<redacted>` |
| `debug_mode` | Enable debug mode | `false` | `false` |
| `encryption_key` | Encryption key for settings (recommended for production, 32 characters) | `false` | `${{ random(32) }}` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://pocketbase.io/
- Source repository: https://github.com/adrianmusante/docker-pocketbase
