# 在 Sealos 上部署和托管 Headscale

Headscale 是一个开源的自托管 Tailscale 控制服务器实现。这个模板会在 Sealos Cloud 上部署 Headscale、Headplane、持久化存储、公开 Ingress 访问能力，并支持可选 PostgreSQL 数据库。

![Headscale 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/headscale/website-screenshot.webp)

## 关于托管 Headscale

Headscale 为私有的 Tailscale 兼容 tailnet 提供协调服务器能力。它负责节点注册、用户管理、路由通告、DNS 设置、ACL 策略存储和控制平面通信；在条件允许时，设备之间的实际流量仍会直接点对点传输。

这个 Sealos 模板会在同一个 StatefulSet 中运行 Headscale 和 Headplane。Headscale 负责控制平面、gRPC 端点和 metrics 端点，Headplane 提供 Web 管理界面，可用于管理 Headscale 用户、机器、路由、DNS、ACL 和预授权密钥。

默认情况下，模板使用 SQLite，并将数据保存在持久化卷中。如果部署时启用 `use_postgresql`，Sealos 会通过 KubeBlocks 创建 PostgreSQL 16.4.0 集群，初始化 `headscale` 数据库，并把 PostgreSQL 配置写入 Headscale 的 `config.yaml`。这是因为 Headscale 从配置文件读取数据库设置，而不是通过数据库环境变量直接配置。

## 常见使用场景

- **私有 Mesh VPN 控制平面**：为 Tailscale 兼容客户端托管自己的协调服务器。
- **家庭实验室和团队网络**：连接跨网络的服务器、笔记本和服务，而不必将所有服务直接暴露到公网。
- **路由和 DNS 管理**：通过 Headplane 管理通告路由、类似 MagicDNS 的设置和网络记录。
- **ACL 和标签管理**：为小团队或实验环境编辑 ACL 策略，并组织机器访问权限。
- **预授权密钥流程**：创建可复用或临时的预授权密钥，简化设备加入流程。

## Headscale 托管依赖

Sealos 模板包含所需的运行组件：Headscale、Headplane、持久化存储、Service/Ingress 资源、Headplane Kubernetes 集成所需的 RBAC，以及可选的 KubeBlocks PostgreSQL。

### 部署依赖

- [Headscale 文档](https://headscale.net/stable/) - Headscale 官方文档
- [Headscale GitHub 仓库](https://github.com/juanfont/headscale) - 源码和版本发布
- [Headplane GitHub 仓库](https://github.com/tale/headplane) - Web UI 源码和文档
- [Tailscale 文档](https://tailscale.com/kb/) - 客户端和 tailnet 相关概念
- [Sealos 文档](https://sealos.io/docs/) - Sealos 平台文档

### 实现细节

**架构组件：**

本模板会部署以下服务和资源：

- **Headscale**：控制服务器容器，使用 `headscale/headscale:0.29.0-beta.1-debug`。
- **Headplane**：Web 管理界面，使用 `ghcr.io/tale/headplane:0.6.3`。
- **SQLite 存储**：默认数据库模式，数据库文件位于持久化卷中的 `/var/lib/headscale/db.sqlite`。
- **PostgreSQL**：启用 `use_postgresql` 时创建的 KubeBlocks PostgreSQL 16.4.0 集群。
- **PostgreSQL 初始化 Job**：以幂等方式创建 `headscale` 数据库，然后应用再连接数据库。
- **ConfigMap**：保存 Headscale、DERP 和 Headplane 配置文件。
- **持久化卷**：保存 `/var/lib/headscale` 和 `/etc/headscale` 下的数据和生成后的配置。
- **Ingress 规则**：通过 `/admin` 暴露 Headplane，通过主域名暴露 Headscale HTTP 流量，并通过独立 gRPC 域名暴露 Headscale gRPC。

**配置：**

- `use_postgresql` 控制模板使用 SQLite 还是创建 PostgreSQL。
- Headscale 数据库设置会在初始化阶段渲染到 `/etc/headscale/config.yaml`。
- Headplane 读取 `/etc/headscale/headplane.yaml`，并在 Pod 内通过 `http://127.0.0.1:8080` 连接 Headscale。
- StatefulSet 使用 `shareProcessNamespace: true`，让 Headplane 可以通过 Kubernetes 集成访问 Headscale 进程。
- Headscale 和 Headplane 都使用适合小规模部署的保守 CPU 与内存限制。

**许可证信息：**

Headscale 使用 BSD-3-Clause 许可证。Headplane 使用 MIT 许可证。这个 Sealos 模板遵循上游项目的许可条款。

## 为什么在 Sealos 上部署 Headscale？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统，覆盖从云端 IDE 开发到生产部署和运维管理的完整应用生命周期。它适合现代应用、内部工具、SaaS 平台和多服务部署。将 Headscale 部署在 Sealos 上，你可以获得：

- **一键部署**：直接从应用商店部署 Headscale 和 Headplane，不需要手写 Kubernetes YAML。
- **可选数据库自动创建**：默认使用 SQLite，也可以启用由 KubeBlocks 管理的 PostgreSQL 数据库。
- **易于自定义**：通过 Sealos UI 配置参数、资源限制、存储和运行时设置。
- **无需 Kubernetes 专业经验**：使用 Kubernetes 支撑的工作负载、服务、持久化卷和 Ingress，而不必直接管理集群。
- **内置持久化存储**：Headscale 状态和配置会在 Pod 重启后继续保留。
- **即时公开访问**：Sealos 会为部署的应用提供公开 URL 和 TLS 证书。
- **AI 辅助运维**：部署后可以通过 Canvas AI 对话调整应用，也可以打开资源卡片修改具体资源。
- **按量付费更高效**：从小资源规格开始，按 tailnet 规模增长逐步调整。

在 Sealos 上部署 Headscale，把精力放在管理私有网络上，而不是维护基础设施。

## 部署指南

1. 打开 [Headscale 模板](https://sealos.io/products/app-store/headscale)，点击 **Deploy Now**。
2. 在弹出的配置对话框中设置参数：
   - 保持 `use_postgresql` 关闭，即使用默认 SQLite 部署。
   - 启用 `use_postgresql`，则由 Sealos 为 Headscale 创建 PostgreSQL 数据库。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可以在 AI 对话框中描述需求，或点击相关资源卡片调整设置。
4. 通过系统提供的访问地址打开应用：
   - **Headplane 管理界面**：打开主应用地址并访问 `/admin`。
   - **Headscale Server URL**：将主应用域名作为 Headscale 客户端使用的服务器地址。
   - **Headscale gRPC 端点**：当远程 CLI 访问需要 gRPC 时，使用独立的 gRPC 域名。

## 配置

部署后，可以通过以下方式配置 Headscale：

- **Headplane 管理界面**：在 `/admin` 管理用户、机器、路由、DNS 设置、ACL 和预授权密钥。
- **AI 对话框**：在 Sealos Canvas 中描述你要修改的配置，由 AI 协助应用变更。
- **资源卡片**：打开 StatefulSet、ConfigMap、Ingress 或数据库资源卡片，进行手动调整。
- **配置文件**：按需修改 ConfigMap 中的 Headscale 设置，并重启工作负载让配置生效。

## 扩容

Headscale 通常作为单实例控制平面部署，因为它负责保存状态并服务一个 tailnet。如需调整容量：

1. 打开对应部署的 Canvas。
2. 点击 Headscale StatefulSet 资源卡片。
3. 根据节点数量和控制平面活动情况调整 CPU 或内存资源。
4. 在对话框中应用变更。

如果启用了 PostgreSQL，也可以打开 PostgreSQL 集群资源卡片，调整数据库资源和存储。

## 故障排查

### 常见问题

**Headplane 无法管理 Headscale**

- 原因：Headplane 需要读取 Headscale 配置，并依赖 Kubernetes 集成设置。
- 解决方法：确认 Headscale Pod 已就绪，并确认 Headplane 容器可以读取 `/etc/headscale/config.yaml`。

**客户端无法注册**

- 原因：客户端可能使用了错误的服务器地址，或缺少预授权密钥。
- 解决方法：使用 Sealos 提供的 Headscale 域名作为服务器地址，并在 Headplane 中创建预授权密钥。

**PostgreSQL 模式无法启动**

- 原因：Headscale 启动前会等待 PostgreSQL 数据库和渲染后的配置就绪。
- 解决方法：在 Canvas 中检查 PostgreSQL 集群、`headscale-*-pg-init` Job 和 Headscale Pod 事件。

### 获取帮助

- [Headscale 文档](https://headscale.net/stable/)
- [Headscale GitHub Issues](https://github.com/juanfont/headscale/issues)
- [Headplane GitHub Issues](https://github.com/tale/headplane/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Headscale 稳定版文档](https://headscale.net/stable/)
- [Headscale GitHub 仓库](https://github.com/juanfont/headscale)
- [Headplane GitHub 仓库](https://github.com/tale/headplane)
- [Tailscale 知识库](https://tailscale.com/kb/)
- [Sealos 文档](https://sealos.io/docs/)

## 许可证

此 Sealos 模板遵循 Sealos 模板仓库的许可证。Headscale 使用 BSD-3-Clause 许可证，Headplane 使用 MIT 许可证。
