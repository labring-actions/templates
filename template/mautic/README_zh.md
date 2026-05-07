# mautic

## 应用概览

Mautic 是一款开源的营销自动化平台，提供电子邮件营销、客户旅程设计、潜在客户管理和行为跟踪等功能，帮助企业自动化营销流程、分析用户互动并个性化客户体验。

此 Sealos 模板会将 **mautic** 部署为 `mautic` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `TIMEZONE` | `TIMEZONE` 部署参数。 | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://www.mautic.org/
- 源码仓库: https://github.com/mautic/mautic
