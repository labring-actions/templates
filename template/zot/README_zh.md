# Zot Registry

## 应用概览

Zot Registry 是一个 OCI 原生容器镜像仓库，默认启用基础认证，并支持在本地存储与 S3 兼容对象存储之间按需选择。

此 Sealos 模板会将 **Zot Registry** 部署为 `zot` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `zot_admin_htpasswd_hash` | `zot_admin_htpasswd_hash` 部署参数。 | `是` | `<已隐藏>` |
| `zot_admin_password` | `zot_admin_password` 部署参数。 | `是` | `<已隐藏>` |
| `zot_admin_user` | `zot_admin_user` 部署参数。 | `是` | `admin` |
| `zot_s3_region` | `zot_s3_region` 部署参数。 | `是` | `us-east-1` |
| `zot_storage_backend` | `zot_storage_backend` 部署参数。 | `是` | `filesystem` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://zotregistry.dev
- 源码仓库: https://github.com/project-zot/zot
