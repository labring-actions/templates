# 在 Sealos 上部署和托管 Ghost

Ghost 是开源发布、邮件通讯、会员和订阅平台。此模板会在 Sealos 上部署 Ghost 6.53.0，并配置托管 MySQL、持久化内容存储、HTTPS Ingress，以及可选的私有 S3 兼容媒体存储。

![Ghost 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/ghost/website-screenshot.webp)

## 关于 Ghost 托管

Ghost 通过一个有状态应用提供公开站点 `/` 和管理后台 `/ghost`。模板会创建 KubeBlocks MySQL 8 集群，并在应用启动前初始化专用 `ghost` 数据库，满足 Ghost 生产模式的数据库要求。

本地模式把主题、图片和内容文件保存在 `/var/lib/ghost/content` 持久卷。可选对象存储模式使用 Ghost 6.53.0 内置的 `S3Storage` 适配器保存图片、媒体和文件，并通过轻量无状态代理从 Sealos 私有 bucket 提供同域名访问。

## 常见使用场景

- **独立出版**：运行专业博客、杂志或文档站点。
- **邮件通讯**：在同一编辑系统中创建文章并发送 Newsletter。
- **会员站点**：管理会员、受限内容和付费订阅。
- **编辑团队**：为作者和编辑提供共享发布工作区。

## Ghost 托管依赖

- **Ghost**：`ghost:6.53.0-alpine`
- **数据库**：KubeBlocks MySQL `ac-mysql-8.0.30-1` 和专用 `ghost` 数据库
- **持久化存储**：`/var/lib/ghost/content`，保存本地主题和内容文件
- **可选对象存储**：Sealos 私有 S3 兼容 bucket 和同域读取代理
- **网络入口**：Service、HTTPS Ingress 和 Sealos App 资源

### 部署依赖链接

- [Ghost 文档](https://ghost.org/docs/) - 官方产品与管理文档
- [Ghost 配置文档](https://ghost.org/docs/config/) - 官方运行配置参考
- [Ghost Docker 镜像](https://hub.docker.com/_/ghost) - 官方容器说明
- [Ghost GitHub 仓库](https://github.com/TryGhost/Ghost) - 源码和版本发布
- [Sealos 文档](https://sealos.io/docs) - 平台部署与运维指南

### 实现细节

模板设置 `NODE_ENV=production`，根据 Sealos 自动生成的域名构造 HTTPS 规范地址，并从 KubeBlocks 连接 Secret 读取数据库凭据。初始化 Job 会先创建使用 `utf8mb4` 的 `ghost` 数据库，再由应用执行完整迁移。

S3 模式会为图片和 `media` 存储配置 Ghost 内置 `S3Storage` 适配器。bucket 始终保持私有，`/__sealos_storage/` 路径由无状态代理处理，代理使用自动生成的 bucket 凭据读取对象。

实测最低资源基线为：Ghost 使用 `100m` CPU 和 `256Mi` 内存；数据库初始化 Job 使用 `100m` CPU 和 `128Mi` 内存；可选存储代理使用 `100m` CPU 和 `128Mi` 内存。Ghost 在 128Mi 冷启动时触发 OOM；256Mi 可完成全新 MySQL 迁移、所有者初始化、媒体上传和文章发布，并保持零重启。MySQL 使用 `500m` CPU 和 `512Mi` 内存。

Ghost 使用 MIT License。

## 为什么在 Sealos 上部署 Ghost？

- **一键创建发布栈**：同时创建 Ghost、MySQL、持久化存储、网络和 TLS。
- **生产数据库**：使用托管 MySQL、自动生成凭据和数据库初始化任务。
- **内容持久化**：Pod 重启后继续保留主题和本地内容文件。
- **私有对象存储选项**：把图片和媒体保存到 Sealos bucket，同时保持同域名访问。
- **即时公网访问**：应用启动后直接打开自动生成的 HTTPS 域名。
- **Canvas 运维**：部署完成后继续调整应用资源和存储容量。

## 部署指南

1. 打开 [Ghost 模板](https://sealos.io/products/app-store/ghost)，点击 **Deploy Now**。
2. 选择存储参数：
   - **启用 S3 兼容对象存储**（`enable_s3_storage`）：默认关闭。启用后，Ghost 会把图片、媒体和文件保存到 Sealos 私有 bucket。
3. 等待 MySQL、数据库初始化 Job、Ghost 和可选存储代理进入就绪状态。全新部署需要创建完整数据库结构，通常需要数分钟。
4. 打开 `https://<your-ghost-domain>/ghost`。
5. 填写站点标题、所有者姓名、邮箱和强密码，然后点击 **Create account & start publishing**。
6. 创建并发布一篇文章，确认 Ghost Admin 和公开站点均可正常使用。

## 首次登录与注册

首次访问 `/ghost` 时需要创建所有者账号：

1. 打开 `https://<your-ghost-domain>/ghost`。
2. 在初始化表单中填写出版物标题和所有者信息。
3. 使用由随机大小写字母、数字和符号组成的强密码。Ghost 会在初始化阶段校验密码强度。
4. 提交表单，等待 Ghost Admin 打开。

初始化完成后，同一 `/ghost` 地址会显示管理员登录页。使用初始化时创建的所有者邮箱和密码登录。配置邮件发送服务后，可在 Ghost Admin 中邀请其他团队成员。

## 配置

- **存储模式**：默认使用本地存储。S3 模式用于图片、媒体和文件，内容卷继续保存主题及其他 Ghost 本地数据。
- **SMTP**：发送 Newsletter、密码重置邮件和团队邀请前，需要配置邮件发送服务。
- **支付**：启用付费会员前，在 Ghost Admin 中添加 Stripe 凭据。
- **Social Web 与 Explore**：模板默认关闭 Social Web 和 Explore ping，形成干净的独立部署。相关公网服务和设置准备完成后，可启用对应功能。
- **团队设备验证**：模板关闭团队设备邮件验证，支持在 SMTP 配置前创建首个所有者账号。

## 扩缩容

默认 `ReadWriteOnce` 内容卷对应一个 Ghost 副本。出版内容、会员数量或 Newsletter 任务增长时，可在 Canvas 中纵向提高 CPU 和内存，并同步扩展 MySQL 与 PVC 资源。多副本架构需要共享内容存储和经过验证的 Ghost 集群方案。

## 故障排查

**部署后 Ghost Admin 仍在加载**

Ghost 可能正在创建初始 MySQL 数据结构。等待 Ghost StatefulSet 进入 Ready 状态，然后刷新 `/ghost`。

**初始化表单拒绝密码**

使用更长的随机密码，并组合大小写字母、数字和符号。

**Newsletter 或邀请邮件未送达**

在使用邮件工作流前配置 Ghost SMTP。

**S3 媒体返回存储错误**

确认 ObjectStorageBucket 和存储代理均已 Ready。保持 bucket 私有，并通过自动生成的 Ghost 域名访问媒体。

**Ghost Pod 启动时 OOM**

保持默认 256Mi 应用内存限制；大型出版站点可继续提高该值。

## 更多资源

- [Ghost Admin 文档](https://ghost.org/docs/admin/)
- [Ghost 会员功能](https://ghost.org/docs/members/)
- [Ghost Newsletter](https://ghost.org/docs/newsletters/)
- [Ghost 自托管常见问题](https://ghost.org/docs/faq/self-hosting/)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Ghost 使用 MIT License。
