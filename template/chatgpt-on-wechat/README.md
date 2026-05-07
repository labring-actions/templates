# chatgpt-on-wechat

## Overview

本项目是基于大模型的智能对话机器人，支持企业微信、微信公众号、飞书、钉钉接入，可选择GPT3.5/GPT4.0/Claude/文心一言/讯飞星火/通义千问/Gemini/LinkAI/ZhipuAI，能处理文本、语音和图片，通过插件访问操作系统和互联网等外部资源，支持基于自有知识库定制企业AI应用。

This Sealos template deploys **chatgpt-on-wechat** as the `chatgpt-on-wechat` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `CHANNEL_TYPE` | 渠道类型 | `true` | `wx` |
| `GROUP_CHAT_PREFIX` | 群聊前缀 | `false` | `["@bot"]` |
| `GROUP_NAME_WHITE_LIST` | 群聊白名单 | `false` | `["ALL_GROUP"]` |
| `MODEL` | 模型名称 | `true` | `gpt-3.5-turbo` |
| `OPEN_AI_API_BASE` | OpenAI API 基础地址，带v1 | `true` | `https://api.openai.com/v1` |
| `OPEN_AI_API_KEY` | OpenAI API KEY | `true` | `<redacted>` |
| `SINGLE_CHAT_PREFIX` | 单聊前缀 | `false` | `["bot"]` |
| `SINGLE_CHAT_REPLY_PREFIX` | 单聊回复前缀 | `false` | `"[bot] "` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/zhayujie/chatgpt-on-wechat
- Source repository: https://github.com/zhayujie/chatgpt-on-wechat
