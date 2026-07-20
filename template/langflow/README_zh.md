# 在 Sealos 上部署和托管 Langflow

Langflow 是一个面向 RAG、智能体工作流和 AI 应用的可视化低代码构建器。此模板会在 Sealos Cloud 上部署 Langflow 1.10.2 持久化服务，默认使用 SQLite，并可选择启用 PostgreSQL。

![Langflow 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/langflow/website-screenshot.webp)

## 关于托管 Langflow

Langflow 提供基于浏览器的画布，用于通过可复用组件构建 AI 工作流。你可以连接语言模型、工具、向量数据库、提示词链和智能体，并在 Web 界面中直接测试和迭代流程。

此 Sealos 模板运行官方 `langflowai/langflow` 容器，通过托管 HTTPS 入口暴露服务，并使用持久化卷保存 Langflow 数据。模板会关闭自动登录，因此公网部署需要使用部署时配置的初始超级用户账号登录。

当 `enable_database` 设置为 `true` 时，模板会通过 KubeBlocks 创建 PostgreSQL 16，并初始化专用的 `langflow` 数据库。如果保持关闭，Langflow 会使用存放在持久化数据卷中的内置 SQLite 数据库。

## 常见使用场景

- **RAG 原型构建**：组合文档、嵌入、向量数据库和 LLM 响应，快速构建检索增强工作流。
- **智能体工作流设计**：以可视化方式编排多步骤智能体流程，再迁移到生产系统。
- **AI 应用实验**：在一个交互式工作区中测试提示词、模型提供商、工具和数据连接器。
- **团队演示与教学**：为工作坊、演示或内部 AI 培训提供托管 Langflow 实例。

## Langflow 托管依赖

Sealos 模板包含 Langflow 应用容器、用于 `/app/data` 和 `/app/flows` 的持久化存储、托管 Ingress 入口，以及可选 PostgreSQL。

### 部署依赖

- [Langflow 文档](https://docs.langflow.org/) - Langflow 官方文档
- [Langflow GitHub 仓库](https://github.com/langflow-ai/langflow) - 源码和版本说明
- [Langflow API Keys and Authentication](https://docs.langflow.org/api-keys-and-authentication) - 认证与 API Key 行为说明
- [Sealos 应用商店](https://sealos.io/products/app-store/langflow) - Langflow 模板页面

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Langflow 服务**：官方 Langflow 1.10.2 容器，在 7860 端口提供 Web UI 和 API。
- **持久化存储**：两个持久化卷，用于保存应用数据和导出的 flow 文件。
- **PostgreSQL（可选）**：启用 `enable_database` 后创建 KubeBlocks PostgreSQL 16.4.0，并通过幂等初始化 Job 创建数据库。
- **Ingress 和应用入口**：Sealos 托管 HTTPS 路由，以及部署后的仪表盘入口。

**配置说明：**

- `admin_username` 设置初始 Langflow 超级用户用户名，为必填项。
- `admin_password` 设置初始超级用户密码，为必填项。
- `enable_database` 可将存储从持久化 SQLite 切换到 PostgreSQL，适合更大规模或生产场景。
- `LANGFLOW_AUTO_LOGIN` 设置为 `false`，因此可视化编辑器需要登录，而不是匿名超级用户访问。
- `LANGFLOW_SECRET_KEY` 会在每次部署时生成，用于 Langflow 内部加密相关能力。

**许可证信息：**

Langflow 使用 MIT License。此 Sealos 模板遵循模板仓库的许可证条款。

## 为什么在 Sealos 上部署 Langflow？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一了部署、网络、存储和生命周期运维。将 Langflow 部署到 Sealos 后，你可以获得：

- **一键部署**：直接从应用商店启动 Langflow，无需编写 Kubernetes YAML。
- **托管 HTTPS 访问**：每个部署都会自动获得公网 HTTPS 地址。
- **内置持久化存储**：Langflow 数据和 flow 会在容器重启或升级后保留。
- **可选托管数据库**：需要托管数据库后端时可启用 PostgreSQL。
- **Canvas + AI 运维**：部署后可通过 Canvas、资源卡片或 AI 对话调整资源和配置。
- **按量使用资源**：从模板内置资源配置开始，并在工作负载增加时扩容。

## 部署指南

1. 打开 [Langflow 模板](https://sealos.io/products/app-store/langflow)，点击 **Deploy Now**。
2. 配置部署参数：
   - `admin_username`：必填的初始超级用户用户名。
   - `admin_password`：必填的初始超级用户密码，部署完成后用于登录。
   - `enable_database`：设置为 `true` 使用 PostgreSQL，保持 `false` 则使用持久化 SQLite。
3. 等待部署完成。Langflow 首次启动需要初始化组件和 Web 服务，通常需要数分钟。
4. 通过 Sealos 提供的 URL 访问应用，并使用配置的 `admin_username` 和 `admin_password` 登录。
5. 登录后可从欢迎页创建第一个 flow，或上传已有 flow JSON 文件。

## 配置

部署后可以通过以下方式管理 Langflow：

- **Langflow UI**：创建 flow、管理 API Key、配置模型提供商并运行工作流。
- **Sealos AI 对话**：描述需要调整的配置或扩容需求，让 Sealos 自动应用变更。
- **资源卡片**：在 Canvas 中打开 StatefulSet、Service、Ingress 或 PostgreSQL 资源卡片，检查或调整运行时设置。
- **环境变量**：在工作负载资源卡片中更新认证、数据库或功能开关等 Langflow 配置。

公网部署时建议保持自动登录关闭，并使用强超级用户密码。需要调用外部模型或服务时，请在 Langflow 内或通过 Sealos 托管环境变量配置对应 API Key。

## 扩缩容

Langflow 以单副本持久化 StatefulSet 部署。如需调整资源：

1. 打开当前部署的 Canvas。
2. 点击 Langflow StatefulSet 资源卡片。
3. 如果运行大型 flow、加载大量组件或使用高内存连接器，可提高 CPU 或内存。
4. 应用变更并等待 Pod 重启后重新就绪。

Langflow 容器使用 `500m` CPU 上限和 `4Gi` 内存上限。实测 SQLite 冷启动峰值约为 `1851Mi`，SQLite 稳态占用为 `1264-1279Mi`，PostgreSQL 分支稳态占用约为 `1249Mi`。`4Gi` 档位为组件加载保留了充足的冷启动余量。

## 故障排查

### 部署后显示登录页

这是预期行为。模板已关闭自动登录，请使用部署时配置的 `admin_username` 和 `admin_password` 登录。

### Pod 在启动时反复重启

Langflow 冷启动时会加载大量 Python 组件。如果手动降低内存后出现 OOMKilled，请恢复模板内存配置或选择更高的 Sealos 内存阶梯。

### flow 调用 API 提供商失败

请确认对应 API Key 已在 Langflow 中配置，并确认部署环境可以访问该提供商。

### 获取帮助

- [Langflow 文档](https://docs.langflow.org/)
- [Langflow GitHub Issues](https://github.com/langflow-ai/langflow/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Langflow Components](https://docs.langflow.org/components-overview)
- [Langflow API Keys and Authentication](https://docs.langflow.org/api-keys-and-authentication)
- [Langflow Docker Deployment](https://docs.langflow.org/deployment-docker)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Langflow 使用 MIT License。
