# 在 Sealos 上部署和托管 RustDesk Server

RustDesk Server 为 RustDesk 客户端提供自托管 ID/会合服务和中继服务。此模板会在 Sealos Cloud 上部署 RustDesk Server S6 镜像，提供持久化密钥存储、面向客户端流量的 NodePort 暴露，以及指向区域 TCP 网关的 Sealos 应用入口。

## 关于托管 RustDesk Server

RustDesk Server 在同一个 StatefulSet 中运行 `hbbs` 会合服务和 `hbbr` 中继服务。模板会把服务器密钥对和轻量 SQLite 元数据保存在 `/data`，因此重启后公钥仍保持稳定。

此部署不是 Web 控制台，不需要浏览器登录或注册账号。用户需要在 RustDesk 桌面端或移动端中填写 Sealos TCP 网关主机、分配到的 NodePort，以及在启用加密时填写 Pod 日志中的公钥。

## 常见使用场景

- **私有远程桌面中继**：通过自己控制的基础设施转发 RustDesk 远程桌面会话。
- **团队支持网关**：为支持工程师和受管设备提供共享 ID 与中继服务器。
- **加密客户端接入**：将 `ENCRYPTED_ONLY` 设置为 `1`，要求 RustDesk 客户端使用服务器公钥。
- **可移植实验环境**：无需维护 Kubernetes 清单，即可运行隔离的远程访问测试中继。

## RustDesk Server 托管依赖

此 Sealos 模板包含所有必需运行资源：RustDesk Server S6 容器、用于 `/data` 的持久化存储、面向 RustDesk 客户端端口的 NodePort Service，以及展示 TCP 网关主机的 Sealos App 链接。

### 部署依赖

- [RustDesk Server GitHub 仓库](https://github.com/rustdesk/rustdesk-server) - 服务器源码和发布说明
- [RustDesk 文档](https://rustdesk.com/docs/) - RustDesk 客户端与自托管文档
- [RustDesk Server Docker Hub](https://hub.docker.com/r/rustdesk/rustdesk-server-s6) - 此模板使用的容器镜像
- [Sealos 应用商店](https://sealos.io/products/app-store/rustdesk) - 一键部署入口

## 实现细节

**架构组件：**

此模板部署一个有状态服务：

- **RustDesk Server**：运行 `hbbs` 处理 ID/会合流量，运行 `hbbr` 处理中继流量。
- **持久化卷**：保存 `/data`，包括生成的 `id_ed25519` 密钥对和 RustDesk 服务器元数据。
- **NodePort Service**：通过 Sealos TCP 网关暴露 RustDesk 客户端端口 `21115/tcp`、`21116/tcp`、`21116/udp` 和 `21117/tcp`。
- **Sealos App 链接**：在 Canvas 中展示网关主机 `tcp.${{ SEALOS_CLOUD_DOMAIN }}`。

**配置：**

- `ENCRYPTED_ONLY=1` 要求客户端配置服务器公钥，这是推荐设置。
- `ENCRYPTED_ONLY=0` 允许客户端不配置服务器公钥即可连接，适合快速测试，但限制更弱。
- `RELAY` 环境变量由生成的 Sealos 主机名设置，确保 `hbbs` 对外声明正确的中继地址。
- 模板使用固定镜像 `rustdesk/rustdesk-server-s6:1.1.15`，对应 S6 服务器镜像可用的最新 RustDesk Server 发布流。

**资源配置：**

Sealos 在线测试已验证：服务在 `1m` CPU / `5Mi` 内存 requests 与 `20m` CPU / `24Mi` 内存 limits 下，`hbbs` 和 `hbbr` 均保持健康。如果你预计有大量并发远程桌面会话或持续中继带宽，请在 Canvas 中提高资源。

**许可证信息：**

RustDesk Server 使用 AGPL-3.0 许可证。此 Sealos 模板作为 RustDesk Server 的部署自动化提供。

## 为什么在 Sealos 上部署 RustDesk Server？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、公网访问、存储和后续运维。在 Sealos 上部署 RustDesk Server 可以获得：

- **一键部署**：直接从应用商店部署 RustDesk Server，无需编写 Kubernetes YAML。
- **持久化密钥存储**：重启后保留生成的 RustDesk 服务器密钥对。
- **即时 TCP 网关访问**：为 RustDesk 客户端使用 Sealos 区域 TCP 网关和分配到的 NodePort。
- **易于自定义**：通过 Canvas 和 AI 辅助运维调整加密模式、资源和存储。
- **按量付费效率**：从最小资源配置开始，只在中继流量需要时扩容。
- **Kubernetes 基础能力**：使用托管 Kubernetes 原语运行 RustDesk Server，无需管理集群细节。

## 部署指南

1. 打开 [RustDesk 模板](https://sealos.io/products/app-store/rustdesk)，点击 **Deploy Now**。
2. 在弹窗中配置 `ENCRYPTED_ONLY`。使用 `1` 启用需要公钥的加密接入，或使用 `0` 进行限制较少的测试部署。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续如需修改，可以在 AI 对话框描述需求，或点击对应资源卡片调整配置。
4. 打开 RustDesk Server Pod 日志，复制以 `Key:` 开头的那一行。当 `ENCRYPTED_ONLY=1` 时必须填写此公钥。
5. 在 Canvas 中打开 Service 资源，记录以下端口分配到的 NodePort：
   - **ID Server**：`rendezvous-tcp` / `rendezvous-udp`，对应端口 `21116`
   - **Relay Server**：`relay`，对应端口 `21117`
   - **NAT Test**：`heartbeat`，对应端口 `21115`
6. 在 RustDesk 客户端中打开 **设置 → 网络 → ID/中继服务器**，填写：
   - **ID Server**：`tcp.${{ SEALOS_CLOUD_DOMAIN }}:<rendezvous-nodeport>`
   - **Relay Server**：`tcp.${{ SEALOS_CLOUD_DOMAIN }}:<relay-nodeport>`
   - **API Server**：留空，除非你另行部署 RustDesk API 服务
   - **Key**：当 `ENCRYPTED_ONLY=1` 时，粘贴 Pod 日志中的公钥
7. 保存设置。RustDesk 客户端连通自托管 ID Server 后，状态应变为就绪。

## 配置

部署后，你可以通过以下方式配置 RustDesk Server：

- **AI 对话框**：描述资源或环境变量调整需求，由 Sealos 应用变更。
- **资源卡片**：在 Canvas 中点击 StatefulSet、Service 或存储卡片，查看并修改配置。
- **RustDesk 客户端设置**：配置客户端侧 ID Server、Relay Server 和 Key。

此模板不包含 RustDesk Server Web 登录功能。访问控制由 RustDesk 客户端配置决定；启用加密模式时，还由服务器公钥限制。

## 扩缩容

如需为更高的中继流量提升资源：

1. 打开此部署的 Canvas。
2. 点击 RustDesk StatefulSet 资源卡片。
3. 根据活跃会话数和中继带宽提高 CPU 与内存 limits。
4. 在对话框中应用变更，并等待 Pod 滚动更新完成。

除非你有自定义多服务器 RustDesk 拓扑，否则建议保持单副本。生成的密钥和本地元数据与 StatefulSet 持久化卷绑定。

## 故障排查

### 客户端无法进入就绪状态

- **原因**：客户端填写了错误的 TCP 网关主机、NodePort 或 Key。
- **解决方案**：重新检查 Service NodePort，使用 `tcp.${{ SEALOS_CLOUD_DOMAIN }}` 作为主机；当 `ENCRYPTED_ONLY=1` 时，从 Pod 日志复制最新 `Key:` 值。

### 中继连接不稳定

- **原因**：客户端缺少 Relay NodePort 或服务器公钥配置。
- **解决方案**：同时填写 RustDesk 客户端中的 ID Server 和 Relay Server。如果启用了加密模式，也要填写 Key 字段。

### Pod 正常运行但客户端无法连接

- **原因**：客户端流量没有到达暴露的 NodePort。
- **解决方案**：确认 Service 已列出 `21116/tcp`、`21116/udp`、`21117/tcp` 和 `21115/tcp` 的 NodePort，然后在允许访问该网关 TCP/UDP 出站流量的网络中测试。

## 其他资源

- [RustDesk 官网](https://rustdesk.com/)
- [RustDesk Server Releases](https://github.com/rustdesk/rustdesk-server/releases)
- [RustDesk 文档](https://rustdesk.com/docs/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板按仓库许可证提供。RustDesk Server 本身使用 AGPL-3.0 许可证。
