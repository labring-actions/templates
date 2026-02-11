# 在 Sealos 上部署并托管 Hasura

Hasura 是一款面向数据场景的高性能 GraphQL API 引擎。该模板会在 Sealos Cloud 上部署 Hasura GraphQL Engine，并配套 PostgreSQL 元数据存储与 Data Connector Agent。

## 关于在 Sealos 上托管 Hasura

Hasura 可以基于现有数据源快速生成 GraphQL API，支持元数据驱动的模式管理、基于角色的权限控制，以及事件/Webhook 集成能力。这个模板中，Hasura 作为主服务对外提供 API 与 Console，并连接到托管 PostgreSQL 集群存储元数据。

整套部署包含两个应用工作负载：`hasura/graphql-engine` 与 `hasura/graphql-data-connector`。Data Connector Agent 提供面向外部与联邦数据后端的连接器端点；Hasura 则将元数据与运行时状态写入由 Kubeblocks 提供的 PostgreSQL。

此外，Sealos 会自动提供 HTTPS Ingress、公网访问域名、持久化数据库存储，以及基于 Kubernetes 的 Canvas 生命周期管理能力。

## 常见使用场景

- **内部 API 平台**：为内部工具与数据看板统一提供 GraphQL API。
- **SaaS 后端提速**：快速对 PostgreSQL 数据暴露 GraphQL 接口，加速产品开发。
- **组合式数据网关**：借助 Hasura 元数据与连接器整合多数据系统。
- **事件驱动工作流**：基于数据变化触发 Webhook 与异步业务流程。
- **从原型到生产**：一键起步，后续通过 Canvas 平滑扩缩容。

## Hasura 托管依赖

该 Sealos 模板已内置完整依赖：Hasura GraphQL Engine、Hasura Data Connector Agent，以及带持久化存储的托管 PostgreSQL 16.4 集群。

### 部署依赖链接

- [Hasura Documentation](https://hasura.io/docs/latest/) - 官方产品与运维文档
- [Hasura GraphQL Engine Repository](https://github.com/hasura/graphql-engine) - 源码与版本发布信息
- [Hasura Data Connectors](https://hasura.io/docs/latest/databases/data-connectors/) - 连接器与集成说明
- [Hasura Discord Community](https://discord.gg/hasura) - 社区支持与交流

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **Hasura GraphQL Engine**：主 API 与 Console 服务，通过 HTTPS Ingress 对外暴露。
- **Data Connector Agent**：连接器辅助服务，端口为 `8081`。
- **PostgreSQL（Kubeblocks）**：元数据数据库集群（`postgresql-16.4.0`），带持久化存储。

**配置说明：**

- Hasura 通过 Kubeblocks 托管 Secret 的字段（`host`、`port`、`username`、`password`）获取数据库连接信息。
- 启动命令会先拼装完整 PostgreSQL DSN（Data Source Name），再启动 `graphql-engine`。
- Ingress 默认启用 TLS 与公网域名，两个应用工作负载均为单副本默认配置。

**许可证信息：**

Hasura GraphQL Engine 采用 [Apache License 2.0](https://github.com/hasura/graphql-engine/blob/master/LICENSE) 许可证。

## 为什么在 Sealos 上部署 Hasura？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，覆盖开发、部署与运维全流程。将 Hasura 部署在 Sealos 上，你可以获得：

- **一键部署**：无需手写复杂 YAML，即可同时拉起 Hasura、PostgreSQL 与连接器组件。
- **托管 Kubernetes 运行时**：兼顾 Kubernetes 的稳定性与更低运维门槛。
- **易于定制**：通过 Canvas 对话框与资源卡片直接调整环境变量和资源配置。
- **开箱 HTTPS 访问**：自动获得带 TLS 的公网地址，可直接访问 Hasura Console 与 API。
- **内置持久化存储**：元数据安全落盘，重启与升级场景更稳妥。
- **按需扩缩容**：可在 Canvas 中按业务量调整 CPU、内存与副本数。
- **AI 辅助运维**：在 AI 对话框描述需求，即可快速应用变更。

把 Hasura 放到 Sealos 上，让团队把精力放在 API 交付，而不是基础设施细节。

## 部署指南

1. 打开 [Hasura 模板](https://sealos.io/appstore/hasura)，点击 **Deploy Now**。
2. 在弹窗中填写并确认部署参数。
3. 等待部署完成（通常约 2-3 分钟）。部署结束后会自动跳转到 Canvas。
4. 使用系统生成的域名访问 Hasura：
   - **Hasura Console**：`https://<your-domain>/console`
   - **版本/健康检查**：`https://<your-domain>/v1/version` 与 `https://<your-domain>/healthz`

## 配置

部署完成后，可通过以下方式配置 Hasura：

- **AI Dialog**：直接描述变更需求（例如启用 admin secret 或调整运行参数）。
- **资源卡片**：编辑 Deployment 的环境变量、探针与资源限制。
- **Hasura Console**：管理元数据、权限与已追踪数据源。

建议的生产环境基线：

- 设置 `HASURA_GRAPHQL_ADMIN_SECRET`。
- 根据实际环境配置 CORS 与认证相关参数。
- 在生产环境关闭开发模式（`HASURA_GRAPHQL_DEV_MODE=false`）。

## 扩缩容

如需扩缩容：

1. 在 Canvas 打开该应用。
2. 选择 Hasura 与 Data Connector 对应的 Deployment。
3. 按需调整 CPU/内存与副本数。
4. 应用变更后，持续观察 Pod 健康状态与响应延迟。

## 故障排查

### 常见问题

**问题：初次部署时 Hasura Pod 反复重启**
- 原因：PostgreSQL 集群可能仍在初始化。
- 处理：等待 PostgreSQL 状态变为 `Running`，再查看 Hasura Pod 日志。

**问题：Console 无法访问**
- 原因：Ingress 生效或 TLS 证书签发尚未完成。
- 处理：稍等片刻后，在 Canvas 中检查 Ingress 域名与证书状态。

**问题：自定义变更后出现元数据数据库连接错误**
- 原因：数据库相关环境变量被覆盖为不完整值。
- 处理：保持 DB 字段来自 Kubeblocks Secret，并保留 DSN 拼装逻辑。

### 获取帮助

- [Hasura Docs](https://hasura.io/docs/latest/)
- [Hasura GitHub Issues](https://github.com/hasura/graphql-engine/issues)
- [Sealos Discord](https://discord.gg/sealos)

## 更多资源

- [Hasura Deployment Guide](https://hasura.io/docs/latest/deployment/)
- [Hasura Metadata API](https://hasura.io/docs/latest/api-reference/metadata-api/index/)
- [Hasura Permissions Guide](https://hasura.io/docs/latest/auth/authorization/permissions/)

## 许可证

该 Sealos 模板遵循模板仓库自身许可证。Hasura GraphQL Engine 本体采用 Apache License 2.0。
