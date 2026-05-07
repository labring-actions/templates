# OpenClaw

## Overview

AI agent gateway with multi-channel support including WhatsApp, Telegram, and Discord integration

This Sealos template deploys **OpenClaw** as the `openclaw` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `api_key` | Provider API key | `true` | `<redacted>` |
| `base_url` | Compatible provider base URL (must end with /v1 for OpenAI-compatible) | `true` | `https://aiproxy.usw-1.sealos.io/v1` |
| `model` | Default model id (raw id, e.g. gpt-5.2 / claude-opus-4-6-20251101) | `true` | `claude-opus-4-6` |
| `provider_kind` | provider kind (openai_compat or anthropic_compat) | `true` | `anthropic_compat` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://openclaw.ai/
- Source repository: https://github.com/openclaw/openclaw
