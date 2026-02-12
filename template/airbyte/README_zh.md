# 在 Sealos 上部署与托管 Airbyte

Airbyte 是一个开源数据集成平台，可将数据库、API 和 SaaS 工具的数据构建为 ELT 流水线，统一同步到你的数据仓库或数据湖。该模板会在 Sealos Cloud 上部署 Airbyte Open Source，并同时安装 PostgreSQL、Temporal、对象存储集成及所需控制平面组件。

![Airbyte Logo](./logo.svg)

## 关于在 Sealos 托管 Airbyte

Airbyte 由多项服务协同运行，包括 Web UI、API/控制服务、Worker、调度器、Connector Builder API、工作流引擎和元数据库。这个 Sealos 模板已完成服务发现、健康探针和启动顺序编排，无需你手工拼装 Kubernetes 清单即可稳定运行。

部署过程中会通过 KubeBlocks 自动创建托管 PostgreSQL 集群，用于元数据持久化与迁移初始化；同时创建兼容 S3 的对象存储桶，用于日志、状态和任务产物。模板还会为 Airbyte Web 应用暴露公网 HTTPS 入口。

在安全方面，模板默认启用内置认证，并从部署配置中注入管理员凭据与 JWT 密钥。部署完成后，你仍可在 Canvas 里通过 AI 对话或资源卡片继续管理资源。

## 常见使用场景

- **分析场景下的集中式 ELT**：将 SaaS 平台和业务数据库数据统一同步到数仓。
- **反向 ETL 与内部数据运营**：在下游激活前，先统一做好数据摄取与编排。
- **自托管数据集成平台**：在自有 Kubernetes 环境运行 Airbyte，满足数据驻留与合规要求。
- **连接器开发与测试**：结合 Connector Builder 服务进行连接器迭代。
- **定时批量同步任务**：利用 Worker 执行与重试机制，稳定跑周期性同步。

## Airbyte 托管依赖

该模板已包含完整依赖：Airbyte 控制平面服务、Temporal 工作流引擎、PostgreSQL、对象存储桶集成、Ingress 与启动初始化 Job。

### 部署依赖文档

- [Airbyte Documentation](https://docs.airbyte.com/) - Airbyte 官方文档
- [Airbyte GitHub Repository](https://github.com/airbytehq/airbyte) - 源码与版本发布
- [Airbyte Security Guide](https://docs.airbyte.com/operator-guides/security/#securing-airbyte-open-source) - 安全加固指南
- [Temporal Documentation](https://docs.temporal.io/) - 工作流引擎参考
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - 数据库参考

## 实现细节

### 架构组件

该模板会部署以下资源：

- **Airbyte Webapp (`airbyte/webapp:0.63.11`)**：通过 HTTPS Ingress 对外提供界面访问。
- **Airbyte Server (`airbyte/server:0.63.11`)**：负责认证、编排与控制平面 API。
- **Airbyte Worker (`airbyte/worker:0.63.11`)**：负责同步与连接器任务的后台执行。
- **Airbyte Cron (`airbyte/cron:0.63.11`)**：负责周期性控制任务与维护任务。
- **Connector Builder Server (`airbyte/connector-builder-server:0.63.11`)**：提供 Connector Builder API 服务。
- **Temporal (`temporalio/auto-setup:1.23.0`)**：负责编排、重试与工作流管理。
- **PostgreSQL Cluster (`postgresql-16.4.0`)**：通过 KubeBlocks 提供带持久化的元数据库。
- **Object Storage Bucket**：兼容 S3，用于日志、状态与任务产物存储。
- **Bootloader Job (`airbyte/bootloader:0.63.11`)**：启动时初始化/迁移数据库结构。

### 服务拓扑

- 公网入口通过 Ingress 路由到 `webapp`。
- `webapp` 在集群内调用 `server`。
- `server`、`worker` 与 `cron` 通过 `temporal:7233` 协调工作流。
- `server`、`worker`、`cron` 与 bootloader 通过 KubeBlocks 生成的 Secret 获取 PostgreSQL 凭据。
- `server` 与 `worker` 通过 Sealos 对象存储 Secret 获取对象存储凭据。

### 默认资源与存储配置

- 应用 Deployment 默认采用较保守的 Kubernetes 请求/限制，可在 Canvas 中调整。
- PostgreSQL 默认申请 `1Gi` 持久化存储。
- Temporal 动态配置通过 ConfigMap 挂载到 `/etc/temporal/config/dynamicconfig`。

### 认证输入参数

模板暴露以下安全相关输入参数：

- `auth_admin_username`：初始管理员用户名（默认 `admin`，可修改）
- `auth_admin_password`：初始管理员密码（默认随机值，可修改）
- JWT 签名密钥与刷新密钥：自动生成随机值

首次登录请使用你在部署配置中填写的管理员凭据，随后建议按安全策略立即轮换。

### 许可证信息

Airbyte 采用 [Elastic License 2.0](https://github.com/airbytehq/airbyte/blob/master/LICENSE) 发布。用于生产环境前，请确认并遵循上游许可证条款。

## 为什么在 Sealos 部署 Airbyte？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一了应用部署与运维体验。在 Sealos 部署 Airbyte，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单即可拉起多服务 Airbyte 栈。
- **数据库自动接入**：PostgreSQL 自动创建并完成连接配置。
- **持久化存储就绪**：元数据、同步产物和工作流状态均可持久化保存。
- **安全公网访问**：通过 HTTPS Ingress 和托管网络能力对外提供访问。
- **配置调整便捷**：可在 Canvas 中直接调整环境变量与资源规格。
- **AI 辅助运维**：可用自然语言发起部署后变更。
- **按需付费扩展**：根据实际同步负载弹性扩缩容。

把精力放在数据管道本身，而不是底层平台拼装。

## 部署指南

1. 打开 [Airbyte 模板](https://sealos.io/appstore/airbyte)，点击 **Deploy Now**。
2. 在弹窗中填写部署参数。
3. 等待部署完成（通常 2-3 分钟）。部署成功后会跳转至 Canvas。后续如果要调整配置，可在对话框描述需求由 AI 执行，或直接点击对应资源卡片修改。
4. 打开生成的公网地址并登录：
   - **用户名**：你配置的 `auth_admin_username`
   - **密码**：你配置的 `auth_admin_password`

## 配置说明

部署完成后，你可以通过以下方式配置 Airbyte：

- **AI 对话框**：描述你希望的改动，由 AI 自动落地。
- **资源卡片**：修改 Deployment 资源、环境变量和探针配置。
- **Airbyte UI**：管理数据源、目标端、工作区和同步计划。

建议在部署后优先完成以下动作：

1. 轮换管理员凭据并复核安全配置。
2. 确认数据源与目标连接器的权限设置。
3. 通过一次测试同步验证对象存储与数据库连通性。
4. 为 worker 和 temporal 健康状态配置告警与监控。

## 扩缩容

如需扩缩容，可按以下顺序操作：

1. 在 Canvas 打开当前部署。
2. 优先扩容 `worker` Deployment，以提升并发同步能力。
3. 当编排吞吐成为瓶颈时，增加 `server` 与 `temporal` 的资源配额。
4. 随着元数据写入增长，重新评估 PostgreSQL 规格。

## 故障排查

### 常见问题

**问题：Worker 启动探针报错 `strconv.Atoi: parsing "heartbeat"`**
- 原因：探针端口引用了未正确解析的命名端口。
- 解决：确保 worker 探针使用数值端口 `9000`（或容器端口列表中真实存在的命名端口）。

**问题：Temporal 报错 `dynamic config ... development.yaml: no such file or directory`**
- 原因：动态配置 ConfigMap 未正确挂载。
- 解决：检查 Temporal Deployment 中是否存在 `dynamic-config` 卷及挂载路径 `/etc/temporal/config/dynamicconfig`。

**问题：Temporal 健康检查在 `:7233` 出现 connection refused**
- 原因：Temporal 容器启动失败（常见原因是动态配置挂载缺失）。
- 解决：先修复动态配置挂载，再重启或滚动发布 Temporal Deployment。

**问题：登录页提示实例公网可达但未启用认证**
- 原因：安全/认证相关配置不完整。
- 解决：检查认证相关环境变量是否齐全，并参考 [Airbyte Security Guide](https://docs.airbyte.com/operator-guides/security/#securing-airbyte-open-source) 完成加固。

### 获取帮助

- [Airbyte Documentation](https://docs.airbyte.com/)
- [Airbyte GitHub Issues](https://github.com/airbytehq/airbyte/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Airbyte Open Source Docs](https://docs.airbyte.com/)
- [Airbyte Connectors Catalog](https://docs.airbyte.com/integrations/)
- [Temporal Documentation](https://docs.temporal.io/)
- [Sealos Documentation](https://sealos.io/docs)

## 许可证

本 Sealos 模板遵循模板仓库许可证条款；Airbyte 项目本身采用 [Elastic License 2.0](https://github.com/airbytehq/airbyte/blob/master/LICENSE)。
