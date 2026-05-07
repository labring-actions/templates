# Nakama Server

## 应用概览

Nakama 是一个开源的游戏开发平台，能自动处理用户登录、实时聊天、排行榜、成就系统，还能智能匹配玩家。

此 Sealos 模板会将 **Nakama Server** 部署为 `nakama` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `console_password` | `console_password` 部署参数。 | `是` | `<已隐藏>` |
| `console_username` | `console_username` 部署参数。 | `是` | `admin` |
| `enable_grpc` | `enable_grpc` 部署参数。 | `否` | `false` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://heroiclabs.com/nakama/
- 源码仓库: https://github.com/heroiclabs/nakama
