# Sub2API

## 应用概览

面向上游 AI 服务订阅额度分发与管理的 API 网关平台，支持多账号接入、密钥分发、计费与调度。

此 Sealos 模板会将 **Sub2API** 部署为 `sub2api` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `admin_email` | `admin_email` 部署参数。 | `否` | `admin@sub2api.local` |
| `admin_password` | `admin_password` 部署参数。 | `否` | `<已隐藏>` |
| `antigravity_oauth_client_secret` | `antigravity_oauth_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `gemini_cli_oauth_client_secret` | `gemini_cli_oauth_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `gemini_oauth_client_id` | `gemini_oauth_client_id` 部署参数。 | `否` | `` |
| `gemini_oauth_client_secret` | `gemini_oauth_client_secret` 部署参数。 | `否` | `<已隐藏>` |
| `gemini_oauth_scopes` | `gemini_oauth_scopes` 部署参数。 | `否` | `` |
| `gemini_quota_policy` | `gemini_quota_policy` 部署参数。 | `否` | `` |
| `run_mode` | `run_mode` 部署参数。 | `否` | `standard` |
| `security_url_allowlist_allow_insecure_http` | `security_url_allowlist_allow_insecure_http` 部署参数。 | `否` | `false` |
| `security_url_allowlist_allow_private_hosts` | `security_url_allowlist_allow_private_hosts` 部署参数。 | `否` | `false` |
| `security_url_allowlist_enabled` | `security_url_allowlist_enabled` 部署参数。 | `否` | `false` |
| `security_url_allowlist_upstream_hosts` | `security_url_allowlist_upstream_hosts` 部署参数。 | `否` | `` |
| `timezone` | `timezone` 部署参数。 | `否` | `Asia/Shanghai` |
| `update_proxy_url` | `update_proxy_url` 部署参数。 | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://demo.sub2api.org/
- 源码仓库: https://github.com/Wei-Shaw/sub2api
