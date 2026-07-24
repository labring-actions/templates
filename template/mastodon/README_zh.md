# 在 Sealos 上部署和托管 Mastodon

Mastodon 是面向 Fediverse 社区的开源去中心化社交网络服务器。此模板会部署 Mastodon 4.6.3、PostgreSQL、Redis、Sidekiq、实时 streaming、HTTPS，并提供本地持久化媒体存储和私有 Sealos 对象存储两种选择。

![Mastodon 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mastodon/website-screenshot.webp)

## 关于 Mastodon 托管

Mastodon 让社区拥有独立的社交服务器、审核策略、公开身份，并接入更广泛的 Fediverse。Web 进程提供用户界面和 API，Sidekiq 处理后台任务与联邦任务，streaming 进程提供实时更新。

模板会在部署阶段创建数据库结构和第一个 Owner 账号。公开注册可以保持关闭、采用管理员审核或立即开放。初始 Owner 可以直接登录；账号确认、邀请、通知和密码恢复等邮件流程需要可用的 SMTP。

每次部署还会自动派生一组稳定的 VAPID 密钥，用于 Web Push。Pod 重启和滚动更新会持续使用同一组密钥，管理员只需填写业务配置，部署表单会自动处理加密参数。

## 常见使用场景

- **社区社交网络**：为组织、创作者社区或兴趣小组运行带审核能力的空间。
- **机构公开身份**：为学校、公司、非营利组织或公共机构托管官方账号。
- **私有实例**：为内部团队或受邀成员运行封闭服务器。
- **Fediverse 发布**：从自己的服务器发布内容，并与兼容服务器上的账号互动。

## Mastodon 托管依赖

- **Mastodon Web 与 Sidekiq**：`tootsuite/mastodon:v4.6.3`
- **Streaming**：`tootsuite/mastodon-streaming:v4.6.3`
- **数据库**：KubeBlocks PostgreSQL 16 和专用 `mastodon_production` 数据库
- **队列与缓存**：KubeBlocks Redis 7 和 Sentinel
- **媒体存储**：默认使用共享本地持久卷，也可以选择私有 Sealos 对象存储
- **初始化**：数据库 Job 和 Mastodon Setup Job
- **网络入口**：Service、HTTPS Ingress 和 Sealos App 资源

### 部署依赖链接

- [Mastodon 文档](https://docs.joinmastodon.org/) - 官方用户与管理员文档
- [Mastodon 配置参考](https://docs.joinmastodon.org/admin/config/) - 生产环境变量说明
- [Mastodon 对象存储文档](https://docs.joinmastodon.org/admin/optional/object-storage/) - 官方对象存储指南
- [Mastodon GitHub 仓库](https://github.com/mastodon/mastodon) - 源码和版本发布
- [Sealos 文档](https://sealos.io/docs) - 平台部署与运维指南

### 实现细节

本地存储模式会为 Web 与 Sidekiq 创建共享的 `ReadWriteOnce` 媒体卷。模板通过 Pod Affinity 和 Recreate 策略，让两个媒体写入角色调度到该卷所在节点。

可选 S3 模式会创建私有 `ObjectStorageBucket`。Mastodon 使用自动生成的凭据写入私有对象，无状态同域代理通过 `/__sealos_media/` 提供授权读取。对象原始地址会继续限制匿名读写。

模板会为每个实例生成专属种子，并在 Setup、Web 和 Sidekiq 进程中派生合法的 P-256 VAPID 密钥对。派生后的私钥仅存在于进程内存中，公钥则通过 Mastodon 标准实例 API 提供给浏览器，用于创建推送订阅。

实测最低应用资源基线为：

- Web：`100m` CPU 和 `512Mi` 内存
- Sidekiq：`100m` CPU 和 `512Mi` 内存
- Streaming：`100m` CPU 和 `128Mi` 内存
- Setup Job：`100m` CPU 和 `512Mi` 内存
- 可选媒体代理：`100m` CPU 和 `128Mi` 内存

Web 与 Sidekiq 在相邻的 `256Mi` 内存档位均触发 `OOMKilled`。上述资源可以完成冷启动、Owner 创建、登录、媒体上传、嘟文发布、喜欢与书签操作，并在稳定窗口内保持零重启。

Mastodon 使用 GNU Affero General Public License v3.0。

## 为什么在 Sealos 上部署 Mastodon？

- **一键创建完整栈**：同时创建 Mastodon、PostgreSQL、Redis、存储、网络和 TLS。
- **托管数据服务**：使用自动生成的数据库与 Redis 凭据，并完成自动初始化。
- **存储模式可选**：使用本地持久卷起步，或选择私有 S3 兼容媒体存储。
- **Owner 账号就绪**：Setup Job 和 Web Deployment 完成后即可登录。
- **即时 HTTPS 访问**：从 Sealos Canvas 打开自动生成的应用域名。
- **Canvas 运维**：在一个工作区查看日志、健康状态、资源、存储和网络路由。

## 部署指南

1. 打开 [Mastodon 模板](https://sealos.io/products/app-store/mastodon)，点击 **Deploy Now**。
2. 填写初始 Owner 信息：
   - `admin_username`：使用小写字母、数字或下划线。
   - `admin_email`：用于首次登录的邮箱。
   - `admin_password`：Owner 账号的强密码。
3. 选择 `registration_mode`：
   - `none`：关闭公开注册，由 Owner 管理用户。
   - `approved`：访客提交注册申请，由管理员审核。
   - `open`：访客可以立即创建账号。
4. 选择媒体存储模式：
   - 保持 `enable_s3_storage` 关闭，使用共享本地持久卷。
   - 启用 `enable_s3_storage`，创建私有 Sealos S3 兼容 bucket 和同域媒体代理。
5. 实例需要账号邮件流程时，启用 SMTP 并填写服务器、端口、登录名、密码和发件地址。
6. 开始部署，等待 PostgreSQL、Redis、数据库迁移、Owner 创建、VAPID 密钥派生和应用启动完成。全新部署通常需要数分钟。
7. 从 Canvas 打开自动生成的 Mastodon URL。

## 首次登录与注册

打开 `https://<your-mastodon-domain>/auth/sign_in`，使用部署时填写的 `admin_email` 或 `admin_username` 和 `admin_password` 登录。Setup Job 会自动确认并批准这个 Owner 账号。

登录后，打开 **Preferences** 和 **Administration**，配置服务器名称、说明、规则、审核、角色、联邦和注册设置。

使用 `approved` 或 `open` 注册模式时，请在邀请公众注册前配置 SMTP。新用户随后可以收到 Mastodon 账号确认和生命周期邮件。

## 配置

- **注册**：部署后可以从 Administration 调整注册行为。
- **SMTP**：为账号确认、邀请、通知和密码恢复配置可靠的出站邮件服务。
- **Web Push**：每个实例都会自动生成 VAPID 密钥，并在 Pod 重启和滚动更新期间保持稳定。
- **存储**：本地模式把媒体保存在共享 PVC；S3 模式把媒体保存在私有 bucket，并通过应用域名提供读取。
- **域名**：Mastodon 身份与 `LOCAL_DOMAIN` 绑定。向社区开放实例前，请先规划自定义域名迁移。
- **备份**：同时保护 PostgreSQL 与所选媒体存储，形成完整恢复点。

## 扩缩容

根据请求延迟和队列深度提高 Web 与 Sidekiq 的 CPU 和内存。社区规模增长后，可以增加 Sidekiq 容量，并根据真实任务分布调整队列。本地媒体模式围绕共享 `ReadWriteOnce` 卷保留一个 Web 副本和一个同节点 Sidekiq 副本。S3 模式可以为后续多副本设计提供存储基础，扩容前需要验证联邦处理与后台任务行为。

## 故障排查

**Owner 凭据无法登录**

使用部署表单中填写的 Owner 邮箱或用户名和密码。登录前确认 Setup Job 已成功完成。

**账号确认或密码恢复邮件缺失**

启用 SMTP，并检查发件地址、服务器、端口、登录名、密码、TLS 行为和邮件服务商投递日志。

**浏览器推送注册失败**

检查 Setup、Web 和 Sidekiq 日志中的 VAPID 派生错误。完整重建实例会生成新密钥，用户再次访问站点时会注册新的浏览器推送订阅。

**媒体上传或图片读取失败**

本地模式需要检查共享媒体 PVC 与 Web/Sidekiq 调度状态。S3 模式需要检查 ObjectStorageBucket、媒体代理 Deployment、`/__sealos_media/` 路由和对象存储凭据。

**Web 或 Sidekiq 触发 OOMKilled**

每个角色至少保留实测通过的 `512Mi` 内存，并随社区流量增长继续提高资源。

**时间线更新缓慢**

检查 Sidekiq 队列深度、Redis 健康状态、streaming 日志和联邦投递延迟。提高 Sidekiq 资源后再调整队列并发。

## 更多资源

- [Mastodon 管理员指南](https://docs.joinmastodon.org/admin/)
- [Mastodon 扩缩容指南](https://docs.joinmastodon.org/admin/scaling/)
- [Mastodon 审核指南](https://docs.joinmastodon.org/admin/moderation/)
- [Mastodon GitHub Issues](https://github.com/mastodon/mastodon/issues)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Mastodon 使用 GNU Affero General Public License v3.0。
