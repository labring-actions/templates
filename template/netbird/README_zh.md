# 在 Sealos 上部署并托管 NetBird

NetBird 是一个基于 WireGuard 的零信任网络平台，用于在分布式设备之间建立安全的私有连接。这个模板会在 Sealos Cloud 上部署一个可用于生产环境的自托管 NetBird 控制平面，包含内置身份提供方、信令与中继服务。

## 关于在 Sealos 托管 NetBird

NetBird 提供了现代化的私有网络控制平面能力，包括节点管理、策略控制、信令与中继。在本模板中，NetBird 使用内置（embedded）身份提供方（IdP），因此基础部署不需要额外接入外部 OIDC 提供方。

该部署包含四个核心运行服务：Dashboard、Management、Signal 和 Relay。模板为 Management 与 Signal 提供持久化存储，自动生成 TLS Ingress 域名，并单独划分 gRPC 域名，用于避免在同一个 Sealos Ingress Host 上同时承载 HTTP/gRPC 导致的协议冲突。

默认情况下，本模板采用 relay-first 方案，不会内置一个依赖动态公网端口范围的 TURN 服务。如果你的网络环境需要 TURN，可通过模板输入参数配置外部 TURN 服务。

## 常见使用场景

- **远程团队访问**：为分布式团队与内部服务构建安全私有网络。
- **多云私网互联**：在公有云与本地节点之间实现统一策略下的互通。
- **Homelab 与边缘节点接入**：对家庭实验室、分支节点、边缘设备做统一安全管理。
- **服务间隔离**：在内部服务之间落实零信任连接策略。
- **替代传统自建 VPN**：用 WireGuard 节点组网替代传统 VPN 集中器架构。

## NetBird 托管依赖

该 Sealos 模板已包含自托管 NetBird 控制平面所需的全部运行组件：

- NetBird Dashboard
- NetBird Management
- NetBird Signal
- NetBird Relay
- Embedded IdP（内置在 Management）
- 有状态服务所需的持久卷

### 部署依赖文档

- [NetBird Documentation](https://docs.netbird.io/)
- [NetBird Self-Hosted Guide](https://docs.netbird.io/selfhosted/selfhosted-guide)
- [NetBird Local Identity Provider](https://docs.netbird.io/selfhosted/identity-providers/local)
- [NetBird GitHub Repository](https://github.com/netbirdio/netbird)
- [WireGuard Documentation](https://www.wireguard.com/)

### 实现细节

**架构组件：**

本模板会部署以下服务：

- **Dashboard (`netbirdio/dashboard:v2.31.0`)**：管理后台 Web UI 与用户引导入口。
- **Management (`netbirdio/management:0.64.5`)**：核心 API、内置 IdP 与控制平面逻辑。
- **Signal (`netbirdio/signal:0.64.5`)**：节点协商所需的信令服务。
- **Relay (`netbirdio/relay:0.64.5`)**：受限网络环境下的数据中继通道。

**Ingress 与域名路由：**

- **主 HTTPS 域名**（`${app_host}.${SEALOS_CLOUD_DOMAIN}`）：
  - `/` -> Dashboard
  - `/api`, `/oauth2`, `/ws-proxy/management` -> Management
  - `/ws-proxy/signal` -> Signal
  - `/relay` -> Relay
- **独立 gRPC 域名**（`${grpc_host}.${SEALOS_CLOUD_DOMAIN}`）：
  - `/management.ManagementService/` -> Management gRPC
  - `/signalexchange.SignalExchange/` -> Signal gRPC

需要独立 gRPC Host 的原因是：在 Sealos Ingress 上，HTTP 与 gRPC 混用同一 Host 时，后端协议配置会相互影响，稳定性不可保证。

**资源默认值（当前模板）：**

- 每个运行容器统一使用：
  - **limits**：`cpu: 200m`，`memory: 256Mi`
  - **requests**：`cpu: 20m`，`memory: 25Mi`

**存储：**

- Management StatefulSet：`100Mi` PVC（`/var/lib/netbird`）
- Signal StatefulSet：`100Mi` PVC（`/var/lib/netbird`）

## 为什么在 Sealos 上部署 NetBird？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，覆盖从部署到 Day-2 运维的完整生命周期。将 NetBird 部署在 Sealos 上，你可以获得：

- **一键部署**：无需手写 Kubernetes YAML，快速拉起多服务 NetBird 控制平面。
- **自动 HTTPS 访问**：Dashboard 与 API 默认获得公网 TLS 域名。
- **持续运维顺滑**：通过 Canvas 资源卡片和 AI 对话完成配置调整与变更。
- **Kubernetes 级可靠性**：默认使用 StatefulSet/Deployment 与持久卷机制。
- **易于横向和纵向扩展**：业务增长后可在 Sealos UI 中直接调整副本和资源。
- **默认无需外部 IdP**：内置 IdP 降低自托管接入复杂度。

将 NetBird 部署到 Sealos 后，你可以把精力集中在网络策略与访问治理，而不是基础设施编排。

## 部署指南

1. 访问 [NetBird Template Page](https://sealos.io/products/app-store/netbird)
2. 点击 **Deploy Now**
3. 配置必要参数：
   - `disable_default_policy`
   - 可选外部 TURN 参数（`external_turn_host`、`external_turn_username`、`external_turn_password`）
4. 等待部署完成（通常 2-3 分钟）
5. 在 Canvas 中打开生成的应用访问地址
6. 在 Dashboard 中创建初始管理员账号并完成引导

## 配置说明

部署后可通过以下方式更新配置：

- **Canvas 的 AI 对话框**：描述你要变更的内容并应用。
- **资源卡片**：直接编辑 Deployment、StatefulSet、Service 与 Ingress。

### 输入参数

- **`disable_default_policy`**：是否关闭默认 all-to-all 策略（`true`/`false`）。
- **`external_turn_host`**：可选 TURN 地址（`host:port`），例如 `turn.example.com:3478`。
- **`external_turn_username`**：TURN 用户名（启用外部 TURN 时必填）。
- **`external_turn_password`**：TURN 密码（启用外部 TURN 时必填）。

### 外部 TURN 说明

- 当 `external_turn_host` 为空时，管理配置中的 TURN/STUN 条目会被省略。
- 若你的环境存在严格 NAT 限制，建议提供稳定的外部 TURN 端点，而不是依赖动态 NodePort 端口范围映射。

## 扩缩容

扩缩容步骤如下：

1. 打开应用对应 Canvas。
2. 选择目标资源卡片（`Deployment` 或 `StatefulSet`）。
3. 调整副本数或 CPU/内存。
4. 提交变更并观察 rollout 状态。

## 故障排查

### 常见问题

**问题：管理员注册成功后出现 “There was an error logging you in. Error: Unauthenticated”**
- 原因：内置 IdP 路径或 issuer 路由不一致。
- 排查项：
  - `https://<app-host>/oauth2/.well-known/openid-configuration` 应返回 `200`
  - Management Ingress 必须包含到 Management 服务的 `/oauth2` 路由
  - Dashboard 的 `AUTH_AUTHORITY` 应指向 `https://<app-host>/oauth2`

**问题：Dashboard 可访问，但节点连接不稳定**
- 原因：网络路径受限，需要 TURN 辅助。
- 解决：通过模板输入参数配置外部 TURN 服务。

**问题：HTTP UI 正常，但 gRPC 调用失败**
- 原因：gRPC 与 HTTP 的 Host/协议配置不匹配。
- 解决：
  - 确认独立 gRPC 域名已正确配置且可解析
  - 确认 gRPC Ingress 使用 `nginx.ingress.kubernetes.io/backend-protocol: GRPC`

### 获取帮助

- [NetBird Docs](https://docs.netbird.io/)
- [NetBird GitHub Issues](https://github.com/netbirdio/netbird/issues)
- [NetBird Community](https://netbird.io/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [NetBird Architecture](https://docs.netbird.io/about-netbird/architecture)
- [NetBird Peer and Route Management](https://docs.netbird.io/how-to/manage-peers)
- [WireGuard Protocol Overview](https://www.wireguard.com/protocol/)

## 许可证

该 Sealos 模板遵循 Sealos templates 仓库的许可证策略。NetBird 项目本身采用 [BSD-3-Clause License](https://github.com/netbirdio/netbird/blob/main/LICENSE)。
