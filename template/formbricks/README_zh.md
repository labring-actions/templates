# 在 Sealos 上部署和托管 Formbricks

Formbricks 是一个开源体验管理平台，支持应用内、网站、链接和邮件问卷。此模板会在 Sealos Cloud 上部署带 PostgreSQL、Redis、持久化上传目录、公网 HTTPS 访问和 Sealos 应用资源的 Formbricks。

![Formbricks 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/formbricks/website-screenshot.webp)

## 关于托管 Formbricks

Formbricks 帮助产品团队在用户旅程中收集反馈，从产品内定向问卷到公开链接问卷和邮件活动都可以覆盖。应用会把问卷定义、回答、用户和工作区数据存储在 PostgreSQL 中，并使用 Redis 支撑服务端缓存和限流相关流程。

此 Sealos 模板会创建完整运行环境：Formbricks StatefulSet、PostgreSQL 16、Redis 7、数据库初始化 Job、迁移 initContainer、持久化上传存储，以及 HTTPS Ingress。Formbricks 默认启用注册，因此部署后可以直接创建第一个工作区。模板不会生成默认用户名或密码；请在 Web UI 中创建第一个账号，然后用该邮箱和密码登录。

模板还会创建 Formbricks 容器启动流程所需的额外 SAML 数据库。由于此模板未配置 SMTP，默认关闭邮件验证和密码重置。

## 常见使用场景

- **产品内反馈收集**：在产品中触发定向问卷，了解用户转化、流失或受阻原因。
- **网站和落地页问卷**：在公开页面嵌入问卷，收集访客反馈和线索信息。
- **链接式用户研究**：向客户、测试用户或内部团队分享独立问卷链接。
- **客户体验追踪**：在一个自托管平台中运行 NPS、CSAT 或产品市场匹配度问卷。
- **注重隐私的反馈运营**：将反馈数据保存在自己的 Sealos 托管环境中，而不是完全依赖 SaaS 托管。

## Formbricks 托管依赖

此 Sealos 模板包含全部必需依赖：Formbricks Web 应用容器、用于应用数据的 PostgreSQL 16、用于缓存和限流支持的 Redis 7、用于上传文件和 SAML 连接数据的持久卷，以及用于公网访问的 HTTPS Ingress。

### 部署依赖

- [Formbricks 文档](https://formbricks.com/docs) - Formbricks 官方文档
- [Formbricks 自托管指南](https://formbricks.com/docs/self-hosting) - 自托管和配置说明
- [Formbricks GitHub 仓库](https://github.com/formbricks/formbricks) - 源码和问题追踪
- [Sealos 应用商店](https://sealos.io/products/app-store) - Sealos 应用模板

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Formbricks StatefulSet**：运行 `ghcr.io/formbricks/formbricks:4.9.7`，在 `3000` 端口提供 Web UI 和 API，并挂载上传文件与 SAML 连接文件的持久化存储。
- **PostgreSQL 集群**：在 `formbricks` 数据库中存储 Formbricks 应用数据，并创建独立的 `formbricks-saml` 数据库用于 SAML 支持。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建两个数据库。
- **Formbricks 迁移 initContainer**：运行官方数据库迁移命令，再由 Web 容器承担稳定运行流量，使应用容器可以跳过启动迁移。
- **Redis 集群**：提供带 Sentinel 拓扑的 Redis 7，用于服务端缓存和限流相关运行时能力。
- **Service 和 Ingress**：通过 Sealos 托管的 HTTPS 域名暴露 Formbricks HTTP 服务。
- **App 资源**：在 Sealos 桌面中注册应用入口，部署后可一键访问。

**配置：**

应用会通过 Sealos 管理的数据库 Secret 和服务 DNS 组合出 `DATABASE_URL`、`MIGRATE_DATABASE_URL`、`SAML_DATABASE_URL` 和 `REDIS_URL`。生成默认值会提供 `NEXTAUTH_SECRET`、`ENCRYPTION_KEY` 和 `CRON_SECRET`，法律页面 URL 则作为可选部署输入暴露。

默认运行设置会关闭 Docker cron、邮件验证、密码重置和遥测。注册和邀请保持启用，便于部署后从 Web UI 初始化实例。模板不会生成管理员账号。

**许可信息：**

Formbricks 使用 AGPL-3.0 许可证。此 Sealos 模板作为 Sealos templates 仓库的一部分提供。

## 为什么在 Sealos 上部署 Formbricks？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、公网访问、存储和运维。将 Formbricks 部署在 Sealos 上，你可以获得：

- **一键部署**：从应用商店启动 Formbricks，无需手写 Kubernetes YAML。
- **托管依赖**：PostgreSQL、Redis、持久卷、Service、Ingress 和 App 入口会随模板一起创建。
- **即时公网访问**：每个部署都会通过 Sealos 托管的 Ingress 和证书获得公网 HTTPS URL。
- **持久化数据**：数据库数据、上传文件和 SAML 连接文件会在应用重启后保留。
- **Canvas + AI 运维**：部署后可使用 Canvas、AI 对话和资源卡调整配置或资源。
- **按需付费资源**：按工作负载调节 CPU、内存和存储，避免过度配置。
- **Kubernetes 可靠性**：使用 Kubernetes 原语运行 Formbricks，同时由 Sealos 提供更直观的运维界面。

在 Sealos 上部署 Formbricks，把精力放在反馈流程，而不是基础设施搭建上。

## 部署指南

1. 打开 [Formbricks 模板](https://sealos.io/products/app-store/formbricks)，点击 **立即部署**。
2. 在弹窗中配置可选的法律页面参数：
   - `PRIVACY_URL`：隐私政策页面 URL。
   - `TERMS_URL`：服务条款页面 URL。
   - `IMPRINT_URL`：法律声明页面 URL。
3. 等待部署完成，通常需要 3-5 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话中描述需求，或点击相关资源卡调整设置。
4. 通过提供的 URL 访问应用：
   - **Formbricks Web UI**：打开 App 入口或生成的 `https://<your-app-host>.<sealos-cloud-domain>` URL，然后创建初始账号和工作区。

## 注册和登录

此模板不会创建默认用户名或密码。默认启用注册，并且由于未配置 SMTP，邮件验证处于关闭状态。

初始化实例时，部署完成后打开 Formbricks URL，选择 **注册** 或 **创建账号**，输入邮箱和密码，然后创建第一个工作区。之后在登录页使用同一邮箱和密码登录。

## 配置

部署后，你可以通过以下方式配置 Formbricks：

- **Formbricks Web UI**：在应用界面中创建团队、产品、环境、问卷和集成。
- **AI 对话**：描述需要修改的环境变量或资源，让 Sealos 应用更新。
- **资源卡**：在 Canvas 中打开 StatefulSet、数据库、Redis、Service 或 Ingress 资源卡，查看并更新设置。
- **法律 URL**：部署时设置 `PRIVACY_URL`、`TERMS_URL` 和 `IMPRINT_URL`，指向你自己的法律页面。

默认不配置 SMTP。如果后续启用邮件验证或密码重置，请先添加 Formbricks 所需的 SMTP 环境变量。

## 扩缩容

此模板默认运行 1 个 Formbricks 副本，与内置的持久化上传存储和迁移 initContainer 流程保持一致。如需调整资源：

1. 打开当前部署的 Canvas。
2. 点击 Formbricks StatefulSet 资源卡。
3. 根据访问量和问卷规模调整 CPU 与内存资源。此模板使用 Formbricks 4.9.7 测试通过的最小资源组合：迁移 initContainer 为 500m CPU / 512Mi 内存，Web 容器为 300m CPU / 256Mi 内存。
4. 在对话中应用变更，并等待 Pod 重新就绪。

对于更大规模的安装，请先阅读 Formbricks 自托管指南，尤其要关注共享上传目录、后台任务和数据库容量。

## 故障排查

### 常见问题

**首次启动时间较长**
- 原因：PostgreSQL 初始化 Job 和 Formbricks 迁移 initContainer 需要先完成，Web UI 才会完全就绪。
- 解决方法：等待迁移 initContainer 完成，并确认 StatefulSet Pod 日志显示服务已开始监听。如果启动反复失败，请在 Canvas 中查看 PostgreSQL、迁移 initContainer 和 Formbricks 日志。

**邮件验证或密码重置没有发送邮件**
- 原因：默认未包含 SMTP 设置，并且邮件验证/密码重置处于关闭状态。
- 解决方法：先添加 Formbricks SMTP 环境变量，再启用这些功能。在此之前，请通过内置注册流程初始化实例，并妥善保存第一个账号的凭据。

**上传文件或 SAML 连接文件需要持久化**
- 原因：这些文件存储在挂载的持久卷中。
- 解决方法：保留 StatefulSet 生成的 PVC。除非你明确要删除已存储文件，否则不要删除这些 PVC。

### 获取帮助

- [Formbricks 文档](https://formbricks.com/docs)
- [Formbricks GitHub Issues](https://github.com/formbricks/formbricks/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Formbricks 自托管](https://formbricks.com/docs/self-hosting)
- [Formbricks 开发者文档](https://formbricks.com/docs/developer-docs)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板按仓库许可证提供。Formbricks 本身使用 [AGPL-3.0 许可证](https://github.com/formbricks/formbricks/blob/main/LICENSE)。
