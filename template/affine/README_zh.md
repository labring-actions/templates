# 在 Sealos 上部署和托管 AFFiNE

AFFiNE 是一个本地优先、隐私优先的工作区，可用于笔记、文档、白板和知识管理。此模板会在 Sealos Cloud 上部署 AFFiNE 0.26.6，并自动配置 PostgreSQL、Redis、持久化存储、HTTPS Ingress 和首次管理员初始化流程。

![AFFiNE 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/affine/website-screenshot.webp)

## 关于 AFFiNE 托管

AFFiNE 以 self-hosted all-in-one 模式运行，一个应用工作负载同时提供 Web UI、API、文档协作和后台任务。模板会同时创建托管 PostgreSQL 与 Redis，分别用于工作区元数据、缓存和任务协调，无需手动配置数据库连接。

部署会将 AFFiNE 配置和上传文件保存到持久卷，挂载路径分别为 `/root/.affine/config` 和 `/root/.affine/storage`。Sealos 负责公网 HTTPS 入口、Kubernetes 调度、资源限制和后续 Canvas 运维。

## 常见使用场景

- **个人知识库**：自托管笔记、文档和白板工作区。
- **团队文档协作**：管理项目计划、会议记录和共享知识。
- **白板与视觉化整理**：使用 AFFiNE 的画布式块结构进行图示、头脑风暴和视觉规划。
- **隐私优先工作区**：在自己的 Sealos 部署中保存工作区数据，而不是完全依赖 SaaS 账号。

## AFFiNE 托管依赖

此 Sealos 模板包含运行 AFFiNE 所需的依赖：

- **AFFiNE 应用**：`ghcr.io/toeverything/affine:0.26.6`
- **PostgreSQL**：Kubeblocks 托管的 `postgresql-16.4.0` 集群，并创建专用 `affine` 数据库
- **Redis**：Kubeblocks 托管的 `redis-7.2.7` 集群，用于缓存和后台任务
- **持久化卷**：分别保存 AFFiNE 配置和上传文件
- **Ingress 与 App 入口**：通过 Sealos 暴露 HTTPS 公网访问地址

### 部署依赖链接

- [AFFiNE 官方网站](https://affine.pro/) - 产品介绍和功能信息
- [AFFiNE 自托管文档](https://docs.affine.pro/docs/self-host-affine) - 官方自托管指南
- [AFFiNE GitHub 仓库](https://github.com/toeverything/AFFiNE) - 源码、版本发布和问题追踪
- [Sealos 文档](https://sealos.io/docs) - 平台使用和运维文档

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **AFFiNE StatefulSet**：运行 self-hosted all-in-one AFFiNE 服务，监听 `3010` 端口。
- **迁移 Job**：在应用对外服务前执行 `node ./scripts/self-host-predeploy.js`。
- **PostgreSQL 集群**：在 `affine` 数据库中保存账号、工作区和应用元数据。
- **Redis 集群**：为 AFFiNE 服务提供缓存和队列协调。
- **Service + Ingress + App**：将生成的 HTTPS 域名路由到 AFFiNE 服务。
- **持久化存储**：保留 `/root/.affine/config` 和 `/root/.affine/storage` 数据，Pod 重启后不丢失。

**配置说明：**

- `DATABASE_URL` 由 Kubeblocks PostgreSQL Secret 拼装，并指向 `affine` 数据库。
- `REDIS_SERVER_HOST`、`REDIS_SERVER_USER` 和 `REDIS_SERVER_PASSWORD` 来自 Redis 服务和 Secret。
- `AFFINE_SERVER_EXTERNAL_URL` 设置为 Sealos 生成的 HTTPS 地址，用于生成正确的公网链接。
- `AFFINE_INDEXER_ENABLED=false` 与上游单节点自托管配置保持一致，避免依赖外部搜索索引器。

**资源基线：**

经部署测试，AFFiNE 应用的稳定最小基线为 `500m` CPU 和 `512Mi` 内存；PostgreSQL 为 `500m` CPU 和 `512Mi` 内存；Redis 每个组件为 `500m` CPU 和 `512Mi` 内存。AFFiNE 应用在 256Mi 内存限制下可以启动但冷启动期间出现过一次重启，因此模板使用 512Mi 作为稳定基线。

**许可证信息：**

AFFiNE 采用混合许可证模式。仓库根目录声明大部分源码使用 MIT；后端 Enterprise Edition 部分受 AFFiNE EE 许可证约束，Community Edition 部分使用 MPL-2.0。生产使用前请查看上游仓库中的许可证文件。

## 为什么在 Sealos 上部署 AFFiNE？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一处理部署、存储、网络和应用运维。将 AFFiNE 部署到 Sealos 可以获得：

- **一键部署**：通过一个模板同时启动 AFFiNE、PostgreSQL、Redis、存储和 HTTPS 路由。
- **托管 Kubernetes 运行时**：无需手写清单或直接维护集群底层资源，也能获得 Kubernetes 的可靠性。
- **默认持久化数据**：AFFiNE 配置和上传的工作区文件会写入 PVC。
- **易于定制**：可在 Canvas 资源卡片或 AI 对话中调整资源、环境变量和存储。
- **即时公网访问**：部署完成后自动获得 HTTPS 访问地址。
- **按量使用资源**：从已测试的资源基线开始，只在业务需要时扩展 CPU、内存和存储。

在 Sealos 上部署 AFFiNE，可以在掌控工作区数据的同时减少基础设施维护成本。

## 部署指南

1. 打开 [AFFiNE 模板](https://sealos.io/products/app-store/affine)，点击 **Deploy Now**。
2. 在弹窗中检查生成的应用名称和域名。保留默认配置即可部署可用实例。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas；后续变更可在对话框中描述需求让 AI 应用，或点击相关资源卡片调整配置。
4. 从应用卡片打开生成的 AFFiNE 访问地址。
5. 首次访问时，AFFiNE 会跳转到 `/admin/setup`。填写姓名、邮箱和密码，创建第一个管理员账号。
6. 初始化完成后，点击 **Open AFFiNE** 或返回应用访问地址。之后使用刚创建的管理员邮箱和密码登录。

## 首次登录与注册

AFFiNE 自托管模式必须先创建初始管理员，工作区才能正常使用。

1. 打开系统生成的 AFFiNE 地址。
2. 如果实例尚未初始化，会自动跳转到 `https://<your-affine-domain>/admin/setup`。
3. 点击 **Continue**，创建第一个管理员账号。
4. 后续使用同一个邮箱和密码登录 AFFiNE，也可以通过 `/admin` 进入管理后台。

请使用强密码。AFFiNE 要求密码长度为 8-32 个字符，建议至少包含两类字符，例如大写字母、小写字母、数字或符号。

## 配置

部署完成后，可通过以下方式配置 AFFiNE：

- **AFFiNE 管理后台**：在生成域名后追加 `/admin`，管理自托管设置。
- **Canvas AI 对话**：描述资源调整或环境变量变更，由 AI 应用修改。
- **资源卡片**：编辑 AFFiNE StatefulSet、PostgreSQL 集群、Redis 集群、Service、Ingress 或 PVC。
- **AFFiNE 界面**：在应用内管理工作区、成员和文档。

此模板默认不配置 SMTP 和 OAuth Provider。如需邮件邀请、密码重置或第三方登录，请按 AFFiNE 官方文档在管理后台或环境变量中补充配置。

## 扩缩容

大多数小型 AFFiNE 工作区建议保持单副本，并优先纵向扩容：

1. 在 Canvas 打开该部署。
2. 选择 AFFiNE StatefulSet 资源卡片。
3. 如果导入、工作区规模或并发用户增加，可提升 CPU 或内存。
4. 当数据规模增长时，通过 PostgreSQL、Redis 和 PVC 资源卡片扩展容量。

除非已确认 AFFiNE 自托管多副本行为，否则建议保持应用单副本运行。

## 故障排查

### 常见问题

**问题：应用跳转到 `/admin/setup`**
- 原因：AFFiNE 实例尚未初始化。
- 处理：在 setup 页面创建第一个管理员账号，然后返回应用地址。

**问题：部署后页面没有立即就绪**
- 原因：PostgreSQL、Redis、数据库初始化 Job 和迁移 Job 仍在启动。
- 处理：等待几分钟，并在 Canvas 中确认 AFFiNE StatefulSet、PostgreSQL 集群、Redis 集群和迁移 Job 均为健康状态。

**问题：邮件邀请或密码重置邮件无法发送**
- 原因：模板默认未配置 SMTP。
- 处理：在依赖邮件流程前，按照 AFFiNE 自托管文档配置 SMTP。

**问题：冷启动时 Pod 重启**
- 原因：AFFiNE 启动和后台服务所需内存高于当前限制。
- 处理：保持默认 512Mi 应用内存限制；大型工作区可在 Canvas 中继续提高。

### 获取帮助

- [AFFiNE 自托管文档](https://docs.affine.pro/docs/self-host-affine)
- [AFFiNE GitHub Issues](https://github.com/toeverything/AFFiNE/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [AFFiNE 文档](https://docs.affine.pro/)
- [AFFiNE 社区](https://community.affine.pro/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证。AFFiNE 本身使用其上游仓库许可证文件中描述的混合许可证模式。
