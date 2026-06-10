# 在 Sealos 上部署和托管 Ghost

Ghost 是开源发布、邮件通讯、会员和订阅平台。本模板在 Sealos Cloud 上部署 Ghost、KubeBlocks MySQL 和持久化内容存储。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/ghost/website-screenshot.webp)

## 关于托管 Ghost

Ghost 作为 Node.js 应用运行，公开站点和 Ghost Admin 共用同一个访问地址。Sealos 模板会创建外接 MySQL 数据库，因为 Ghost 生产模式需要 MySQL 8，并把 `/var/lib/ghost/content` 挂载为持久化存储，用于保存主题、图片和本地内容文件。

部署内容包括公开 HTTPS 地址、NGINX Ingress、KubeBlocks MySQL 集群、数据库初始化任务和有状态 Ghost 工作负载。

## 常见使用场景

- **独立出版**：运行专业博客或内容站点。
- **邮件通讯运营**：统一管理文章、会员和 Newsletter。
- **会员内容站点**：构建付费订阅和受限内容流程。
- **团队编辑协作**：为作者和编辑提供共享发布后台。

## Ghost 托管依赖

Sealos 模板包含 Ghost、KubeBlocks MySQL、持久化存储、HTTPS Ingress 和自动数据库创建。

### 部署依赖

- [Ghost 文档](https://ghost.org/docs/) - 官方 Ghost 文档
- [Ghost Docker 镜像](https://hub.docker.com/_/ghost) - 官方 Docker 镜像文档
- [Ghost GitHub 仓库](https://github.com/TryGhost/Ghost) - 源码与发布记录

### 实现细节

**架构组件：**

- **Ghost**：主发布与管理应用，使用 `ghost:6.44.1-alpine`
- **MySQL**：KubeBlocks MySQL `ac-mysql-8.0.30-1`
- **持久化存储**：挂载到 `/var/lib/ghost/content`
- **Ingress**：通过 Sealos 域名提供 HTTPS 访问

**配置：**

模板设置 `NODE_ENV=production`，把 `url` 配置为生成的 HTTPS 地址，并连接到自动创建的 MySQL 数据库。Ghost 公开站点位于 `/`，管理后台位于 `/ghost`。

**许可证：**

Ghost 使用 MIT License。

## 为什么在 Sealos 上部署 Ghost？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用从开发到生产部署和管理的完整生命周期。在 Sealos 上部署 Ghost 可以获得：

- **一键部署**：一次部署 Ghost、MySQL、存储、Ingress 和 SSL。
- **内置持久化存储**：重启后保留上传内容和主题。
- **托管数据库**：使用 KubeBlocks MySQL 运行 Ghost。
- **即时公网访问**：部署完成后直接使用生成的 HTTPS 地址。
- **轻松调整配置**：在 Sealos Canvas 中调整资源和环境变量。

在 Sealos 上部署 Ghost，把精力放在内容发布上。

## 部署指南

1. 打开 [Ghost 模板](https://sealos.io/products/app-store/ghost)，点击 **Deploy Now**。
2. 配置部署参数：
   - **use_s3_storage**：需要让 Ghost 媒体和上传文件使用 S3 兼容对象存储时启用。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可在对话框中描述需求让 AI 执行，或点击对应资源卡片调整配置。
4. 通过提供的 URL 访问 Ghost：
   - **公开站点**：使用 Sealos 生成的 HTTPS 地址。
   - **管理员初始化**：在同一地址后追加 `/ghost`，创建第一个所有者账号。

## 配置

Ghost Admin 位于 `https://[your-app-url]/ghost`。首次访问会进入站点所有者账号创建流程，需要创建管理员邮箱和密码。完成后继续使用 `/ghost` 进行管理员登录。

模板在首次初始化阶段关闭 staff-device 邮箱验证，因此可先创建所有者账号，再配置 SMTP。发送 Newsletter 或邀请团队成员前，请在 Ghost Admin 中配置 SMTP。

模板默认关闭 Social Web 和 Ghost Explore ping，让单节点部署启动日志保持干净。后续需要这些功能时，可在 Ghost Admin 中补充对应支撑服务和公网配置后再启用。

本模板默认使用本地持久化内容存储。**Use S3-compatible object storage through the Ghost storage adapter configuration** 开关会创建 Sealos 对象存储 bucket，在启动阶段把 Ghost S3 存储适配器安装到 `/var/lib/ghost/content/adapters/storage/s3`，并注入 S3 适配器配置变量。

## 扩缩容

调整 Ghost 资源：

1. 打开当前部署的 Canvas。
2. 点击 Ghost StatefulSet 资源卡片。
3. 调整 CPU、内存或存储。
4. 在对话框中应用变更。

## 故障排查

**管理员初始化页面加载失败**

- 原因：Ghost 可能仍在初始化或等待 MySQL。
- 解决：等待 Ghost 工作负载就绪后再次打开 `/ghost`。

**图片或主题重启后丢失**

- 原因：内容卷被修改或删除。
- 解决：保持 `/var/lib/ghost/content` 挂载到持久化存储。

## 更多资源

- [Ghost 配置](https://ghost.org/docs/config/)
- [Ghost Admin](https://ghost.org/docs/admin/)
- [Ghost Docker 镜像](https://hub.docker.com/_/ghost)

## 许可证

本 Sealos 模板遵循仓库许可证。Ghost 本身使用 MIT License。
