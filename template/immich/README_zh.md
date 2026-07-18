# 在 Sealos 上部署和托管 Immich

Immich 是一款自托管照片和视频管理平台，可用于备份、整理、搜索和分享个人媒体。此模板会在 Sealos Cloud 上部署 Immich，并包含 PostgreSQL、Redis、持久化媒体存储和可选机器学习服务。

![Immich 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/immich/website-screenshot.webp)

## 关于 Immich 托管

Immich 提供浏览器界面、移动端同步接口、后台媒体处理和智能图库功能。Sealos 模板会自动创建应用服务、带 pgvector 的 PostgreSQL 16.4、Redis 7.2.7、持久化上传存储，以及可选的机器学习服务。

应用服务会将照片和视频保存在挂载到 `/usr/src/app/upload` 的持久化卷中。PostgreSQL 保存元数据、用户、相册、任务和向量索引；Redis 负责后台任务队列和缓存。启用机器学习后，独立的 Immich ML 服务会提供人脸识别、目标检测和智能搜索能力。

## 常见使用场景

- **个人照片备份**：将手机照片和视频同步到自己的私有服务。
- **家庭媒体库**：集中管理共享相册、人物、地点和时间线。
- **私有智能搜索**：使用本地机器学习能力进行人脸识别和语义搜索。
- **自托管 Google Photos 替代方案**：将媒体文件和元数据保留在自己的 Sealos 部署中。

## Immich 托管依赖

此 Sealos 模板包含单节点 Immich 部署所需的运行依赖：

- **Immich Server v2.7.5**：Web 界面、API、后台处理和移动端同步入口。
- **Immich Machine Learning v2.7.5**：可选机器学习服务，用于人脸识别和智能搜索。
- **PostgreSQL 16.4**：由 KubeBlocks 管理，并启用 pgvector 扩展。
- **Redis 7.2.7**：由 KubeBlocks 管理，用于任务队列和缓存协调。
- **持久化卷**：媒体上传、机器学习缓存、PostgreSQL 数据和 Redis 数据都会持久化保存。

### 部署依赖

- [Immich 文档](https://immich.app/docs/) - 官方文档
- [Immich 安装后配置指南](https://immich.app/docs/install/post-install/) - 首个用户和管理员设置
- [Immich GitHub 仓库](https://github.com/immich-app/immich) - 源码和发布记录

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Immich Server**：StatefulSet，监听 `2283` 端口，提供 Web 界面和 API。
- **Immich Machine Learning**：可选 StatefulSet，监听 `3003` 端口，处理机器学习请求。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4 集群，包含 `immich` 数据库和向量扩展。
- **Redis**：KubeBlocks Redis 7.2.7 集群，用于 Immich 任务队列和缓存。
- **Ingress 和 App 入口**：由 Sealos 管理的 HTTPS 访问地址。

**配置说明：**

- `enable_machine_learning` 控制是否部署 Immich ML 服务。
- 启用机器学习时，服务端通过 `IMMICH_MACHINE_LEARNING_URL` 访问 ML 服务。
- PostgreSQL 初始化任务会幂等创建 `immich` 数据库和所需扩展。
- 上传的媒体文件保存在 `/usr/src/app/upload`；备份时请同时备份此卷和 PostgreSQL。

**许可证信息：**

Immich 使用 GNU Affero General Public License v3.0 发布。此 Sealos 模板遵循模板仓库的许可证。

## 为什么在 Sealos 上部署 Immich？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一管理部署、网络、存储和应用生命周期。在 Sealos 上部署 Immich 可以获得：

- **一键部署**：通过一个模板部署 Immich、PostgreSQL、Redis、存储和 HTTPS 入口。
- **内置持久化存储**：媒体上传、模型缓存、数据库和 Redis 数据可在重启后保留。
- **Kubernetes 底座**：无需手写 Kubernetes YAML，也能运行在托管 Kubernetes 上。
- **易于调整配置**：可通过 Canvas 资源卡片或 AI 对话调整资源、存储、环境变量和扩缩容设置。
- **即时公网访问**：部署完成后获得 Sealos 管理的 HTTPS 地址。
- **按量使用资源**：从测试过的资源配置开始，随着媒体库增长逐步扩容。

## 部署指南

1. 打开 [Immich 模板](https://sealos.io/products/app-store/immich)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `enable_machine_learning`：保留 `true` 可启用人脸识别和智能搜索；设为 `false` 可获得更轻量的部署。
3. 等待部署完成。通常需要 2-3 分钟，首次启动时 PostgreSQL、Redis 和应用服务依次初始化，可能需要更久。
4. 通过生成的地址访问应用：
   - **Immich Web 界面**：打开 Sealos 生成的 URL，例如 `https://<your-app-host>.<your-sealos-domain>`。
5. 如需后续调整，请打开部署 Canvas，在 AI 对话中描述需求，或点击对应资源卡片修改资源、存储或环境变量。

## 首次登录和注册

Immich 不提供默认用户名或密码。全新部署后，打开 Web 界面并完成 **Getting Started** 流程；第一个注册的用户会成为管理员。

管理员账号创建后，使用该邮箱和密码登录。后续可根据访问策略，在 Immich 管理设置中邀请或创建其他用户。

## 配置

部署完成后，可以通过以下方式配置 Immich：

- **Immich 管理界面**：管理用户、图库、任务、存储模板设置和服务偏好。
- **Sealos AI 对话**：描述需要的变更，例如增加资源或更新环境变量。
- **Sealos 资源卡片**：调整 StatefulSet 资源、存储容量、Ingress 设置或数据库资源。
- **移动端 App**：在官方 Immich 移动端中，将 Sealos 生成的 URL 填为服务器地址。

## 扩缩容

建议先使用模板默认配置，再根据媒体库规模和功能使用情况扩容：

1. 打开 Immich 部署对应的 Canvas。
2. 点击 Immich Server、ML 服务、PostgreSQL 或 Redis 资源卡片。
3. 按需增加 CPU、内存、存储或副本配置。
4. 应用变更并等待资源滚动更新完成。

大型媒体库和高强度机器学习任务会需要更多内存和存储。进行大版本升级或存储变更前，请先备份 PostgreSQL 和上传卷。

## 故障排查

### Web 页面刚部署后暂时不可用

Immich 依赖 PostgreSQL 和 Redis。若部署后页面暂时无法打开，请等待 PostgreSQL、Redis 和 Immich Server Pod 都进入就绪状态后再刷新生成的 URL。

### 首次登录时要求创建账号

这是全新 Immich 部署的正常行为。请在 Getting Started 流程中注册第一个账号，该账号会成为管理员。

### 上传或机器学习任务较慢

请在 Sealos Canvas 中增加 Immich Server 或 ML 服务的 CPU 和内存。大视频上传、缩略图生成、人脸识别和智能搜索索引都会消耗较多资源。

### 获取帮助

- [Immich 文档](https://immich.app/docs/)
- [Immich GitHub Issues](https://github.com/immich-app/immich/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Immich 移动端文档](https://immich.app/docs/features/mobile-app/)
- [Immich 备份与恢复指南](https://immich.app/docs/administration/backup-and-restore/)
- [Immich 发布记录](https://github.com/immich-app/immich/releases)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Immich 本身使用 GNU Affero General Public License v3.0。
