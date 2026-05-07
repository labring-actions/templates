# NetBird

## 应用概览

基于 WireGuard 的零信任网络平台，支持自托管管理、信令与中继。

此 Sealos 模板会将 **NetBird** 部署为 `netbird` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `disable_default_policy` | `disable_default_policy` 部署参数。 | `是` | `false` |
| `external_turn_host` | `external_turn_host` 部署参数。 | `否` | `` |
| `external_turn_password` | `external_turn_password` 部署参数。 | `否` | `<已隐藏>` |
| `external_turn_username` | `external_turn_username` 部署参数。 | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://netbird.io/
- 源码仓库: https://github.com/netbirdio/netbird
