# chatgpt-next-web

## 应用概览

chatgpt-next-web 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **chatgpt-next-web** 部署为 `chatgpt-next-web` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `AZURE_API_KEY` | Azure 密钥 | `否` | `<已隐藏>` |
| `AZURE_API_VERSION` | Azure API 版本 | `否` | `` |
| `AZURE_URL` | Azure 部署地址 | `否` | `https://{azure-resource-url}/openai/deployments/{deploy-name}` |
| `BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `否` | `https://api.openai.com` |
| `CODE` | 设置页面中的访问密码，可以使用逗号隔开多个密码 | `否` | `` |
| `DISABLE_GPT4` | 如果你不想让用户使用 GPT-4，将此环境变量设置为 1 即可 | `否` | `` |
| `HIDE_BALANCE_QUERY` | 如果你想启用余额查询功能，将此环境变量设置为 1 即可 | `否` | `` |
| `HIDE_USER_API_KEY` | 如果你不想让用户自行填入 API Key，将此环境变量设置为 1 即可 | `否` | `<已隐藏>` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥，使用英文逗号隔开多个 key，这样可以随机轮询这些 key | `是` | `<已隐藏>` |
| `OPENAI_ORG_ID` | 指定 OpenAI 中的组织 ID | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/Yidadaa/ChatGPT-Next-Web
- 源码仓库: https://github.com/Yidadaa/ChatGPT-Next-Web
