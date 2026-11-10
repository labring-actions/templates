# 在 Sealos 上部署并托管 SigNoz

SigNoz 是一款基于 OpenTelemetry 的开源可观测性平台，可统一管理日志、分布式链路追踪、指标、仪表盘与告警。本模板将官方自托管 SigNoz 完整运行时作为一套持久化四服务架构部署到 Sealos 上。

![SigNoz 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/signoz/website-screenshot.webp)

## 关于托管 SigNoz

SigNoz 为应用团队提供统一的可观测性界面：分布式链路追踪、应用性能监控（APM）、日志检索、基础设施指标监控、仪表盘与告警。应用程序将 OpenTelemetry 遥测数据发送到内置的 Collector，经过处理后写入 ClickHouse 列式存储，并通过 SigNoz Web 控制台统一查询展示。

Sealos 自动提供公网 HTTPS 端点、持久化存储卷、服务发现、健康检查与有序启动流程。部署完成后，通过 SigNoz 首次注册流程创建初始管理员账号。

## 常见使用场景

- **应用性能监控 (APM)**：实时监控服务的延迟、吞吐量和错误率。
- **分布式追踪**：端到端追踪跨服务请求链路，���速定位慢调用与异常 Span。
- **集中式日志分析**：在追踪与指标同一上下文内检索并关联日志。
- **基础设施监控**：采集并展示主机、容器与 Kubernetes 集群指标。
- **仪表盘与告警**：自定义业务与运维大屏，按遥测指标触发告警。

## 依赖说明

模板包含完整的自托管运行时及其持久化数据平面。

### 部署参考

- [SigNoz 官方文档](https://signoz.io/docs/) - 产品与接入指南
- [SigNoz 自托管部署指南](https://signoz.io/docs/install/) - 官方安装与容量规划
- [OpenTelemetry 文档](https://opentelemetry.io/docs/) - OTel SDK 与 Collector 使用指南
- [SigNoz GitHub 仓库](https://github.com/SigNoz/signoz) - 源码与 Issue 跟踪

### 架构组件

- **SigNoz**：Web 控制台、API、鉴权、告警引擎与查询服务。
- **OpenTelemetry Collector**：通过 gRPC 与 HTTP 接收 OTLP 遥测数据，启动时自动幂等执行 ClickHouse 表结构迁移，并将处理后的遥测流写入 ClickHouse。
- **ClickHouse**：高性能列式分析存储，保存链路、日志、指标、元数据与计量数据。
- **ClickHouse Keeper**：官方新一代轻量级 C++ Raft 协调引擎，替代老旧笨重的 ZooKeeper，内存开销降低 70% 以上且免去 JVM 负担。

**持久化存储：**

SigNoz 控制台使用独立持久卷中的 SQLite 保存用户、会话与系统设置；ClickHouse 遥测数据及 Keeper 协调日志/快照分别挂载专用持久卷。

**版本对应关系：**

组件镜像与配置完全遵循官方 SigNoz `v0.146.0` 架构规范，包含 SigNoz OpenTelemetry Collector `v0.144.14`、ClickHouse Server `25.12.5` 以及 ClickHouse Keeper `25.12.5`。

**许可证信息：**

SigNoz 核心代码遵循 MIT 许可证；企业版增强目录携带 SigNoz Enterprise 许可证，请参考上游许可说明。

## 为什么选择在 Sealos 上部署？

- **一键极速交付**：单个模板完整拉起全套 APM 与可观测性技术栈。
- **原生持久化**：容器漂移或 Pod 重建后，遥测数据与账号状态均完整保留。
- **自动化网络拓扑**：自动分配高可用 HTTPS 公网域名与命名空间内服务发现。
- **高资源能效**：精简后的 ClickHouse Keeper 架构显著降低空载内存，适合高效托管。
- **完整全生命周期运维**：随时使用 Canvas 可视化画布、环境变量调节、扩缩容与日志查看。

## 部署流程

1. 打开 [SigNoz 应用模板](https://sealos.io/products/app-store/signoz)，点击 **立即部署**。
2. 启动部署并等待所有服务就绪。
3. 从部署完成的画布打开 SigNoz 公网访问链接。

## 首次登录与初始化

1. 部署完成后首次打开页面，填写注册表单创建管理员账号。
2. 密码需满足至少 12 位，且包含大小写字母、数字和特殊字符。
3. 使用注册的邮箱和密码登录，即可进入 SigNoz 仪表盘主页，开始探索各项监控能力。

## 接入上报 (OTLP)

同一 Sealos 命名空间（项目）内的应用程序可直接通过以下内部地址上报 OTLP 数据：

- **OTLP gRPC**：`http://<app-name>-collector:4317`
- **OTLP HTTP**：`http://<app-name>-collector:4318`

将 `<app-name>` 替换为画布上生成的实际应用前缀名。

## 常见问题排查

### 部署后处于初始化阶段

初次启动时，ClickHouse 需要初始化数据目录，Collector 会在开放端口前自动执行完整表结构迁移（`bootstrap`、`sync up`、`async up`）。可在 Canvas 画布中查看各 Pod 日志确认进度。

### 登录失败或提示密码策略错误

首次访问时请务必通过注册界面创建账号，并确保密码满足 12 位的复杂度策略要求。

### 资源扩容

在流量和遥测上报量增大时，可在 Canvas 画布中针对 ClickHouse 或 Collector 单独调大 CPU 与内存配额。

## 许可证

本 Sealos 模板遵循模板仓库开源协议，各 SigNoz 组件保留各自上游许可证。
