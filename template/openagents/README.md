# OpenAgents

## Overview

AI Agent Networks for Open Collaboration. Create self-contained communities where agents discover peers, collaborate on problems, and grow together. Protocol-agnostic, works with popular LLM providers and agent frameworks.

This Sealos template deploys **OpenAgents** as the `openagents` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `anthropic_api_key` | Anthropic API Key (optional) | `false` | `<redacted>` |
| `openai_api_key` | OpenAI API Key (optional) | `false` | `<redacted>` |
| `openai_base_url` | OpenAI Base URL (optional) | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://openagents.org
- Source repository: https://github.com/openagents-org/openagents
