# 在 Sealos 上部署和托管 SigNoz

SigNoz 是一款基于 OpenTelemetry 的可观测平台，可统一管理日志、链路追踪、指标、仪表盘和告警。此模板会在 Sealos 上部署官方 SigNoz 自托管运行栈，包含四项长期运行服务和完整的持久化能力。

![SigNoz 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/signoz/website-screenshot.webp)

## SigNoz 托管说明

SigNoz 为应用团队提供分布式追踪、应用性能监控、日志检索、基础设施指标、仪表盘和告警功能。应用将 OpenTelemetry 数据发送到模板内置的 Collector，Collector 处理后写入 ClickHouse，用户可通过 SigNoz Web 控制台统一查询。

Sealos 会自动配置公网 HTTPS 入口、持久卷、服务发现、健康检查和有序迁移门。部署完成后，由 SigNoz 的首位用户注册流程创建初始管理员账户。

## 常见使用场景

- **应用性能监控**：查看服务延迟、吞吐量和错误率。
- **分布式追踪**：串联跨服务请求，快速定位慢链路。
- **集中式日志分析**：结合链路和指标查询应用日志。
- **基础设施监控**：采集主机、容器和 Kubernetes 遥测数据。
- **仪表盘与告警**：搭建运维视图，并按遥测条件接收通知。

## SigNoz 托管依赖

模板内置完整的自托管运行时和持久化数据平面。

### 部署依赖

- [SigNoz 文档](https://signoz.io/docs/) - 产品与埋点指南
- [SigNoz 自托管指南](https://signoz.io/docs/install/) - 官方部署说明
- [OpenTelemetry 文档](https://opentelemetry.io/docs/) - 遥测 SDK 与 Collector 指南
- [SigNoz GitHub 仓库](https://github.com/SigNoz/signoz) - 源代码与问题跟踪

### 实现细节

**架构组件：**

- **SigNoz**：提供 Web 控制台、API、身份认证、告警和查询引擎。
- **OpenTelemetry Collector**：通过 gRPC 和 HTTP 接收 OTLP 数据，处理后写入 ClickHouse。
- **ClickHouse**：保存链路、日志、指标、元数据、分析数据和计量数据。
- **ZooKeeper**：协调官方运行时所使用的 ClickHouse 复制表结构。
- **Telemetry Store Migrator**：部署时执行一次，在应用启动前完成 ClickHouse 同步迁移和异步迁移。

**持久化数据：**

SigNoz 使用自身持久卷中的 SQLite 保存用户、组织、会话和应用设置。ClickHouse 数据与日志分别使用独立持久卷，ZooKeeper 也拥有独立的协调数据卷。

**版本对应关系：**

组件镜像和配置来自官方 SigNoz `v0.117.0` Docker 部署包，其中包含 SigNoz OpenTelemetry Collector `v0.144.2`、ClickHouse `25.5.6` 和 ZooKeeper `3.7.1`。

**许可证信息：**

SigNoz 仓库中 `ee/` 和 `cmd/enterprise/` 之外的代码采用 MIT Expat 许可证，企业版目录采用独立的 SigNoz Enterprise License。实际使用条款以项目上游许可证文件为准。

## 在 Sealos 上部署 SigNoz 的优势

Sealos 是基于 Kubernetes 的云操作系统，可在同一界面中管理应用全生命周期。

- **一键部署**：通过单个模板创建完整 SigNoz 运行栈。
- **持久化存储**：Pod 替换后仍可保留可观测数据和账户状态。
- **托管网络**：自动获得 HTTPS 应用地址和集群内服务发现能力。
- **资源高效**：默认采用线上验证过的个人低负载资源配置，按已分配资源计费。
- **集成运维**：通过 Canvas、AI 对话框、资源卡片、日志和监控完成后续调整。

## 部署指南

1. 打开 [SigNoz 模板](https://sealos.io/products/app-store/signoz)，点击 **Deploy Now**。
2. 启动部署，等待 ClickHouse 迁移 Job 与四项服务全部就绪。全新部署通常需要数分钟。
3. 从部署完成后的 Canvas 打开 SigNoz 地址。

## 首次登录

1. 全新部署首次打开时，填写 SigNoz 注册表单并创建首个管理员账户。
2. 密码至少包含 12 个字符，并同时包含大写字母、小写字母、数字和符号。
3. 使用注册邮箱和密码登录。进入 SigNoz 工作区首页后，可从 **Services**、**Logs**、**Traces** 或 **Dashboards** 开始查看遥测数据。

请使用安全的密码管理器保存注册凭据。后续用户可通过同一应用地址登录。

## 发送遥测数据

同一 Sealos 命名空间内的应用可将 OTLP 数据发送到：

- **OTLP gRPC**：`http://<app-name>-otel-collector:4317`
- **OTLP HTTP**：`http://<app-name>-otel-collector:4318`

请将 `<app-name>` 替换为 Canvas 上显示的部署名称。各语言 SDK 的具体配置可参考 [SigNoz 埋点指南](https://signoz.io/docs/instrumentation/)。

## 配置与运维

- **AI 对话框**：在 Canvas 中描述资源或配置变更。
- **资源卡片**：查看和编辑工作负载资源、环境变量与存储。
- **扩容**：持续写入量或数据保留规模增长时，可提高 CPU 和内存。
- **备份**：同时为 SigNoz、ClickHouse 数据、ClickHouse 日志和 ZooKeeper 持久卷创建快照，形成一致恢复点。

## 故障排查

### 部署长时间停留在初始化阶段

首次遥测存储迁移会创建大量 ClickHouse 表。请在 Canvas 中查看 Telemetry Store Migrator Job 和 ClickHouse Pod，并等待迁移完成。

### 登录失败

请使用首次访问时注册的邮箱和密码，确认密码符合 12 位复杂度要求，并在 SigNoz Pod 日志中检查身份认证错误。

### 查询变慢或写入量增长

打开 SigNoz 和 ClickHouse 资源卡片，结合实际负载提升 CPU 或内存。默认个人低负载配置以资源效率为优先目标。

### 获取帮助

- [SigNoz 文档](https://signoz.io/docs/)
- [SigNoz GitHub Issues](https://github.com/SigNoz/signoz/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。SigNoz 各组件继续沿用其上游许可证。
