# 在 Sealos 上部署和托管 LobeHub

LobeHub 是开源 AI 工作空间，支持聊天、智能体、知识库、多模态文件和模型服务商管理。本模板会在 Sealos Cloud 上部署 LobeHub 2.2.10，并配置 PostgreSQL、Redis、私有 S3 兼容对象存储和 Better Auth。

![LobeHub 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/lobehub/website-screenshot.webp)

## 关于托管 LobeHub

服务端数据库版会把账户、会话、对话、智能体、设置和知识数据保存到 PostgreSQL。Redis 提供共享身份会话与应用缓存，Sealos 对象存储负责保存上传文件和知识库资产。

LobeHub 2.x 使用 Better Auth，并内置邮箱密码注册。邮箱验证和魔法链接依赖 SMTP 服务，本模板关闭这两项功能。

## 常见使用场景

- **私有 AI 工作空间**：为个人或团队运行带持久化能力的聊天和智能体环境。
- **知识工作**：上传文件、创建知识库，并在对话中调用相关内容。
- **模型服务商管理**：在一个界面中配置 OpenAI 兼容服务和其他模型服务商。
- **共享会话**：通过 Redis 二级存储保持身份会话和缓存状态。

## LobeHub 托管依赖

模板会创建当前 Sealos 拓扑所需的运行组件：

- LobeHub `lobehub/lobehub:2.2.10`
- KubeBlocks PostgreSQL 16.4.0，并安装官方 ParadeDB `pg_search` 0.24.2 扩展包
- 带 Sentinel 的 KubeBlocks Redis 7.2.7
- Sealos 托管的私有 S3 兼容对象存储
- Sealos Service、HTTPS Ingress 和 App 入口

### 部署依赖

- [LobeHub 文档](https://lobehub.com/docs) - 官方产品与自托管文档
- [LobeHub GitHub 仓库](https://github.com/lobehub/lobehub) - 源码与版本发布
- [Better Auth 配置](https://lobehub.com/docs/self-hosting/auth) - 注册与身份认证设置
- [Sealos 应用商店](https://sealos.io/products/app-store/lobehub) - 一键部署入口

### 实现细节

应用监听 `3210` 端口，启动时执行官方数据库迁移，并使用 `DATABASE_DRIVER=node`。PostgreSQL 提供当前迁移和全文检索所需的 `vector` 与 `pg_search` 扩展。

PostgreSQL Pod 首次启动时会下载官方 `pg_search` 0.24.2 Ubuntu 软件包，校验固定 SHA-256 摘要和软件包结构，并把解压后的动态库与 SQL 文件缓存到数据库数据卷。Patroni 回调会更新 KubeBlocks 托管的 PostgreSQL 配置，KubeBlocks 随后执行必要的重启，LobeHub 迁移容器再创建并验证扩展。后续 Pod 替换会复用已经验证的软件包。

模板通过 KubeBlocks 托管凭证组合 `DATABASE_URL` 和 `REDIS_URL`。Sealos 从托管 ObjectStorageBucket 注入 S3 endpoint、bucket、access key 和 secret key。

每个部署都需要独立的私有 RS256 密钥对，用于 OIDC 和内部 JWT 认证。应用首次启动时，模板会通过 Node.js 生成 2048 位 RSA JWKS，校验私钥字段后写入当前部署的 PostgreSQL 数据库。PostgreSQL advisory lock 会让并发启动的多个副本统一使用同一把密钥。后续重启和扩容时，应用会先读取已保存的密钥，再执行 LobeHub 官方启动程序，部署表单只保留运维参数。

JWKS 会随 LobeHub 数据库一起备份和恢复。恢复应用数据与认证状态时，JWT 工作流使用的签名身份也会保持一致。

## 为什么在 Sealos 上部署 LobeHub？

Sealos 在一个部署界面中整合 Kubernetes 应用编排、托管数据库、对象存储、HTTPS 网络和生命周期管理。模板默认运行一个 LobeHub 副本，共享 PostgreSQL、Redis 和 S3 服务可以承接后续应用扩容。

## 部署指南

1. 打开 [LobeHub 模板](https://sealos.io/products/app-store/lobehub)，点击 **Deploy Now**。
2. 按需使用 `AUTH_ALLOWED_EMAILS` 限制注册范围，并配置 OpenAI 兼容模型参数。模板会自动生成并持久化 `JWKS_KEY`。
3. 等待 PostgreSQL、Redis、对象存储和 LobeHub 数据库迁移就绪，通常需要 2-3 分钟。
4. 从 Canvas 打开生成的 LobeHub HTTPS 地址。

## 注册和登录

1. 打开生成的 LobeHub 地址，选择 **Sign up**。
2. 使用邮箱地址和密码注册账户。
3. 使用同一账户登录。
4. 在首次使用流程中选择界面语言、确认显示名称并选择兴趣领域。
5. 打开 **Home** 使用智能体工作台，或打开 **Resources** 创建知识库并上传文件。

`AUTH_ALLOWED_EMAILS` 留空时开放邮箱注册；填写逗号分隔的邮箱地址或域名后，注册流程会过滤用户提交的邮箱字符串。模板关闭了依赖 SMTP 的邮箱验证，因此该过滤器无法验证邮箱所有权。需要可信身份时，请配置 SMTP 并启用 `AUTH_EMAIL_VERIFICATION=1`，或接入外部 SSO 服务商。

## 配置

- **AI 对话框**：在 Canvas 中描述资源或环境变量调整需求。
- **资源卡片**：调整 LobeHub 副本数或资源限制。
- **JWKS 生命周期**：重启、升级或扩容 LobeHub 时保留 PostgreSQL 数据卷，让所有副本持续使用同一把签名密钥。
- **模型服务商设置**：登录后添加聊天模型与嵌入模型凭证。文件可以直接保存，配置嵌入模型后会开始知识索引。
- **SearXNG**：需要联网检索时填写外部 `SEARXNG_URL`。
- **Marketplace**：智能体与任务推荐依赖外部 LobeHub Market 服务，需要访问 `market.lobehub.com`。

## 资源配置

经过验证的基线为 LobeHub 分配 `500m` CPU 和 `1024Mi` 内存。完成注册、Home 和 Resources 操作及文件上传后，应用使用约 `468Mi` 内存。`512Mi` 候选配置触发了 V8 堆上限与进程重启，因此 `1024Mi` 是当前版本在 Sealos 上的最小稳定资源档位。每个 KubeBlocks 数据库组件使用 `500m` CPU 和 `512Mi` 内存。

## 故障排查

### 数据库迁移失败

数据库首次启动会下载约 67 MiB 的 `pg_search` 软件包，并触发一次由 KubeBlocks 管理的 PostgreSQL 替换。健康状态下，PostgreSQL 会显示 `pg_search` 0.24.2，应用日志会包含 `database migration pass`。

### 注册失败

当 `AUTH_ALLOWED_EMAILS` 包含限制条件时，确认注册邮箱符合对应地址或域名。

### JWT 或内部认证失败

首次健康启动的日志会包含 `Generated and stored a deployment-specific JWKS`，后续重启日志会包含 `Loaded deployment-specific JWKS from PostgreSQL`。恢复已有部署时，请使用与应用匹配的 PostgreSQL 数据卷备份，以保持原有签名身份。

### 文件上传失败

确认 ObjectStorageBucket 及其生成的凭证 Secret 已经就绪，然后重启 LobeHub。

### 知识文件显示嵌入错误

在 LobeHub 设置中配置支持嵌入的模型服务商，然后重试该文件。源文件会保存在 Sealos 对象存储中，知识索引会等待有效的模型凭证。

### Marketplace 推荐返回 403

可选的 Agent Market 与每日任务推荐会访问 `market.lobehub.com`。验证期间，Cloudflare 对 Sealos 区域的出站 IP 返回 HTTP 403，同一端点通过另一网络访问时返回 HTTP 200。请使用该公共服务接受的出站路径，或把 `MARKET_BASE_URL` 设置为已授权的自托管 Market 地址。Chat、Tasks、Pages、Resources 和 Memory 继续使用本地 LobeHub 服务。

## 更多资源

- [LobeHub 自托管指南](https://lobehub.com/docs/self-hosting/start)
- [LobeHub 环境变量](https://lobehub.com/docs/self-hosting/environment-variables)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

LobeHub 使用其仓库声明的许可证。本 Sealos 模板遵循模板仓库许可证。
