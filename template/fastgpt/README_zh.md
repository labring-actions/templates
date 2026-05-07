# FastGPT

## 应用概览

FastGPT 是一款开源 AI 知识库与工作流平台，提供 RAG 检索、模型编排、MCP 接入和插件扩展能力。

此 Sealos 模板会将 **FastGPT** 部署为 `fastgpt` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `agent_sandbox_baseurl` | `agent_sandbox_baseurl` 部署参数。 | `否` | `` |
| `agent_sandbox_token` | `agent_sandbox_token` 部署参数。 | `否` | `<已隐藏>` |
| `root_password` | `root_password` 部署参数。 | `是` | `<已隐藏>` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://fastgpt.io/
- 源码仓库: https://github.com/labring/FastGPT
