# AskTable

## Overview

AskTable.com 表格智能体（Table Agent as a Service），专为企业提供基于自然语言的数据分析体验，支持 Excel、数据库和数据仓库的智能查询。用户无需懂 SQL，只需用“说”的方式，即可获得实时数据洞察，广泛应用于运营、财务、人事、销售等业务场景。

This Sealos template deploys **AskTable** as the `asktable` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `LLM_API_KEY` | AI 模型令牌 | `true` | `<redacted>` |
| `LLM_BASE_URL` | 用于访问大语言模型的 API 地址，比如“https://api.openai.com/v1”。默认使用 AskTable 模型API地址。 | `false` | `https://aiproxy.asktable.com/v1` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://asktable.com/
- Source repository: https://github.com/DataMini/asktable-all-in-one
