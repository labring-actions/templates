# 在 Sealos 上部署并托管 OpenObserve

OpenObserve 是一个开源可观测性平台，可用于日志、指标、链路追踪、仪表盘、告警和真实用户监控。该模板会在 Sealos Cloud 上部署一个带持久化存储和 HTTPS Ingress 的单节点 OpenObserve 实例。

![OpenObserve 截图](website-screenshot.webp)

## 关于在 Sealos 托管 OpenObserve

OpenObserve 以 Kubernetes StatefulSet 方式运行，并将数据保存在挂载到 `/data` 的持久化卷中。模板会通过部署参数设置 root 管理员邮箱和密码，容器启动完成后即可用这些凭据登录。

Sealos 会自动创建公网 HTTPS 入口、内部服务发现、持久化存储和 Canvas 运维入口。后续可以通过 Canvas 的 AI 对话或资源卡片调整计算、存储和网络配置。

## 常见使用场景

- **集中式日志检索**：收集并查询应用服务和任务日志。
- **指标仪表盘**：为基础设施和应用指标构建运维看板。
- **链路追踪分析**：排查延迟和故障时检查分布式追踪数据。
- **告警工作流**：为生产信号配置监控规则和告警目标。
- **真实用户监控**：跟踪前端性能、错误和会话数据。

## OpenObserve 托管依赖

该 Sealos 模板包含运行 OpenObserve 所需的全部依赖：OpenObserve 容器、持久化数据卷、Kubernetes Service、HTTPS Ingress 和 Sealos App 入口。

### 部署依赖

- [OpenObserve 文档](https://openobserve.ai/docs/) - 官方文档
- [OpenObserve GitHub 仓库](https://github.com/openobserve/openobserve) - 源码和发布记录
- [OpenObserve Docker 镜像](https://gallery.ecr.aws/zinclabs/openobserve) - 已发布容器镜像
- [Sealos 文档](https://sealos.io/docs) - 平台使用与运维指南

## 实现细节

### 架构组件

该模板会部署以下资源：

- **OpenObserve StatefulSet（`public.ecr.aws/zinclabs/openobserve:v0.90.3`）**：在 `5080` 端口提供 Web UI 和 API。
- **持久化卷（`/data`，1Gi）**：保存 OpenObserve 元数据和本地数据。
- **Service + Ingress**：在集群内暴露 OpenObserve，并通过 HTTPS 对外发布。
- **Sealos App 资源**：在 Canvas 中添加 OpenObserve Web UI 入口。

### 配置方式

模板提供以下部署参数：

- `mail`：root 管理员邮箱，同时作为登录用户名。
- `password`：root 管理员密码。
- `data_dir`：数据目录路径，默认为 `/data`。

应用容器使用 `500m` CPU / `512Mi` 内存限制，以及 `50m` CPU / `51Mi` 内存请求。线上验证显示首次冷启动后内存约 `197Mi`，启用探针后重启约 `178Mi`，因此 `512Mi` 是该模板安全的最小 Sealos 资源阶梯。

### 许可证信息

OpenObserve 由 OpenObserve 项目发布。请查看上游仓库了解当前许可证详情。

## 为什么选择在 Sealos 上部署 OpenObserve？

Sealos 是一个构建在 Kubernetes 之上的 AI 辅助云操作系统，可简化部署和日常运维。将 OpenObserve 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手写 Kubernetes 编排即可启动 OpenObserve。
- **Kubernetes 可靠性且无需复杂运维**：通过简单模板使用 Kubernetes 调度、存储和网络能力。
- **内置持久化存储**：重启后保留可观测性数据。
- **安全公网访问**：通过 Sealos 托管 Ingress 自动获得 HTTPS 访问地址。
- **易于定制**：通过 Canvas AI 对话和资源卡片进行部署后变更。
- **按量使用资源**：随着采集量增长逐步调整资源规格。

在 Sealos 上部署 OpenObserve，把精力放在可观测性工作流，而不是基础设施维护上。

## 部署指南

1. 打开 [OpenObserve 模板页](https://sealos.io/products/app-store/openobserve) 并点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `mail`
   - `password`
   - `data_dir`
3. 等待部署完成（通常 2-3 分钟）。部署完成后会自动跳转到 Canvas。后续如需变更，可在对话框描述需求让 AI 自动调整，或点击对应资源卡片手动修改。
4. 通过生成的访问地址打开 OpenObserve，并使用 `mail` 作为用户名、`password` 作为密码登录。

## 配置说明

部署完成后，可以通过以下方式管理 OpenObserve：

- **AI 对话**：在 Canvas 中请求资源或配置变更。
- **资源卡片**：修改 StatefulSet、Service、Ingress 和存储设置。
- **OpenObserve UI**：配置组织、数据流、仪表盘、告警和采集入口。

## 扩容

扩容 OpenObserve：

1. 在 Canvas 打开当前部署。
2. 点击 OpenObserve StatefulSet 资源卡片。
3. 在采集或查询负载增加时提高 CPU 和内存。
4. 随着数据增长扩展 `/data` 持久化卷。

## 故障排查

### 常见问题

**问题：部署后无法登录**
- 原因：登录邮箱或密码与部署时配置的 root 凭据不一致。
- 解决：使用 `mail` 参数作为用户名，使用 `password` 参数作为密码。

**问题：采集或查询速度较慢**
- 原因：当前资源限制不足以支撑采集量或查询负载。
- 解决：在 Canvas 中提高 StatefulSet 的 CPU 和内存。

### 获取帮助

- [OpenObserve 文档](https://openobserve.ai/docs/)
- [OpenObserve GitHub Issues](https://github.com/openobserve/openobserve/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [OpenObserve API 文档](https://openobserve.ai/docs/api/)
- [OpenObserve 采集指南](https://openobserve.ai/docs/ingestion/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

该 Sealos 模板遵循仓库许可证条款。OpenObserve 本身由上游 OpenObserve 项目发布。
