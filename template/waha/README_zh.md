# 在 Sealos 上部署和托管 WAHA

WAHA 是 WhatsApp HTTP API 服务，提供控制台、Swagger UI、持久会话和 Webhook 支持。此模板在 Sealos Cloud 上部署 WAHA，使用 KubeBlocks PostgreSQL 存储会话，并可选启用 Sealos 对象存储保存 WhatsApp 媒体文件。

![WAHA 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/waha/website-screenshot.webp)

## 关于托管 WAHA

WAHA 通过 HTTP API 和浏览器控制台提供 WhatsApp 自动化能力。你可以创建会话、扫描 WhatsApp 二维码、发送消息、接收 Webhook，并通过 Swagger UI 检查 API。

此模板使用固定镜像 `devlikeapro/waha:chrome-2026.5.1`，因为默认 WEBJS 引擎依赖内置浏览器运行时。PostgreSQL 用于保存 WhatsApp 会话数据，让会话在重启后继续可用。媒体文件默认保存到本地持久卷，部署时可启用 Sealos S3 兼容对象存储。

## 常见使用场景

- **WhatsApp API 网关**：提供发送和接收 WhatsApp 消息的 HTTP 接口。
- **Webhook 自动化**：把 WhatsApp 事件连接到 CRM、客服和工作流系统。
- **会话管理**：从控制台管理多个 WhatsApp 会话。
- **API 测试**：使用 Swagger UI 检查和测试 WAHA 接口。

## WAHA 托管依赖

Sealos 模板包含 WAHA、KubeBlocks PostgreSQL 16.4.0、本地运行文件和媒体持久卷、可选 Sealos 对象存储、公开 HTTPS Ingress 和 App 启动入口。

### 部署依赖

- [WAHA 文档](https://waha.devlike.pro/docs/overview/introduction/) - 官方文档
- [安装指南](https://waha.devlike.pro/docs/how-to/install/) - Docker 部署参考
- [存储指南](https://waha.devlike.pro/docs/how-to/storages/) - 会话和媒体存储选项
- [GitHub 仓库](https://github.com/devlikeapro/waha) - 源码和发布版本

### 实现细节

**架构组件：**

- **WAHA**：主 API、控制台和 Swagger UI 服务。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4.0，用于 WhatsApp 会话存储。
- **持久卷**：本地运行目录和媒体目录。
- **对象存储**：可选 Sealos S3 兼容存储，用于媒体文件。

**配置：**

- 控制台登录使用配置的用户名和生成的密码。
- Swagger 登录使用配置的用户名和生成的密码。
- API 认证使用生成的 `WAHA_API_KEY`。
- 会话存储使用 `WHATSAPP_SESSIONS_POSTGRESQL_URL` 和 KubeBlocks PostgreSQL 连接密钥。
- 模板将 `WAHA_BASE_URL` 和 `WAHA_PUBLIC_URL` 设置为 Sealos HTTPS URL。

**许可证信息：**

WAHA 来自上游项目。版本功能和授权信息请以官方仓库和文档为准。

## 为什么在 Sealos 上部署 WAHA？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从云端开发到生产部署和运维的完整生命周期。它适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 WAHA，你可以获得：

- **一键部署**：同时部署 WAHA、PostgreSQL、存储、HTTPS Ingress 和 App 入口。
- **内置持久存储**：让 WhatsApp 会话和媒体在重启后继续保留。
- **易于定制**：在 Canvas 中调整资源、环境变量和存储配置。
- **无需 Kubernetes 专业知识**：通过简单 UI 管理 Kubernetes 支撑的部署。
- **即时公开访问**：部署完成后通过 HTTPS URL 访问 WAHA。

在 Sealos 上部署 WAHA，把精力放在 WhatsApp 工作流上。

## 部署指南

1. 打开 [WAHA 模板](https://sealos.io/products/app-store/waha)，点击 **Deploy Now**。
2. 配置控制台用户名、Swagger 用户名和可选对象存储设置。
3. 等待部署完成。部署完成后会进入 Canvas。后续变更可在对话框描述需求交给 AI 调整，或点击对应资源卡片修改配置。
4. 从 Canvas 打开 WAHA App URL。App 入口会打开 `/dashboard/` 控制台路径。
5. 使用配置的控制台用户名和模板 defaults 中生成的 `dashboard_password` 登录控制台。
6. 打开 WAHA 根路径 `/` 使用 Swagger UI，或打开 `/-json` 获取 OpenAPI 文档。按提示使用配置的 Swagger 用户名和生成的 `swagger_password` 登录。
7. 需要 API 鉴权时，使用生成的 `api_key` 作为 `WAHA_API_KEY`，例如通过 `X-Api-Key` 请求头传入。

## 配置

部署后可以通过以下方式配置 WAHA：

- **AI 对话框**：描述环境变量、资源或存储变更，由 AI 应用更新。
- **资源卡片**：点击 StatefulSet、PostgreSQL、对象存储、Service 或 Ingress 卡片修改设置。
- **控制台**：在 Web UI 中创建和管理 WhatsApp 会话。
- **Swagger UI**：通过 WAHA 根路径 `/` 测试 API 接口。
- **OpenAPI JSON**：通过同一 host 的 `/-json` 获取 OpenAPI schema。

## 扩展

模板默认运行一个 WAHA 副本，因为基于浏览器的 WhatsApp 会话是有状态的。若要使用同一数据库运行多个 worker，请配置唯一的 `WAHA_WORKER_ID`，并先阅读 WAHA 存储命名空间说明。

## 故障排查

### 控制台登录失败

- 原因：用户名或生成密码不匹配。
- 解决：在部署环境变量中检查 `WAHA_DASHBOARD_USERNAME` 和 `WAHA_DASHBOARD_PASSWORD`。

### 二维码或会话状态丢失

- 原因：会话存储不可用或 PostgreSQL 连接失败。
- 解决：在 Canvas 中检查 WAHA 日志和 PostgreSQL 资源状态。

### 媒体上传需要持久外部 URL

- 原因：本地媒体存储会把文件保存到应用卷。
- 解决：部署时启用对象存储，或用 Sealos S3 变量更新 `WAHA_MEDIA_STORAGE=S3`。

## 更多资源

- [WAHA 配置](https://waha.devlike.pro/docs/how-to/config/)
- [WAHA 控制台](https://waha.devlike.pro/docs/how-to/dashboard/)
- [WAHA Swagger](https://waha.devlike.pro/docs/how-to/swagger/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

WAHA 授权取决于你使用的上游版本和镜像。生产使用前请查看 [上游仓库](https://github.com/devlikeapro/waha) 和 [WAHA 文档](https://waha.devlike.pro/)。
