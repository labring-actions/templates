# 在 Sealos 上部署和托管 Rybbit

Rybbit 是一款现代化、开源、注重隐私的网站与产品分析平台。这个模板会在 Sealos Cloud 上部署完整的 Rybbit 服务，包括独立的 Web 客户端、后端 API、ClickHouse 分析存储，以及 PostgreSQL 元数据数据库。

## 关于 Rybbit 托管

Rybbit 可以帮助团队了解网站和产品的真实使用情况，同时避免依赖侵入式的第三方分析平台。它支持流量分析、产品事件、会话洞察，以及面向现代 Web 应用的隐私友好型分析流程。

这个 Sealos 模板采用多服务架构运行 Rybbit：客户端负责提供 Web 控制台，后端 API 处理认证和分析接口，ClickHouse 存储高吞吐量的分析事件，PostgreSQL 存储应用元数据。Sealos 会自动配置公网 HTTPS 访问、内部服务发现、持久化存储和数据库凭据。

模板面向直接可用的自托管场景设计。默认开启注册，部署完成后可以直接创建第一个账号；应用密钥和数据库凭据则由模板自动生成。

## 常见使用场景

- **隐私友好的网站分析**：统计页面访问、来源、设备、地区和访客行为，无需把数据发送到 Google Analytics。
- **产品分析**：采集并分析产品事件，了解功能采用率和用户旅程。
- **SaaS 产品自托管分析**：把分析数据留在自己的基础设施中，同时继续使用现代化的数据看板。
- **内容站轻量分析**：监控内容表现、获客渠道和受众趋势。
- **内部应用监测**：分析私有控制台、门户和内部工具的使用模式。

## Rybbit 托管依赖

这个 Sealos 模板已经包含运行 Rybbit 所需的全部组件：Rybbit 客户端、Rybbit 后端 API、用于分析事件存储的 ClickHouse、用于元数据存储的 PostgreSQL 16、持久化卷、内部 Service，以及 HTTPS Ingress 资源。

### 部署依赖

- [Rybbit 官网](https://rybbit.io/) - 产品介绍与托管版分析服务信息
- [Rybbit GitHub 仓库](https://github.com/rybbit-io/rybbit) - 源码、问题反馈和上游项目更新
- [ClickHouse 文档](https://clickhouse.com/docs) - ClickHouse 数据库文档
- [PostgreSQL 文档](https://www.postgresql.org/docs/) - PostgreSQL 数据库文档
- [Sealos 文档](https://sealos.io/docs) - Sealos 平台文档

### 实现细节

**架构组件：**

模板会部署以下服务：

- **Rybbit Client**：基于 Next.js 的 Web 控制台，作为主公网应用通过 `3002` 端口对外提供服务。
- **Rybbit Backend**：API 服务，与客户端共用同一个公网域名，并通过 `/api` 路径和 `3001` 端口提供接口。
- **ClickHouse**：使用 `clickhouse/clickhouse-server:25.4.2` 的有状态分析数据库，配备持久化存储，用于保存事件数据。
- **PostgreSQL**：由 Kubeblocks 管理的 PostgreSQL 16 数据库，用于保存 Rybbit 元数据和应用状态。
- **PostgreSQL Init Job**：在后端启动前以幂等方式创建 `analytics` 数据库。
- **Ingress 和应用入口**：由 Sealos 管理的 HTTPS 入口，用于访问 Rybbit 控制台和后端 API。

**配置方式：**

模板会自动生成应用名称、公网域名、Better Auth 密钥和 ClickHouse 密码。PostgreSQL 凭据由 Sealos 托管的数据库密钥提供，后端通过 Kubernetes 的 `secretKeyRef` 读取。

客户端使用 `NEXT_PUBLIC_BACKEND_URL` 指向生成的公网地址。后端使用同一个公网域名作为 `BASE_URL`，通过 Kubernetes 内部 Service 连接 ClickHouse，并通过 Kubeblocks 连接密钥访问 PostgreSQL。

默认配置为 `DISABLE_SIGNUP=false`，也就是允许注册。部署完成后，打开 Rybbit 公网地址并注册第一个用户账号即可开始使用。如果后续需要启用地图相关能力，可以再按需配置 Mapbox token。

**许可证信息：**

Rybbit 使用 GNU Affero General Public License v3.0（AGPL-3.0）许可证。这个 Sealos 模板仅作为在 Sealos Cloud 上运行 Rybbit 的部署配置提供。

## 为什么在 Sealos 上部署 Rybbit？

Sealos 是基于 Kubernetes 的 AI 云操作系统，覆盖从开发、部署到生产运维的完整应用生命周期。将 Rybbit 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单，也不用手动连接数据库，即可完成 Rybbit 部署。
- **Kubernetes 原生运行环境**：在基于 Kubernetes 的平台上运行客户端、后端、ClickHouse 和 PostgreSQL，并获得服务发现与工作负载管理能力。
- **内置持久化存储**：ClickHouse 分析数据和 PostgreSQL 元数据会在重启和升级后继续保留。
- **即时公网访问**：自动获得可访问 Rybbit 控制台和后端 API 的 HTTPS 地址。
- **灵活自定义**：可在 Canvas 中通过 AI 对话或资源卡片调整环境变量、资源规格和存储。
- **按需使用资源**：按实际需要分配 CPU、内存和存储，并随分析负载增长逐步扩容。
- **简化运维**：把注意力放在分析和产品决策上，让 Sealos 处理基础设施创建与编排。

如果你想自托管分析系统，但不想直接管理 Kubernetes 基础设施，Sealos 是部署 Rybbit 的合适选择。

## 部署指南

1. 打开 [Rybbit 模板](https://sealos.io/products/app-store/rybbit)，点击 **Deploy Now**。
2. 在弹窗中配置参数。对于标准部署，保留默认生成值即可。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会自动跳转到 Canvas。后续如需修改配置，可以在 AI 对话中描述需求，或点击对应资源卡片调整设置。
4. 通过系统提供的 URL 访问应用：
   - **Rybbit 控制台**：打开生成的公网 URL，并注册第一个账号。
   - **后端 API**：通过同一域名下的 `/api` 路径提供服务，用于 Rybbit 客户端和埋点请求。

## 配置说明

部署完成后，可以通过以下方式配置 Rybbit：

- **AI 对话**：直接描述想要的变更，例如关闭注册、添加可选 API token，由 AI 帮你应用更新。
- **资源卡片**：打开后端 Deployment 资源卡片，调整 `DISABLE_SIGNUP`、`MAPBOX_TOKEN`、资源限制等环境变量和配置。
- **Canvas 资源视图**：查看模板创建的 ClickHouse StatefulSet、PostgreSQL Cluster、Service 和 Ingress 等资源。
- **Rybbit 控制台**：创建第一个账号，添加网站或产品，并按照 Rybbit 应用内指引安装追踪脚本。

## 扩容

Rybbit 的客户端、后端、ClickHouse 和 PostgreSQL 资源彼此独立。建议先使用默认部署，之后再根据事件量和控制台访问量逐步扩容。

1. 打开当前部署的 Canvas。
2. 点击客户端或后端 Deployment 资源卡片，调整 CPU、内存或副本数。
3. 点击 ClickHouse StatefulSet 资源卡片，为更高的分析查询量增加 CPU 或内存。
4. 通过对话应用变更，并在 Canvas 中观察资源就绪状态。

对于高事件量分析场景，优先提升 ClickHouse 的 CPU、内存和存储容量，再考虑增加前端副本。

## 故障排查

### 无法注册账号

- 原因：创建第一个账号后，`DISABLE_SIGNUP` 可能被改成了 `true`。
- 解决办法：如果需要重新开放注册，请在后端 Deployment 中将 `DISABLE_SIGNUP` 设置为 `false`。

### 地图或地球视图提示需要 token

- 原因：部分地图可视化能力需要配置 `MAPBOX_TOKEN`。
- 解决办法：将 Mapbox token 添加到后端 Deployment 的环境变量中，并重启后端服务。

### 后端没有就绪

- 原因：后端启动前需要等待 ClickHouse 和 PostgreSQL 可用。
- 解决办法：在 Canvas 中检查后端 Deployment、ClickHouse StatefulSet、PostgreSQL Cluster 和 PostgreSQL 初始化 Job。先确认所有数据库资源正常运行，再继续排查后端服务。

### 获取帮助

- [Rybbit GitHub Issues](https://github.com/rybbit-io/rybbit/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Rybbit 官网](https://rybbit.io/)
- [Rybbit 源码](https://github.com/rybbit-io/rybbit)
- [ClickHouse 文档](https://clickhouse.com/docs)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)

## 许可证

这个 Sealos 模板作为部署配置提供给 Sealos 用户使用。Rybbit 本身基于 [GNU Affero General Public License v3.0](https://github.com/rybbit-io/rybbit/blob/master/LICENSE.md) 授权。
