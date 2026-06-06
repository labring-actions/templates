# 在 Sealos 上部署和托管 BunkerWeb

BunkerWeb 是一款基于 NGINX 的开源 Web 应用防火墙和反向代理。本模板在 Sealos Cloud 上部署 BunkerWeb、scheduler、Web UI、PostgreSQL、Redis、受保护演示后端，并提供可选的 S3 兼容备份配置。

![BunkerWeb 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bunkerweb/website-screenshot.webp)

## 关于托管 BunkerWeb

BunkerWeb 通过基于 NGINX 的反向代理保护 Web 服务，提供 ModSecurity、速率限制、IP 控制、机器人防护、自定义响应头、gzip、缓存控制和集中配置等能力。scheduler 负责计算并下发配置，Web UI 提供服务、实例、任务、插件、报告和设置的管理员控制台。

本 Sealos 模板遵循 BunkerWeb 官方多容器部署模型。模板将 BunkerWeb 作为流量网关运行，将 scheduler 作为配置控制面运行，并部署官方 Web UI 管理控制台。PostgreSQL 存储 BunkerWeb 配置数据库，Redis 支撑共享运行时状态。

模板还会部署一个位于 BunkerWeb 后方的 `whoami` 演示后端，便于部署后立即验证反向代理路径。接入真实应用时，请替换该后端并在 BunkerWeb 中更新服务配置。

## 常见使用场景

- **Web 应用防火墙**：为公开 Web 应用添加安全控制。
- **反向代理网关**：将外部 HTTP 流量路由到内部服务。
- **安全策略测试**：在保护生产服务前评估 BunkerWeb 规则和插件行为。
- **集中管理控制台**：通过 BunkerWeb Web UI 管理服务、实例、插件、任务和报告。
- **备份就绪配置**：启用 Sealos 对象存储，为 BunkerWeb PRO S3 备份设置提供凭据。

## BunkerWeb 托管依赖

Sealos 模板包含单实例 BunkerWeb 部署所需的依赖：

- BunkerWeb `1.6.11`
- BunkerWeb Scheduler `1.6.11`
- BunkerWeb Web UI `1.6.11`
- 通过 KubeBlocks 提供的 PostgreSQL `16.4.0`
- 通过 KubeBlocks 提供的 Redis `7.2.7` 和 Sentinel
- 使用 `traefik/whoami` 的受保护演示后端
- scheduler 数据和 Web UI 状态/日志持久卷
- 用于 S3 兼容备份设置的可选 Sealos `ObjectStorageBucket`
- Kubernetes Service 与 HTTPS Ingress

### 部署依赖

- [BunkerWeb 官网](https://www.bunkerweb.io/) - 产品概览
- [BunkerWeb 文档](https://docs.bunkerweb.io/) - 官方文档
- [BunkerWeb GitHub 仓库](https://github.com/bunkerity/bunkerweb) - 源代码和问题跟踪
- [BunkerWeb Helm Chart](https://github.com/bunkerity/helm-charts) - 官方 Kubernetes Chart
- [Sealos 文档](https://sealos.io/docs) - 平台和运维指南

## 实现细节

### 架构组件

本模板部署以下组件：

- **BunkerWeb Gateway**：运行 `bunkerity/bunkerweb:1.6.11`，在 `8080` 端口暴露 HTTP 流量，并在 `5000` 端口为 scheduler 暴露 BunkerWeb API。
- **Scheduler**：运行 `bunkerity/bunkerweb-scheduler:1.6.11`，初始化并维护 BunkerWeb 数据库，保存生成配置，并向 BunkerWeb API 推送变更。
- **Web UI**：运行 `bunkerity/bunkerweb-ui:1.6.11`，在 `7000` 端口提供管理员控制台，并根据部署输入创建初始管理员。
- **PostgreSQL Cluster**：存储 BunkerWeb 配置、UI 用户、服务、任务、插件、报告和元数据。
- **Redis Cluster**：为 BunkerWeb 提供共享缓存、会话和运行时状态。
- **受保护演示后端**：运行 `traefik/whoami`，用于部署后立即验证网关。
- **可选对象存储**：启用 `enable_s3_backup` 后创建私有 Sealos bucket，并注入 BunkerWeb S3 备份配置。

### 配置

- `admin_username` 和 `admin_password` 用于创建 BunkerWeb Web UI 初始管理员。
- `enable_s3_backup` 会创建 Sealos 对象存储并注入官方 BunkerWeb `backup_s3` 设置，该能力属于 BunkerWeb PRO 备份功能。
- 应用公共 URL 通过 BunkerWeb 网关路由到受保护演示后端。
- 管理公共 URL 直接路由到 Web UI。生产运维时，请按照组织策略检查访问控制并保护管理 URL。
- scheduler 通过 `BUNKERWEB_INSTANCES` 指向 BunkerWeb API Service，并将服务配置存储到 PostgreSQL。
- 启动门会等待 PostgreSQL、Redis、BunkerWeb API 和数据库元数据初始化完成，提升冷启动收敛稳定性。

### 反向代理注意事项

默认受保护服务是演示端点。接入真实应用时，请在 BunkerWeb 中更新服务主机和反向代理设置，并根据应用行为验证生成策略。安全规则可能拦截特殊请求头、请求体、机器人、扫描器或路径；上线生产流量前请测试登录、上传、API 和健康检查。

### 许可信息

BunkerWeb 使用 GNU Affero General Public License v3.0。此 Sealos 模板是 BunkerWeb 的部署配置，并遵循模板仓库的许可条款。

## 为什么在 Sealos 上部署 BunkerWeb？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署与运维。在 Sealos 上部署 BunkerWeb 可以获得：

- **一键部署**：一次性启动 BunkerWeb、scheduler、UI、PostgreSQL、Redis、存储和入口。
- **托管数据服务**：PostgreSQL 和 Redis 通过 KubeBlocks 自动创建。
- **即时 HTTPS 访问**：Sealos 为受保护网关和管理 UI 创建公开 HTTPS URL。
- **持久配置**：BunkerWeb 数据通过 PostgreSQL 和持久卷在 Pod 重启后保留。
- **可选对象存储**：从部署表单创建 S3 兼容 bucket，用于备份配置。
- **AI 辅助运维**：通过 Canvas 和 AI 对话调整资源、环境变量和网络配置。

在 Sealos 上部署 BunkerWeb，把 Kubernetes 底层能力交给平台，把精力放在安全网关管理上。

## 部署指南

1. 打开 [BunkerWeb 模板](https://sealos.io/products/app-store/bunkerweb)，点击 **Deploy Now**。
2. 配置部署参数：
   - `admin_username`：BunkerWeb Web UI 管理员用户名。
   - `admin_password`：BunkerWeb Web UI 管理员密码。
   - `enable_s3_backup`：创建 Sealos 对象存储并注入 S3 备份设置。
3. 等待部署完成。BunkerWeb 冷启动包括 PostgreSQL、Redis、scheduler 数据库初始化和 Web UI 启动。
4. 从 Canvas 打开生成的 URL：
   - **受保护服务 URL**：通过 BunkerWeb 路由到演示后端。
   - **BunkerWeb Web UI URL**：打开管理员控制台。
5. 使用配置的管理员凭据登录 Web UI。
6. 按照 BunkerWeb 首次登录页面完成 TOTP 或恢复码流程，然后进入仪表盘。
7. 使用生产流量前，请将演示后端替换为真实服务配置。

## 配置

部署后可以通过以下方式配置 BunkerWeb：

- **BunkerWeb Web UI**：管理服务、实例、插件、任务、报告和账号设置。
- **Sealos AI 对话**：用自然语言描述资源、环境变量、存储或网络变更。
- **资源卡片**：在 Canvas 中打开 Deployment、StatefulSet、Service、Ingress、PostgreSQL、Redis 和对象存储卡片。

首次生产使用前，请检查管理 URL 暴露范围、BunkerWeb 安全规则、反向代理目标、请求大小、机器人防护和备份策略。

## 扩缩容

本模板默认启动一个 BunkerWeb 网关、一个 scheduler、一个 Web UI、一个 PostgreSQL 实例和一个 Redis replication 拓扑。优先通过 BunkerWeb 网关和 scheduler 资源卡片提高 CPU 与内存。多实例网关扩展需要协调 BunkerWeb 实例注册和流量测试。

## 故障排查

### 管理员登录提示 TOTP

BunkerWeb 可能要求首次登录完成双因素认证注册或恢复码处理。请在 Web UI 中完成提示流程，并安全保存恢复码。

### 受保护服务返回安全拦截页面

在 Web UI 报告或日志中查看命中的 BunkerWeb 规则，并针对应用请求模式调整服务策略。

### Web UI 冷启动等待

Web UI 依赖 scheduler 完成数据库初始化。等待 PostgreSQL、Redis、scheduler 和 BunkerWeb Pod 就绪后刷新 Web UI URL。

### S3 备份设置未生效

部署时启用 `enable_s3_backup`，并在 Web UI 中确认 BunkerWeb PRO 备份插件行为。模板会为 BunkerWeb `backup_s3` 设置注入 Sealos 对象存储凭据。

### 获取帮助

- [BunkerWeb 文档](https://docs.bunkerweb.io/)
- [BunkerWeb GitHub Issues](https://github.com/bunkerity/bunkerweb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [BunkerWeb Quick Start](https://docs.bunkerweb.io/latest/quickstart-guide/)
- [BunkerWeb Integrations](https://docs.bunkerweb.io/latest/integrations/)
- [BunkerWeb Features](https://docs.bunkerweb.io/latest/features/)
- [Sealos App Store](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循模板仓库的许可条款。BunkerWeb 本身使用 GNU Affero General Public License v3.0。
