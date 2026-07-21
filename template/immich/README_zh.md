# 在 Sealos 上部署 Immich

[Immich](https://immich.app/) 是一款自托管照片和视频管理平台，提供移动端备份、相册、共享、地图、人脸识别和语义搜索。此模板会部署 Immich v3.0.3、PostgreSQL、Redis、持久化媒体存储、HTTPS 入口和可选机器学习服务。

![Immich 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/immich/website-screenshot.webp)

## 关于 Immich

Immich 让应用和媒体库由你掌控。Web 界面和官方移动端 App 共用一个 HTTPS 入口，PostgreSQL 保存元数据，Redis 负责协调后台任务。

此模板遵循上游容器拓扑：

- **Immich Server v3.0.3** 提供 Web 界面和 API，并运行媒体处理任务。
- **Immich Machine Learning v3.0.3** 为可选组件，提供智能搜索、OCR、目标检测和人脸识别。
- **PostgreSQL 16.4** 保存用户、媒体、相册、任务和向量索引。
- **Redis 7.2.7 与 Sentinel** 协调任务队列和缓存数据。
- **持久化卷** 保存 `/data` 中的媒体文件、机器学习模型缓存和数据库数据。

Immich 社区版使用文件系统保存媒体。备份时需要同时保护 `/data` 卷和 PostgreSQL。

## 在 Sealos 上部署 Immich 的优势

- 通过一个模板创建完整应用、数据库、缓存、存储和 HTTPS 入口。
- 上传文件、模型和数据库数据可在重启后持续保留。
- 通过一个部署参数控制机器学习服务。
- 后续可在 Sealos 资源视图中调整计算和存储规格。

## 部署指南

1. 打开 [Immich 模板](https://sealos.io/products/app-store/immich)，点击 **Deploy Now**。
2. 选择 `enable_machine_learning`：
   - `true` 会启用智能搜索、OCR、人脸识别和目标检测。
   - `false` 会部署资源占用更低的核心照片和视频管理服务。
3. 开始部署，等待 PostgreSQL、Redis、Immich Server 和可选 ML 服务完成初始化。首次启动通常需要数分钟。
4. 从 Sealos 应用入口打开生成的 Immich HTTPS 地址。

## 首次注册和登录

全新 Immich 部署会显示管理员注册页面。

1. 点击 **Get Started**。
2. 填写管理员邮箱、密码、确认密码和显示名称。
3. 点击 **Sign Up**。首个注册账号会成为管理员。
4. 使用同一邮箱和密码登录。
5. 完成新手设置，然后进入 **Photos** 或 **Albums** 开始使用媒体库。

Immich 会由你创建初始凭据。请使用密码管理器保存管理员账号。管理员可在 **Administration > Users** 中创建更多用户。

## 移动端 App 设置

安装官方 Immich 移动端 App，将 Sealos 生成的 HTTPS 地址填入服务器地址。使用 Immich 账号登录，然后在 App 中配置移动端备份目录。

## 资源与存储基线

模板使用已经完成全新部署、上传、缩略图、下载、相册和机器学习工作流验证的最小资源档位：

| 组件 | CPU 上限 | 内存上限 | 初始存储 |
| --- | ---: | ---: | ---: |
| Immich Server | 500m | 2 GiB | 1 GiB 媒体卷 |
| PostgreSQL | 500m | 2 GiB | 1 GiB 数据卷 |
| Redis | 500m | 512 MiB | 1 GiB 数据卷 |
| Redis Sentinel | 500m | 512 MiB | 1 GiB 数据卷 |
| Machine Learning | 500m | 4 GiB | 1 GiB 模型缓存 |

Server 和 PostgreSQL 的 2 GiB 内存上限覆盖首次启动、数据库迁移和媒体工作流峰值。ML 的 4 GiB 内存上限为 OCR、人脸识别和视觉搜索模型同时加载保留运行余量。导入大型媒体库前请扩充存储，大视频和并发机器学习任务也需要更多内存。

## 配置

- 在 Immich 的 **Administration** 中管理用户、任务、图库、存储模板和服务设置。
- 在 Sealos 资源视图中调整 Immich、PostgreSQL、Redis 和 ML 工作负载规格。
- 调整工作负载时保持媒体目录挂载到 `/data`。
- 保持应用通过 Sealos Secret 使用自动生成的数据库和 Redis 凭据。
- 默认 Ingress 接受最大 32 MiB 的上传。上传更大的媒体文件前，请提高已部署 Ingress 的 `nginx.ingress.kubernetes.io/proxy-body-size`。

## 备份与升级

请协调备份 Immich `/data` 卷和 PostgreSQL 数据库。ML 缓存和 Redis 数据可以重新生成，媒体文件和 PostgreSQL 元数据共同组成需要长期保护的媒体库。升级前请阅读 [Immich 备份与恢复指南](https://immich.app/docs/administration/backup-and-restore/)。

## 故障排查

### 页面仍在启动

等待 PostgreSQL、Redis 和 Immich Pod 进入就绪状态。全新数据库初始化和首次模型下载通常需要数分钟。

### 智能搜索或人脸识别无法使用

确认 `enable_machine_learning` 设置为 `true`，并检查 ML Pod 已经就绪。首次请求会将模型下载到持久化缓存。

### 大文件上传失败

提高已部署 Ingress 的 `nginx.ingress.kubernetes.io/proxy-body-size`，检查 `/data` 卷的可用空间，并为大视频或并发上传提高 Immich Server 资源。

## 相关资源

- [Immich 文档](https://immich.app/docs/)
- [安装后配置指南](https://immich.app/docs/install/post-install/)
- [移动端 App 指南](https://immich.app/docs/features/mobile-app/)
- [Immich GitHub 仓库](https://github.com/immich-app/immich)

## 许可证

Immich 使用 GNU Affero General Public License v3.0。此 Sealos 模板遵循模板仓库许可证。
