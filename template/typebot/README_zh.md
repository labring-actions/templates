# 在 Sealos 上部署和托管 Typebot

Typebot 是开源对话式表单构建器，可创建聊天式表单、线索收集流程、问卷和可嵌入助手。此模板在 Sealos Cloud 上部署 Typebot Builder、Typebot Viewer、KubeBlocks PostgreSQL、KubeBlocks Redis、可选 Sealos 对象存储和内置 Mailpit 收件箱。

![Typebot 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/typebot/website-screenshot.webp)

## 关于托管 Typebot

Typebot 将编辑后台和公开机器人运行时分开。Builder 服务提供控制台，用户可登录、创建工作区、设计 typebot 和查看结果。Viewer 服务在独立公开 URL 上托管已发布的 typebot。

此模板使用 PostgreSQL 16.4.0 保存 Typebot 数据，Redis 7.2.7 支撑登录限流和上传相关运行时能力，可选启用 S3 兼容对象存储保存上传文件，并提供内置 Mailpit 收件箱用于默认邮件登录流程。Builder 和 Viewer 共用同一个生成的加密密钥，确保会话和加密凭据在两个服务间可读。

## 常见使用场景

- **线索收集表单**：构建对话式落地页表单和资格筛选流程。
- **客服接待**：在转人工或工单前收集用户上下文。
- **问卷和反馈**：发布聊天式问卷并查看数据分析。
- **可嵌入助手**：把 Typebot 小组件添加到网站和应用中。

## Typebot 托管依赖

Sealos 模板包含 Typebot Builder、Typebot Viewer、KubeBlocks PostgreSQL 16.4.0、KubeBlocks Redis 7.2.7、可选 Sealos 对象存储、默认登录使用的 Mailpit 收件箱、各公开服务的 HTTPS Ingress，以及 Builder 和内置邮件模式下的 Mailpit App 启动入口。

### 部署依赖

- [Typebot 文档](https://docs.typebot.io/) - 官方文档
- [Docker 部署指南](https://docs.typebot.io/self-hosting/deploy/docker) - 自托管参考
- [配置参考](https://docs.typebot.io/self-hosting/configuration) - 环境变量
- [S3 配置指南](https://docs.typebot.io/self-hosting/guides/s3) - 文件上传存储设置
- [GitHub 仓库](https://github.com/baptisteArno/typebot.io) - 源码和发布版本

### 实现细节

**架构组件：**

- **Typebot Builder**：主应用 URL 上的控制台和编辑器服务。
- **Typebot Viewer**：Viewer URL 上的公开机器人运行时。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4.0，初始化 `typebot` 数据库。
- **Redis**：KubeBlocks Redis 7.2.7，用于限流和运行时缓存能力。
- **对象存储**：可选 Sealos S3 兼容 bucket，用于文件上传。
- **Mailpit**：默认邮件认证路径使用的内置 SMTP 捕获器和收件箱。

**配置：**

- `NEXTAUTH_URL` 指向 Builder URL。
- `NEXT_PUBLIC_VIEWER_URL` 指向 Viewer URL。
- `ADMIN_EMAIL` 让匹配邮箱注册的用户获得 `UNLIMITED` 工作区计划。
- 内置邮件认证会把登录链接发送到模板管理的 Mailpit 收件箱。
- 部署时可选择外部 SMTP、GitHub、Google 或自定义 OpenID Connect 认证。
- S3 变量仅在启用对象存储时注入。

**许可证信息：**

Typebot 是开源项目。当前许可证和版本信息请查看上游仓库。

## 为什么在 Sealos 上部署 Typebot？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从云端开发到生产部署和运维的完整生命周期。它适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 Typebot，你可以获得：

- **一键部署**：同时部署 Builder、Viewer、PostgreSQL、Redis、存储、HTTPS Ingress 和 App 入口。
- **托管依赖**：KubeBlocks 自动创建数据库和 Redis 资源。
- **易于定制**：在 Canvas 中配置邮件登录、OAuth、存储、资源和环境变量。
- **持久数据**：Typebot 数据、会话和上传内容在重启后保留。
- **即时公开访问**：Builder 和 Viewer 都会获得 HTTPS URL。

在 Sealos 上部署 Typebot，把精力放在对话式流程设计上。

## 部署指南

1. 打开 [Typebot 模板](https://sealos.io/products/app-store/typebot)，点击 **Deploy Now**。
2. 输入管理员邮箱。若 typebot 需要文件、图片、视频或导出存储，启用对象存储。
3. 选择登录 provider：
   - Built-in Email：使用内置 Mailpit 收件箱接收首次登录链接。
   - Email：配置 `smtp_host`、`smtp_port`、`smtp_from`，并在服务商要求认证时填写 SMTP 凭据。
   - GitHub：`https://[builder-url]/api/auth/callback/github`
   - Google：`https://[builder-url]/api/auth/callback/google`
   - Custom OAuth：配置 `custom_oauth_issuer`，回调地址使用 `https://[builder-url]/api/auth/callback/custom-oauth`。
4. 等待部署完成。部署完成后会进入 Canvas。后续变更可在对话框描述需求交给 AI 调整，或点击对应资源卡片修改配置。
5. 从 Canvas 打开 Typebot App URL。这个入口是 Builder。
6. 使用配置的认证流程注册或登录。选择 Built-in Email 时，从 Canvas 打开 Typebot Mailpit App URL，复制最新邮件里的登录链接，并在 Builder 中完成登录。邮箱匹配 `admin_email` 的用户会获得 `UNLIMITED` 工作区计划。
7. 发布 typebot 后，使用 Viewer URL 对外提供访问。

## 配置

部署后可以通过以下方式配置 Typebot：

- **AI 对话框**：描述邮件登录、OAuth、资源或存储变更，由 AI 应用更新。
- **资源卡片**：点击 Builder、Viewer、Mailpit、PostgreSQL、Redis、对象存储、Service 或 Ingress 卡片修改设置。
- **Builder 控制台**：创建工作区、typebot、集成、主题和结果导出。
- **Viewer URL**：从公开运行时域名分享已发布的 typebot。

## 扩展

Builder 和 Viewer 是两个独立 Deployment。公开机器人访问量增长时，可提高 Viewer 资源或副本数。Builder 和 Viewer 需要保持相同的 `ENCRYPTION_SECRET`、`DATABASE_URL`，以及匹配的一组 `NEXTAUTH_URL` / `NEXT_PUBLIC_VIEWER_URL`。

## 故障排查

### 登录页面显示错误

- 原因：认证 provider、SMTP、回调 URL 或 `NEXTAUTH_URL` 设置不匹配。
- 解决：Built-in Email 使用 Canvas 中的 Mailpit App URL。外部 SMTP 登录检查 `SMTP_HOST`、`SMTP_PORT`、`NEXT_PUBLIC_SMTP_FROM`，并在服务商要求认证时确认凭据。OAuth 登录把 provider 回调 URL 更新为部署后的 Builder URL，并确认 `NEXTAUTH_URL` 与其一致。

### 管理员用户仍是免费计划

- 原因：注册邮箱与 `ADMIN_EMAIL` 不一致。
- 解决：使用配置的管理员邮箱注册，或更新 `ADMIN_EMAIL` 后创建匹配用户。

### 文件上传失败

- 原因：S3 变量或 bucket 策略缺失。
- 解决：启用对象存储，并确认 `S3_ACCESS_KEY`、`S3_SECRET_KEY`、`S3_BUCKET`、`S3_ENDPOINT` 和 `S3_PUBLIC_CUSTOM_DOMAIN` 已填充。

## 更多资源

- [Typebot 自托管](https://docs.typebot.io/self-hosting/get-started)
- [Typebot 故障排查](https://docs.typebot.io/self-hosting/troubleshoot)
- [Typebot API 参考](https://docs.typebot.io/api-reference/authentication)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

Typebot 是开源项目。当前许可证和使用条款请查看 [上游仓库](https://github.com/baptisteArno/typebot.io)。
