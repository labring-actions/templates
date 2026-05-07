# Paperless-ngx

## 应用概览

Paperless-ngx 是一个社区支持的开源文档管理系统，可以将您的纸质文档转换为可搜索的在线档案，让您减少纸张使用。

此 Sealos 模板会将 **Paperless-ngx** 部署为 `paperless-ngx` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `admin_mail` | `admin_mail` 部署参数。 | `是` | `admin@example.com` |
| `admin_password` | `admin_password` 部署参数。 | `是` | `<已隐藏>` |
| `admin_user` | `admin_user` 部署参数。 | `是` | `` |
| `paperless_ocr_language` | `paperless_ocr_language` 部署参数。 | `否` | `eng` |
| `paperless_ocr_languages` | `paperless_ocr_languages` 部署参数。 | `否` | `` |
| `paperless_secret_key` | `paperless_secret_key` 部署参数。 | `否` | `<已隐藏>` |
| `paperless_time_zone` | `paperless_time_zone` 部署参数。 | `否` | `UTC` |
| `usermap_gid` | `usermap_gid` 部署参数。 | `否` | `1000` |
| `usermap_uid` | `usermap_uid` 部署参数。 | `否` | `1000` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://paperless-ngx.com/
- 源码仓库: https://github.com/paperless-ngx/paperless-ngx
