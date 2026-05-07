# chatany

## 应用概览

chatany 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **chatany** 部署为 `chatany` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `否` | `` |
| `CODE` | 设置页面中的访问密码 | `否` | `` |
| `MJ_CHANNEL_ID` | Discord 频道 ID | `是` | `` |
| `MJ_DISCORD_CDN_PROXY` | Discord CDN 代理域名 | `否` | `https://cdn.discordapp.com` |
| `MJ_DISCORD_PROXY` | Discord 代理域名 | `否` | `https://discord.com` |
| `MJ_DISCORD_WSS_PROXY` | Discord Websocket 代理域名 | `否` | `wss://gateway.discord.gg` |
| `MJ_SERVER_ID` | Discord 服务器 ID | `是` | `` |
| `MJ_USER_TOKEN` | Discord 用户 Token | `是` | `<已隐藏>` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥 | `是` | `<已隐藏>` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/ChatAnyTeam/ChatAny
- 源码仓库: https://github.com/ChatAnyTeam/ChatAny
