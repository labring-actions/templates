# OpenDeepWiki

## Overview

由于涉及到Github仓库拉取等功能，建议部署在新加坡服务器上。OpenDeepWiki 是参考DeepWiki 作为灵感，基于 .NET 9 和 Semantic Kernel 开发的开源项目。它旨在帮助开发者更好地理解和使用代码库，提供代码分析、文档生成、知识图谱等功能。

This Sealos template deploys **OpenDeepWiki** as the `OpenDeepWiki` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `DB_CONNECTION_STRING` | - | `false` | `Data Source=/data/KoalaWiki.db` |
| `DB_TYPE` | 数据库类型 | `false` | `sqlite` |
| `ENABLE_INCREMENTAL_UPDATE` | 是否启用增量更新 | `false` | `true` |
| `EnableSmartFilter` | 是否启用智能过滤，这可能影响AI得到仓库的文件目录 | `false` | `true` |
| `KOALAWIKI_REPOSITORIES` | 存放仓库的位置 | `false` | `/repositories` |
| `LANGUAGE` | 中文 或 English | `false` | `中文` |
| `REPAIR_MERMAID` | 是否修复Mermaid，1为修复，其他为不修复 | `false` | `1` |
| `TASK_MAX_SIZE_PER_USER` | 每个用户AI处理文档生成的最大数量 | `false` | `5` |
| `UPDATE_INTERVAL` | 仓库增量更新间隔 | `false` | `5` |
| `analysis_model` | 分析模型，用于生成仓库目录结构，建议gpt-4.1 | `true` | `${{ defaults.model }}` |
| `api_endpoint` | 输入你的API接口 | `true` | `${{ defaults.api_server }}` |
| `api_key` | 输入API Key | `true` | `<redacted>` |
| `chat_model` | 必须要支持function的模型 | `true` | `${{ defaults.model }}` |
| `volume_size_data` | 保存文档（Gi） | `true` | `1` |
| `volume_size_repositories` | 保存仓库 (Gi) | `true` | `3` |
| `wiki_image` | wiki后端的镜像 | `false` | `${{ defaults.wiki_image }}` |
| `wiki_web_image` | wiki后端的镜像 | `false` | `${{ defaults.wiki_web_image }}` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://opendeep.wiki
- Source repository: https://github.com/AIDotNet/OpenDeepWiki
