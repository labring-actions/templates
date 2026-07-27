# 在 Sealos 上部署 Chatwoot

Chatwoot 是一款开源客户支持平台，提供实时聊天、共享收件箱、联系人管理、自动化和全渠道会话能力。此模板会部署 Chatwoot、托管 PostgreSQL、Redis、后台任务进程和 HTTPS 入口，并支持本地持久化存储与私有 Sealos S3 对象存储两种附件方案。

![使用 S3 附件的 Chatwoot 会话](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/chatwoot/website-screenshot.webp)

## 模板包含的组件

- **Chatwoot `v4.16.2` Web**：在 `3000` 端口运行 Rails 应用
- **Chatwoot `v4.16.2` Sidekiq**：处理后台任务
- **PostgreSQL `16.4.0` + pgvector**：由 KubeBlocks 管理
- **Redis `7.2.7` + Sentinel**：由 KubeBlocks 管理
- **数据库初始化与迁移 Job**：执行 `db:chatwoot_prepare`
- **本地持久化存储**：默认附件存储方案
- **私有 Sealos S3 兼容对象存储**：可选附件存储方案
- **公网 HTTPS**：由 Sealos 管理 Service 和 Ingress
- **启动、就绪与存活探针**：检查 `/health` 和 `/api`

Chatwoot 的生产架构依赖 Rails Web、Sidekiq、PostgreSQL 和 Redis。邮件发送需要额外配置 SMTP 或事务邮件服务。

## 常见用途

- 网站实时客服
- 客服、销售和运营团队共享收件箱
- 通过 API 接入客户会话
- 联系人与会话管理
- 邮件、即时通信和社交渠道集成
- 客服自动化、报表与帮助中心

## 部署步骤

1. 打开 [Sealos 应用商店中的 Chatwoot 模板](https://sealos.io/products/app-store/chatwoot)。
2. 首次部署时保持 **Enable account signup** 开启。
3. 选择本地附件存储，或启用私有 Sealos S3 存储。
4. 点击 **部署**，等待 Web 与 Sidekiq 工作负载进入就绪状态。首次创建 PostgreSQL 和 Redis 通常需要数分钟。
5. 打开 Sealos 展示的 HTTPS 地址。

### 部署参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `enable_account_signup` | `true` | 开启首位管理员初始化与账号注册流程 |
| `enable_s3_storage` | `false` | 为附件创建私有 Sealos 对象存储 Bucket |

模板会自动生成 `SECRET_KEY_BASE`，数据库、Redis 和对象存储凭据来自 Sealos 管理的 Kubernetes Secret。

## 创建管理员与登录

模板内预设账号数量为零。首次打开 Chatwoot 后，通过初始化页面创建管理员：

1. 打开部署后的 URL。
2. 填写 **Name**、**Company Name**、**Work Email** 和高强度 **Password**。
3. 点击 **Finish Setup**。
4. 完成角色、网站、语言、时区、行业和团队规模等资料。
5. Chatwoot 展示登录页时，使用刚才填写的工作邮箱和密码登录。

所需账号创建完成后，可以在部署配置中将 `enable_account_signup` 设为 `false`，关闭公开账号注册入口。已有用户与受邀坐席继续使用各自凭据登录。

密码重置、坐席邀请和邮件渠道依赖可用的发信服务。正式使用这些邮件流程前，请在 Sealos Canvas 中配置对应的 SMTP 或事务邮件环境变量。

## 验证应用功能

登录后可以完成一条完整验证流程：

1. 打开 **Settings → Inboxes → Add Inbox**。
2. 选择 **Website** 或 **API** 等渠道。
3. 设置收件箱名称并添加坐席。
4. 发起一条测试会话。
5. 回复消息并上传附件。

公网地址还提供两个运行状态入口：

- `/health`：Rails 进程健康时返回 `{"status":"woot"}`。
- `/api`：返回 Chatwoot 版本与依赖状态。

## 附件存储

### 本地持久化存储

当 `enable_s3_storage=false` 时，附件保存在挂载到 Web 与 Sidekiq Pod 的 `1Gi` 共享持久卷 `/app/storage`。模板会将两个 Pod 调度到同一工作节点，确保 ReadWriteOnce 卷可以同时服务这两个进程。

本地模式适合评估和小型单副本部署。备份计划应同时覆盖 PostgreSQL 与 Chatwoot 存储卷。

### 私有 Sealos S3 存储

当 `enable_s3_storage=true` 时，模板会创建私有 `ObjectStorageBucket`，并配置 Chatwoot 官方支持的 `s3_compatible` Active Storage 服务。Bucket、Endpoint、Access Key 和 Secret Key 由 Sealos Secret 注入。Web 与 Sidekiq 共用同一个对象存储后端，应用工作负载无需附件 PVC。

匿名直接访问对象会收到 `403`。用户通过 Chatwoot 下载附件时，应用会向对象存储发起授权请求。

Sealos S3 更适合长期保存附件、独立备份以及后续扩展应用副本。

## 持久化数据

| 路径或服务 | 用途 | 创建条件 |
| --- | --- | --- |
| PostgreSQL 数据卷 | 账号、收件箱、联系人、会话、配置与附件元数据 | 始终创建 |
| Redis 数据卷 | 队列、缓存与运行时协调 | 始终创建 |
| `/app/storage` | 本地 Active Storage 附件 | `enable_s3_storage=false` |
| 私有 Sealos Bucket | S3 兼容 Active Storage 附件 | `enable_s3_storage=true` |

备份时请同时保存 PostgreSQL 与当前附件后端。两者共同组成完整的附件记录。

## 默认资源

应用资源规格来自冷启动和真实操作测试，覆盖管理员初始化、创建收件箱、创建会话、坐席回复以及附件上传下载：

| 组件 | CPU 上限 | 内存上限 | CPU 请求 | 内存请求 |
| --- | ---: | ---: | ---: | ---: |
| Chatwoot Web | `100m` | `1024Mi` | `10m` | `102Mi` |
| Chatwoot Sidekiq | `100m` | `1024Mi` | `10m` | `102Mi` |
| 数据库迁移 Job | `100m` | `512Mi` | `10m` | `51Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis Sentinel | `500m` | `512Mi` | `50m` | `51Mi` |
| 依赖检查与 PostgreSQL 初始化容器 | `100m` | `128Mi` | `10m` | `12Mi` |

当并发访问、渠道集成、自动化、批量操作和团队规模增加时，请提高 Web 与 Sidekiq 的 CPU，并持续观察 PostgreSQL、Redis、队列延迟和对象存储流量。

## 扩展副本

模板默认启动 1 个 Web 副本和 1 个 Sidekiq 副本。扩展应用时建议启用 Sealos S3，让所有副本连接同一套 PostgreSQL 与 Redis，保持一致的 `SECRET_KEY_BASE`，并根据队列任务量调整 Sidekiq 资源。PostgreSQL 与 Redis 拓扑升级需要配套的备份和故障切换方案。

## 升级

Chatwoot 版本升级可能包含数据库迁移。更新镜像标签前请执行以下步骤：

1. 备份 PostgreSQL 与附件存储。
2. 阅读目标版本的 Chatwoot Release Notes。
3. 将 Web 与 Sidekiq 更新为相同镜像标签。
4. 执行 `bundle exec rails db:chatwoot_prepare`。
5. 验证 `/health`、`/api`、登录、会话、后台任务和附件功能。

早期 v4.7.0 模板创建的 StatefulSet 使用了不同的不可变存储定义。升级这类实例时应执行并行迁移：备份 PostgreSQL 与两个附件 PVC，使用新的应用名称部署本模板，迁移数据库和附件，完成验证后再切换流量。新部署时请选择本地存储或 Sealos S3；切换存储模式同样需要迁移数据。

## 故障排查

### 应用仍在启动

在 Sealos Canvas 中检查 Web、Sidekiq、PostgreSQL、Redis 和迁移 Job。依赖检查容器会等待数据库 Schema 与 Redis 可用后再启动 Chatwoot。首次创建数据库可能需要数分钟。

### 首位管理员初始化页面无法打开

使用 `enable_account_signup=true` 部署，然后再次打开 Chatwoot 公网地址。后续登录使用初始化页面创建的工作邮箱和密码。

### 邀请或密码重置邮件未送达

为 Chatwoot 配置 SMTP 或事务邮件服务对应的环境变量，然后重启 Web 与 Sidekiq。

### S3 对象地址返回 `403`

Bucket 使用私有策略。请从已登录的 Chatwoot 会话打开附件，由应用完成授权下载。

### 后台操作持续等待

检查 Sidekiq 就绪状态与日志、Redis 健康状态和队列延迟。异步任务的处理能力由 Sidekiq 决定。

## 相关文档

- [Chatwoot 官网](https://www.chatwoot.com)
- [自托管安装指南](https://developers.chatwoot.com/self-hosted)
- [生产架构](https://developers.chatwoot.com/self-hosted/deployment/architecture)
- [Docker 部署指南](https://developers.chatwoot.com/self-hosted/deployment/docker)
- [环境变量参考](https://developers.chatwoot.com/self-hosted/configuration/environment-variables)
- [对象存储支持列表](https://developers.chatwoot.com/self-hosted/deployment/storage/supported-providers)
- [Chatwoot GitHub 仓库](https://github.com/chatwoot/chatwoot)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Chatwoot 社区版采用 [MIT License](https://github.com/chatwoot/chatwoot/blob/v4.16.2/LICENSE)。部分功能可能具有其他许可条件，正式使用前请查看 Chatwoot 仓库和产品条款。此仓库仅提供 Sealos 部署模板，Chatwoot 本身的许可保持不变。
