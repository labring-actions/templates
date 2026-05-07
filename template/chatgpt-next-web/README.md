# chatgpt-next-web

## Overview

A cross-platform ChatGPT/Gemini UI.

This Sealos template deploys **chatgpt-next-web** as the `chatgpt-next-web` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `AZURE_API_KEY` | Azure 密钥 | `false` | `<redacted>` |
| `AZURE_API_VERSION` | Azure API 版本 | `false` | `` |
| `AZURE_URL` | Azure 部署地址 | `false` | `https://{azure-resource-url}/openai/deployments/{deploy-name}` |
| `BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `false` | `https://api.openai.com` |
| `CODE` | 设置页面中的访问密码，可以使用逗号隔开多个密码 | `false` | `` |
| `DISABLE_GPT4` | 如果你不想让用户使用 GPT-4，将此环境变量设置为 1 即可 | `false` | `` |
| `HIDE_BALANCE_QUERY` | 如果你想启用余额查询功能，将此环境变量设置为 1 即可 | `false` | `` |
| `HIDE_USER_API_KEY` | 如果你不想让用户自行填入 API Key，将此环境变量设置为 1 即可 | `false` | `<redacted>` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥，使用英文逗号隔开多个 key，这样可以随机轮询这些 key | `true` | `<redacted>` |
| `OPENAI_ORG_ID` | 指定 OpenAI 中的组织 ID | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/Yidadaa/ChatGPT-Next-Web
- Source repository: https://github.com/Yidadaa/ChatGPT-Next-Web
