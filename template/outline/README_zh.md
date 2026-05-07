# Outline

## 应用概览

为成长型团队打造的最快速的知识库。美观、实时协作、功能丰富且兼容 Markdown。

此 Sealos 模板会将 **Outline** 部署为 `outline` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `auth_provider` | `auth_provider` 部署参数。 | `是` | `oidc` |
| `google_client_id` | `google_client_id` 部署参数。 | `是` | `` |
| `google_client_secret` | `google_client_secret` 部署参数。 | `是` | `<已隐藏>` |
| `oidc_auth_uri` | `oidc_auth_uri` 部署参数。 | `是` | `` |
| `oidc_client_id` | `oidc_client_id` 部署参数。 | `是` | `` |
| `oidc_client_secret` | `oidc_client_secret` 部署参数。 | `是` | `<已隐藏>` |
| `oidc_token_uri` | `oidc_token_uri` 部署参数。 | `是` | `<已隐藏>` |
| `oidc_userinfo_uri` | `oidc_userinfo_uri` 部署参数。 | `是` | `` |
| `secret_key` | `secret_key` 部署参数。 | `是` | `<已隐藏>` |
| `slack_client_id` | `slack_client_id` 部署参数。 | `是` | `` |
| `slack_client_secret` | `slack_client_secret` 部署参数。 | `是` | `<已隐藏>` |
| `smtp_enabled` | `smtp_enabled` 部署参数。 | `否` | `false` |
| `smtp_from_email` | `smtp_from_email` 部署参数。 | `是` | `` |
| `smtp_host` | `smtp_host` 部署参数。 | `是` | `` |
| `smtp_password` | `smtp_password` 部署参数。 | `是` | `<已隐藏>` |
| `smtp_port` | `smtp_port` 部署参数。 | `是` | `587` |
| `smtp_username` | `smtp_username` 部署参数。 | `是` | `` |
| `storage_type` | `storage_type` 部署参数。 | `是` | `s3` |
| `utils_secret` | `utils_secret` 部署参数。 | `是` | `<已隐藏>` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://www.getoutline.com/
- 源码仓库: https://github.com/outline/outline
