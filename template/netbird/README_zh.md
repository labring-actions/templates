# 在 Sealos 上部署和托管 NetBird

NetBird 是一个基于 WireGuard 的零信任网络平台，用于在分布式设备之间建立安全的私有连接。此模板会在 Sealos Cloud 上部署自托管 NetBird 控制平面，包括 Dashboard、Management、Signal、Relay、嵌入式 IdP 和持久化状态存储。

![NetBird 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/netbird/website-screenshot.webp)

## 关于托管 NetBird

NetBird 提供私有网络、节点注册、访问策略、信令和中继辅助连接所需的控制平面。此 Sealos 模板使用 NetBird 的嵌入式身份提供方，因此基础自托管部署不需要额外接入外部 OIDC 服务。

模板将公开 Web/API 域名与 gRPC 域名分离。主域名负责 Dashboard、Management HTTP API、嵌入式 IdP 路由、Signal websocket 路径和 Relay 路径；独立 gRPC 域名通过 GRPC ingress 后端暴露 Management 和 Signal 的 gRPC 流量。

模板不内置 TURN，因为动态公开 UDP/TCP 端口范围不适合此 Sealos 模板。如果你的节点处于严格 NAT 环境并需要 TURN，请通过模板输入配置外部 TURN 服务。

## 常见使用场景

- **远程团队访问**：为分布式团队和内部工具建立基于 WireGuard 的私有网络。
- **多云互联**：用统一策略模型连接云端、边缘和本地设备。
- **Homelab 与边缘管理**：管理私有设备访问，而不必公开每一个服务。
- **零信任服务访问**：基于用户、用户组和节点策略控制内部资源。
- **自托管 VPN 替代方案**：用点对点 WireGuard 连接和集中策略控制替代传统 VPN 网关。

## NetBird 托管依赖

此 Sealos 模板包含自托管 NetBird 控制平面所需的运行组件：

- NetBird Dashboard
- 带嵌入式 IdP 的 NetBird Management
- NetBird Signal
- NetBird Relay
- Management 与 Signal 的持久化存储

### 部署依赖

- [NetBird 文档](https://docs.netbird.io/) - 官方文档
- [NetBird 自托管指南](https://docs.netbird.io/selfhosted/selfhosted-guide) - 自托管概览
- [NetBird 本地用户管理](https://docs.netbird.io/selfhosted/identity-providers/local) - 嵌入式 IdP 与首次初始化
- [NetBird GitHub 仓库](https://github.com/netbirdio/netbird) - 源码和版本发布
- [WireGuard 文档](https://www.wireguard.com/) - WireGuard 协议信息

### 实现细节

**架构组件：**

此模板部署四个 NetBird 服务：

- **Dashboard (`netbirdio/dashboard:v2.38.1`)**：用于管理、引导和日常操作的 Web UI。
- **Management (`netbirdio/management:0.71.4`)**：核心 HTTP/gRPC API、嵌入式 IdP、策略引擎和账号状态。
- **Signal (`netbirdio/signal:0.71.4`)**：用于节点协调连接的信令服务。
- **Relay (`netbirdio/relay:0.71.4`)**：用于受限网络路径的中继端点。

**Ingress 与域名路由：**

- **主 HTTPS 域名**（`${app_host}.${SEALOS_CLOUD_DOMAIN}`）：
  - `/` 路由到 Dashboard
  - `/api`、`/oauth2` 和 `/ws-proxy/management` 路由到 Management
  - `/ws-proxy/signal` 路由到 Signal
  - `/relay` 路由到 Relay
- **专用 gRPC 域名**（`${grpc_host}.${SEALOS_CLOUD_DOMAIN}`）：
  - `/management.ManagementService/` 路由到 Management gRPC
  - `/signalexchange.SignalExchange/` 路由到 Signal gRPC

**配置：**

- Management 使用 SQLite 将控制平面和嵌入式 IdP 数据存储在 `/var/lib/netbird`。
- Management 和 Signal 使用 `100Mi` 持久化卷。
- Relay 通过主 HTTPS ingress 路径暴露为 `rels://<app-host>:443/relay`。
- 可通过 `external_turn_host`、`external_turn_username` 和 `external_turn_password` 配置可选外部 TURN。

**许可证信息：**

此 Sealos 模板遵循 Sealos templates 项目的仓库许可证政策。NetBird 本身采用 [BSD-3-Clause License](https://github.com/netbirdio/netbird/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 NetBird？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、扩缩容和日常运维。在 Sealos 上部署 NetBird 可以获得：

- **一键部署**：无需手写 Kubernetes 清单即可部署 NetBird 控制平面。
- **自动 HTTPS 访问**：Sealos 会为 Dashboard、API 和 gRPC 端点分配公网 URL 与 TLS 证书。
- **内置持久化状态**：Management 和 Signal 状态会通过持久化存储在重启后保留。
- **Canvas 运维**：部署后可通过 Canvas、AI 对话和资源卡片查看或调整资源。
- **资源高效默认值**：以紧凑的 CPU limit、内存和存储配置启动，适合初始自托管使用。
- **Kubernetes 基础能力**：使用标准 Kubernetes 原语运行 NetBird，同时避免直接管理集群的复杂度。

在 Sealos 上部署 NetBird，把精力集中在安全私有网络，而不是基础设施编排上。

## 部署指南

1. 打开 [NetBird 模板](https://sealos.io/products/app-store/netbird)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `disable_default_policy`：选择是否禁用 NetBird 默认的全互通策略。
   - `external_turn_host`：可选外部 TURN 端点，例如 `turn.example.com:3478`。
   - `external_turn_username` 和 `external_turn_password`：仅在配置外部 TURN 端点时需要。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话中描述需求，或点击相关资源卡片调整配置。
4. 打开生成的 NetBird 应用 URL。
5. 完成首次初始化：
   - 如果需要初始化，Dashboard 会跳转到 `/setup`。
   - 输入初始 owner 邮箱、密码和可选姓名。
   - NetBird 会通过 setup API 创建 owner 账号，然后跳转到登录页。
6. 使用刚创建的 owner 凭据登录。

## 配置

部署后，你可以通过以下方式配置 NetBird：

- **NetBird Dashboard**：管理用户、节点、setup key、访问策略、路由、DNS 和反向代理设置。
- **Canvas AI 对话**：描述变更需求，让 Sealos 应用资源更新。
- **资源卡片**：编辑 Deployment、StatefulSet、Service、Ingress 和环境变量。

### 输入参数

- **`disable_default_policy`**：禁用默认全互通策略（`true` 或 `false`）。
- **`external_turn_host`**：可选外部 TURN 主机和端口。
- **`external_turn_username`**：TURN 用户名；设置 `external_turn_host` 时需要。
- **`external_turn_password`**：TURN 密码；设置 `external_turn_host` 时需要。

### 首次登录与注册

此模板使用 NetBird 嵌入式 IdP 本地用户。模板没有预置默认管理员。首次访问时，打开应用 URL 并完成 `/setup` 向导来创建初始 owner 账号。只有当 `GET /api/instance` 返回 `setup_required: true` 时，setup 向导才可使用。

如需自动初始化，可在部署后调用一次 setup API：

```bash
curl -X POST "https://<your-netbird-url>/api/setup"   -H "Content-Type: application/json"   -d '{"email":"admin@example.com","password":"securepassword123","name":"Admin User"}'
```

请安全保存 owner 凭据。初始化完成后，可在 Dashboard 中创建或邀请更多用户。

## 扩缩容

扩缩容步骤：

1. 打开 NetBird 部署对应的 Canvas。
2. 点击相关 Deployment 或 StatefulSet 资源卡片。
3. 调整 CPU limit、内存、存储或副本设置。
4. 应用变更并观察滚动更新状态。

对于小团队，建议每个组件保持 1 个副本，除非你已评估 NetBird 在目标拓扑下的状态和 ingress 要求。

## 故障排查

### 初始化页面没有出现

- 检查 `https://<your-netbird-url>/api/instance`。
- 如果返回 `{"setup_required": true}`，打开 `https://<your-netbird-url>/setup`。
- 如果返回 `false`，说明 owner 账号已经存在，请直接登录。

### 初始化后无法登录

- 确认 Management Pod 正在运行。
- 确认 `https://<your-netbird-url>/oauth2/.well-known/openid-configuration` 能返回嵌入式 IdP 元数据。
- 确认 owner 密码没有被修改或遗失。

### 节点连接不稳定

- 检查节点网络是否需要 TURN。
- 如果严格 NAT 穿透是必需的，请通过模板输入配置外部 TURN 端点。

### Dashboard 可用但 gRPC 操作失败

- 确认 Canvas 中存在专用 gRPC 域名。
- 确认 Management 和 Signal gRPC ingress 使用 GRPC backend protocol。

### 获取帮助

- [NetBird 文档](https://docs.netbird.io/)
- [NetBird GitHub Issues](https://github.com/netbirdio/netbird/issues)
- [NetBird 社区](https://netbird.io/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [NetBird 架构](https://docs.netbird.io/about-netbird/architecture)
- [NetBird 节点管理](https://docs.netbird.io/how-to/manage-peers)
- [NetBird 本地用户管理](https://docs.netbird.io/selfhosted/identity-providers/local)
- [WireGuard 协议概览](https://www.wireguard.com/protocol/)

## 许可证

此 Sealos 模板遵循 Sealos templates 项目的仓库许可证政策。NetBird 本身采用 [BSD-3-Clause License](https://github.com/netbirdio/netbird/blob/main/LICENSE)。
