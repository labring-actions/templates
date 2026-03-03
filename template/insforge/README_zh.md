# 在 Sealos 上部署并托管 InsForge

InsForge 是一个面向 AI 代理（Agent）的后端平台，提供数据库、认证、存储与函数运行时能力，用于快速构建全栈应用。该模板会在 Sealos Cloud 上部署由 PostgreSQL、PostgREST 和 Deno Runtime 组成的 InsForge 多服务栈。

## 关于在 Sealos 托管 InsForge

在 Sealos 上，InsForge 以协同架构运行：主服务提供 API、控制台与认证端点；PostgREST 将 PostgreSQL 暴露为 REST 接口；Deno Runtime 负责函数执行任务。模板还会自动准备 PostgreSQL 所需扩展和角色，确保核心后端能力开箱即用。

部署同时包含应用数据、日志和运行时缓存的持久化存储，并自动配置 HTTPS Ingress 与公网域名。Sealos 负责网络、证书和 Kubernetes 资源编排，你可以把重点放在业务功能本身。

## 常见使用场景

- **Agent 原生 SaaS 后端**：构建可由 AI 编码代理创建和维护的后端服务。
- **Supabase 风格基础设施**：低成本启动带数据库、认证和 REST API 的应用底座。
- **内部工具与自动化系统**：快速搭建具备安全认证与服务端逻辑的内部系统。
- **MVP 快速验证**：借助完整后端栈，在更短时间内完成产品原型。
- **AI 工作流平台**：将 API 能力与函数运行时结合，支撑 AI 辅助业务流程。

## InsForge 托管依赖

该 Sealos 模板已包含 InsForge 运行所需核心依赖：InsForge 主服务、PostgreSQL、PostgREST、Deno Runtime、Ingress 与持久卷。

### 部署依赖

- [InsForge 官方网站](https://insforge.dev) - 产品介绍与更新信息
- [InsForge GitHub 仓库](https://github.com/insforge/insforge) - 源码与版本发布
- [InsForge GitHub Issues](https://github.com/insforge/insforge/issues) - 问题追踪与社区支持
- [Sealos Cloud](https://sealos.run) - 部署平台

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **InsForge Core（StatefulSet）**：主服务，开放 `7130`（API）、`7131`（dashboard）、`7132`（auth）。
- **PostgreSQL Cluster（KubeBlocks）**：PostgreSQL `16.4.0`，提供持久化数据存储。
- **PostgreSQL 扩展初始化 Job**：安装并启用 `pg_cron`、`http`、`pgcrypto`，并确保所需角色存在。
- **PostgreSQL 扩展巡检 CronJob**：每 5 分钟复查扩展可用性，提升运行稳定性。
- **PostgREST（Deployment）**：`3000` 端口 REST 网关，集成 JWT 配置。
- **Deno Runtime（StatefulSet）**：`7133` 端口函数运行时，执行后端任务。
- **Ingress + Service 资源**：提供公网 HTTPS 入口与集群内服务发现。

**配置说明：**

- **必填参数**：`admin_password`
- **可选参数**：`admin_email`、`openrouter_api_key`，以及 Google、GitHub、Discord、Microsoft、LinkedIn、X、Apple 的 OAuth 凭据
- **安全默认值**：`JWT_SECRET` 与 `ENCRYPTION_KEY` 自动随机生成
- **默认存储配置**：
  - InsForge 数据目录：`/insforge-storage`（103Mi）
  - InsForge 日志目录：`/insforge-logs`（103Mi）
  - Deno 运行时缓存：`/deno-dir`（103Mi）
  - PostgreSQL 数据卷：`1Gi`

**许可证信息：**

InsForge 为开源软件，具体许可证条款请以上游仓库最新说明为准。

## 为什么在 Sealos 上部署 InsForge？

Sealos 是构建于 Kubernetes 之上的 AI 辅助云操作系统，覆盖开发、部署与运维全流程。将 InsForge 部署到 Sealos，你可以获得：

- **一键部署**：无需手写复杂 YAML，即可拉起完整多服务后端栈。
- **Kubernetes 级可靠性**：默认具备调度、服务发现和自动恢复能力。
- **配置简单直观**：通过 Sealos 表单与对话框管理环境变量和资源规格。
- **持久化存储内置**：数据库和应用数据可跨重启稳定保留。
- **自动 HTTPS 公网访问**：自动分配公网地址并签发 SSL 证书。
- **按量计费更高效**：按需分配资源，业务增长时再扩容。
- **AI 辅助运维**：可通过 Canvas 与 AI 对话完成部署后变更。

将 InsForge 部署到 Sealos 后，你可以把精力集中在产品交付，而不是基础设施维护。

## 部署指南

1. 打开 [InsForge 模板页面](https://sealos.io/products/app-store/insforge)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **admin_password**（必填）：管理员密码
   - **admin_email**（可选）：管理员邮箱
   - **openrouter_api_key**（可选）：OpenRouter 集成密钥
   - **OAuth client settings**（可选）：Google、GitHub、Discord、Microsoft、LinkedIn、X、Apple
3. 等待部署完成（通常 2-3 分钟）。完成后会自动跳转到 Canvas。后续如需调整，可在对话框描述需求让 AI 应用变更，或点击资源卡片手动修改。
4. 通过生成的公网地址访问应用：
   - **InsForge Web/API Endpoint**：经 HTTPS Ingress 暴露的主入口

## 配置

部署完成后，可通过以下方式配置 InsForge：

- **AI Dialog**：用自然语言描述你要调整的内容，由 AI 自动应用。
- **Resource Cards**：在 StatefulSet/Deployment 资源卡片中修改环境变量和资源规格。
- **管理员凭据**：在部署配置中更新管理员邮箱/密码与 OAuth 参数。
- **服务连通性**：`postgrest`、`deno`、`postgres` 通过集群 DNS 自动管理内部通信。

## 扩缩容

如需扩展 InsForge 部署能力：

1. 在 Canvas 中打开 InsForge 部署。
2. 选择目标资源卡片（`insforge`、`insforge-postgrest` 或 `insforge-deno`）。
3. 按需调整 CPU/内存配置。
4. 在弹窗中应用变更。

在高吞吐场景下，建议先对 PostgreSQL 与 InsForge Core 做纵向扩容，再评估更复杂的拓扑调整。

## 故障排查

### 常见问题

**问题：首次启动时间明显偏长**
- 原因：PostgreSQL 扩展与角色初始化任务仍在执行。
- 解决方案：等待初始化任务完成后，再检查相关 Pod 就绪状态。

**问题：认证或 JWT 相关 API 报错**
- 原因：`JWT_SECRET` 配置错误，或认证配置不一致。
- 解决方案：核对部署环境变量并重新应用正确值。

**问题：OAuth 登录失败**
- 原因：OAuth client ID/secret 缺失或填写错误。
- 解决方案：在部署参数中重新配置凭据，并重启受影响 Pod。

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
- [Sealos 文档](https://sealos.run/docs)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

该 Sealos 模板遵循本 templates 仓库的许可证规则。InsForge 项目本身遵循其上游仓库声明的许可证条款。
