# 在 Sealos 上部署和托管 Outline

Outline 是一个开源团队知识库，适合编写内部文档、产品规格、会议记录和支持答案。此模板会在 Sealos Cloud 上部署 Outline、PostgreSQL、Redis、可选附件存储和公网 HTTPS 入口。

![Outline 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/outline/website-screenshot.webp)

## 关于托管 Outline

Outline 以单个 Web 应用运行，使用 PostgreSQL 保存工作区数据，使用 Redis 支撑协作、缓存和实时协调。Sealos 会根据模板创建所需数据库、持久化存储、内部网络和 HTTPS Ingress。

为了简化自托管登录，此模板默认使用 **Email Magic Link**。用户输入邮箱后，通过 SMTP 收到的一次性链接或验证码登录。Outline 仍不提供传统本地用户名和密码注册；如果你需要外部 SSO，也可以继续选择 OpenID Connect、Google 或 Slack。

## 常见使用场景

- **内部知识库**：发布团队手册、工程笔记、制度流程和操作文档。
- **产品文档**：集中维护产品规格、发布说明、路线图和决策记录。
- **支持与入职**：创建可搜索的答案、入职指南和运维手册。
- **Markdown 协作**：用实时协作和 Markdown 兼容工作流编写结构化文档。

## Outline 托管依赖

此 Sealos 模板包含托管 Outline 所需的运行时依赖。

### 部署依赖

- [Outline 文档](https://docs.getoutline.com/) - 官方产品与自托管文档
- [Outline GitHub 仓库](https://github.com/outline/outline) - 源码和发布历史
- [OpenID Connect 配置](https://docs.getoutline.com/s/hosting/doc/oidc-8CPBm6uC0I) - 通用 OIDC 提供商配置
- [Google OAuth 配置](https://docs.getoutline.com/s/hosting/doc/google-hOuvtCmTqQ) - Google 登录配置
- [Slack OAuth 配置](https://docs.getoutline.com/s/hosting/doc/slack-sgMujR8J9J) - Slack 登录配置
- 邮件服务商提供的 SMTP 账号 - Email Magic Link 登录必需，也可用于事务邮件

## 实现细节

**架构组件：**

此模板会部署以下服务：

- **Outline Web 服务**：运行 `outlinewiki/outline:1.8.0-1`，通过 `3000` 端口提供 Web UI、API 和认证回调。
- **PostgreSQL**：Kubeblocks 托管的 PostgreSQL `postgresql-16.4.0`，在 `outline` 数据库中保存工作区数据。
- **Redis**：Kubeblocks 托管的 Redis `7.2.7`，用于协作、缓存和后台协调。
- **附件存储**：可使用 Sealos 对象存储桶作为 S3 兼容上传目标，也可使用挂载到 `/var/lib/outline/data` 的本地持久卷。
- **Ingress 与 App 链接**：通过 Sealos 管理的 HTTPS Ingress 和 App 资源暴露访问入口。

**配置：**

- `auth_provider` 默认是 `email`，用于 Email Magic Link 登录。
- Email Magic Link 需要填写 `smtp_host`、`smtp_port`、`smtp_username`、`smtp_password` 和 `smtp_from_email`。
- 如果需要外部 OAuth/SSO，`auth_provider` 也可以选择 `oidc`、`google` 或 `slack`。
- OIDC 部署需要填写 `oidc_client_id`、`oidc_client_secret`、`oidc_auth_uri`、`oidc_token_uri` 和 `oidc_userinfo_uri`。
- Google 和 Slack 部署需要填写对应 OAuth 客户端 ID 和客户端密钥。
- OAuth/OIDC 回调地址必须匹配部署后的域名，例如 `https://<your-outline-domain>/auth/oidc.callback`、`https://<your-outline-domain>/auth/google.callback` 或 `https://<your-outline-domain>/auth/slack.callback`。
- `secret_key` 和 `utils_secret` 默认自动生成；已有部署应保持这两个值稳定。
- 使用 OAuth 提供商时，可开启 `smtp_enabled` 发送事务邮件；当 `auth_provider` 为 `email` 时，SMTP 实际上是必需配置。

**许可证信息：**

Outline 使用 Business Source License 1.1。此 Sealos 模板遵循仓库许可证发布。

## 为什么在 Sealos 上部署 Outline？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、网络、存储和生命周期管理。在 Sealos 上部署 Outline 可以获得：

- **一键部署**：通过一个模板创建 Outline、PostgreSQL、Redis、存储、Service、Ingress 和 App 链接。
- **更简单的登录**：默认使用 Email Magic Link，无需在首次启动前配置 OAuth。
- **托管公网访问**：Sealos 自动为 Outline 工作区创建 HTTPS 访问入口。
- **持久化数据**：PostgreSQL、Redis 和可选本地附件存储都使用持久卷。
- **易于配置**：通过部署输入配置邮箱登录、OAuth/OIDC、SMTP 和存储方式。
- **简化运维**：部署后可通过 Canvas、AI 对话和资源卡片调整配置，无需手写 Kubernetes YAML。

## 部署指南

1. 打开 [Outline 模板](https://sealos.io/products/app-store/outline)，点击 **Deploy Now**。
2. 保持默认的 `email` 认证提供商，并填写 SMTP 设置。Outline 会用 SMTP 发送一次性登录链接或验证码。
3. 可选：如果已有 OAuth/SSO 提供商，也可以改选 `oidc`、`google` 或 `slack`，并在对应提供商后台配置客户端 ID、客户端密钥和回调地址。
4. 选择附件存储方式：
   - `s3` 会创建并使用 Sealos 对象存储桶。
   - `local` 会将附件保存到 Outline Pod 挂载的持久卷。
5. 等待部署完成，通常需要 2-3 分钟。部署后 Sealos 会跳转到 Canvas。
6. 从 App 资源打开生成的 Outline URL。新安装会先创建第一个工作区和管理员用户；之后使用已配置的 Email Magic Link 或 OAuth 提供商登录。

## 配置

部署后可以通过以下方式配置 Outline：

- **AI 对话**：描述资源调整或环境变量更新需求，由 Sealos 应用变更。
- **资源卡片**：打开 StatefulSet、数据库、Redis、存储或 Ingress 卡片查看并调整资源。
- **SMTP 提供商控制台**：管理发件地址、SMTP 主机、端口、用户名、密码和邮件投递状态。
- **身份提供商控制台**：使用外部提供商时，在提供商后台管理 OAuth/OIDC 用户、回调地址、客户端 ID 和客户端密钥。

## 认证说明

### Email Magic Link

Email Magic Link 是此模板默认且最简单的登录方式。部署时配置 SMTP，打开 Outline URL 后先创建第一个工作区和管理员用户。完成初始化后，用户输入邮箱即可通过邮箱中的链接或验证码登录。

请确保 `smtp_from_email` 是邮件服务商允许使用的有效发件地址。如果邮件投递被拦截，Outline 可能仍然运行正常，但用户收不到登录链接。

### OAuth 和 SSO

OIDC 使用以下回调地址：

```text
https://<your-outline-domain>/auth/oidc.callback
```

Google OAuth 使用以下回调地址：

```text
https://<your-outline-domain>/auth/google.callback
```

Slack OAuth 使用以下回调地址：

```text
https://<your-outline-domain>/auth/slack.callback
```

如果提供商凭据或回调地址不正确，Outline 页面仍可能正常加载并通过健康检查，但登录会在提供商回调阶段失败。

## 扩缩容

如需扩缩容或调优 Outline：

1. 打开当前部署的 Canvas。
2. 点击 Outline StatefulSet 资源卡片。
3. 根据需要调整 CPU、内存、存储或副本数。
4. 在对话中应用变更。

重启 Outline 前请确保 PostgreSQL 和 Redis 可用。冷启动期间数据库初始化和迁移会让启动时间变长。

## 故障排查

### 邮箱登录链接没有收到

- 原因：SMTP 配置缺失或错误、邮件服务商拦截，或 `smtp_from_email` 不是允许的发件地址。
- 解决：检查 SMTP 主机、端口、用户名、密码、发件地址和服务商安全设置，同时查看垃圾邮件与邮件投递日志。

### OAuth 登录回调失败

- 原因：OAuth/OIDC 提供商配置缺失或不正确。
- 解决：检查所选提供商输入，并确认提供商后台使用了当前部署域名对应的精确回调地址。

### 应用早于依赖启动

- 原因：PostgreSQL、Redis 或数据库初始化 Job 仍在启动。
- 解决：等待 PostgreSQL 和 Redis 集群进入 `Running`，并确认 `pg-init` Job 完成；如有需要再重启 Outline StatefulSet。

### 附件上传失败

- 原因：存储类型或存储桶凭据配置错误。
- 解决：使用 `s3` 作为 Sealos 对象存储，或使用 `local` 作为持久卷，并确认对应存储资源已创建。

## 更多资源

- [Outline 文档](https://docs.getoutline.com/)
- [Outline GitHub](https://github.com/outline/outline)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循仓库许可证发布。Outline 本身使用 Business Source License 1.1。
