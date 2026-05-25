# 在 Sealos 上部署和托管 EMQX

EMQX 是一个面向物联网、工业物联网和车联网消息场景的开源 MQTT 消息服务器。此模板会在 Sealos Cloud 上以集群 StatefulSet 方式部署 EMQX，并配置持久化数据与日志存储。

![EMQX 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/emqx/website-screenshot.webp)

## 关于托管 EMQX

EMQX 提供 MQTT、MQTT over TLS、WebSocket 和 Dashboard 访问能力，适合设备消息接入与转发。此 Sealos 模板使用基于 DNS 的集群发现机制，让多个副本可以自动组成 broker 集群。

部署会为每个 Pod 持久化 `/opt/emqx/data` 和 `/opt/emqx/log`，通过 HTTPS 暴露 Dashboard，并可按需通过 NodePort 暴露 MQTT TCP 与 TLS 监听端口。

## 常见使用场景

- **物联网设备消息**：通过 MQTT topic 连接传感器、网关和业务应用。
- **工业物联网遥测**：接入工厂、设备和边缘站点的实时遥测数据。
- **车联网消息**：处理车辆状态、指令和遥测消息。
- **MQTT WebSocket 接入**：让浏览器客户端通过 `/mqtt` WebSocket 路径连接。
- **Broker 评估测试**：快速在 Kubernetes 上验证 EMQX 集群和 Dashboard 能力。

## EMQX 托管依赖

此 Sealos 模板包含 EMQX broker 容器、Kubernetes StatefulSet 编排、持久化卷、内部 Service、公开 HTTPS Ingress 和 Sealos App 入口。

### 部署依赖

- [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/) - 官方 EMQX 文档
- [EMQX GitHub 仓库](https://github.com/emqx/emqx) - 源码与发布版本
- [EMQX Docker 镜像](https://hub.docker.com/r/emqx/emqx) - 此模板使用的容器镜像

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **EMQX StatefulSet**：运行 1、3 或 5 个 EMQX broker 副本。
- **Headless Service**：为 EMQX 集群发现提供 DNS 记录。
- **ClusterIP Service**：在集群内暴露 Dashboard 和 MQTT WebSocket 监听端口。
- **Ingress**：通过 HTTPS 发布 Dashboard 和 `/mqtt` WebSocket 端点。
- **可选 NodePort Service**：启用后暴露 MQTT TCP (`1883`) 和 MQTT TLS (`8883`)。
- **持久化卷**：保存每个 broker Pod 的 EMQX 数据和日志。

**配置：**

- Dashboard 用户名为 `admin`。
- `ADMIN_PASSWORD` 用于设置初始 Dashboard 管理员密码，首次登录后建议立即修改。
- `REPLICA_COUNT` 控制 broker 副本数量。
- `TCP_ENABLE` 控制是否暴露外部 MQTT TCP 和 TLS 端口。
- EMQX 集群通过模板管理的 headless service 进行 DNS 发现。

**许可证信息：**

EMQX 使用 Apache License 2.0。此 Sealos 模板作为 Sealos 模板仓库的一部分提供。

## 为什么在 Sealos 上部署 EMQX？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维和扩缩容流程。在 Sealos 上部署 EMQX 可以获得：

- **一键部署**：无需手写 Kubernetes YAML 即可部署 EMQX。
- **内置持久化存储**：Pod 重启后仍保留 broker 数据与日志。
- **自动 HTTPS 访问**：使用自动生成的公网 URL 和 TLS 访问 Dashboard 与 WebSocket 端点。
- **集群就绪默认配置**：内置 DNS 集群发现，并支持配置副本数量。
- **Canvas 运维**：后续可通过 Sealos Canvas、AI 对话或资源卡片调整资源与配置。

当你需要快速启动一个 MQTT broker，同时保留 Kubernetes 原生部署能力时，可以选择在 Sealos 上部署 EMQX。

## 部署指南

1. 打开 [EMQX 模板](https://sealos.run/products/app-store/emqx)，点击 **Deploy Now**。
2. 配置部署参数：
   - `REPLICA_COUNT`：选择 `1`、`3` 或 `5` 个 broker 副本。
   - `ADMIN_PASSWORD`：设置初始 Dashboard 管理员密码。
   - `TCP_ENABLE`：仅在需要外部 MQTT TCP/TLS 访问时启用。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续如需调整配置，可以在对话框描述需求让 AI 执行，也可以点击对应资源卡片修改设置。
4. 通过生成的地址访问 EMQX：
   - **Dashboard**：打开应用 URL，使用用户名 `admin` 和你配置的密码登录。
   - **MQTT WebSocket**：浏览器 MQTT 客户端可使用 `wss://[your-app-url]/mqtt`。
   - **MQTT TCP/TLS**：如果启用了 `TCP_ENABLE`，请使用 Sealos 中显示的 NodePort 服务信息连接。

## 配置

部署完成后，可以通过以下方式配置 EMQX：

- **EMQX Dashboard**：管理监听器、认证、授权、客户端、规则和集群设置。
- **Sealos AI 对话**：描述资源或模板变更需求，让 AI 执行调整。
- **资源卡片**：在 Canvas 中点击 StatefulSet、Service 或 Ingress 卡片，调整资源与网络配置。

## 扩缩容

如需在部署后扩缩容 EMQX：

1. 打开该部署的 Canvas。
2. 点击 EMQX StatefulSet 资源卡片。
3. 调整副本数量和资源限制。
4. 应用变更，等待 EMQX 集群完成重新平衡。

生产工作负载建议使用 `3` 或 `5` 这样的奇数副本，并在滚动更新期间验证客户端重连行为。

## 故障排查

### Dashboard 登录失败

- 原因：初始密码可能已经在首次启动后被修改。
- 解决方法：使用当前 Dashboard 密码。如果需要重置，请参考 EMQX 文档，通过 CLI 或 Dashboard 修改 Dashboard 用户。

### MQTT TCP 客户端无法连接

- 原因：可能未启用 `TCP_ENABLE`，或客户端使用了错误的 NodePort 端点。
- 解决方法：部署时启用 `TCP_ENABLE`，或后续通过 Sealos 网络设置暴露监听端口。

### 集群副本无法 Ready

- 原因：EMQX 需要稳定 DNS 名称和足够资源完成集群启动。
- 解决方法：在 Canvas 中检查 Pod 日志，确认所有副本可以解析 headless service，并在启动探针持续失败时增加 CPU 或内存。

### 获取帮助

- [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/)
- [EMQX GitHub Issues](https://github.com/emqx/emqx/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [EMQX Dashboard 指南](https://docs.emqx.com/zh/emqx/latest/dashboard/introduction.html)
- [MQTT 监听器配置](https://docs.emqx.com/zh/emqx/latest/configuration/listener.html)
- [EMQX 集群](https://docs.emqx.com/zh/emqx/latest/deploy/cluster/create-cluster.html)

## 许可证

此 Sealos 模板遵循仓库许可证提供。EMQX 本身使用 Apache License 2.0。
