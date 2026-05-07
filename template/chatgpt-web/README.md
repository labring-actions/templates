# chatgpt-web

## Overview

A ChatGPT Interactive Demo Web Application Developed with Express and Vue3.

This Sealos template deploys **chatgpt-web** as the `chatgpt-web` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `AUTH_SECRET_KEY` | 访问权限密钥 | `false` | `<redacted>` |
| `HTTPS_PROXY` | HTTPS 代理，支持 http，https，socks5 | `false` | `` |
| `MAX_REQUEST_PER_HOUR` | 每小时最大请求次数 | `false` | `` |
| `OPENAI_API_BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `false` | `` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥 | `true` | `<redacted>` |
| `OPENAI_API_MODEL` | API 模型 | `false` | `` |
| `SOCKS_PROXY_HOST` | Socks代理，和 SOCKS_PROXY_PORT 一起时生效 | `false` | `` |
| `SOCKS_PROXY_PORT` | Socks代理端口，和 SOCKS_PROXY_HOST 一起时生效 | `false` | `` |
| `TIMEOUT_MS` | 超时，单位毫秒 | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/Chanzhaoyu/chatgpt-web
- Source repository: https://github.com/Chanzhaoyu/chatgpt-web
