# Lobe Chat

## Overview

An open-source, modern-design ChatGPT/LLMs UI/Framework. Supports speech-synthesis, multi-modal, and extensible (function call) plugin system.

This Sealos template deploys **Lobe Chat** as the `lobe-chat` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ACCESS_CODE` | Add a password to access this service; you can set a long password to avoid leaking. If this value contains a comma, it is a password array. | `false` | `` |
| `OPENAI_API_KEY` | This is the API key you apply on the OpenAI account page | `false` | `<redacted>` |
| `OPENAI_MODEL_LIST` | Used to control the model list. Use + to add a model, - to hide a model, and model_name=display_name to customize the display name of a model, separated by commas. | `false` | `` |
| `OPENAI_PROXY_URL` | If you manually configure the OpenAI interface proxy, you can use this configuration item to override the default OpenAI API request base URL | `false` | `https://api.openai.com/v1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/lobehub/lobe-chat
- Source repository: https://github.com/lobehub/lobe-chat
