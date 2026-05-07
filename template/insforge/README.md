# InsForge

## Overview

InsForge is the Agent-Native Supabase Alternative, enabling AI agents to build and manage full-stack applications autonomously.

This Sealos template deploys **InsForge** as the `insforge` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_email` | Administrator email address | `false` | `admin@example.com` |
| `admin_password` | Administrator password | `true` | `<redacted>` |
| `apple_client_id` | Apple OAuth client ID | `false` | `` |
| `apple_client_secret` | Apple OAuth client secret | `false` | `<redacted>` |
| `discord_client_id` | Discord OAuth client ID | `false` | `` |
| `discord_client_secret` | Discord OAuth client secret | `false` | `<redacted>` |
| `github_client_id` | GitHub OAuth client ID | `false` | `` |
| `github_client_secret` | GitHub OAuth client secret | `false` | `<redacted>` |
| `google_client_id` | Google OAuth client ID | `false` | `` |
| `google_client_secret` | Google OAuth client secret | `false` | `<redacted>` |
| `linkedin_client_id` | LinkedIn OAuth client ID | `false` | `` |
| `linkedin_client_secret` | LinkedIn OAuth client secret | `false` | `<redacted>` |
| `microsoft_client_id` | Microsoft OAuth client ID | `false` | `` |
| `microsoft_client_secret` | Microsoft OAuth client secret | `false` | `<redacted>` |
| `openrouter_api_key` | OpenRouter API key | `false` | `<redacted>` |
| `x_client_id` | X OAuth client ID | `false` | `` |
| `x_client_secret` | X OAuth client secret | `false` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://insforge.dev
- Source repository: https://github.com/insforge/insforge
