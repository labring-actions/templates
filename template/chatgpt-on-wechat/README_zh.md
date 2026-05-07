# chatgpt-on-wechat

## 应用概览

chatgpt-on-wechat 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **chatgpt-on-wechat** 部署为 `chatgpt-on-wechat` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `CHANNEL_TYPE` | 渠道类型 | `是` | `wx` |
| `GROUP_CHAT_PREFIX` | 群聊前缀 | `否` | `["@bot"]` |
| `GROUP_NAME_WHITE_LIST` | 群聊白名单 | `否` | `["ALL_GROUP"]` |
| `MODEL` | 模型名称 | `是` | `gpt-3.5-turbo` |
| `OPEN_AI_API_BASE` | OpenAI API 基础地址，带v1 | `是` | `https://api.openai.com/v1` |
| `OPEN_AI_API_KEY` | `OPEN_AI_API_KEY` 部署参数。 | `是` | `<已隐藏>` |
| `SINGLE_CHAT_PREFIX` | 单聊前缀 | `否` | `["bot"]` |
| `SINGLE_CHAT_REPLY_PREFIX` | 单聊回复前缀 | `否` | `"[bot] "` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/zhayujie/chatgpt-on-wechat
- 源码仓库: https://github.com/zhayujie/chatgpt-on-wechat
