# 在 Sealos 上部署并托管 InsForge

InsForge 是一个面向 AI 代理（Agent）的后端平台，提供数据库、认证、存储、REST API 与函数运行时能力，用于快速构建全栈应用。该 Sealos 模板会部署 InsForge `v2.1.8`，并配套 PostgreSQL、PostgREST 与 Deno Runtime，形成可直接使用的后端栈。

## 关于在 Sealos 托管 InsForge

在 Sealos 上，InsForge 以多服务协同架构运行：主服务提供 Dashboard、后端 API 与认证路由；PostgREST 将 PostgreSQL 暴露为 REST 接口；Deno Runtime 负责函数执行；KubeBlocks PostgreSQL 负责持久化数据存储。

模板会自动创建所需数据库角色和扩展，准备 PostgreSQL HTTP 扩展包，并在 InsForge 迁移执行前移除与迁移不兼容的默认监控扩展，然后通过 HTTPS Ingress 暴露控制台。Sealos 负责 Kubernetes 资源、网络、证书与持久卷管理，你可以专注于业务逻辑。

## 常见使用场景

- **Agent 原生 SaaS 后端**：构建可由 AI 编码代理创建和运维的后端服务。
- **Supabase 风格应用底座**：快速启动需要数据库、认证、存储与 REST API 的应用。
- **内部工具与自动化系统**：部署具备认证、服务端逻辑和持久数据的内部应用。
- **MVP 快速验证**：用完整后端栈更快完成全栈原型。
- **AI 工作流平台**：结合 API、数据库状态和函数运行时，支撑 AI 辅助产品。

## InsForge 托管依赖

该 Sealos 模板已包含运行所需组件：InsForge Core、PostgreSQL、PostgREST、Deno Runtime、初始化任务、Ingress、Service 与持久卷。

### 部署依赖

- [InsForge 官方网站](https://insforge.dev) - 产品介绍与更新信息
- [InsForge GitHub 仓库](https://github.com/insforge/insforge) - 源码与版本发布
- [InsForge v2.1.8 Release](https://github.com/InsForge/InsForge/releases/tag/v2.1.8) - 当前模板使用版本
- [InsForge GitHub Issues](https://github.com/insforge/insforge/issues) - 问题追踪与社区支持
- [Sealos Cloud](https://sealos.io) - 部署平台

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **InsForge Core（StatefulSet）**：主服务，开放 `7130`（API/Dashboard）、`7131` 与 `7132`，镜像为 `ghcr.io/insforge/insforge-oss:v2.1.8`。
- **PostgreSQL Cluster（KubeBlocks）**：PostgreSQL `16.4.0`，使用 `1Gi` 持久化数据卷。
- **PostgreSQL 扩展初始化 Job**：安装 HTTP 扩展包，为默认 `postgres_log` foreign table 准备兼容日志文件，启用 `pg_cron`、`http`、`pgcrypto`，创建所需角色，并在迁移前移除不兼容的 `pg_auth_mon`、`pg_stat_kcache`、`pg_stat_statements` 扩展。
- **PostgreSQL 扩展巡检 CronJob**：每 5 分钟复查扩展可用性，提升运行稳定性。
- **PostgREST（Deployment）**：`3000` 端口 REST 网关，集成 JWT 配置。
- **Deno Runtime（StatefulSet）**：`7133` 端口函数运行时，镜像为 `ghcr.io/insforge/deno-runtime:2.0.6`。
- **Ingress + Service 资源**：提供公网 HTTPS 入口与集群内服务发现。

**配置说明：**

- **必填参数**：`admin_password`
- **可选参数**：`admin_email`、`openrouter_api_key`，以及 Google、GitHub、Discord、Microsoft、LinkedIn、X、Apple 的 OAuth 凭据
- **安全默认值**：`JWT_SECRET` 与 `ENCRYPTION_KEY` 由模板自动随机生成
- **默认存储配置**：
  - InsForge 数据目录：`/insforge-storage`（`103Mi`）
  - InsForge 日志目录：`/insforge-logs`（`103Mi`）
  - Deno 运行时缓存：`/deno-dir`（`103Mi`）
  - PostgreSQL 数据卷：`1Gi`

**已验证的最小资源：**

该模板已在以下资源配置下完成部署和访问验证：

- InsForge Core：请求 `20m` CPU / `25Mi` 内存，限制 `200m` CPU / `256Mi` 内存
- PostgREST：请求 `20m` CPU / `25Mi` 内存，限制 `200m` CPU / `256Mi` 内存
- Deno Runtime：请求 `20m` CPU / `25Mi` 内存，限制 `200m` CPU / `256Mi` 内存
- PostgreSQL：请求 `50m` CPU / `51Mi` 内存，限制 `500m` CPU / `512Mi` 内存，存储 `1Gi`

**许可证信息：**

InsForge 为开源软件，具体许可证条款请以上游仓库最新说明为准。

## 为什么在 Sealos 上部署 InsForge？

Sealos 是构建于 Kubernetes 之上的 AI 辅助云操作系统，覆盖开发、部署与运维流程。将 InsForge 部署到 Sealos，你可以获得：

- **一键部署**：无需手写复杂 YAML，即可拉起完整多服务后端栈。
- **Kubernetes 级可靠性**：默认具备调度、服务发现、持久化存储和自动恢复能力。
- **配置简单直观**：通过 Sealos 表单与对话框管理环境变量和资源规格。
- **自动 HTTPS 公网访问**：自动分配公网地址并签发 SSL 证书。
- **按量计费更高效**：以较小资源启动，业务增长后再扩容。
- **AI 辅助运维**：可通过 Canvas 与 AI 对话完成部署后变更。

将 InsForge 部署到 Sealos 后，你可以把精力集中在产品交付，而不是基础设施维护。

## 部署指南

1. 打开 [InsForge 模板页面](https://sealos.io/products/app-store/insforge)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **admin_password**（必填）：管理员密码。生产环境请使用强密码，不要保留示例密码。
   - **admin_email**（可选）：管理员邮箱，默认值为 `admin@example.com`。
   - **openrouter_api_key**（可选）：OpenRouter 集成密钥。
   - **OAuth client settings**（可选）：Google、GitHub、Discord、Microsoft、LinkedIn、X、Apple 的 OAuth 凭据。
3. 等待部署完成。PostgreSQL 初始化和迁移完成后，通常约 2-3 分钟可就绪。
4. 通过生成的公网地址访问应用。根路径会跳转到 `/dashboard/login`，可在此登录 InsForge Dashboard。

## 登录与注册

部署完成后，打开生成的公网地址并进入 `/dashboard/login`。

- **管理员控制台登录**：使用部署弹窗中的 `admin_email` 和 `admin_password`。
- **管理员 API 登录接口**：`POST /api/auth/admin/sessions`，JSON 请求体为 `{ "email": "<admin_email>", "password": "<admin_password>" }`。
- **终端用户注册**：当注册未被禁用时，公开认证 API 支持 `POST /api/auth/users`，提交邮箱和密码即可注册。默认认证配置中 `disableSignup: false`；你也可以在 Dashboard 的 Authentication 页面调整注册策略。
- **终端用户登录**：使用 `POST /api/auth/sessions` 提交已注册用户的邮箱和密码，或在 Dashboard/部署参数中配置 OAuth Provider 后使用第三方登录。
- **Compute services**：如果未配置 Fly.io 等计算服务提供商，Dashboard 可能显示 compute-service 未配置提示。该提示不影响数据库、认证、存储与 Dashboard 访问。

生产环境建议先替换默认管理员邮箱，设置强密码，并在邀请用户前配置 OAuth 或 SMTP。

## 配置

部署完成后，可通过以下方式配置 InsForge：

- **Dashboard**：管理员登录后管理 Authentication 设置、用户、Provider 和项目配置。
- **AI Dialog**：用自然语言描述调整内容，由 Sealos 应用变更。
- **Resource Cards**：在 StatefulSet/Deployment 资源卡片中修改环境变量和资源规格。
- **服务连通性**：PostgREST、Deno Runtime 与 PostgreSQL 的内部访问由集群 DNS 自动管理。

## 扩缩容

如需扩展 InsForge 部署能力：

1. 在 Canvas 中打开 InsForge 部署。
2. 选择目标资源卡片（`insforge`、`insforge-postgrest`、`insforge-deno` 或 PostgreSQL）。
3. 按需调整 CPU、内存和存储配置。
4. 在弹窗中应用变更。

在高吞吐场景下，建议先对 PostgreSQL 与 InsForge Core 做纵向扩容，再评估更复杂的拓扑调整。

## 故障排查

### 常见问题

**问题：首次启动时间明显偏长**
- 原因：PostgreSQL 启动、扩展初始化和 InsForge 数据库迁移仍在执行。
- 解决方案：等待初始化 Job 完成后，再检查相关 Pod 就绪状态。

**问题：Dashboard 登录失败**
- 原因：`admin_email` 或 `admin_password` 填写错误。
- 解决方案：确认部署弹窗中使用的值，必要时更新部署配置。

**问题：终端用户注册或登录失败**
- 原因：注册可能被禁用、密码不符合策略，或 OAuth/SMTP 配置未完成。
- 解决方案：以管理员身份登录，进入 Authentication 设置检查注册、密码、OAuth 与邮件配置。

**问题：OAuth 登录失败**
- 原因：OAuth client ID/secret 缺失或填写错误。
- 解决方案：重新配置 Provider 凭据，必要时重启相关 Pod。

**问题：Compute services 显示未配置**
- 原因：自托管 compute 需要配置外部提供商凭据，例如 `FLY_API_TOKEN` 和 `FLY_ORG`。
- 解决方案：使用 compute-service 部署能力前先配置支持的计算服务提供商；未配置时，其它核心功能仍可正常使用。

**问题：函数运行失败**
- 原因：Deno Runtime 服务未就绪，或内部连通性异常。
- 解决方案：检查 `insforge-deno` Pod 状态，并确认集群内服务 DNS 解析正常。

### 获取帮助

- [InsForge 官网](https://insforge.dev)
- [InsForge GitHub 仓库](https://github.com/insforge/insforge)
- [InsForge GitHub Issues](https://github.com/insforge/insforge/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [InsForge 源码仓库](https://github.com/insforge/insforge)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

该 Sealos 模板遵循本 templates 仓库的许可证规则。InsForge 项目本身遵循其上游仓库声明的许可证条款。
