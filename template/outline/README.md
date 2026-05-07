# Outline

## Overview

The fastest knowledge base for growing teams. Beautiful, realtime collaborative, feature packed, and markdown compatible.

This Sealos template deploys **Outline** as the `outline` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `auth_provider` | Authentication provider | `true` | `oidc` |
| `google_client_id` | Google OAuth Client ID | `true` | `` |
| `google_client_secret` | Google OAuth Client Secret | `true` | `<redacted>` |
| `oidc_auth_uri` | OIDC Authorization URI | `true` | `` |
| `oidc_client_id` | OIDC Client ID | `true` | `` |
| `oidc_client_secret` | OIDC Client Secret | `true` | `<redacted>` |
| `oidc_token_uri` | OIDC Token URI | `true` | `<redacted>` |
| `oidc_userinfo_uri` | OIDC User Info URI | `true` | `` |
| `secret_key` | Secret key for encrypting data (32 bytes hex) | `true` | `<redacted>` |
| `slack_client_id` | Slack OAuth Client ID | `true` | `` |
| `slack_client_secret` | Slack OAuth Client Secret | `true` | `<redacted>` |
| `smtp_enabled` | Enable SMTP for sending emails | `false` | `false` |
| `smtp_from_email` | SMTP From Email Address | `true` | `` |
| `smtp_host` | SMTP Server Host | `true` | `` |
| `smtp_password` | SMTP Password | `true` | `<redacted>` |
| `smtp_port` | SMTP Server Port | `true` | `587` |
| `smtp_username` | SMTP Username | `true` | `` |
| `storage_type` | Storage type for attachments | `true` | `s3` |
| `utils_secret` | Utility secret for internal operations | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.getoutline.com/
- Source repository: https://github.com/outline/outline
