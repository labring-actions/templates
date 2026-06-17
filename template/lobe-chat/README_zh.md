# 在 Sealos 上部署和托管 Lobe Chat

Lobe Chat 是一个开源 AI 聊天工作区，适用于 ChatGPT 兼容接口和多模型提供商工作流。此模板会在 Sealos Cloud 上部署轻量版 Lobe Chat，并提供公网 HTTPS 访问入口。

## 关于 Lobe Chat 托管

Lobe Chat 以单个 Next.js 应用运行在 Sealos 上。模板通过 Sealos Ingress 暴露 Web UI，固定容器镜像版本，并为每次部署生成独立的认证密钥，确保内置会话 API 正常工作。

此模板适合个人或团队快速使用，聊天数据可保存在浏览器中。如果需要服务端账号、云端同步、PostgreSQL、对象存储或外部身份登录，请使用单独的 Lobe Chat 数据库版模板。

## 常见使用场景

- **个人 AI 工作区**：用统一界面访问 OpenAI 兼容模型和自定义模型列表。
- **团队演示环境**：通过可选访问码保护托管后的 Lobe Chat URL。
- **模型网关前端**：将 `OPENAI_PROXY_URL` 指向 OpenAI 兼容网关或代理。
- **提示词和 Agent 实验**：在托管 HTTPS 入口中测试助手、插件和多模态聊天界面。

## Lobe Chat 托管依赖

此 Sealos 模板包含 Lobe Chat 应用容器、Kubernetes Deployment、Service、Ingress 和 App 快捷入口。轻量版不会自动创建 PostgreSQL、Redis 或对象存储。

### 部署依赖

- [Lobe Chat 文档](https://lobehub.com/docs) - 官方文档
- [自托管指南](https://lobehub.com/docs/self-hosting/start) - 部署方式和配置说明
- [Docker 镜像](https://hub.docker.com/r/lobehub/lobe-chat) - 已发布的容器标签
- [GitHub 仓库](https://github.com/lobehub/lobe-chat) - 源码和问题反馈

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Lobe Chat Web 应用**：使用 `lobehub/lobe-chat:1.143.3` 镜像，在 `3210` 端口提供 Next.js 应用。
- **Service**：集群内 ClusterIP 服务，将流量转发到应用 Pod。
- **Ingress**：使用生成的 Sealos 域名提供公网 HTTPS 访问。
- **App 快捷入口**：在 Sealos 控制台中打开已部署的 Lobe Chat URL。

**配置：**

- `OPENAI_API_KEY` 可预配置 OpenAI API Key，用户也可以在部署后从 UI 中配置模型提供商。
- `OPENAI_PROXY_URL` 默认是 `https://api.openai.com/v1`，也可以指向任意兼容 API 网关。
- `ACCESS_CODE` 为可选项。设置强访问码后，用户需要输入密码才能使用应用。
- `OPENAI_MODEL_LIST` 可用于新增、隐藏或重命名可见模型 ID。

**登录和注册：**

此轻量版模板不会创建服务端用户账号，也不需要初始化注册。打开部署后的 URL，如配置了 `ACCESS_CODE`，先输入访问码，然后在 Lobe Chat 界面中添加或确认模型提供商设置。服务端邮箱密码注册和 SSO 属于数据库版能力。

**许可证信息：**

Lobe Chat 使用 Apache-2.0 许可证。此 Sealos 模板遵循模板仓库许可证。

## 为什么在 Sealos 上部署 Lobe Chat？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，可以在统一控制台中管理部署、网络、扩缩容和运维。在 Sealos 上部署 Lobe Chat 可以获得：

- **一键部署**：打开模板页面，填写少量参数，由 Sealos 创建 Kubernetes 资源。
- **托管 HTTPS 访问**：每次部署都会获得公网 HTTPS URL，无需手动配置证书或 Ingress。
- **资源控制**：当流量或模型使用方式变化时，可从 Canvas 调整 CPU 和内存。
- **AI 辅助运维**：通过 Sealos AI 对话框或资源卡片更新环境变量和运行时设置。
- **按量使用**：从已验证的基础资源开始，只在需要时扩容。

## 部署指南

1. 打开 [Lobe Chat 模板](https://sealos.io/products/app-store/lobe-chat)，点击 **Deploy Now**。
2. 在弹窗中配置参数。直接使用 OpenAI 时填写 `OPENAI_API_KEY`；如需保护应用，设置 `ACCESS_CODE`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需修改配置，可在 AI 对话框中描述需求，或点击对应资源卡片调整设置。
4. 通过提供的 URL 访问应用：
   - **Lobe Chat Web UI**：打开生成的 Sealos URL，如配置了访问码则先输入访问码，然后开始配置模型提供商或聊天。

## 配置

部署后，你可以通过以下方式配置 Lobe Chat：

- **AI 对话框**：描述需要变更的环境变量，例如模型列表或代理 URL。
- **资源卡片**：打开 Deployment 资源卡片，编辑 CPU、内存、副本数或环境变量。
- **Lobe Chat UI**：如果未通过模板输入预配置，可在应用设置中配置模型提供商凭据和聊天偏好。

## 扩缩容

此模板的验证基线为 `200m` CPU 和 `1024Mi` 内存（冷启动验证中 512Mi 不稳定），对应 requests 为 `20m` CPU 和 `102Mi` 内存。扩容步骤：

1. 打开当前部署的 Canvas。
2. 点击 Lobe Chat 的 Deployment 资源卡片。
3. 如果并发用户、长会话或插件使用需要更多容量，提高 CPU 或内存。
4. 应用变更并等待滚动更新完成。

## 故障排查

### 常见问题

**应用可以打开，但模型调用失败**
- 原因：`OPENAI_API_KEY`、`OPENAI_PROXY_URL` 或提供商设置缺失或无效。
- 解决：更新模板输入，或在 Lobe Chat UI 中配置提供商凭据。

**页面要求输入访问密码**
- 原因：部署时配置了 `ACCESS_CODE`。
- 解决：输入已配置的访问码，或在 Sealos Canvas 中修改 Deployment 环境变量。

**需要服务端登录或注册**
- 原因：此轻量版模板主要使用浏览器存储。
- 解决：部署 Lobe Chat 数据库版模板，以使用 PostgreSQL 支持的账号和 SSO。

### 获取帮助

- [官方文档](https://lobehub.com/docs)
- [自托管文档](https://lobehub.com/docs/self-hosting/start)
- [GitHub Issues](https://github.com/lobehub/lobe-chat/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [LobeHub 官网](https://lobehub.com)
- [Lobe Chat GitHub](https://github.com/lobehub/lobe-chat)
- [模型提供商环境变量](https://lobehub.com/docs/self-hosting/environment-variables/model-provider)
- [访问码和基础变量](https://lobehub.com/docs/self-hosting/environment-variables/basic)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Lobe Chat 本身使用 Apache-2.0 许可证。
