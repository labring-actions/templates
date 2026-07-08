# 在 Sealos 上部署和托管 n8n

n8n 是一个工作流自动化平台，可通过可视化编辑器连接 API、应用和数据流程。本模板在 Sealos Cloud 上部署 n8n 2.22.4，包含持久化存储，可选启用 PostgreSQL 16.4、Redis 队列模式，以及用于 Enterprise S3 二进制数据存储的 Sealos ObjectStorage。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/n8n/website-screenshot.webp)

## 关于 n8n 托管

n8n 以 Node.js Web 应用运行，同一个服务提供工作流编辑器、API、Webhook 端点和执行引擎。默认部署使用持久化存储上的 SQLite，适合轻量项目、测试环境和个人自动化。

生产工作负载建议在部署时启用 PostgreSQL。Sealos 会自动创建 PostgreSQL、初始化 `n8n` 数据库、通过 Kubernetes Secret 注入连接凭据，并确保工作流数据在重启后仍然保留。如需并行执行工作流，可启用队列模式；模板会创建 Redis、PostgreSQL、n8n Worker 和外部任务 Runner。

如果工作流会生成二进制文件，可启用 Sealos ObjectStorage。模板会将托管的 S3 兼容 Bucket 注入 n8n 官方 S3 二进制数据变量，适合需要共享二进制数据存储的队列模式部署。n8n 的 S3 二进制数据模式需要 Enterprise 许可证。

## 常见使用场景

- **API 集成**：连接 SaaS 工具、内部 API 和数据库，无需编写大量胶水代码。
- **Webhook 自动化**：接收 Webhook 并触发通知、数据更新或后续处理。
- **定时任务**：使用 cron 类触发器运行周期性任务，并支持时区配置。
- **数据管道**：在业务系统之间抽取、转换和分发数据。
- **DevOps 流程**：自动化部署通知、故障响应和日常维护任务。

## n8n 托管依赖

Sealos 模板包含 n8n 应用服务、1Gi 持久化存储、可选的 PostgreSQL 生产数据库、可选的 Redis 队列资源，以及可选的 Sealos ObjectStorage S3 二进制数据存储。

### 部署依赖

- [n8n 文档](https://docs.n8n.io/) - n8n 官方文档
- [n8n 托管指南](https://docs.n8n.io/hosting/) - 自托管和配置指南
- [n8n 外部存储](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/use-external-storage/) - S3 二进制数据和执行数据存储指南
- [n8n 集成](https://docs.n8n.io/integrations/) - 可用节点和集成
- [PostgreSQL 文档](https://www.postgresql.org/docs/) - 数据库后端文档
- [Redis 文档](https://redis.io/docs/latest/) - 队列后端文档

## 实现细节

### 架构组件

本模板会部署以下资源：

- **n8n StatefulSet**：运行 n8n 2.22.4，并将 `/home/node/.n8n` 存储在持久卷中。
- **Service 和 Ingress**：通过 HTTPS 暴露 n8n Web 界面、API 和 Webhook 端点。
- **PostgreSQL Cluster（可选）**：提供适合生产环境的工作流与执行数据存储。
- **PostgreSQL 初始化 Job（可选）**：在 PostgreSQL 就绪后幂等创建 `n8n` 数据库。
- **Redis Cluster（队列模式）**：提供 n8n 队列执行所需的 Bull 队列后端。
- **n8n Worker 和 Runner（队列模式）**：将工作流执行和隔离任务执行器从编辑器进程中拆分出来。
- **Sealos ObjectStorage（可选）**：为 n8n Enterprise 二进制数据存储提供 S3 兼容 Bucket。

### 资源配置

| 组件 | CPU 请求 | CPU 限制 | 内存请求 | 内存限制 | 存储 |
|------|----------|----------|----------|----------|------|
| n8n | 50m | 500m | 100Mi | 1G | 1Gi |
| PostgreSQL（可选） | 50m | 500m | 51Mi | 512Mi | 1Gi |
| Redis（队列模式） | 50m | 500m | 51Mi | 512Mi | 1Gi |
| Redis Sentinel（队列模式） | 50m | 500m | 51Mi | 512Mi | 1Gi |
| n8n Worker（队列模式） | 20m | 200m | 51Mi | 512Mi | - |
| n8n Runners（队列模式） | 20m | 200m | 25Mi | 256Mi | - |
| ObjectStorage（可选） | Sealos 托管 | Sealos 托管 | Sealos 托管 | Sealos 托管 | S3 Bucket |

### 配置

- **n8n 版本**：2.22.4
- **PostgreSQL 版本**：启用时为 16.4.0
- **Redis 版本**：启用队列模式时为 7.2.7
- **端口**：5678
- **时区**：部署时可配置
- **加密密钥**：每次部署自动生成
- **S3 二进制数据存储**：可选 Sealos ObjectStorage 分支会设置 `N8N_AVAILABLE_BINARY_DATA_MODES=filesystem,s3`、`N8N_DEFAULT_BINARY_DATA_MODE=s3` 和官方 `N8N_EXTERNAL_STORAGE_S3_*` 变量
- **启动行为**：n8n 依赖 Kubernetes 自动重启和健康探针处理 PostgreSQL、Redis 就绪过程；队列 Worker 会等待主 n8n `/healthz` 端点就绪，确保数据库迁移先由编辑器进程完成
- **探针配置**：已延长启动和存活探针超时，避免数据库迁移期间被误重启
- **公网地址**：`https://<app-host>.<region-domain>/`
- **Webhook 地址**：使用 Sealos 生成的 HTTPS 公网地址

### 许可证信息

n8n 采用 [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)。本 Sealos 模板遵循 Sealos templates 仓库的许可证。

## 为什么在 Sealos 上部署 n8n？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维和扩缩容。在 Sealos 上部署 n8n，你可以获得：

- **一键部署**：打开模板页并点击 **Deploy Now**，无需编写 Kubernetes YAML。
- **内置持久化存储**：工作流数据和本地配置可在重启和升级后保留。
- **可选托管 PostgreSQL**：生产工作负载可启用 PostgreSQL，无需手动配置凭据。
- **可选队列模式**：可启用 Redis、Worker 和 Runner，实现工作流并行执行。
- **可选对象存储**：可启用托管 S3 兼容 Bucket，用于 Enterprise 二进制数据存储。
- **自动 HTTPS 访问**：Sealos 为编辑器和 Webhook 端点提供带 SSL 的公网地址。
- **简化运维**：通过 Canvas、AI 对话和资源卡片调整资源或查看运行状态。
- **按量使用资源**：从已测试的最小资源开始，根据工作流压力再扩容。

## 部署指南

1. 打开 [n8n 模板](https://sealos.io/products/app-store/n8n)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **Use PostgreSQL**：生产工作负载或多用户场景建议启用。
   - **Timezone**：选择定时和 Cron 节点使用的时区。
   - **Use Queue Mode**：启用基于 Redis 的 Worker 执行模式。队列模式会在模板中自动启用 PostgreSQL。
   - **Use Sealos ObjectStorage**：适用于将二进制数据存储到 S3 的 n8n Enterprise 部署。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续如需修改配置，可在 AI 对话中描述需求，或点击相关资源卡片直接调整。
4. 通过 Canvas 中显示的 URL 访问 n8n。
5. 首次打开 n8n 时创建第一个所有者账号。

## 登录和注册

首次访问时，设置页面会要求你填写邮箱、姓名和密码来创建所有者账号。

所有者账号创建完成后，请使用同一个邮箱和密码在 n8n 登录页登录。若后续需要添加团队成员，请以所有者身份登录后，在 n8n 用户管理设置中邀请其他用户。

## 配置

部署后可通过以下方式配置 n8n：

- **n8n 界面**：创建凭据、工作流、变量和项目设置。
- **AI 对话**：描述资源或环境变量修改需求，由 Sealos 应用更新。
- **资源卡片**：在 Canvas 中打开 StatefulSet、Ingress、存储或 PostgreSQL 卡片进行调整。
- **PostgreSQL 模式**：需要生产数据库后端时，在部署时启用 PostgreSQL。
- **队列模式**：需要基于 Worker 的并行执行时，在部署时启用队列模式。
- **ObjectStorage 模式**：已获得 n8n Enterprise 外部存储能力时，可在部署时启用 Sealos ObjectStorage。

## 扩缩容

建议先使用默认资源配置。n8n 编辑器使用 `1G` 内存阶梯，是因为队列模式冒烟测试中，初始 PostgreSQL 迁移和工作流索引会超过较小的 512Mi 配置。若工作流执行缓慢、处理大体积数据，或界面响应变慢，可从 n8n StatefulSet 资源卡片增加 CPU 或内存。

更重的生产工作负载建议启用 PostgreSQL，并在 Canvas 中监控数据库存储、CPU 和内存。当执行历史或并发工作流增加时，可提高 PostgreSQL 资源。若希望将工作流执行从编辑器进程拆分出来，请启用队列模式，并监控 Worker、Runner 和 Redis 资源卡片。

## 故障排查

### 首次打开页面要求创建账号

这是正常行为。首次访问时需要创建所有者账号。

### 定时工作流时区不正确

检查部署时的 timezone 参数。如需部署后修改，请更新 StatefulSet 环境变量中的 `GENERIC_TIMEZONE` 和 `TZ`。

### PostgreSQL 部署未正常启动

在 Canvas 中检查 PostgreSQL Cluster 和 `pg-init` Job。初始化 Job 会等待 PostgreSQL 就绪，并自动创建 `n8n` 数据库。n8n 也会等待 PostgreSQL 服务端口可连接后再启动，因此数据库创建期间短暂等待属于正常现象。

### 队列模式 Worker 未启动

在 Canvas 中检查 Redis Cluster、n8n Worker 和 Runner 部署。队列模式需要 Redis、PostgreSQL 和主 n8n 服务就绪后，Worker 才能开始处理工作流；Worker initContainer 会等待主 `/healthz` 端点，相关服务创建和数据库迁移期间短暂等待属于正常现象。

### ObjectStorage 模式启动退出

确认 n8n 许可证包含 Enterprise 外部存储能力。n8n 官方 S3 二进制数据模式需要有效 Enterprise 许可证；请关闭 **Use Sealos ObjectStorage** 或添加有效许可证后再重启。

### Webhook URL 不正确

确认 `WEBHOOK_URL`、`N8N_HOST`、`N8N_PROTOCOL` 和 `N8N_EDITOR_BASE_URL` 与 Canvas 中显示的公网地址一致。

## 更多资源

- [n8n 文档](https://docs.n8n.io/)
- [n8n 工作流模板](https://n8n.io/workflows)
- [n8n 社区论坛](https://community.n8n.io/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 Sealos templates 仓库的许可证。n8n 本身采用 [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)。
