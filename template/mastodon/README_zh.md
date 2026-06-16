# 在 Sealos 上部署和托管 Mastodon

Mastodon 是一个免费开源的去中心化社交网络服务器，面向 Fediverse 社区。本模板在 Sealos Cloud 上部署 Mastodon，并包含 PostgreSQL、Redis、Sidekiq、streaming 和 Sealos 对象存储。

![Mastodon 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mastodon/website-screenshot.webp)

## 关于托管 Mastodon

Mastodon 运行一个联邦社交媒体服务器，本地用户可以发帖、关注兼容服务器上的账号、管理社区活动，并在自有域名下维护公开身份。Web 服务提供主界面和 API，Sidekiq 处理后台任务，streaming 服务提供实时更新。

本 Sealos 模板遵循 Mastodon 的 Docker 和 Helm 部署模型。PostgreSQL 存储账号、嘟文、设置和审核数据；Redis 支撑缓存、队列和 streaming 状态；Sealos 对象存储通过 Mastodon 的 S3 兼容配置存储上传媒体。

模板会在初始化阶段创建第一个 owner 账号。公开注册模式可以在部署表单中选择关闭、审核制或开放。

## 常见使用场景

- **社区社交网络**：为组织、创作者社区或兴趣小组运行带审核能力的社交平台。
- **联邦发布**：从自有服务器发布内容，并与 Fediverse 上的用户互动。
- **私有实例**：运行只允许初始 owner 和受邀用户参与的封闭服务器。
- **研究与测试**：评估 Mastodon 运维、审核设置和联邦行为。
- **机构公开身份**：为团队、学校、公司或非营利组织托管受控账号体系。

## Mastodon 托管依赖

Sealos 模板包含以下依赖：

- Mastodon `4.5.11`
- Mastodon Streaming `4.5.11`
- 通过 KubeBlocks 提供的 PostgreSQL `16.4.0`
- 通过 KubeBlocks 提供的 Redis `7.2.7` 和 Sentinel
- 用于 S3 兼容媒体存储的 Sealos `ObjectStorageBucket`
- 用于数据库准备和初始 owner 创建的 Setup Job
- Web、Sidekiq 和 streaming Deployment
- Kubernetes Service 与 HTTPS Ingress

### 部署依赖

- [Mastodon 官网](https://joinmastodon.org/) - 产品概览
- [Mastodon 文档](https://docs.joinmastodon.org/) - 官方文档
- [Mastodon 管理员安装指南](https://docs.joinmastodon.org/admin/install/) - 服务器安装指南
- [Mastodon Chart](https://github.com/mastodon/chart) - 官方 Helm chart
- [Mastodon GitHub 仓库](https://github.com/mastodon/mastodon) - 源代码和问题跟踪
- [Sealos 文档](https://sealos.io/docs) - 平台与运维指南

## 实现细节

### 架构组件

本模板部署以下组件：

- **Web**：运行 `ghcr.io/mastodon/mastodon:v4.5.11`，在 `3000` 端口提供主 Mastodon 界面和 API，并暴露 `/health`。
- **Sidekiq**：运行 Mastodon 后台队列，处理投递、邮件、拉取任务、调度任务和联邦相关工作。
- **Streaming**：运行 `ghcr.io/mastodon/mastodon-streaming:v4.5.11`，在 `4000` 端口提供实时时间线和通知。
- **PostgreSQL Cluster**：存储 Mastodon 应用数据，并初始化专用 `mastodon_production` 数据库。
- **Redis Cluster**：提供队列、缓存和 streaming 状态。
- **对象存储**：创建私有 Sealos bucket，并注入用于 Mastodon 媒体的 S3 兼容凭据。
- **Setup Job**：运行 `db:prepare`，创建或更新初始 owner 账号，确认邮箱，批准用户，并应用所选注册模式。

### 配置

- `admin_username`、`admin_email` 和 `admin_password` 用于创建第一个 owner 账号。
- `registration_mode` 控制公开注册模式，可选 `none`、`approved` 或 `open`。
- `vapid_private_key` 和 `vapid_public_key` 用于 Web Push 签名。部署前请用 `RAILS_ENV=production bundle exec rake mastodon:webpush:generate_vapid_key` 生成同一组密钥。
- `smtp_enabled` 控制部署表单中是否显示 SMTP 字段。需要密码重置、账号确认和通知邮件时，请先配置 SMTP。
- 对象存储始终创建，因为 Mastodon 官方部署支持 S3 兼容媒体存储，本模板使用 Sealos 对象存储作为后端。
- `LOCAL_DOMAIN` 由 Sealos 应用主机名生成，使 Mastodon 使用平台创建的公开 HTTPS URL。

### 登录和注册

部署完成后，使用配置的 owner 用户名或邮箱以及密码登录。默认 `registration_mode=none` 会关闭公开注册，用户由 owner 在 Mastodon 管理后台中管理。选择 `approved` 可启用审核制公开注册请求，选择 `open` 可启用即时公开注册。

生产社区建议配置 SMTP，让账号邮件、邀请、确认和密码恢复流程稳定工作。

### 许可信息

Mastodon 使用 GNU Affero General Public License v3.0。此 Sealos 模板是 Mastodon 的部署配置，并遵循模板仓库的许可条款。

## 为什么在 Sealos 上部署 Mastodon？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署与运维。在 Sealos 上部署 Mastodon 可以获得：

- **一键部署**：一次性启动 Mastodon web、Sidekiq、streaming、PostgreSQL、Redis、对象存储和 HTTPS 入口。
- **托管数据服务**：PostgreSQL 和 Redis 通过 KubeBlocks 自动创建。
- **S3 兼容媒体存储**：上传媒体使用 Sealos 对象存储，无需手动创建 bucket。
- **即时 HTTPS 访问**：Sealos 为 Mastodon 服务器创建公开 HTTPS URL。
- **持久应用状态**：数据库和媒体数据通过托管存储在 Pod 重启后保留。
- **AI 辅助运维**：通过 Canvas 和 AI 对话调整资源、环境变量和网络配置。

在 Sealos 上部署 Mastodon，可以运行 Fediverse 服务器，并把 Kubernetes 运维保留在平台工作流中。

## 部署指南

1. 打开 [Mastodon 模板](https://sealos.io/products/app-store/mastodon)，点击 **Deploy Now**。
2. 配置部署参数：
   - `admin_username`：初始 owner 用户名。
   - `admin_email`：初始 owner 邮箱地址。
   - `admin_password`：初始 owner 密码。
   - `registration_mode`：公开注册模式，可选 `none`、`approved` 或 `open`。
   - `vapid_private_key` 和 `vapid_public_key`：使用 `RAILS_ENV=production bundle exec rake mastodon:webpush:generate_vapid_key` 生成的 Web Push 密钥对。
   - SMTP 字段：服务器需要发送邮件时启用并填写。
3. 等待部署完成。Mastodon 冷启动包括 PostgreSQL、Redis、对象存储、数据库迁移、owner 账号创建、Sidekiq 启动、streaming 启动和 web 启动。
4. 从 Canvas 打开生成的 Mastodon URL。
5. 点击 **Sign in**，使用配置的 owner 邮箱或用户名以及密码登录。
6. 打开 **Preferences** 和 **Administration**，检查服务器设置、个人资料设置、审核工具、注册设置和 Sidekiq 状态。

## 配置

部署后可以通过以下方式配置 Mastodon：

- **Mastodon 管理后台**：管理服务器设置、角色、审核、联邦、注册、举报和公告。
- **Sealos AI 对话**：用自然语言描述资源、环境变量、存储或网络变更。
- **资源卡片**：在 Canvas 中打开 Deployment、Service、Ingress、PostgreSQL、Redis 和对象存储卡片。

生产使用前，请检查 SMTP 投递、备份策略、审核规则、保留设置、实例规则、媒体存储访问和域名策略。

## 扩缩容

本模板默认启动一个 web Pod、一个 Sidekiq Pod、一个 streaming Pod、一个 PostgreSQL 实例、一个 Redis replication 拓扑和一个对象存储 bucket。优先通过提高 web 与 Sidekiq Deployment 的 CPU 和内存进行纵向扩容。规模更大的服务器可以在了解流量模式后增加 Sidekiq worker 并调整队列分配。

## 故障排查

### 部署后无法登录

使用部署表单中的 `admin_email` 或 `admin_username` 和 `admin_password`。等待 setup Job 和 web Deployment 完成后再登录。

### 密码重置或确认邮件失败

启用 SMTP，并提供可用的服务器、端口、用户名、密码和发件地址。Mastodon 账号生命周期流程依赖出站邮件。

### 媒体上传失败

检查对象存储 bucket、S3 凭据和 Mastodon 环境中的存储端点。模板会自动创建 Sealos bucket 并注入 S3 兼容变量。

### 时间线延迟明显

检查 Sidekiq 健康状态和队列深度。提高 Sidekiq CPU 和内存，再考虑提升并发或增加 worker。

### 获取帮助

- [Mastodon 文档](https://docs.joinmastodon.org/)
- [Mastodon GitHub Issues](https://github.com/mastodon/mastodon/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Mastodon Admin Guide](https://docs.joinmastodon.org/admin/)
- [Mastodon Configuration Reference](https://docs.joinmastodon.org/admin/config/)
- [Mastodon Scaling Guide](https://docs.joinmastodon.org/admin/scaling/)
- [Sealos App Store](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循模板仓库的许可条款。Mastodon 本身使用 GNU Affero General Public License v3.0。
