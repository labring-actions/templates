# InsForge

## 应用概览

InsForge 是面向 AI 编码代理的后端平台替代方案，支持数据库、认证、存储与函数能力的一体化部署。

此 Sealos 模板会将 **InsForge** 部署为 `insforge` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `admin_email` | `admin_email` 部署参数。 | `否` | `admin@example.com` |
| `admin_password` | `admin_password` 部署参数。 | `是` | `<已隐藏>` |
| `apple_client_id` | `apple_client_id` 部署参数。 | `否` | `` |
| `apple_client_secret` | `apple_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `discord_client_id` | `discord_client_id` 部署参数。 | `否` | `` |
| `discord_client_secret` | `discord_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `github_client_id` | `github_client_id` 部署参数。 | `否` | `` |
| `github_client_secret` | `github_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `google_client_id` | `google_client_id` 部署参数。 | `否` | `` |
| `google_client_secret` | `google_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `linkedin_client_id` | `linkedin_client_id` 部署参数。 | `否` | `` |
| `linkedin_client_secret` | `linkedin_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `microsoft_client_id` | `microsoft_client_id` 部署参数。 | `否` | `` |
| `microsoft_client_secret` | `microsoft_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `openrouter_api_key` | `openrouter_api_key` 部署参数。 | `否` | `<已隐藏>` |
| `x_client_id` | `x_client_id` 部署参数。 | `否` | `` |
| `x_client_secret` | `x_client_secret` 部署参数。 | `否` | `<已隐藏>` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://insforge.dev
- 源码仓库: https://github.com/insforge/insforge
