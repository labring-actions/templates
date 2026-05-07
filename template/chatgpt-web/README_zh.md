# chatgpt-web

## 应用概览

chatgpt-web 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **chatgpt-web** 部署为 `chatgpt-web` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `AUTH_SECRET_KEY` | 访问权限密钥 | `否` | `<已隐藏>` |
| `HTTPS_PROXY` | HTTPS 代理，支持 http，https，socks5 | `否` | `` |
| `MAX_REQUEST_PER_HOUR` | 每小时最大请求次数 | `否` | `` |
| `OPENAI_API_BASE_URL` | 如果你手动配置了 OpenAI 接口代理，可以使用此配置项来覆盖默认的 OpenAI API 请求基础 URL | `否` | `` |
| `OPENAI_API_KEY` | 这是你在 OpenAI 账户页面申请的 API 密钥 | `是` | `<已隐藏>` |
| `OPENAI_API_MODEL` | API 模型 | `否` | `` |
| `SOCKS_PROXY_HOST` | Socks代理，和 SOCKS_PROXY_PORT 一起时生效 | `否` | `` |
| `SOCKS_PROXY_PORT` | Socks代理端口，和 SOCKS_PROXY_HOST 一起时生效 | `否` | `` |
| `TIMEOUT_MS` | 超时，单位毫秒 | `否` | `` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/Chanzhaoyu/chatgpt-web
- 源码仓库: https://github.com/Chanzhaoyu/chatgpt-web
