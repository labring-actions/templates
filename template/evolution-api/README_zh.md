# 在 Sealos 上部署和托管 Evolution API

Evolution API 是开源 WhatsApp API 平台，支持 Baileys、WhatsApp Cloud API、Webhook、机器人、聊天和媒体集成。本模板会在 Sealos Cloud 上部署 Evolution API，并自动配置 PostgreSQL、Redis、持久化实例存储，以及可选的 S3 兼容对象存储。

![Evolution API 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/evolution-api/website-screenshot.webp)

## 关于 Evolution API 托管

Evolution API 通过 HTTP API 提供 WhatsApp 自动化和集成能力。它可以管理 WhatsApp 实例、二维码配对、消息事件、Webhook、聊天集成和媒体流程。

Sealos 模板会以 Kubernetes StatefulSet 运行 Evolution API。KubeBlocks 会创建 PostgreSQL 用于持久化应用数据，并创建 Redis 用于缓存和实例协同。模板还会创建持久卷保存本地 WhatsApp 实例状态，也可选择启用 S3 兼容对象存储保存媒体文件。

Sealos 会负责公网 HTTPS 访问、服务发现、存储、数据库创建和资源配置，让你无需手写 Kubernetes 配置也能运行 Evolution API。

## 常见使用场景

- **WhatsApp 自动化 API**：为业务消息流程创建和管理 WhatsApp 实例。
- **Webhook 事件中心**：把消息、联系人、聊天、群组和连接事件发送到外部系统。
- **聊天机器人集成**：把 WhatsApp 会话连接到机器人平台和自动化工具。
- **媒体处理**：将 WhatsApp 媒体保存在本地持久卷或 S3 兼容对象存储中。
- **客户沟通后端**：为 CRM、客服和通知系统提供可编程后端。

## Evolution API 托管依赖

本 Sealos 模板包含以下运行依赖：

- Evolution API `v2.3.7`
- 通过 KubeBlocks 部署的 PostgreSQL `16.4.0`
- 通过 KubeBlocks 部署的 Redis `7.2.7`
- 用于 `/evolution/instances` 的持久化存储
- 用于媒体文件的可选 S3 兼容对象存储
- HTTPS Ingress 和 Sealos App 入口

### 部署依赖

- [Evolution API GitHub 仓库](https://github.com/evolution-foundation/evolution-api) - 源码和版本发布
- [Evolution API 文档](https://doc.evolution-api.com/) - 官方文档
- [Docker Hub 镜像](https://hub.docker.com/r/evoapicloud/evolution-api) - 已发布容器镜像

## 实现细节

**架构组件：**

- **Evolution API StatefulSet**：使用 `evoapicloud/evolution-api:v2.3.7` 镜像运行，监听 `8080` 端口。
- **PostgreSQL Cluster**：存储实例、消息、联系人、聊天、标签和运行时元数据。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `evolution_db` 数据库。应用使用 `evolution_api` PostgreSQL schema，与上游示例连接 URI 保持一致。
- **Redis Cluster**：提供缓存和实例协同能力。
- **持久化实例卷**：将 WhatsApp 实例状态保存在 `/evolution/instances`。
- **可选 ObjectStorageBucket**：启用 `use_object_storage` 后提供 S3 兼容媒体存储。
- **Service、Ingress 和 App Resource**：通过公网 HTTPS 地址暴露 Evolution API。

**配置：**

模板会自动生成 `AUTHENTICATION_API_KEY`。本模板中的 Evolution API 没有注册流程；请使用生成的 API key 访问 Manager UI 和 HTTP API。API manager 默认启用，可通过公网应用地址访问。

对象存储有两种模式：

- **本地媒体模式**：默认模式。媒体和实例文件保存在持久卷中。
- **S3 媒体模式**：部署时启用 `use_object_storage` 后，模板会创建 S3 兼容存储桶并配置 `S3_*` 环境变量。

**默认资源：**

- App CPU limit：`200m`
- App Memory limit：`256Mi`
- 数据库 CPU limit：`500m`
- 数据库 Memory limit：`512Mi`

**健康检查：**

模板使用 `8080` 端口的 `/` 作为启动、就绪和存活探针。live deploy 时还需要检查日志，并用生成的 API key 完成一次认证 API 请求。

**许可信息：**

Evolution API 基于 Apache License 2.0 发布，同时上游 license 文件包含额外商业和署名条件。

## 为什么在 Sealos 上部署 Evolution API？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统，统一应用部署、存储、网络和运维。在 Sealos 上部署 Evolution API 可以获得：

- **一键部署**：通过一个模板部署 Evolution API、PostgreSQL、Redis、存储和 HTTPS 访问。
- **内置持久化**：数据库数据和 WhatsApp 实例状态可在重启后保留。
- **可选对象存储**：为媒体较多的场景启用 S3 兼容存储。
- **即时公网访问**：Sealos 自动分配公网 HTTPS 入口。
- **易于自定义**：可在 Sealos Canvas 调整环境变量、资源和存储。
- **AI 辅助运维**：可通过 Sealos AI 对话或资源卡片修改部署。

## 部署指南

1. 打开 [Evolution API 模板](https://sealos.io/products/app-store/evolution-api)，点击 **Deploy Now**。
2. 配置部署参数：
   - **use_object_storage**：需要把媒体文件保存到 S3 兼容对象存储时启用。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会进入 Canvas。后续如需修改配置，可以在对话框中描述需求，让 AI 自动应用变更；也可以点击对应资源卡片手动调整设置。
4. 通过提供的 URL 访问 Evolution API：
   - **Manager UI 和 API Base URL**：使用 Sealos 提供的公网 HTTPS 地址。
   - **API 认证**：打开 StatefulSet 资源卡片，从工作负载环境变量中读取生成的 `AUTHENTICATION_API_KEY`，并在 Manager UI 或 API 请求中使用。

## 配置

部署后可通过以下方式配置 Evolution API：

- **Manager UI**：使用生成的 API key 创建和管理 WhatsApp 实例以及二维码配对。
- **HTTP API**：请求中使用生成的 API key。
- **资源卡片**：修改 Webhook、集成、日志、S3 和代理相关环境变量。
- **Canvas AI 对话**：描述想要变更的配置，让 Sealos 应用到部署资源。

## 故障排查

### API 请求未通过认证

- **原因**：请求缺少生成的 `AUTHENTICATION_API_KEY`。
- **解决方法**：从 Evolution API 工作负载环境变量读取该值，并按 Evolution API 文档要求加入请求。

### 实例配对或媒体处理失败

- **原因**：实例存储不可写，或 S3 设置缺失。
- **解决方法**：保留模板中的持久卷和权限初始化容器。启用对象存储时，确认 ObjectStorageBucket 和对象存储密钥已经创建。

### 启动时间较长

- **原因**：PostgreSQL 和 Redis 需要先就绪，应用才会启动。
- **解决方法**：在 Canvas 查看 StatefulSet 日志以及 PostgreSQL、Redis 资源卡片。

## 更多资源

- [Evolution API 文档](https://doc.evolution-api.com/)
- [Evolution API GitHub Issues](https://github.com/evolution-foundation/evolution-api/issues)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

本 Sealos 模板提供在 Sealos 上运行 Evolution API 的部署配置。Evolution API 本身基于 Apache License 2.0 发布，并受上游 license 文件中的额外条件约束。
