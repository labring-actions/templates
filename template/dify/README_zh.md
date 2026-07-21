# 在 Sealos 上部署和托管 Dify

Dify 是一个开源的大模型应用开发平台，可用于构建 AI Agent、工作流、聊天机器人和 RAG 应用。此模板会在 Sealos Cloud 上部署 Dify 1.15.0，包含 PostgreSQL、Redis、Weaviate、沙箱执行、插件守护进程，以及可选的私有 Sealos 对象存储桶。

![Dify 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/dify/website-screenshot.webp)

## 关于托管 Dify

Dify 以多服务 AI 应用平台运行。Web 服务提供控制台和公开应用页面，API 服务处理后端请求，Worker 处理异步任务，Worker Beat 负责周期性任务调度。Dify Sandbox 提供隔离代码执行环境，Plugin Daemon 负责安装和运行插件市场中的插件。

此模板会自动创建 PostgreSQL、Redis、Weaviate，以及可选的 Sealos ObjectStorage Bucket。PostgreSQL 存储应用和插件元数据，Redis 支撑 Celery 队列，Weaviate 提供默认向量数据库，对象存储用于上传文件和插件包。Sealos 还会通过 Ingress 管理公网 HTTPS 入口，并在仪表盘中生成 Dify 应用入口。

## 常见使用场景

- **AI Agent 和聊天机器人**：连接模型、工具和记忆能力，构建可托管的智能助手。
- **RAG 应用**：上传文档，通过 Weaviate 建立索引，并提供基于知识库的回答。
- **工作流自动化**：运行多步骤 LLM 工作流，并由后台 Worker 处理异步任务。
- **插件扩展**：通过 Plugin Daemon 和插件市场安装 Dify 插件。
- **团队 AI 门户**：为团队提供统一控制台，用于创建、测试和发布 AI 应用。

## Dify 托管依赖

此 Sealos 模板包含 Dify Web、Dify API、Celery Worker、Celery Beat、Dify Sandbox、Dify Plugin Daemon、PostgreSQL、Redis、Weaviate 和可选 Sealos ObjectStorage。

### 部署依赖

- [Dify 文档](https://docs.dify.ai/) - 产品和自托管文档
- [Docker Compose 部署](https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose) - 官方自托管拓扑
- [Dify GitHub 仓库](https://github.com/langgenius/dify) - 源码和版本发布
- [Sealos 应用商店](https://sealos.io/products/app-store/dify) - Dify 模板页面

### 实现细节

**架构组件：**

- **Web**：提供 Dify 控制台和公开应用页面。
- **API**：处理控制台 API、应用 API、文件路由、MCP 路由、数据库迁移和首次设置。
- **Worker**：处理数据集、工作流、邮件和异步任务队列。
- **Worker Beat**：调度周期性后台任务。
- **Sandbox**：通过内部服务端点执行隔离代码。
- **Plugin Daemon**：管理插件安装、运行和远程插件调试端点。
- **PostgreSQL**：存储 Dify 应用元数据和独立插件数据库。
- **Redis**：为 API、Worker 和 Plugin Daemon 提供队列与缓存。
- **Weaviate**：作为默认向量数据库，用于知识库索引。
- **存储**：默认使用持久化本地卷。将 `enable_s3_storage` 设置为 `true` 后，上传文件和插件包会使用私有 Sealos 对象存储桶。

**配置：**

- `init_password` 为必填项，用于解锁 Dify 首次设置页面。
- `enable_s3_storage` 默认为 `false`。设置为 `true` 后，模板会创建私有 Sealos Object Storage Bucket，并注入 S3 兼容凭据。
- Dify 控制台、API、应用和服务端点统一配置为 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。
- PostgreSQL 和 Redis 凭据来自 Sealos 管理的 KubeBlocks Secret。
- API、Redis、Weaviate、Sandbox 和 Plugin Daemon 的内部通信使用带命名空间的集群域名。

**许可证信息：**

Dify 使用 Dify Open Source License。此 Sealos 模板遵循 Sealos 应用模板仓库的许可证。

## 为什么在 Sealos 上部署 Dify？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一管理应用部署、网络、存储和运维。在 Sealos 上部署 Dify 可以获得：

- **一键部署**：直接从应用商店部署完整 Dify 栈。
- **依赖自动创建**：模板会创建 PostgreSQL、Redis、Weaviate、存储和公网路由。
- **即时 HTTPS 访问**：部署完成后获得带 SSL 的公网 URL。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡片完成部署后调整。
- **按量资源**：根据使用量调整 CPU、内存和副本数。

## 部署指南

1. 打开 [Dify 模板](https://sealos.io/products/app-store/dify)，点击 **立即部署**。
2. 配置部署参数：
   - `init_password`：填写用于解锁首次设置页面的必填密码。
   - `enable_s3_storage`：保持 `false` 使用持久化本地存储；设置为 `true` 使用私有 Sealos S3 兼容存储桶。
3. 等待部署完成。数据库、迁移、API Worker 和 Web 控制台首次启动通常需要数分钟。
4. 打开 Dify 应用入口，或打开 Sealos 展示的公网 URL。
5. 在**管理员初始化密码**页面输入 `init_password`，点击**验证**。
6. 在下一页填写管理员邮箱、显示名称和账号密码，然后点击**设置**。账号密码可以和 `init_password` 使用不同的值。
7. 后续使用管理员邮箱和第 6 步创建的账号密码登录 Dify。

## 首次登录检查

登录后，执行两个核心交互：

1. 打开 **Studio**，创建一个 Workflow 或 Chatflow 应用，并进入编辑器。
2. 打开 **Knowledge**，上传一个小型文本文件，用于确认 API、Worker、Redis 队列、Weaviate 和所选存储路径已连通。

模型供应商需要在 Dify 控制台内配置。运行基于模型的聊天或工作流前，请先在设置中添加模型供应商 API Key。

## 配置

部署后，可以通过以下方式配置 Dify：

- **Dify 控制台**：添加模型供应商、创建应用、配置工具和管理知识库。
- **AI 对话**：在 Sealos Canvas 对话框中描述基础设施变更。
- **资源卡片**：调整 Deployment、StatefulSet、数据库、存储和 Ingress 资源。
- **环境变量**：从对应工作负载资源卡片更新 Dify 运行配置。

## 扩缩容

扩展 Dify 的步骤：

1. 打开部署对应的 Canvas。
2. 点击 Web、API、Worker、Sandbox、Plugin Daemon、PostgreSQL、Redis 或 Weaviate 资源卡片。
3. 调整 CPU、内存、存储或副本数。
4. 在对话框中应用变更，并等待滚动更新完成。

应用组件使用以下实测资源档位：

| 组件 | CPU 上限 | 内存上限 | 实测内存峰值 |
| --- | ---: | ---: | ---: |
| API | `500m` | `1Gi` | 双 Gunicorn Worker 下 `756Mi` |
| Worker | `500m` | `1Gi` | `400Mi` |
| Worker Beat | `500m` | `1Gi` | `390Mi` |
| Web | `200m` | `1Gi` | `388Mi` |
| Weaviate | `500m` | `512Mi` | `79Mi` |
| Sandbox | `200m` | `512Mi` | `46Mi` |
| Plugin Daemon | `200m` | `512Mi` | `15Mi` |

API 使用两个 Gunicorn Worker，让控制台流量、插件请求和健康检查可以并行处理。健康检查采用 Dify 官方 Compose 同款的容器内 `/health` 请求。

更大负载下，优先扩展 API 和 Worker 容器，再根据瓶颈提升 PostgreSQL、Redis 和 Weaviate 资源。

## 故障排查

### 首次设置页面循环

- 原因：API 服务仍在等待 PostgreSQL 迁移或 Redis 连通。
- 解决方法：在 Canvas 中查看 API 和 Worker 日志，并确认 PostgreSQL 与 Redis 资源健康。

### 知识库索引卡住

- 原因：Worker、Redis、Weaviate 或对象存储连接存在延迟。
- 解决方法：查看 Worker 日志、Redis 状态和 Weaviate 就绪状态，并确认部署时的 `enable_s3_storage` 模式符合预期存储后端。

### 插件安装失败

- 原因：Plugin Daemon 存储或内部 API 凭据不可用。
- 解决方法：查看 Plugin Daemon 日志，并确认 API 服务可从 Plugin Daemon 资源访问。

### 获取帮助

- [Dify 文档](https://docs.dify.ai/)
- [Dify GitHub Issues](https://github.com/langgenius/dify/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Dify 自托管指南](https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose)
- [Dify 插件](https://docs.dify.ai/plugins)
- [Dify API Reference](https://docs.dify.ai/api-reference)

## 许可证

此 Sealos 模板遵循 Sealos 模板仓库的许可证。Dify 本身使用 Dify Open Source License。
