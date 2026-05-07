# Stirling-PDF

## 应用概览

Stirling-PDF 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **Stirling-PDF** 部署为 `s-pdf` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `DOCKER_ENABLE_SECURITY` | `DOCKER_ENABLE_SECURITY` 部署参数。 | `否` | `false` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` 部署参数。 | `否` | `true` |
| `LANGS` | `LANGS` 部署参数。 | `否` | `en-GB,en-US,zh-CN,zh-TW` |
| `METRICS_ENABLED` | `METRICS_ENABLED` 部署参数。 | `否` | `true` |
| `SECURITY_ENABLELOGIN` | `SECURITY_ENABLELOGIN` 部署参数。 | `否` | `false` |
| `SYSTEM_DEFAULTLOCALE` | `SYSTEM_DEFAULTLOCALE` 部署参数。 | `否` | `en-US` |
| `SYSTEM_GOOGLEVISIBILITY` | `SYSTEM_GOOGLEVISIBILITY` 部署参数。 | `否` | `true` |
| `UI_APPNAME` | `UI_APPNAME` 部署参数。 | `否` | `Stirling-PDF` |
| `UI_APPNAMENAVBAR` | `UI_APPNAMENAVBAR` 部署参数。 | `否` | `Stirling-PDF` |
| `UI_HOMEDESCRIPTION` | `UI_HOMEDESCRIPTION` 部署参数。 | `否` | `Demo site for Stirling-PDF` |
| `use_postgresql` | `use_postgresql` 部署参数。 | `否` | `false` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/Stirling-Tools/Stirling-PDF
- 源码仓库: https://github.com/Stirling-Tools/Stirling-PDF
