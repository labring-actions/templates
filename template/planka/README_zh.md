# 在 Sealos 上部署和托管 PLANKA

PLANKA 是一款实时看板项目管理工具，适合团队和个人管理任务、项目与协作流程。此模板会在 Sealos Cloud 上部署 PLANKA、PostgreSQL 数据库、持久化应用数据和公网 HTTPS 入口。

## 关于在 Sealos 上托管 PLANKA

PLANKA 支持通过看板、列表、卡片、标签、评论、附件和实时协作来组织项目。它适合替代轻量级 Trello 风格工作流，同时保留自托管部署方式。

此 Sealos 模板会自动创建 PLANKA Web 应用、KubeBlocks PostgreSQL 集群、数据库初始化 Job、`/app/data` 持久化存储、Service、Ingress 和 Sealos App 入口。模板还会配置 `BASE_URL`、`DATABASE_URL`、代理支持、健康检查和初始管理员账号。

PLANKA 首次访问需要管理员账号。部署时请配置初始管理员邮箱、用户名、密码和显示名称。登录后，可以在 PLANKA 管理界面中管理用户和工作区设置。

## 常见使用场景

- **团队项目跟踪**：用共享看板管理多个项目的任务流转。
- **产品路线图**：跟踪功能、里程碑、标签和负责人。
- **内容编辑流程**：让文章、问题或设计任务在不同审核阶段中流转。
- **客户项目空间**：按项目组织交付物、讨论和附件。
- **个人任务管理**：创建私有看板，用于个人计划和跟进。

## PLANKA 托管依赖

此 Sealos 模板包含运行所需的全部依赖：

- **PLANKA 2.1.1**：Web 应用镜像 `ghcr.io/plankanban/planka:2.1.1`。
- **PostgreSQL 16.4.0**：由 KubeBlocks 管理的 PostgreSQL 集群。
- **持久化存储**：PLANKA 应用数据 1 GiB，PostgreSQL 数据 1 GiB。
- **Sealos 网络能力**：Service、Ingress、自动公网 URL 和 TLS 终止。

### 部署依赖

- [PLANKA 官方文档](https://docs.planka.cloud/docs/welcome/) - 官方文档。
- [生产版 Docker 部署指南](https://docs.planka.cloud/docs/installation/docker/production-version/) - 官方生产部署参考。
- [配置文档](https://docs.planka.cloud/docs/category/configuration/) - PLANKA 配置选项。
- [PLANKA GitHub 仓库](https://github.com/plankanban/planka) - 源码与版本发布。

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **PLANKA StatefulSet**：运行 `ghcr.io/plankanban/planka:2.1.1`，暴露 `1337` 端口，将上传文件和运行时数据保存在 `/app/data`，并在 PostgreSQL 可用后启动。
- **PostgreSQL Cluster**：使用 Sealos KubeBlocks PostgreSQL 16.4.0 模板，单副本运行并持久化数据库数据。
- **PostgreSQL Init Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `planka` 数据库。
- **Service 和 Ingress**：通过 Sealos 生成的公网 HTTPS 地址暴露 PLANKA。
- **Sealos App Resource**：在 Sealos 仪表盘中创建可点击的 PLANKA 入口。

**配置：**

- `BASE_URL` 设置为 Sealos 生成的公网 URL。
- `DATABASE_URL` 由 KubeBlocks PostgreSQL 连接 Secret 拼接生成。
- `SECRET_KEY` 由模板自动生成。
- `TRUST_PROXY` 已开启，用于适配 Sealos Ingress TLS 终止。
- `DEFAULT_ADMIN_EMAIL`、`DEFAULT_ADMIN_USERNAME`、`DEFAULT_ADMIN_PASSWORD` 和 `DEFAULT_ADMIN_NAME` 来自部署输入，用于首次启动时创建初始管理员账号。

**资源配置：**

- PLANKA 应用容器：`100m` CPU、`128Mi` 内存。
- PostgreSQL KubeBlocks 组件：`500m` CPU、`512Mi` 内存。
- PLANKA 应用存储：`1Gi`。
- PostgreSQL 数据存储：`1Gi`。

该应用资源配置已通过全新 Sealos 部署、登录冒烟测试、仪表盘访问和基础界面交互验证。

**许可证信息：**

PLANKA 使用 PLANKA Fair Use License，并提供 Pro 和 Enterprise 授权选项。此 Sealos 模板作为 Sealos templates 仓库的一部分提供。

## 为什么在 Sealos 上部署 PLANKA？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、网络、存储和数据库管理。在 Sealos 上部署 PLANKA 可以获得：

- **一键部署**：通过一个模板同时部署 PLANKA 应用和 PostgreSQL 数据库。
- **易于定制**：在部署弹窗中配置管理员凭据和资源设置。
- **内置持久化存储**：PLANKA 上传文件、运行时数据和 PostgreSQL 数据可跨重启保留。
- **即时公网访问**：部署完成后自动获得 HTTPS 公网地址。
- **Kubernetes 原生运行时**：使用健康检查、服务发现和托管数据库资源运行 PLANKA。

## 部署指南

1. 打开 [PLANKA 模板](https://sealos.io/products/app-store/planka)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **Initial administrator email address**：首次管理员登录邮箱。
   - **Initial administrator username**：首次管理员用户名。
   - **Initial administrator password**：首次管理员密码。
   - **Initial administrator display name**：PLANKA 中显示的管理员名称。
3. 等待部署完成。全新部署通常需要几分钟，因为 PostgreSQL 必须先就绪，PLANKA 才会启动。
4. 通过部署后提供的 URL 访问应用：
   - **PLANKA 界面**：打开 Sealos 生成的公网 URL，使用第 2 步配置的管理员邮箱或用户名及密码登录。
5. 如果首次登录时出现终端用户条款弹窗，请滚动阅读条款，勾选确认框，然后继续进入仪表盘。
6. 在仪表盘中创建第一个项目，然后按需添加看板、列表、卡片、标签和用户。

## 配置

部署后，可以通过以下方式配置 PLANKA：

- **PLANKA 管理界面**：使用初始管理员账号登录，打开用户或系统管理菜单。
- **Sealos AI 对话框**：描述需要调整的资源或配置，让 Sealos 应用修改。
- **资源卡片**：在 Sealos Canvas 中点击 StatefulSet、数据库、存储、Service 或 Ingress 卡片，查看或调整运行时设置。

此模板未开启公开自助注册。请先使用配置的管理员账号登录，再在 PLANKA 中管理用户。

## 扩缩容

调整资源时：

1. 打开该部署的 Canvas。
2. 点击 PLANKA StatefulSet 或 PostgreSQL 资源卡片。
3. 根据负载调整 CPU、内存或存储。
4. 应用修改，并等待部署重新就绪。

如果团队规模较大，建议先提升 PLANKA 内存，再增加访问量或上传文件量。PostgreSQL 资源应根据看板、卡片、附件和活动历史的规模同步调整。

## 故障排查

### 使用配置的管理员账号无法登录

- 原因：部署时输入的管理员凭据与当前使用的不一致，或已有数据库中已经存在用户。
- 解决：检查部署时配置的值。全新模板部署中，请使用配置的初始管理员邮箱或用户名，以及对应密码登录。

### PLANKA 需要几分钟才可访问

- 原因：PLANKA 会等待 KubeBlocks PostgreSQL 服务和数据库初始化 Job 完成后再启动。
- 解决：在 Sealos Canvas 中等待 PostgreSQL 集群和 PLANKA StatefulSet 都变为就绪。

### 公网 URL 可以打开，但登录或跳转异常

- 原因：PLANKA 要求 `BASE_URL` 与公网入口一致。
- 解决：此模板会根据 Sealos 生成的访问域名设置 `BASE_URL`。如果自定义域名，请同步更新 `BASE_URL`。

### 获取帮助

- [PLANKA 官方文档](https://docs.planka.cloud/docs/welcome/)
- [PLANKA GitHub Issues](https://github.com/plankanban/planka/issues)
- [PLANKA 社区 Discord](https://discord.gg/WqqYNd7Jvt)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [PLANKA API 参考](https://plankanban.github.io/planka/swagger-ui/)
- [PLANKA 配置文档](https://docs.planka.cloud/docs/category/configuration/)
- [PLANKA 生产版 Docker 部署指南](https://docs.planka.cloud/docs/installation/docker/production-version/)

## 许可证

此 Sealos 模板作为 Sealos templates 仓库的一部分提供。PLANKA 本身使用 PLANKA Fair Use License，并提供 Pro 和 Enterprise 授权选项。
