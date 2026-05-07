# OpenDeepWiki

## 应用概览

OpenDeepWiki 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **OpenDeepWiki** 部署为 `OpenDeepWiki` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `DB_CONNECTION_STRING` | `DB_CONNECTION_STRING` 部署参数。 | `否` | `Data Source=/data/KoalaWiki.db` |
| `DB_TYPE` | 数据库类型 | `否` | `sqlite` |
| `ENABLE_INCREMENTAL_UPDATE` | 是否启用增量更新 | `否` | `true` |
| `EnableSmartFilter` | 是否启用智能过滤，这可能影响AI得到仓库的文件目录 | `否` | `true` |
| `KOALAWIKI_REPOSITORIES` | 存放仓库的位置 | `否` | `/repositories` |
| `LANGUAGE` | 中文 或 English | `否` | `中文` |
| `REPAIR_MERMAID` | 是否修复Mermaid，1为修复，其他为不修复 | `否` | `1` |
| `TASK_MAX_SIZE_PER_USER` | 每个用户AI处理文档生成的最大数量 | `否` | `5` |
| `UPDATE_INTERVAL` | 仓库增量更新间隔 | `否` | `5` |
| `analysis_model` | 分析模型，用于生成仓库目录结构，建议gpt-4.1 | `是` | `${{ defaults.model }}` |
| `api_endpoint` | 输入你的API接口 | `是` | `${{ defaults.api_server }}` |
| `api_key` | 输入API Key | `是` | `<已隐藏>` |
| `chat_model` | 必须要支持function的模型 | `是` | `${{ defaults.model }}` |
| `volume_size_data` | 保存文档（Gi） | `是` | `1` |
| `volume_size_repositories` | 保存仓库 (Gi) | `是` | `3` |
| `wiki_image` | wiki后端的镜像 | `否` | `${{ defaults.wiki_image }}` |
| `wiki_web_image` | wiki后端的镜像 | `否` | `${{ defaults.wiki_web_image }}` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://opendeep.wiki
- 源码仓库: https://github.com/AIDotNet/OpenDeepWiki
