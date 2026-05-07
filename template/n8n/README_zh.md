# N8N

## 应用概览

n8n 是一个工作流自动化平台，通过将代码的灵活性与无代码的速度相结合，帮助技术团队构建自动化流程。

此 Sealos 模板会将 **N8N** 部署为 `n8n` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `timezone` | `timezone` 部署参数。 | `否` | `America/New_York` |
| `use_postgresql` | `use_postgresql` 部署参数。 | `否` | `false` |
| `use_queue_mode` | `use_queue_mode` 部署参数。 | `否` | `false` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://n8n.io/
- 源码仓库: https://github.com/n8n-io/n8n
