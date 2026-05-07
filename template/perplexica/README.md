# Perplexica

## Overview

Perplexica is an open-source AI-powered searching tool or an AI-powered search engine that goes deep into the internet to find answers.

This Sealos template deploys **Perplexica** as the `perplexica` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `OPENAI_API_KEY` | The API Key of the OpenAI-compatible service | `true` | `<redacted>` |
| `OPENAI_API_URL` | The API URL of the OpenAI-compatible service (e.g. "https://api.openai.com/v1" for official API, or custom endpoint URL that follows OpenAI API format/structure) | `true` | `https://api.openai.com/v1` |
| `OPENAI_MODEL_NAME` | The model name of the OpenAI-compatible service | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/ItzCrazyKns/Perplexica
- Source repository: https://github.com/ItzCrazyKns/Perplexica
