# Lobe Chat Database Version

## Overview

An open-source, modern-design ChatGPT/LLMs UI/Framework. Supports speech-synthesis, multi-modal, and extensible (function call) plugin system.

This Sealos template deploys **Lobe Chat Database Version** as the `lobe-chat-db` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `AUTH_LOGTO_ID` | The Client ID of the Logto application. | `true` | `` |
| `AUTH_LOGTO_ISSUER` | The OpenID Connect issuer of the Logto application. | `true` | `` |
| `AUTH_LOGTO_SECRET` | The Client Secret of the Logto application. | `true` | `<redacted>` |
| `OPENAI_API_KEY` | This is the API key you apply on the OpenAI account page | `false` | `<redacted>` |
| `OPENAI_MODEL_LIST` | Used to control the model list. Use + to add a model, - to hide a model, and model_name=display_name to customize the display name of a model, separated by commas. | `false` | `` |
| `OPENAI_PROXY_URL` | If you manually configure the OpenAI interface proxy, you can use this configuration item to override the default OpenAI API request base URL | `false` | `https://api.openai.com/v1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/lobehub/lobe-chat
- Source repository: https://github.com/lobehub/lobe-chat
