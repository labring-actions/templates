# 在 Sealos 上部署和托管 LLM Gateway

LLM Gateway 是一个开源 LLM API 网关，可统一路由、管理和分析多个模型服务商的请求。此模板会在 Sealos 上部署 LLM Gateway Dashboard、API 服务、OpenAI 兼容网关、后台 Worker、文档服务、PostgreSQL 和 Redis。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/llmgateway/website-screenshot.webp)

## 关于托管 LLM Gateway

LLM Gateway 为多个 LLM 服务商提供统一的 OpenAI 兼容 API，并在 Web 控制台中提供路由、成本追踪、API Key、使用日志和服务商管理能力。Sealos 模板采用官方拆分服务部署模型，分别部署 Dashboard、REST API、Gateway、Worker 和 Docs。

Sealos 通过 KubeBlocks 提供外部 PostgreSQL 和 Redis，避免使用内置数据库容器。PostgreSQL 存储用户、组织、项目、API Key 和日志；Redis 支撑认证会话、缓存和网关队列流程。

首次注册后，自托管流程会自动验证账号邮箱，创建默认组织和默认项目，并创建自动生成的 Playground API Key。

## 常见使用场景

- **统一 LLM API 网关**：通过一个 OpenAI 兼容端点路由多个服务商请求。
- **成本和用量可观测**：在一个控制台中追踪请求、Token、模型用量和费用。
- **Provider Key 管理**：为 AI 应用管理服务商密钥和网关配置。
- **自托管 AI 基础设施**：在 Sealos 工作区运行 Gateway、API、Worker、PostgreSQL 和 Redis。
- **团队 API Key 流程**：创建项目级 API Key，并查看应用和 Agent 的活动记录。

## LLM Gateway 托管依赖

此 Sealos 模板包含运行所需依赖：LLM Gateway Dashboard、API、Gateway、Worker、Docs、KubeBlocks PostgreSQL `postgresql-16.4.0`、KubeBlocks Redis `7.2.7`、Kubernetes Service、Ingress 和 Sealos App 入口。

### 部署依赖

- [官方文档](https://docs.llmgateway.io/) - LLM Gateway 文档
- [自托管指南](https://llmgateway.io/self-host) - 官方自托管指南
- [GitHub 仓库](https://github.com/theopenco/llmgateway) - 源码和发布版本
- [Helm Chart](https://github.com/theopenco/llmgateway/tree/main/infra/helm/llmgateway) - 官方 Kubernetes 部署参考

### 实现细节

**架构组件：**

- **Dashboard UI**：用于注册、登录、组织、项目、API Key、Provider Key、用量和活动管理的主界面。
- **API Service**：提供认证、控制台 API、项目管理、API Key 管理和数据库迁移。
- **Gateway Service**：提供 `/v1/*` OpenAI 兼容 LLM 网关。
- **Worker**：处理日志、统计和计划维护任务。
- **Docs Service**：自托管文档界面。
- **PostgreSQL**：由 KubeBlocks 管理的 `postgresql-16.4.0`，并创建专用 `llmgateway` 数据库。
- **Redis**：由 KubeBlocks 管理的 Redis `7.2.7`，用于缓存、认证和队列流程。

**配置：**

- API 启动时使用 `RUN_MIGRATIONS=true` 自动执行数据库迁移。
- 模板分别公开 Dashboard、API、Gateway 和 Docs URL。
- 部署时可选填 OpenAI 和 Anthropic Provider Key。
- Provider Key 和项目 API Key 也可以在登录后通过 Dashboard 管理。
- 自托管注册流程设置 `HOSTED=false`，邮箱会自动完成验证。

**许可证信息：**

LLM Gateway 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 LLM Gateway？

Sealos 是基于 Kubernetes 的 AI 云操作系统，将从云 IDE 开发到生产部署和管理的应用生命周期统一起来。它适合构建和扩展 AI 应用、SaaS 平台和微服务系统。在 Sealos 上部署 LLM Gateway，你可以获得：

- **一键部署**：一次点击即可部署完整多服务栈。
- **托管数据库**：使用 KubeBlocks 托管 PostgreSQL 和 Redis，并带持久化存储。
- **即时公网访问**：Dashboard、API、Gateway 和 Docs 会自动获得 HTTPS URL。
- **便捷定制**：可在 Sealos Canvas 中调整环境变量、资源限制、域名和副本数。
- **Kubernetes 原生运行**：获得 Kubernetes 编排能力，同时通过可视化界面完成日常管理。
- **集成运维**：在一个工作区查看工作负载、日志、存储、域名和数据库资源。

在 Sealos 上部署 LLM Gateway，把精力放在交付 AI 应用上。

## 部署指南

1. 打开 [LLM Gateway 模板](https://sealos.io/products/app-store/llmgateway)，点击 **Deploy Now**。
2. 在弹窗中配置可选 Provider Key：
   - **OpenAI API Key**：用于 OpenAI 兼容路由的可选密钥。
   - **Anthropic API Key**：用于 Anthropic 模型路由的可选密钥。
3. 等待部署完成。首次冷启动通常需要数分钟，因为 PostgreSQL、Redis、数据库初始化和迁移需要先完成，API 与 Gateway 随后就绪。
4. 通过生成的 URL 访问应用：
   - **Dashboard UI**：创建账号，然后管理组织、项目、Provider Key、API Key 和活动记录。
   - **API Endpoint**：用于认证后的控制台和配置 API 调用。
   - **Gateway Endpoint**：作为 OpenAI 兼容 base URL，访问 `/v1/chat/completions`、`/v1/models` 等网关 API。
   - **Docs**：查看随部署提供的 LLM Gateway 文档。

## 首次登录与 API Key 设置

1. 打开 Dashboard UI URL，进入 `/signup`。
2. 使用邮箱和密码创建账号。自托管模式下，账号邮箱会自动验证。
3. 首次会话建立后，LLM Gateway 会创建 **Default Organization**、**Default Project** 和 **Auto-generated playground key**。
4. 打开 Dashboard 的 API Key 页面查看脱敏 Key，或创建新的项目 API Key。
5. 通过 Dashboard 的 Provider Key 设置配置服务商凭据，也可以在部署时填入可选 Provider Key。
6. 将 Gateway URL 作为 OpenAI 兼容 base URL，并把项目 API Key 作为 Bearer Token 传入。

示例：

```bash
curl "$GATEWAY_URL/v1/models" \
  -H "Authorization: Bearer $LLMGATEWAY_API_KEY"
```

## 配置

部署后，可以通过以下方式配置 LLM Gateway：

- **Dashboard UI**：管理组织、项目、Provider Key、API Key、路由、用量和活动记录。
- **AI Dialog**：在 Sealos 中描述需要的修改，让 AI 应用更新。
- **Resource Cards**：在 Canvas 中点击工作负载、域名、ConfigMap、PostgreSQL 或 Redis 卡片调整设置。
- **Gateway URL**：将 SDK base URL 配置为 `https://<your-gateway-domain>/v1`。

## 扩缩容

扩展部署容量：

1. 打开 LLM Gateway 部署对应的 Canvas。
2. 点击对应的 Deployment 卡片，例如 Dashboard UI、API、Gateway、Worker 或 Docs。
3. 调整 CPU、内存或副本数。
4. 应用变更，并在工作负载卡片中观察就绪状态。

默认模板为每个服务使用 1 个副本。请求量增长时，优先增加 API 和 Gateway 的资源。

## 故障排查

### 首次启动需要数分钟

- 原因：PostgreSQL、Redis、数据库初始化和迁移需要完成后，API 与 Gateway 才能就绪。
- 解决：等待 PostgreSQL 和 Redis 卡片显示健康，再检查 API 和 Gateway 工作负载状态。

### 注册成功但 API 调用失败

- 原因：Authorization header 中缺少 API Key，或目标上游模型没有配置 Provider Key。
- 解决：从 Dashboard 创建或复制项目 API Key，然后在 Provider Key 设置中配置服务商凭据。

### Gateway 返回服务商认证错误

- 原因：选定服务商的密钥缺失、无效或触发限流。
- 解决：在 Dashboard 中更新 Provider 凭据，并使用支持的模型重试。

### 获取帮助

- [官方文档](https://docs.llmgateway.io/)
- [GitHub Issues](https://github.com/theopenco/llmgateway/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [LLM Gateway 官网](https://llmgateway.io/)
- [API 文档](https://docs.llmgateway.io/)
- [自托管指南](https://llmgateway.io/self-host)
- [OpenAI 兼容网关指南](https://docs.llmgateway.io/)

## 许可证

LLM Gateway 使用 [Apache License 2.0](https://github.com/theopenco/llmgateway/blob/main/LICENSE)。
