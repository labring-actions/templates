# 在 Sealos 上部署和托管 Derper

Derper 是 Tailscale DERP 中继服务器的精简构建，适合自托管中继和 STUN 服务。此模板会在 Sealos Cloud 上以单个 NodePort 服务部署 Derper。

![Derper 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/derper/website-screenshot.webp)

## 关于 Derper 托管

Derper 提供自托管 DERP 中继。当 Tailscale 兼容客户端无法直接点对点连接时，可以通过它转发流量。它也会暴露 STUN 端口，帮助客户端发现自己的公网地址，从而改善 NAT 穿透效果。

此模板会运行一个轻量 Derper 容器，并分别提供 DERP TCP 服务和 STUN UDP 服务。启动时的配置 Job 会检测 Sealos 分配的 NodePort，自动更新 Service 与 Deployment，再用最终端口启动 Derper 工作负载。

Derper 不是 Web 应用，没有浏览器登录或注册流程。部署完成后，请在 Headscale 或 Tailscale 的 DERP map 中配置服务详情里显示的主机名和端口。

## 常见使用场景

- **自托管 DERP 中继**：为 Tailscale 或 Headscale 网络提供私有中继服务器。
- **NAT 穿透辅助**：同时启用 STUN，让客户端更容易穿透 NAT。
- **私有网络实验**：无需手动管理服务器，即可测试自定义 DERP map 和中继行为。
- **区域中继部署**：在更靠近用户或设备的区域部署额外中继，改善连接体验。

## Derper 托管依赖

Sealos 模板包含运行所需的全部资源：一个 Derper 容器、一个用于 DERP 和 STUN 流量的 NodePort Service，以及一个短生命周期配置 Job。模板不需要外部数据库、对象存储或持久化卷。

### 部署依赖

- [Derper 源码仓库](https://github.com/yangchuansheng/derper) - 镜像来源与运行说明
- [Tailscale 自定义 DERP 服务器](https://tailscale.com/kb/1118/custom-derp-servers) - 自定义 DERP map 概念
- [Headscale DERP 文档](https://headscale.net/stable/ref/derp/) - Headscale DERP 配置说明
- [Sealos 应用商店](https://sealos.io/products/app-store/derper) - 一键部署入口

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Derper Deployment**：运行 `ghcr.io/yangchuansheng/derper:v1.99.0-pre`，并启用 DERP 与 STUN。
- **NodePort Service**：暴露一个 DERP TCP 端口和一个 STUN UDP 端口。
- **配置 Job**：读取分配到的 NodePort，更新 Service 端口、Derper 环境变量，并将 Deployment 扩容到 1 个副本。

**配置说明：**

- `enable_stun` 控制是否启用 STUN 服务，默认值为 `true`。
- `DERP_DOMAIN` 设置为 `tcp.${{ SEALOS_CLOUD_DOMAIN }}`，客户端可通过当前区域的 Sealos TCP 网关域名访问。
- `DERP_VERIFY_CLIENTS` 设置为 `false`，便于自托管场景快速使用。
- 部署使用已测试通过的 Sealos 最小资源档位：`100m` CPU 和 `128Mi` 内存。

**许可证信息：**

Derper 遵循其上游仓库的许可证条款。生产使用前，请查看 [Derper 仓库](https://github.com/yangchuansheng/derper) 和 [Tailscale 仓库](https://github.com/tailscale/tailscale)。

## 为什么在 Sealos 上部署 Derper？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖从云端开发到生产部署和运维管理的完整应用生命周期。它适合部署轻量网络工具、自托管服务和生产工作负载，同时避免手动维护 Kubernetes 的复杂度。

在 Sealos 上部署 Derper，你可以获得：

- **一键部署**：打开模板即可部署，无需编写 Kubernetes YAML。
- **NodePort 网络**：通过 Sealos 管理的 Service 暴露 DERP TCP 和 STUN UDP 端口。
- **易于配置**：可在部署弹窗或 Canvas 中调整输入参数和资源设置。
- **无需 Kubernetes 经验**：通过可视化流程使用 Kubernetes 的调度与生命周期管理能力。
- **按量使用资源**：从已测试的最小资源配额开始，只在需要时扩容。
- **AI 辅助运维**：部署后可通过 Canvas AI 对话或资源卡片调整配置。

在 Sealos 上部署 Derper，把精力放在 tailnet 配置上，而不是服务器基础设施维护上。

## 部署指南

1. 打开 [Derper 模板](https://sealos.io/products/app-store/derper)，点击 **Deploy Now**。
2. 在弹窗中配置参数。除非只需要 DERP TCP 中继流量，否则建议保持 `enable_stun` 为 `true`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会自动跳转到 Canvas。后续如需修改，可在对话框描述需求让 AI 应用变更，或点击相关资源卡片手动调整。
4. 在 Canvas 中打开 Derper Service 详情，记录分配到的端口：
   - **DERP TCP**：将 `derp-tcp` NodePort 与 `tcp.${{ SEALOS_CLOUD_DOMAIN }}` 一起使用。
   - **STUN UDP**：如果启用了 STUN，将 `stun-udp` NodePort 与 `tcp.${{ SEALOS_CLOUD_DOMAIN }}` 一起使用。
5. 将这些值写入 Headscale 或 Tailscale 的 DERP map。此应用没有 Web 登录或注册页面。

## 配置

Derper 主要通过环境变量配置。此模板已按 Sealos NodePort 网络预设上游 Derper 运行参数，部署后可以在 Canvas 中查看或调整。

你可以通过以下方式配置 Derper：

- **AI 对话**：描述希望调整的内容，让 AI 应用变更。
- **资源卡片**：点击 Deployment 或 Service 资源卡片，查看端口、环境变量和资源限制。
- **DERP Map**：更新 Headscale 或 Tailscale 配置，让客户端指向生成的主机名和端口。

### 运行参数

| 变量 | 模板值 | 作用 |
|------|--------|------|
| `DERP_DOMAIN` | `tcp.${{ SEALOS_CLOUD_DOMAIN }}` | Derper 对外声明的主机名，必须与客户端实际连接的主机名保持一致。 |
| `DERP_CERT_MODE` | `manual` | 从 `DERP_CERT_DIR` 读取证书；如果证书不存在，镜像会自动生成自签名证书。 |
| `DERP_CERT_DIR` | `/cert` | 存放生成或手动提供的 `*.crt` 与 `*.key` 文件。 |
| `DERP_ADDR` | 自动更新为 `:<derp-tcp-nodeport>` | DERP TCP 监听地址。配置 Job 会把占位端口替换为实际分配的 NodePort。 |
| `DERP_STUN` | `${{ inputs.enable_stun }}` | 控制是否启用 STUN。除非只需要 DERP 中继流量，否则建议保持默认值 `true`。 |
| `DERP_STUN_PORT` | 自动更新为 `<stun-udp-nodeport>` | STUN UDP 端口。配置 Job 会把占位端口替换为实际分配的 NodePort。 |
| `DERP_HTTP_PORT` | `-1` | 关闭可选 HTTP 调试端点。 |
| `DERP_VERIFY_CLIENTS` | `false` | 关闭 DERP peer 校验，便于自托管场景快速使用。 |
| `DERP_VERIFY_CLIENT_URL` | 未设置 | 用于获取校验密钥的上游可选配置；此模板默认不暴露。 |

当 `DERP_CERT_MODE=manual` 且证书不存在时，上游镜像会自动生成有效期两年的自签名证书。此构建面向自托管场景，并放宽了证书校验要求，请只在理解信任模型的受控环境中使用。

### Headscale 或 Tailscale DERP Map

部署完成后，打开 Service 资源卡片，复制当前 `derp-tcp` 和 `stun-udp` NodePort。请在 DERP map 中使用这些实际值，不要直接照抄下面的示例端口。

Headscale DERP 节点字段示例：

```json
{
  "HostName": "tcp.<your-sealos-cloud-domain>",
  "DERPPort": 12345,
  "STUNPort": 3478,
  "InsecureForTests": true
}
```

只有当客户端必须接受此 Derper 构建使用的自签名证书时，才设置 `InsecureForTests`。如果用于更严格的生产环境，请改用受信任证书方案。

## 扩容

Derper 通常以单副本运行，因为中继客户端会连接到明确配置的主机名和端口。如需调整资源：

1. 打开当前部署的 Canvas。
2. 点击 Derper Deployment 资源卡片。
3. 如果流量增长，将 CPU 和内存调整到下一个 Sealos 资源档位。
4. 在对话框中应用变更。

## 故障排查

### 常见问题

**客户端无法连接 DERP 服务器**
- 原因：DERP map 中的主机名或 NodePort 可能不正确。
- 解决：检查 Service 资源卡片，将当前 `derp-tcp` NodePort 复制到 DERP map。

**STUN 无法工作**
- 原因：STUN 可能被禁用，或客户端配置中缺少 UDP NodePort。
- 解决：保持 `enable_stun` 为 `true`，并使用 Service 详情中的 `stun-udp` NodePort。

**出现自签名证书警告**
- 原因：此 Derper 镜像面向自托管场景，可能使用自签名证书。
- 解决：Headscale 测试场景可在 DERP map 中设置 `InsecureForTests`。更严格的生产环境应在模板之外规划受信任证书方案。

### 获取帮助

- [Derper 源码仓库](https://github.com/yangchuansheng/derper)
- [Tailscale 自定义 DERP 服务器](https://tailscale.com/kb/1118/custom-derp-servers)
- [Headscale DERP 文档](https://headscale.net/stable/ref/derp/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Tailscale DERP 概览](https://tailscale.com/blog/how-tailscale-works/)
- [Tailscale ACL DERP 服务器](https://tailscale.com/kb/1192/acl-derp-servers)
- [Headscale 文档](https://headscale.net/stable/)

## 许可证

此 Sealos 模板遵循仓库许可证。Derper 及其上游组件分别遵循各自上游项目的许可证。
