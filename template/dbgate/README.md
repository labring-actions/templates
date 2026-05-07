# DbGate

## Overview

DbGate is cross-platform database manager. It is designed to be simple to use and effective, when working with more databases simultaneously. But there are also many advanced features like schema compare, visual query designer, chart visualisation or batch export and import.

This Sealos template deploys **DbGate** as the `dbgate` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `token_lifetime` | Set token lifetime | `false` | `<redacted>` |
| `user_name` | Set username | `true` | `admin` |
| `user_password` | Set password | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://dbgate.org
- Source repository: https://github.com/dbgate/dbgate
