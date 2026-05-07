# chatany

## Overview

One-click to own your own ChatGPT+StabilityAI+Midjourney web service

This Sealos template deploys **chatany** as the `chatany` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `false` | `` |
| `CODE` | 设置页面中的访问密码 | `false` | `` |
| `MJ_CHANNEL_ID` | Discord 频道 ID | `true` | `` |
| `MJ_DISCORD_CDN_PROXY` | Discord CDN 代理域名 | `false` | `https://cdn.discordapp.com` |
| `MJ_DISCORD_PROXY` | Discord 代理域名 | `false` | `https://discord.com` |
| `MJ_DISCORD_WSS_PROXY` | Discord Websocket 代理域名 | `false` | `wss://gateway.discord.gg` |
| `MJ_SERVER_ID` | Discord 服务器 ID | `true` | `` |
| `MJ_USER_TOKEN` | Discord 用户 Token | `true` | `<redacted>` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥 | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/ChatAnyTeam/ChatAny
- Source repository: https://github.com/ChatAnyTeam/ChatAny
