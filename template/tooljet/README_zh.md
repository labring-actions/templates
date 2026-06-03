# 在 Sealos 上部署和托管 ToolJet

ToolJet 是一个开源低代码平台，可用于构建内部工具、仪表盘、业务应用和工作流界面。此模板会在 Sealos Cloud 上部署 ToolJet CE，并同时创建 PostgreSQL、Redis、PostgREST、数据库初始化任务和公网 HTTPS 访问入口。

## 关于托管 ToolJet

ToolJet 是一个基于 Web 的应用构建平台。团队可以连接数据库和 API，在浏览器中设计内部管理后台、构建仪表盘，并搭建日常运营工作流。

此 Sealos 模板会为单实例 ToolJet 部署创建所需服务。PostgreSQL 用于存储 ToolJet 元数据和 ToolJet 数据库，Redis 支持实时与后台能力，PostgREST 提供 ToolJet 数据库功能所需的内部 REST 接口。

模板还会在 Web 应用启动前运行初始化和迁移任务，避免首次启动时出现数据库表缺失问题，并确保公网地址可访问时已经可以进入初始化页面。

## 常见使用场景

- **内部管理后台**：为运营、客服、财务或业务团队构建 CRUD 界面。
- **仪表盘和报表**：连接数据源，为内部用户创建轻量仪表盘。
- **工作流工具**：构建审批流、工单分流工具和运营流程。
- **数据库驱动应用**：结合 PostgreSQL、REST API 和其他数据源构建内部应用。
- **业务应用原型**：在投入定制开发前，快速验证内部工具想法。

## ToolJet 托管依赖

此 Sealos 模板包含所需运行时和服务：

- **ToolJet CE**：`tooljet/tooljet-ce:v3.20.170-lts`
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4.0，1 Gi 存储
- **Redis**：KubeBlocks Redis + Sentinel，共 2 Gi 存储
- **PostgREST**：PostgREST v12.0.2，用于 ToolJet 数据库 API
- **初始化任务**：创建 PostgreSQL 数据库并执行 ToolJet 数据库迁移

### 部署依赖

- [ToolJet 文档](https://docs.tooljet.ai/) - ToolJet 官方文档
- [ToolJet GitHub 仓库](https://github.com/ToolJet/ToolJet) - 源码和版本发布
- [Sealos 文档](https://sealos.io/docs) - Sealos 部署与运维指南

## 实现细节

### 架构组件

此模板会部署以下组件：

- **ToolJet Web 应用**：在 `3000` 端口提供前端和后端 API。
- **PostgreSQL 集群**：存储 `tooljet_production` 和 `tooljet_db` 两个数据库。
- **Redis 集群**：提供 ToolJet 使用的缓存和实时协同能力。
- **PostgREST 部署**：为 ToolJet DB 功能提供内部 REST 服务。
- **数据库初始化任务**：在迁移前创建两个必需的 PostgreSQL 数据库。
- **迁移任务**：执行 ToolJet 生产数据库迁移和数据迁移。
- **Ingress 和 Service**：通过 Sealos 托管的 HTTPS 域名暴露 ToolJet。

### 资源配置

此模板基于 Sealos 实际部署测试调优，适合最小可用的单实例部署：

- ToolJet 应用：`500m` CPU，`1536Mi` 内存
- 迁移任务：`1` CPU，`2Gi` 内存
- PostgreSQL：`200m` CPU，`256Mi` 内存，`1Gi` 存储
- Redis：两个 `200m` CPU / `256Mi` 内存组件，各 `1Gi` 存储
- PostgREST：`200m` CPU，`256Mi` 内存

ToolJet 运行时会打开多个数据库连接。模板会让主应用的主要 ORM 连接使用 PostgreSQL 连接池端口，同时保留 ToolJet DB 连接使用直连端口，因为 ToolJet 会为 ToolJet DB 连接传入 `statement_timeout` 启动参数。

### 配置说明

模板会自动生成 ToolJet 必需的密钥：

- `LOCKBOX_MASTER_KEY`
- `SECRET_KEY_BASE`
- `PGRST_JWT_SECRET`

`admin_email` 输入项会作为默认发件人邮箱，用于首次部署说明。ToolJet 仍会在浏览器中要求你创建第一个管理员账号。

### 许可证信息

ToolJet 使用 GNU Affero General Public License v3.0（AGPL-3.0）许可证。此 Sealos 模板遵循模板仓库许可证。

## 为什么在 Sealos 上部署 ToolJet？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一管理应用部署、网络、存储和运维。在 Sealos 上部署 ToolJet 可以获得：

- **一键部署**：从一个模板同时部署 ToolJet 和所有依赖服务。
- **自动公网访问**：无需手动配置 Ingress，即可获得 HTTPS 地址。
- **持久化存储**：PostgreSQL 和 Redis 数据会在重启后保留。
- **集成运维能力**：可在 Sealos Canvas 中调整资源并查看日志。
- **降低 Kubernetes 使用门槛**：无需手写清单即可在 Kubernetes 上运行 ToolJet。

## 部署指南

1. 打开 [ToolJet 模板](https://sealos.io/products/app-store/tooljet)，点击 **Deploy Now**。
2. 检查 `admin_email` 参数。测试时可保留默认值，生产使用时建议填写自己的邮箱。
3. 点击 **Deploy**，等待 PostgreSQL、Redis、PostgREST、迁移任务和 ToolJet 应用就绪。首次部署需要执行数据库迁移，通常需要数分钟。
4. 打开 Sealos 生成的应用地址，例如 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。

## 首次初始化和登录

ToolJet 需要在浏览器中完成首次初始化：

1. 打开 Sealos 应用地址。
2. 在 **Set up your admin account** 页面输入姓名、工作邮箱和密码，然后点击 **Sign up**。
3. 在 **Set up your workspace** 页面保留建议的工作区名称，或输入自定义名称，然后点击 **Continue**。
4. 初始化完成后会进入 ToolJet 工作区仪表盘。你可以点击 **Create an app** 或 **Create new application** 开始构建应用。
5. 后续访问时，在同一应用地址打开 `/login`，使用初始化时创建的邮箱和密码登录。

模板默认设置 `SMTP_DISABLED=true`，因此首次注册不需要邮箱验证。如果需要邀请邮件、密码重置邮件或生产邮件投递，请在部署后配置 SMTP 相关环境变量。

## 配置

部署后可以通过以下方式配置 ToolJet：

- **ToolJet 工作区设置**：管理用户、应用、数据源和工作区偏好。
- **Sealos Canvas**：查看 ToolJet、PostgreSQL、Redis 和 PostgREST 的 Pod、日志和资源。
- **资源卡片**：当工作区规模增长时，调整 CPU、内存或存储。

## 扩容

如需扩容或调优：

1. 打开 ToolJet 部署所在的 Canvas。
2. 点击 ToolJet 应用资源卡片，调整 CPU 或内存。
3. 点击 PostgreSQL 或 Redis 资源卡片，调整数据库资源或存储。
4. 应用变更并等待相关资源重启完成。

如果用于生产或有较多用户、复杂仪表盘、大量数据源，建议提前增加 PostgreSQL 和 ToolJet 资源。

## 故障排查

### 初始化页面没有出现

等待迁移任务完成，并确认 ToolJet Deployment 已就绪。模板会在必需数据库表存在后才启动 Web 应用。

### 无法创建应用或数据库请求失败

在 Sealos Canvas 中检查 PostgreSQL 和 ToolJet 日志。ToolJet 需要 PostgreSQL、Redis 和 PostgREST 都正常运行。工作区规模增大后，请增加 PostgreSQL 和 ToolJet 资源。

### 邀请邮件或密码重置邮件没有发送

模板默认禁用 SMTP。使用邀请或密码重置邮件前，请先配置 ToolJet 的 SMTP 相关环境变量。

### 获取帮助

- [ToolJet 文档](https://docs.tooljet.ai/)
- [ToolJet GitHub Issues](https://github.com/ToolJet/ToolJet/issues)
- [Sealos 文档](https://sealos.io/docs)

## 更多资源

- [ToolJet 官网](https://www.tooljet.ai/)
- [ToolJet 文档](https://docs.tooljet.ai/)
- [ToolJet GitHub 仓库](https://github.com/ToolJet/ToolJet)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循模板仓库许可证。ToolJet 本身使用 AGPL-3.0 许可证。
