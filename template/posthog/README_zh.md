# 在 Sealos 上部署与托管 PostHog

PostHog 是一款开源产品分析平台，支持事件追踪、会话回放、功能开关和实验分析。该模板可在 Sealos Cloud 上一键部署自托管 PostHog 全栈，包含 PostgreSQL、Redis、Kafka 兼容消息队列、ClickHouse、对象存储和后台工作组件。

## 关于在 Sealos 上托管 PostHog

PostHog 是一个多服务协同的分析系统：核心 Django Web 服务负责 UI 和 API 请求，Worker 组件负责异步任务、数据摄取、插件执行和功能开关计算。整条分析链路依赖消息队列与流式处理，再将高吞吐事件数据写入 ClickHouse，把关系型元数据写入 PostgreSQL。

这个 Sealos 模板会一次性拉起核心运行时与有状态依赖，包括 PostgreSQL 和 Redis（通过 KubeBlocks）、Kafka 兼容 Broker、Zookeeper、ClickHouse，以及 S3 兼容对象存储集成，同时自动创建 TLS Ingress 和公网访问地址。

## 常见使用场景

- **SaaS 产品分析**：统一追踪用户事件、漏斗、留存和功能采纳情况。
- **会话回放与问题定位**：结合事件上下文回放用户行为，快速定位前端问题。
- **功能开关灰度发布**：基于服务端与客户端开关进行渐进发布与 A/B 风格实验。
- **转化分析与实验优化**：通过实验结果评估关键产品与增长指标的变化。
- **内部事件平台**：为多个内部应用集中提供事件采集、存储与分析能力。

## PostHog 托管依赖

该 Sealos 模板已包含运行 PostHog 所需的全部关键依赖：PostHog 运行时服务、PostgreSQL、Redis、Kafka 兼容消息系统、ClickHouse、Zookeeper、对象存储桶集成和 HTTPS Ingress。

### 部署依赖

- [PostHog Documentation](https://posthog.com/docs) - PostHog 官方文档与自托管说明
- [PostHog Self-Hosting Docs](https://posthog.com/docs/self-host) - 部署与运维指南
- [PostHog GitHub Repository](https://github.com/PostHog/posthog) - 源码仓库与版本历史
- [Sealos Platform](https://sealos.io) - 云原生部署与运维平台

## 实现细节

**架构组件：**

该模板会部署以下服务与资源：

- **PostHog Web（Deployment）**：主应用服务，监听 `8000` 端口，并在启动阶段执行迁移任务。
- **PostHog Worker（Deployment）**：运行 Celery Worker + 调度器，处理后台任务。
- **PostHog Plugins（Deployment）**：运行插件服务，包含心跳 Sidecar 和 MMDB 初始化容器。
- **Capture 服务（Deployments）**：独立的 `capture` 与 `replay-capture` 数据摄取组件。
- **Feature Flags 服务（Deployment）**：独立低延迟功能开关计算服务。
- **PostgreSQL（KubeBlocks Cluster）**：主关系型数据库，配套启动初始化 Job，确保 `posthog` 数据库存在。
- **Redis（KubeBlocks Cluster）**：缓存与队列辅助组件，采用 Redis + Sentinel 拓扑。
- **Kafka 兼容队列（StatefulSet）**：承载摄取链路与插件/事件流水线的消息 Broker。
- **ClickHouse + Zookeeper**：高吞吐分析存储引擎及其协调依赖。
- **对象存储桶（Object Storage Bucket）**：用于会话回放等二进制数据的 S3 兼容存储。
- **Ingress + App 资源**：提供公网 HTTPS 入口并在 Sealos 应用卡片中发布访问地址。

**配置说明：**

- 数据库与缓存凭据由托管 Kubernetes Secret 注入。
- 各内部服务通过集群 DNS 服务名与固定内部端口通信。
- 默认各组件为单副本，便于低成本启动；后续可在 Canvas 中按需扩容。

**许可证信息：**

PostHog 为开源项目，许可条款请以其[上游 LICENSE](https://github.com/PostHog/posthog/blob/master/LICENSE)为准。

## 为什么在 Sealos 上部署 PostHog？

Sealos 是一个构建于 Kubernetes 之上的 AI 辅助云操作系统，能同时简化部署流程与日常运维。将 PostHog 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手写复杂 Kubernetes 编排，即可拉起多组件分析栈。
- **托管运行底座**：保留 Kubernetes 可靠性的同时，降低运维复杂度。
- **便捷自定义**：通过 Canvas 对话框和资源卡片快速调整环境变量、算力与存储配置。
- **即开即用 HTTPS**：自动生成带 TLS 的公网访问地址。
- **持久化数据能力**：依托有状态组件与持久卷，保障分析数据稳定落盘。
- **按量使用更高效**：先小规模启动，再按业务流量平滑扩展。
- **AI 辅助运维**：可通过 Sealos AI 对话快速完成部署后的变更和调优。

把 PostHog 部署到 Sealos，你可以把精力放在分析结果和业务决策上，而不是基础设施编排。

## 部署指南

1. 打开 [PostHog 模板页面](https://sealos.io/appstore/posthog)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数（例如 `app_name`、`app_host`）。
3. 等待部署完成（通常 2-3 分钟）。完成后会自动跳转到 Canvas。后续如需调整，可在对话框描述需求让 AI 自动修改，或点击相关资源卡片手动修改。
4. 通过生成的公网地址访问应用：
   - **PostHog Web UI**：`https://<your-domain>`
   - **首次登录**：在 UI 中完成初始化引导并创建首个管理员账号。

## 配置

部署完成后，你可以通过以下方式配置 PostHog：

- **AI 对话**：描述你需要的变更（资源、环境变量、扩缩容），由 AI 自动应用。
- **资源卡片**：在 Canvas 中调整 Deployment/StatefulSet、存储与网络配置。
- **PostHog 管理界面**：配置项目、摄取密钥、功能开关与数据保留策略。

常见部署后操作：

1. 在初始化流程中创建首个组织和管理员用户。
2. 接入产品 SDK Key 并开始上报事件。
3. 根据预期事件量调整数据保留和存储策略。
4. 按生产要求完善域名与安全相关配置。

## 扩缩容

如需扩容：

1. 在 Canvas 中打开该部署。
2. 选择目标工作负载（例如 `web`、`worker`、`plugins`、`capture`）。
3. 按摄取吞吐和查询压力提升 CPU/内存与副本数。
4. 应用变更后，观察 Pod 就绪状态与队列积压情况。

多数场景下，建议先扩摄取链路与 Worker，再根据流量增长扩 Web 与 ClickHouse 容量。

## 故障排查

### 常见问题

**问题：Web 已可访问，但后台处理延迟明显**
- 原因：Worker 或队列相关组件仍在初始化。
- 解决方案：检查 `worker`、`plugins` 和队列服务 Pod 日志，等待依赖全部就绪。

**问题：PostHog UI 中插件服务校验失败**
- 原因：插件服务无法连通 Redis 或 Kafka 兼容 Broker。
- 解决方案：检查插件 Pod 环境变量与 Redis/队列连通性，然后重启 plugins Deployment。

**问题：启动阶段出现数据库连接错误**
- 原因：PostgreSQL 集群或初始化 Job 尚未完成。
- 解决方案：确认 PostgreSQL 状态为 `Running` 且初始化 Job 成功后，再重启应用 Pod。

**问题：公网地址短时间不可访问**
- 原因：Ingress 生效或 TLS 证书签发仍在进行中。
- 解决方案：稍等片刻后，在 Canvas 中复查 Ingress 与证书状态。

### 获取帮助

- [PostHog Docs](https://posthog.com/docs)
- [PostHog GitHub Issues](https://github.com/PostHog/posthog/issues)
- [Sealos Discord](https://discord.gg/sealos)

## 更多资源

- [PostHog Product Analytics Guide](https://posthog.com/docs/product-analytics)
- [PostHog Session Replay Docs](https://posthog.com/docs/session-replay)
- [PostHog Feature Flags Docs](https://posthog.com/docs/feature-flags)
- [Sealos Documentation](https://sealos.io/docs)

## 许可证

该 Sealos 模板遵循当前仓库的许可策略。PostHog 项目本身遵循其上游仓库中声明的许可证条款。
