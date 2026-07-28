# 在 Sealos 上部署和托管 Rocket.Chat 微服务版

Rocket.Chat 是一个开源团队通信平台，支持频道、私信、文件共享和集成。此模板会在 Sealos Cloud 上部署 Rocket.Chat 7.9.3 官方微服务拓扑，并自动配置 MongoDB、NATS 集群、HTTPS 路由和可选的 Sealos 私有对象存储桶。Rocket.Chat 官方将微服务拓扑列为 Premium/Enterprise 能力，因此每个部署都需要覆盖微服务能力的有效 Rocket.Chat 授权权益（entitlement）或许可证。

![Rocket.Chat 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketchat-micro/website-screenshot.webp)

## 关于 Rocket.Chat 微服务版托管

Rocket.Chat 主应用负责 Web 界面和核心 API，账户、鉴权、在线状态、DDP 流和 Stream Hub 服务分别处理专用工作负载。NATS 通过内部消息总线连接各个服务，MongoDB 保存工作区、用户、房间和消息数据。

模板保留上游 7.9.3 微服务布局：一个 Rocket.Chat 主实例、五个微服务各一个副本、两个 NATS 副本。NATS 配置了 Pod 反亲和与中断预算；Sealos 负责内部服务发现、启动协调、WebSocket 路由和自动生成的公网 HTTPS 地址。

文件上传默认使用 MongoDB GridFS。启用 S3 模式后，模板会创建 Sealos 私有对象存储桶，并让 Rocket.Chat 通过经过身份验证的应用入口代理受保护文件。

## 常见使用场景

- **私有团队沟通**：在自托管工作区中使用频道、私信、讨论串和文件共享。
- **客户与社区协作**：通过公开或私有房间组织支持、项目和用户社区。
- **集成中心**：将机器人、Webhook 和外部服务连接到 Rocket.Chat API。
- **微服务运维**：分别扩展账户、鉴权、在线状态、DDP 和流处理工作负载。
- **可控文件存储**：选择 MongoDB GridFS 或由 Sealos 管理的私有 S3 兼容存储桶。

## Rocket.Chat 微服务版托管依赖

此 Sealos 模板包含完整运行时：

- **Rocket.Chat 主应用**：`rocketchat/rocket.chat:7.9.3`
- **Rocket.Chat 授权权益/许可证**：覆盖官方微服务能力的有效 Premium/Enterprise 授权权益；资格与激活由 Rocket.Chat 管理
- **账户服务**：`rocketchat/account-service:7.9.3`
- **鉴权服务**：`rocketchat/authorization-service:7.9.3`
- **DDP Streamer 服务**：`rocketchat/ddp-streamer-service:7.9.3`
- **在线状态服务**：`rocketchat/presence-service:7.9.3`
- **Stream Hub 服务**：`rocketchat/stream-hub-service:7.9.3`
- **NATS 集群**：两个 `nats:2.4.0-alpine` 副本及配置重载容器；最小运行档使用 `8222` 内置监控端点，并保持 NATS exporter 与 nats-box 关闭
- **MongoDB**：由 KubeBlocks 管理的 MongoDB 8.0.4 和持久化存储
- **对象存储**：用于文件上传的可选 Sealos 私有对象存储桶
- **公网访问**：HTTPS Ingress，以及分别处理 `/sockjs` 和 `/websocket` 的 WebSocket 路由

### 部署依赖链接

- [Rocket.Chat 官方网站](https://www.rocket.chat/) - 产品信息
- [Rocket.Chat 微服务文档](https://docs.rocket.chat/docs/microservices) - 架构与服务职责
- [Rocket.Chat Kubernetes 部署指南](https://docs.rocket.chat/docs/deploy-with-kubernetes) - 官方 Kubernetes 指南
- [Rocket.Chat 文件上传文档](https://docs.rocket.chat/docs/file-upload) - 存储后端配置
- [Rocket.Chat GitHub 仓库](https://github.com/RocketChat/Rocket.Chat) - 源码与版本发布
- [Sealos 文档](https://sealos.io/docs) - 平台部署和运维指南

### 实现细节

**架构组件：**

- **主 Deployment**：在 `3000` 端口提供 Web UI、REST API、管理后台和核心工作区能力。
- **五个微服务 Deployment**：分别处理账户、鉴权、DDP 流、在线状态和 Stream Hub 工作负载。
- **NATS StatefulSet**：运行两个稳定身份副本，每个 Pod 配置独立的 1Gi 运行目录 PVC，并设置 Pod 反亲和和 `minAvailable: 1` 中断预算。Init Container 会在 NATS 启动前清理陈旧 PID 状态。
- **MongoDB Cluster**：保存 Rocket.Chat 应用数据，以及实时更新所需的 oplog。
- **启动协调**：Init Container 会等待 MongoDB Primary、NATS 和 Rocket.Chat 迁移锁，再启动对应服务。
- **Service 与 Ingress**：将 HTTP 流量发送到主应用，将长连接 WebSocket 流量发送到 DDP Streamer。
- **可选 ObjectStorageBucket**：创建私有 S3 兼容存储桶，并向 Rocket.Chat 注入由 Sealos 管理的凭据。

**存储模式：**

| 模式 | 部署参数 | 行为 |
| --- | --- | --- |
| MongoDB GridFS | `enable_s3_storage=false` | 将上传文件保存在 MongoDB，并通过 Rocket.Chat 提供受保护文件。 |
| Sealos 对象存储 | `enable_s3_storage=true` | 创建私有存储桶，将上传文件保存到 S3，并通过 Rocket.Chat 代理经过身份验证的下载。 |

请在部署时确定存储模式，并在该工作区的生命周期内保持同一后端。

**实测资源基线：**

| 工作负载 | 副本数 | 单容器限制 |
| --- | ---: | --- |
| Rocket.Chat 主应用 | 1 | `200m` CPU、`1024Mi` 内存 |
| 账户、鉴权、DDP、在线状态、Stream Hub | 各 1 | `100m` CPU、`128Mi` 内存 |
| NATS Server | 2 | `100m` CPU、`128Mi` 内存 |
| NATS 配置重载容器 | 2 | `100m` CPU、`128Mi` 内存 |
| NATS 运行目录 Init Container | 2 | `100m` CPU、`128Mi` 内存 |
| 启动 Init Container | 每个 Rocket.Chat Pod | `100m` CPU、`128Mi` 内存 |
| MongoDB | 1 | `500m` CPU、`512Mi` 内存 |

主应用在 `100m` CPU 档位的重复冷启动中超过五分钟启动探针预算；`512Mi` 内存档位触发 Node.js 堆上限。模板采用 `200m` CPU 和 `1024Mi` 内存，确保冷启动可以稳定复现。

**许可证信息：**

Rocket.Chat 上游 `apps/meteor/ee/` 和 `ee/` 目录之外的源码使用 MIT 许可证。Enterprise Edition 目录遵循 Rocket.Chat 仓库中附带的独立许可证。

源码许可证与 Premium/Enterprise 产品授权权益是两项独立要求。官方微服务能力需要适用的 Rocket.Chat 授权权益。

## 为什么在 Sealos 上部署 Rocket.Chat 微服务版？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，将应用部署、网络、存储和后续运维集中在一个工作区中。

- **一键部署完整拓扑**：通过一个模板启动 Rocket.Chat、五个微服务、MongoDB、NATS、Ingress 和存储。
- **Kubernetes 服务编排**：在托管运行时中获得服务发现、健康检查、Pod 调度和中断控制。
- **私有 S3 选项**：通过一个部署选项创建私有存储桶和应用凭据。
- **即时 HTTPS 访问**：自动获得工作区域名和 TLS 入口。
- **Canvas 与 AI 运维**：通过 Canvas 资源卡片或 AI 对话调整资源。
- **按用途配置持久化存储**：工作区数据保存在 MongoDB 中；每个 NATS Pod 使用独立的 1Gi 运行目录 PVC，由 Server 与 Reloader 共享。NATS Init Container 会在启动时清理陈旧 PID 状态。
- **按量使用资源**：从实测基线开始，随着工作区负载增长逐步提升容量。

## 部署指南

1. 打开 [Rocket.Chat 微服务版模板](https://sealos.io/products/app-store/rocketchat-micro)，点击 **Deploy Now**。
2. 确认 Rocket.Chat 组织拥有覆盖微服务能力的有效 Premium/Enterprise 授权权益或许可证。
3. 在弹窗中选择文件存储模式：
   - 保持 **Enable S3 storage** 关闭，使用 MongoDB GridFS。
   - 开启 **Enable S3 storage**，创建 Sealos 私有对象存储桶。
4. 开始部署。Sealos 通常会在 2-3 分钟内创建资源；首次 MongoDB 迁移和全部微服务健康检查还会继续运行几分钟。
5. 在 Canvas 中等待主应用、五个微服务、MongoDB 和两个 NATS Pod 全部进入健康状态。
6. 从应用资源打开系统生成的 Rocket.Chat HTTPS 地址。

## 首次登录与工作区注册

注册期间请准备好已获得授权权益的 Rocket.Chat 组织或账号，以及有效的管理员邮箱。Rocket.Chat Cloud 会通过工作区注册流程关联部署，并维护授权权益与许可证更新。

首次打开应用时，Rocket.Chat 会进入四步设置向导：

1. 输入初始管理员的姓名、用户名、邮箱地址和强密码。
2. 填写组织名称、行业、规模和国家或地区。
3. 使用有效的管理员邮箱注册工作区，接受 Rocket.Chat 条款，然后打开 Rocket.Chat Cloud 发送的确认邮件。
4. 核对浏览器与邮件中的安全代码，完成向导并进入工作区首页。

第一个账号会获得管理员和 Owner 权限。后续访问系统生成的 Rocket.Chat 地址，使用同一用户名或邮箱和密码登录。更多用户可通过 **Administration > Workspace > Users** 或工作区邀请加入。

工作区注册会连接 Rocket.Chat Cloud，用于识别授权权益、更新许可证和发送安全通知。首次设置期间请保持管理员邮箱可用；确认页面提供 **Resend** 和 **Change email** 操作。Premium/Enterprise 微服务授权权益来自与该部署关联的 Rocket.Chat 组织或订阅。

## 配置

部署完成后，可通过以下入口管理 Rocket.Chat：

- **Rocket.Chat Administration**：配置账号、权限、认证、集成、邮件和文件上传策略。
- **Canvas AI 对话**：描述资源、环境变量或网络变更，由 Sealos 应用修改。
- **Canvas 资源卡片**：编辑各个 Deployment、StatefulSet、MongoDB Cluster、Service、Ingress、PVC 或 Bucket。
- **部署参数**：`enable_s3_storage` 在部署时选择 GridFS 或私有 S3 存储。

S3 模式下，存储桶保持私有，Rocket.Chat 负责代理受保护的上传文件。Sealos 生成的访问密钥保存在应用 Pod 引用的 Kubernetes Secret 中。

## 扩缩容

1. 在 Canvas 中打开 Rocket.Chat 部署。
2. 选择主应用或专用微服务资源卡片。
3. 根据工作负载压力提升 CPU、内存或副本数。
4. 保持至少两个 NATS 副本，并保留中断预算以维持 Broker 可用性。
5. 随着消息和文件数据增长，扩展 MongoDB 与持久卷容量。

调整各服务副本比例前，请先阅读 Rocket.Chat 微服务文档。并发提升时，DDP 流、在线状态和鉴权服务可以分别扩展。

## 故障排查

### 常见问题

**部署后设置向导仍在加载**

- MongoDB 迁移和微服务启动检查仍在收敛。
- 请在 Canvas 中确认 MongoDB、两个 NATS Pod、主应用和五个微服务均为健康状态。

**工作区注册正在等待确认**

- 使用可以接收 Rocket.Chat Cloud 邮件的管理员邮箱。
- 核对页面显示的安全代码与邮件内容，也可以在确认页面使用 **Resend** 或 **Change email**。

**S3 上传失败**

- 确认部署时选择了 `enable_s3_storage=true`。
- 检查 ObjectStorageBucket 已就绪，并确认工作区内存在 Sealos 对象存储 Secret。
- 保持 Rocket.Chat S3 代理和受保护文件设置开启，以提供经过身份验证的下载。

**主应用在冷启动期间重启**

- 将实测的 `200m` CPU 和 `1024Mi` 内存作为最低基线。
- 大型工作区、导入任务或并发用户增长时，可继续提高主 Deployment 资源。

**消息连接反复重连**

- 检查主 HTTP Ingress，以及专门处理 `/sockjs` 和 `/websocket` 的 Ingress 路由。
- 确认 DDP Streamer 和两个 NATS 副本均已就绪。

### 获取帮助

- [Rocket.Chat 文档](https://docs.rocket.chat/)
- [Rocket.Chat GitHub Issues](https://github.com/RocketChat/Rocket.Chat/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Rocket.Chat 管理指南](https://docs.rocket.chat/docs/administration)
- [Rocket.Chat 环境变量设置](https://docs.rocket.chat/docs/manage-settings-using-environmental-variables)
- [Rocket.Chat 文件上传建议](https://docs.rocket.chat/docs/recommendations-for-file-upload)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。Rocket.Chat 社区源码使用 MIT 许可证，上游 Enterprise Edition 目录使用其附带的 EE 许可证。
