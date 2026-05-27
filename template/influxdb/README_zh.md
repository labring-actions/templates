# 在 Sealos 上部署和托管 InfluxDB

InfluxDB 是一款开源时序数据库，适合处理实时分析、指标、事件和物联网数据。本模板会在 Sealos Cloud 上部署 InfluxDB 2.9.1，提供持久化存储、精简默认资源规格和公网 Web UI。

## InfluxDB 托管说明

InfluxDB 用于存储带时间戳的测量数据，适合接入仪表盘、告警系统、可观测性流水线和传感器数据。本 Sealos 模板会以单个 StatefulSet 运行 InfluxDB，并将持久化卷挂载到 `/var/lib/influxdb2`，确保数据库、bucket、token 和元数据在重启后仍然保留。

首次启动时，模板会根据部署表单中的配置创建管理员用户、组织、bucket 和 API token。Sealos 会通过 Ingress 提供 HTTPS 访问，并在 Canvas 中创建应用入口，方便直接打开 InfluxDB UI。

## 常见使用场景

- **基础设施监控**：存储 CPU、内存、磁盘、网络和服务指标，用于仪表盘和告警。
- **物联网遥测**：接收设备、网关和边缘系统产生的大量传感器数据。
- **应用分析**：记录事件、计数器、耗时和产品使用趋势。
- **DevOps 可观测性**：保留构建、部署和运行时指标，辅助排障。
- **实时实验分析**：查询近期时序数据，支撑运营分析和原型验证。

## InfluxDB 托管依赖

本 Sealos 模板已包含 InfluxDB 容器镜像、持久化存储、Kubernetes Service、HTTPS Ingress 和 Sealos App 入口。模板不需要外部数据库。

### 部署依赖

- [InfluxDB 文档](https://docs.influxdata.com/influxdb/v2/) - InfluxDB 2.x 官方文档
- [Docker 官方镜像](https://hub.docker.com/_/influxdb) - InfluxDB 官方容器标签
- [InfluxDB GitHub 仓库](https://github.com/influxdata/influxdb) - 源码与版本发布
- [Sealos](https://sealos.io) - 本模板使用的云平台

### 实现细节

**架构组件：**

本模板会部署以下资源：

- **InfluxDB StatefulSet**：运行 `docker.io/library/influxdb:2.9.1`，默认限制为 `200m` CPU 和 `128Mi` 内存，并将数据保存到 `/var/lib/influxdb2`。
- **持久化卷**：提供 1 GiB 持久化存储，用于保存时序数据和元数据。
- **Service**：在集群内通过 `8086` 端口暴露 InfluxDB HTTP API 和 Web UI。
- **Ingress**：通过 Sealos 自动生成的域名提供 HTTPS 访问。
- **App 入口**：在 Sealos Canvas 中创建 InfluxDB 快捷入口。

**配置说明：**

模板使用 InfluxDB 官方的一次性初始化环境变量。部署时请填写管理员密码和 API token，并妥善保存。默认组织为 `sealos`，初始 bucket 为 `primary`。

**许可证信息：**

InfluxDB 使用 InfluxData 在官方项目中发布的开源许可证。本 Sealos 模板只是官方 InfluxDB 容器镜像的部署封装。

## 为什么在 Sealos 上部署 InfluxDB？

Sealos 是基于 Kubernetes 的 AI 云操作系统，覆盖从部署到日常运维的应用生命周期。在 Sealos 上部署 InfluxDB，可以获得：

- **一键部署**：从应用商店启动 InfluxDB，无需手写 Kubernetes YAML。
- **内置持久化存储**：重启后仍保留时序数据和元数据。
- **即时公网访问**：自动生成 HTTPS URL，用于访问 InfluxDB UI 和 API。
- **便捷配置调整**：通过部署表单和 Canvas 修改凭据、资源和存储配置。
- **Kubernetes 底座**：获得服务发现、滚动更新和资源控制等云原生能力。
- **按量使用资源**：先用较小规格启动，后续按写入和查询压力扩容。

## 部署指南

1. 打开 [InfluxDB 模板](https://sealos.io/products/app-store/influxdb)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **Initial InfluxDB admin password**：`admin` Web UI 用户的登录密码。
   - **Initial InfluxDB API token**：用于 CLI、API 和客户端集成的访问 token。
3. 部署前请妥善保存密码和 token。InfluxDB 会在首次初始化时使用这些值。
4. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需调整，可在对话框中描述需求让 AI 修改，或点击相关资源卡片手动配置。
5. 通过生成的 App URL 访问 InfluxDB。
6. 使用以下信息登录 Web UI：
   - **用户名**：`admin`
   - **密码**：部署时配置的管理员密码

本模板不会开放公开注册。初始管理员账号会在首次启动时自动创建。

## 配置

部署完成后，可以通过以下方式配置 InfluxDB：

- **InfluxDB UI**：在 Web 界面中创建 bucket、token、仪表盘和数据源。
- **InfluxDB API 和 CLI**：使用部署时配置的 API token 进行自动化操作。
- **Sealos AI 对话框**：描述资源或配置变更，让 AI 辅助修改。
- **资源卡片**：在 Canvas 中打开 StatefulSet、Service、Ingress 或存储卡片，查看并调整配置。

## 扩容

如果写入量或查询压力增加，可以按以下步骤调整资源：

1. 打开当前部署的 Canvas。
2. 点击 InfluxDB StatefulSet 资源卡片。
3. 根据实际负载调整 CPU 和内存。
4. 如果保留策略需要更大容量，可增加持久化存储。
5. 在对话框中应用变更，并等待 Pod 重新进入 Ready 状态。

## 故障排查

### 无法登录

- 原因：UI 中输入的密码与首次部署时配置的值不一致。
- 解决方法：使用用户名 `admin` 和部署表单中的初始管理员密码登录。如果密码遗失，可以重新部署并设置新的密码和 token，或在 InfluxDB 内手动重置凭据。

### Pod 未就绪

- 原因：首次初始化仍在进行，或当前资源限制不足以支撑负载。
- 解决方法：等待几分钟后，从 Canvas 查看 StatefulSet 日志。如果 Pod 在负载下重启，请提高内存配置。

### API 客户端认证失败

- 原因：客户端使用的 token 与部署时配置的初始 API token 或 UI 中创建的 token 不一致。
- 解决方法：使用部署 token，或在 InfluxDB UI 的 **Load Data → API Tokens** 中创建新 token。

### 获取帮助

- [InfluxDB 文档](https://docs.influxdata.com/influxdb/v2/)
- [InfluxDB 社区](https://www.influxdata.com/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [InfluxDB 入门指南](https://docs.influxdata.com/influxdb/v2/get-started/)
- [InfluxDB API 文档](https://docs.influxdata.com/influxdb/v2/api/)
- [Line Protocol 参考](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/)

## 许可证

本 Sealos 模板遵循模板仓库的许可证。InfluxDB 本身遵循官方项目仓库中由 InfluxData 发布的许可证。
