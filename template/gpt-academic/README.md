# gpt-academic

## Overview

GPT Academic Optimization

This Sealos template deploys **gpt-academic** as the `gpt-academic` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ADD_WAIFU` | 加一个 live2d 看板娘装饰 | `false` | `True` |
| `API_KEY` | 可同时填写多个 API-KEY，用英文逗号分割 | `true` | `<redacted>` |
| `API_URL_REDIRECT` | 重新URL重新定向，实现更换API_URL的作用 | `false` | `` |
| `AVAIL_LLM_MODELS` | 所有可用模型 | `false` | `["gpt-3.5-turbo", "api2d-gpt-3.5-turbo", "gpt-4", "api2d-gpt-4", "sparkv2", "qianfan"]` |
| `LLM_MODEL` | 模型选择 | `false` | `gpt-3.5-turbo` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/binary-husky/gpt_academic
- Source repository: https://github.com/binary-husky/gpt_academic
