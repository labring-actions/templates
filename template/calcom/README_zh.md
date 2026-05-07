# Cal.com

## 应用概览

开源日程预约平台，适合个人、团队与企业自托管。

此 Sealos 模板会将 **Cal.com** 部署为 `calcom` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `calcom_license_key` | `calcom_license_key` 部署参数。 | `否` | `` |
| `email_from` | `email_from` 部署参数。 | `否` | `` |
| `email_from_name` | `email_from_name` 部署参数。 | `否` | `Cal.com` |
| `email_server_host` | `email_server_host` 部署参数。 | `否` | `` |
| `email_server_password` | `email_server_password` 部署参数。 | `否` | `<已隐藏>` |
| `email_server_port` | `email_server_port` 部署参数。 | `否` | `587` |
| `email_server_user` | `email_server_user` 部署参数。 | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://cal.com/
- 源码仓库: https://github.com/calcom/cal.com
