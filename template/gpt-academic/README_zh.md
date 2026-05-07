# gpt-academic

## 应用概览

gpt-academic 是一个可在 Sealos 上一键部署的应用，模板会创建所需资源并提供应用访问入口。

此 Sealos 模板会将 **gpt-academic** 部署为 `gpt-academic` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `ADD_WAIFU` | 加一个 live2d 看板娘装饰 | `否` | `True` |
| `API_KEY` | 可同时填写多个 API-KEY，用英文逗号分割 | `是` | `<已隐藏>` |
| `API_URL_REDIRECT` | 重新URL重新定向，实现更换API_URL的作用 | `否` | `` |
| `AVAIL_LLM_MODELS` | 所有可用模型 | `否` | `["gpt-3.5-turbo", "api2d-gpt-3.5-turbo", "gpt-4", "api2d-gpt-4", "sparkv2", "qianfan"]` |
| `LLM_MODEL` | 模型选择 | `否` | `gpt-3.5-turbo` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://github.com/binary-husky/gpt_academic
- 源码仓库: https://github.com/binary-husky/gpt_academic
