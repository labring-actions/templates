# Tolgee

## 应用概览

Tolgee 是一个开源的本地化平台，专为开发者设计，支持上下文直接翻译、一键生成翻译截图、生产环境实时编辑，并集成多种机器翻译服务（如 DeepL、Google Translate），提供翻译记忆与自动化功能，简化多语言应用的开发流程。

此 Sealos 模板会将 **Tolgee** 部署为 `tolgee` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `TOLGEE_AUTHENTICATION_INITIAL_PASSWORD` | `TOLGEE_AUTHENTICATION_INITIAL_PASSWORD` 部署参数。 | `是` | `<已隐藏>` |
| `TOLGEE_AUTHENTICATION_INITIAL_USERNAME` | `TOLGEE_AUTHENTICATION_INITIAL_USERNAME` 部署参数。 | `是` | `admin` |
| `TOLGEE_SMTP_AUTH` | `TOLGEE_SMTP_AUTH` 部署参数。 | `否` | `false` |
| `TOLGEE_SMTP_FROM` | `TOLGEE_SMTP_FROM` 部署参数。 | `否` | `test@test.com` |
| `TOLGEE_SMTP_HOST` | `TOLGEE_SMTP_HOST` 部署参数。 | `否` | `smtp.test.com` |
| `TOLGEE_SMTP_PASSWORD` | `TOLGEE_SMTP_PASSWORD` 部署参数。 | `否` | `<已隐藏>` |
| `TOLGEE_SMTP_PORT` | `TOLGEE_SMTP_PORT` 部署参数。 | `否` | `0` |
| `TOLGEE_SMTP_SSL_ENABLED` | `TOLGEE_SMTP_SSL_ENABLED` 部署参数。 | `否` | `false` |
| `TOLGEE_SMTP_USERNAME` | `TOLGEE_SMTP_USERNAME` 部署参数。 | `否` | `test` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://tolgee.io/
- 源码仓库: https://github.com/tolgee/tolgee-platform
