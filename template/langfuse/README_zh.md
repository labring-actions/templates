# 在 Sealos 上部署和托管 Langfuse

Langfuse 是用于追踪、提示词管理、评估和可观测性的开源 LLM 工程平台。此模板会在 Sealos Cloud 上部署 Langfuse，并包含 PostgreSQL、Redis、ClickHouse、Worker 处理组件和条件式 S3 兼容对象存储。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/langfuse/website-screenshot.webp)

## 关于托管 Langfuse

Langfuse 是一个多服务可观测性系统。Web 服务负责仪表盘、API、认证和初始化，Worker 服务负责后台摄取和分析任务。

此模板通过 KubeBlocks 创建 PostgreSQL 16.4.0 和 Redis 7.2.7。模板还会部署持久化 ClickHouse 用于高吞吐事件数据，并允许选择 Sealos S3 兼容对象存储来保存事件和媒体数据。

## 常见使用场景

- **LLM 追踪**：从 AI 应用捕获 traces、spans、generations、scores 和元数据。
- **提示词管理**：对提示词进行版本管理，并协作推进实验。
- **评估**：基于生产 traces 进行人工评估和自动评估。
- **可观测性**：在同一个仪表盘中监控延迟、成本、质量和模型行为。

## Langfuse 托管依赖

此 Sealos 模板包含全部运行依赖：Langfuse Web、Langfuse Worker、PostgreSQL、Redis、ClickHouse、条件式 S3 兼容对象存储、内部 Service 和 HTTPS Ingress。

### 部署依赖

- [Langfuse 文档](https://langfuse.com/docs) - 官方文档
- [自托管指南](https://langfuse.com/self-hosting) - 自托管文档
- [配置参考](https://langfuse.com/self-hosting/configuration) - 环境变量和存储配置
- [GitHub 仓库](https://github.com/langfuse/langfuse) - 源代码和发布版本

### 实现细节

**架构组件：**

- **Langfuse Web**：使用 `docker.io/langfuse/langfuse:3.180.0`，在 `3000` 端口提供仪表盘和 API。
- **Langfuse Worker**：使用 `docker.io/langfuse/langfuse-worker:3.180.0` 处理后台摄取和队列任务。
- **PostgreSQL**：KubeBlocks PostgreSQL `postgresql-16.4.0`，用于关系型元数据。
- **Redis**：KubeBlocks Redis `7.2.7`，用于队列和缓存。
- **ClickHouse**：使用 `clickhouse/clickhouse-server:25.4.2` 的有状态分析存储。
- **对象存储**：用于事件和媒体数据的条件式 S3 兼容存储。`use_object_storage=true` 时使用 Sealos ObjectStorageBucket；关闭后部署私有 MinIO 服务。批量导出默认保持关闭。

**配置：**

模板会自动生成 salt、加密密钥、NextAuth secret、ClickHouse 密码、MinIO 凭据和启动组织标识。你可以选择填写 `init_user_email`、`init_user_name` 和 `init_user_password` 来创建首个 Langfuse 用户，并让该用户成为自动生成组织的 owner。

**许可证信息：**

Langfuse 核心产品能力采用 MIT 许可证。SCIM、审计日志、数据保留策略等企业模块在自托管时需要商业许可证。

## 为什么在 Sealos 上部署 Langfuse？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端 IDE 开发到生产部署与运维的完整应用生命周期。它非常适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 Langfuse，你可以获得：

- **一键部署**：一次流程部署完整 Langfuse 栈和数据库、存储依赖。
- **内置自动扩缩容**：随着追踪流量增长调整 Web 和 Worker 资源。
- **易于自定义**：通过 Sealos UI 配置启动用户、对象存储和资源限制。
- **无需 Kubernetes 专业知识**：无需手动管理 Kubernetes 即可运行 PostgreSQL、Redis、ClickHouse、Worker 和 Ingress。
- **内置持久化存储**：重启后保留元数据、分析数据和上传对象。
- **即时公网访问**：自动获得公网 HTTPS 仪表盘地址。

在 Sealos 上部署 Langfuse，把精力放在改进 AI 应用上。

## 部署指南

1. 打开 [Langfuse 模板](https://sealos.io/products/app-store/langfuse)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可在对话框中描述需求让 AI 执行，或点击对应资源卡片调整配置。
4. 通过提供的 URL 访问应用：
   - **Langfuse 仪表盘**：如果配置了启动用户，使用该账号登录；也可以在首次访问时使用 Langfuse 注册流程。

## 配置

初始用户由 `init_user_email`、`init_user_name` 和 `init_user_password` 控制。填写这些值时，模板会同时创建 Langfuse 所需的组织。留空时使用交互式注册流程。

`use_object_storage` 选项控制对象存储：

- `true`：使用 Sealos S3 兼容对象存储保存 Langfuse 事件和媒体数据。
- `false`：部署内置 MinIO 服务，并把对象保存到模板管理的持久化卷。

## 扩缩容

Langfuse 包含独立的 Web、Worker、ClickHouse、PostgreSQL 和 Redis 组件。摄取延迟增加时优先扩 Worker，仪表盘/API 流量增加时提升 Web 资源，分析查询压力增加时提升 ClickHouse 资源。

## 故障排查

### Langfuse Web 启动较慢

- 原因：Web 服务需要等待 PostgreSQL、Redis、ClickHouse 和存储配置可用。
- 解决办法：在 Canvas 中检查数据库集群、ClickHouse StatefulSet、对象存储路径和 Worker 日志。

### 文件或媒体上传失败

- 原因：S3 endpoint 或 bucket 凭据不可用。
- 解决办法：确认所选对象存储模式，并检查 Sealos ObjectStorageBucket 资源或 MinIO StatefulSet。

## 更多资源

- [Langfuse 文档](https://langfuse.com/docs)
- [自托管指南](https://langfuse.com/self-hosting)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)

## 许可证

此 Sealos 模板遵循仓库许可证。Langfuse 核心产品能力采用 MIT 许可证，部分企业模块在自托管时需要上游商业许可证。
