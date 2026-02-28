# 在 Sealos 上部署并托管 Node-RED

Node-RED 是一个低代码、流程编排（flow-based）开发工具，可用于连接 API、设备和各类服务。该模板会在 Sealos Cloud 上部署一个具备持久化能力、可用于生产环境的 Node-RED 服务。

![Node-RED Logo](logo.png)

## 关于在 Sealos 托管 Node-RED

Node-RED 提供浏览器可视化编辑器，你可以通过拖拽和连接节点来构建集成流程与自动化任务。它常用于物联网（IoT）流程、Webhook 编排、数据路由以及内部运维自动化。

该 Sealos 模板以单 StatefulSet 方式部署 Node-RED，并将持久化存储挂载到 `/data`，用于保存流程、凭据和运行时数据。公网访问通过 Sealos Ingress 提供 HTTPS，并由平台自动管理 TLS 证书。

## 常见使用场景

- **工作流自动化**：连接软件即服务（SaaS）工具、内部 API 与事件流，无需编写完整后端服务。
- **IoT 数据处理**：采集、转换并分发设备遥测数据到数据库、消息队列或仪表盘。
- **Webhook 编排**：接收 Webhook 事件，补充上下文数据后触发下游业务逻辑。
- **集成原型快速验证**：在正式开发长期方案前，先快速验证集成可行性。
- **内部运维工具**：构建轻量自动化能力，用于告警、通知和定时任务。

## Node-RED 托管依赖

该 Sealos 模板已包含 Node-RED 运行所需的全部核心依赖：

- Node-RED 应用容器
- 用于稳定运行身份的 Kubernetes `StatefulSet`
- 用于集群内流量转发的 Kubernetes `Service`
- 用于公网 HTTPS 暴露的 Kubernetes `Ingress`
- 挂载到 `/data` 的持久卷声明（Persistent Volume Claim, PVC）

### 部署依赖文档

- [Node-RED Official Website](https://nodered.org/) - 产品概览与社区入口
- [Node-RED Documentation](https://nodered.org/docs/) - 安装、运行与节点开发文档
- [Node-RED GitHub Repository](https://github.com/node-red/node-red) - 源码与问题跟踪
- [Sealos Documentation](https://sealos.io/docs) - 平台使用与运维文档

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Node-RED StatefulSet**（`nodered/node-red:4.1.6`）：主服务，`1` 个副本
- **Service**：在集群内暴露容器端口 `1880`
- **Ingress**：通过 `https://<app_host>.<SEALOS_CLOUD_DOMAIN>` 提供 TLS 访问
- **Persistent Storage**：`0.1Gi` PVC，挂载路径为 `/data`

**配置说明：**

- `app_host` 控制公网域名前缀。
- `app_name` 控制 Kubernetes 资源命名。
- 默认 Pod 资源配置：
  - **limits**：`cpu: 100m`，`memory: 128Mi`
  - **requests**：`cpu: 10m`，`memory: 12Mi`
- Node-RED 会将流程与凭据等数据持久化到 `/data`。

**许可证信息：**

Node-RED 采用 [Apache License 2.0](https://github.com/node-red/node-red/blob/master/LICENSE)。

## 为什么在 Sealos 上部署 Node-RED？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，覆盖部署、运维与日常管理全流程。将 Node-RED 部署到 Sealos，你可以获得：

- **一键部署**：无需手写 Kubernetes YAML，即可快速上线 Node-RED。
- **Kubernetes 级可靠性**：基于成熟的 StatefulSet、Service 和 Ingress 原语运行。
- **内置持久化存储**：流程和运行数据在重启后依然可保留。
- **即时公网 HTTPS 访问**：默认获得带托管 TLS 证书的公网地址。
- **灵活配置能力**：通过 Canvas 对话框和 AI 辅助方式完成参数调整。
- **按量计费更省成本**：资源随使用规模弹性调整，避免过度预留。

把 Node-RED 部署到 Sealos 后，你可以把精力放在流程自动化本身，而不是基础设施维护。

## 部署指南

1. 打开 [Node-RED 模板](https://sealos.io/appstore/node-red)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - `app_host`
   - `app_name`
3. 等待部署完成（通常 2-3 分钟）。部署完成后会自动跳转到 Canvas。
4. 在 Canvas 打开生成的 Node-RED 访问地址，即可进入 Web 编辑器开始创建流程。

## 配置

部署完成后，你可以通过以下方式管理 Node-RED：

- **AI Dialog**：描述你想要的配置或资源变更，由 AI 自动应用。
- **Resource Cards**：点击 StatefulSet、Service、Ingress 或存储卡片进行调整。
- **Node-RED Editor**：在 Web 界面中导入/导出流程并配置节点。

### 模板参数

| Parameter | Description | Default |
| --- | --- | --- |
| `app_host` | Node-RED 公网地址使用的域名前缀 | `node-red-<random>` |
| `app_name` | 本次部署的 Kubernetes 资源名前缀 | `node-red-<random>` |

## 扩缩容

如需调整 Node-RED 资源，可按以下步骤操作：

1. 在 Canvas 打开你的部署。
2. 点击 Node-RED 的 StatefulSet 资源卡片。
3. 调整 CPU 与内存 limits/requests。
4. 应用变更并观察滚动更新状态。

对于大多数流程自动化场景，建议先进行纵向扩容（CPU/内存）再评估是否需要调整副本数。

## 故障排查

### 常见问题

**问题：部署后 Node-RED URL 无法立即访问**
- 原因：Ingress 配置或 DNS 传播尚未完成。
- 解决：等待几分钟后，从 Canvas 刷新并重新访问。

**问题：重启后流程或凭据丢失**
- 原因：`/data` 未正确持久化，或存储配置被意外修改。
- 解决：检查 PVC 绑定状态，并确认卷已挂载到 `/data`。

**问题：编辑器公网可访问，但没有预期的登录保护**
- 原因：Node-RED 默认不会强制启用管理员认证。
- 解决：在 Node-RED 配置中启用 `adminAuth`，并重新部署受保护的运行配置。

### 获取帮助

- [Node-RED Documentation](https://nodered.org/docs/)
- [Node-RED Forum](https://discourse.nodered.org/)
- [Node-RED GitHub Issues](https://github.com/node-red/node-red/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Node-RED Flows Library](https://flows.nodered.org/)
- [Node-RED Getting Started](https://nodered.org/docs/getting-started/)
- [Node-RED User Guide](https://nodered.org/docs/user-guide/)
- [Node-RED Docker Guide](https://nodered.org/docs/getting-started/docker)

## 许可证

该 Sealos 模板遵循 templates 仓库的许可证策略。Node-RED 本身采用 [Apache License 2.0](https://github.com/node-red/node-red/blob/master/LICENSE)。
