# 在 Sealos 上部署和托管 FileCodeBox

FileCodeBox 是一款基于 FastAPI 和 Vue 构建的轻量级匿名文本与文件分享服务。此模板会在 Sealos Cloud 上部署 FileCodeBox，默认使用持久化本地存储，并支持可选的 Sealos 对象存储开关。

![FileCodeBox 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/filecodebox/website-screenshot.webp)

## 关于托管 FileCodeBox

FileCodeBox 支持用户分享文本片段或文件，并生成提取码供接收者取用内容。公开分享流程默认允许游客上传，`/admin` 管理面板则提供仪表盘指标、文件管理、存储设置和安全控制。

此 Sealos 模板会将 FileCodeBox 作为单个 StatefulSet 运行，并把持久化卷挂载到 `/app/data`。该卷用于保存 SQLite 数据库、本地上传文件、启动锁文件和运行时配置，因此分享内容和管理设置会在重启后继续保留。

模板还提供可选的 `enable_s3_storage` 开关。启用后，Sealos 会创建 `ObjectStorageBucket`，模板会按 FileCodeBox 官方 S3 兼容配置初始化应用，并通过服务端代理下载访问私有存储桶中的文件。

## 常见使用场景

- **临时文件传输**：通过短提取码在设备或团队之间快速分享文件。
- **文本与代码片段分享**：分享笔记、日志、配置片段和短文档，无需创建用户账号。
- **私有文件投递箱**：为团队或实验室部署轻量内部文件交换服务。
- **API 驱动的传输流程**：把 REST API 接入脚本，自动上传文本或文件并分发提取码。
- **S3 后端存储**：将分享文件存入 Sealos 管理的 S3 兼容存储桶，同时在 SQLite 中保留 FileCodeBox 元数据。

## FileCodeBox 托管依赖

此 Sealos 模板包含 FileCodeBox 容器镜像、StatefulSet、持久化卷、Kubernetes Service、Ingress 和 Sealos App 入口。选择对象存储时，模板还会创建 Sealos `ObjectStorageBucket`，并把生成的 S3 凭据注入应用。

### 部署依赖

- [FileCodeBox 文档](https://fcb-docs.aiuo.net/en/) - 官方英文文档
- [FileCodeBox GitHub 仓库](https://github.com/vastsa/FileCodeBox) - 源码、Dockerfile 和问题跟踪
- [存储配置](https://fcb-docs.aiuo.net/en/guide/storage.html) - 官方存储后端指南
- [API 文档](https://fcb-docs.aiuo.net/en/api/) - REST API 参考

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **FileCodeBox Web 服务**：运行 `lanol/filecodebox`，监听 `12345` 端口，提供 Web UI、分享 API、管理 API 和后台清理任务。
- **持久化存储**：挂载到 `/app/data` 的 `1Gi` 卷，用于保存 SQLite 数据库和本地文件。
- **可选对象存储**：Sealos `ObjectStorageBucket` 通过 FileCodeBox 官方 S3 兼容存储设置保存上传文件。
- **Ingress 与 App 入口**：Sealos 通过 HTTPS URL 暴露 FileCodeBox，并创建仪表盘直达入口。

**配置：**

模板需要填写：

- `admin_password`：FileCodeBox `/admin` 管理面板的初始密码。
- `enable_s3_storage`：启用 Sealos 对象存储作为 FileCodeBox 的 S3 兼容文件后端。

首次启动时，容器会把所选管理员密码和存储模式写入 FileCodeBox 的 SQLite settings 行。之后在 FileCodeBox 管理面板中完成的修改会保存在 `/app/data/filecodebox.db`。

**许可证信息：**

FileCodeBox 使用 GNU Lesser General Public License v3.0。此 Sealos 模板是 FileCodeBox 的部署配置，不改变上游应用许可证。

## 为什么在 Sealos 上部署 FileCodeBox？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖从部署到运维的应用生命周期。在 Sealos 上部署 FileCodeBox 可以获得：

- **一键部署**：通过一个模板部署 FileCodeBox、存储、网络和 App 入口。
- **内置持久化存储**：SQLite 数据和上传文件会在重启后保留。
- **可选对象存储**：可在同一个部署表单中创建私有 Sealos 存储桶。
- **即时公网访问**：每次部署都会获得用于分享和管理的 HTTPS URL。
- **易于自定义**：可通过 Sealos Canvas 和 AI 对话调整资源、存储和环境变量。
- **按量使用资源**：轻量分享场景可从紧凑资源配置起步。

在 Sealos 上部署 FileCodeBox，可以用托管 Kubernetes 基础能力运行一个小而实用的自托管文件分享服务。

## 部署指南

1. 打开 [FileCodeBox 模板](https://sealos.io/products/app-store/filecodebox)，点击 **Deploy Now**。
2. 输入用于 `/admin` 管理面板的 `admin_password`。
3. 保持 `enable_s3_storage` 关闭时，上传文件会保存在挂载到 `/app/data` 的持久化卷中；启用它则会创建私有 Sealos 对象存储桶，并配置 FileCodeBox 使用 S3 兼容存储。
4. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话框中描述需求，或点击对应资源卡片调整配置。
5. 从 App 入口打开生成的 FileCodeBox URL。
6. 在首页分享文本或文件，并复制生成的提取码。
7. 打开 `https://[your-app-url]/admin`，使用配置的 `admin_password` 登录，查看仪表盘、管理文件并调整 FileCodeBox 设置。

## 配置

部署后，你可以通过以下方式配置 FileCodeBox：

- **FileCodeBox 管理面板**：访问 `/admin`，使用配置的密码登录，然后更新站点设置、上传限制、存储设置、主题和安全选项。
- **Sealos AI 对话**：描述环境变量、资源或存储调整需求，让 AI 协助修改。
- **资源卡片**：在 Canvas 中点击 StatefulSet、Ingress、Service、App、持久化卷或对象存储卡片，查看并调整配置。

用于公开服务时，建议部署后立即检查上传大小、上传频率限制、过期模式和管理员密码。FileCodeBox 会把管理配置保存在 SQLite 中，因此配置会随 `/app/data` 卷持久化。

## 扩展

在 Sealos 上扩展 FileCodeBox：

1. 打开 FileCodeBox 部署对应的 Canvas。
2. 点击 FileCodeBox StatefulSet 资源卡片。
3. 当文件流量、并发上传或 API 使用量增长时，提高 CPU 或内存。
4. 应用变更并等待 Pod 重新就绪。

默认模板使用一个 worker 和适合轻量分享负载的紧凑资源配置。对于更大的文件或持续流量，可提高资源限制，并考虑使用对象存储后端。

## 故障排查

### 管理员登录失败

请使用部署时输入的 `admin_password`，并直接访问 `/admin`。在管理面板中修改密码后，后续登录使用新密码。

### 上传文件占满持久化卷

可在管理面板中检查过期文件，并从 Sealos 资源卡片扩容 StatefulSet 存储卷。文件量较大时，对象存储更适合作为后端。

### S3 后端下载失败

打开 `/admin`，检查 `file_storage=s3`，确认存储桶配置，并为私有 Sealos 对象存储桶保持服务端代理下载。

### 获取帮助

- [FileCodeBox 文档](https://fcb-docs.aiuo.net/en/)
- [FileCodeBox GitHub Issues](https://github.com/vastsa/FileCodeBox/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [FileCodeBox API 参考](https://fcb-docs.aiuo.net/en/api/)
- [FileCodeBox 存储指南](https://fcb-docs.aiuo.net/en/guide/storage.html)
- [FileCodeBox Docker 镜像](https://hub.docker.com/r/lanol/filecodebox)

## 许可证

此 Sealos 模板遵循仓库中的模板许可证。FileCodeBox 本身使用 GNU Lesser General Public License v3.0。
