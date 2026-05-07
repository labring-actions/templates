# 在 Sealos 上部署和托管 Directus

Directus 是一个开源数据平台和 Headless CMS，可用于管理 SQL 数据库，并提供 API、认证、文件管理和管理后台。本模板会在 Sealos Cloud 上部署 Directus，并自动配置 PostgreSQL、Redis、持久化存储卷，以及可选的 S3 兼容对象存储。

## 关于 Directus 托管

Directus 基于 SQL 数据库提供无代码管理后台、REST API、GraphQL API、认证、权限、文件管理和自动化能力。它常用于把已有或新建数据库快速变成一套可管理的内容与数据平台，而不必从零开发后端系统。

Sealos 模板会以 Kubernetes StatefulSet 的形式运行 Directus，并使用 PostgreSQL 存储应用数据，使用 Redis 处理缓存、限流和运行时协同。模板还会为本地上传文件和扩展创建持久化存储卷，也可以选择为上传文件启用 S3 兼容对象存储。

Sealos 会负责公网 HTTPS 访问、服务发现、持久化存储、资源配置和数据库创建，让你无需手写 Kubernetes 配置，也能完成 Directus 部署。

## 常见使用场景

- **Headless CMS**：管理内容模型、媒体文件、用户、角色、权限和 API 访问。
- **数据库管理后台**：为基于 PostgreSQL 的内部工具提供清晰易用的管理界面。
- **API 后端**：基于受控 SQL schema 暴露带认证和权限控制的 REST 与 GraphQL API。
- **低代码数据平台**：围绕结构化业务数据构建数据流程、仪表盘和运营工具。
- **媒体与文件管理**：根据部署需求，将上传文件保存在本地持久卷或 S3 兼容对象存储中。

## Directus 托管依赖

本 Sealos 模板包含 Directus 运行所需的依赖：

- Directus `11.17.4`
- 通过 KubeBlocks 部署的 PostgreSQL `16.4.0`
- 通过 KubeBlocks 部署的 Redis `7.2.7`
- 用于上传文件和扩展的持久化存储
- 用于上传文件的可选 S3 兼容对象存储
- HTTPS Ingress 和 Sealos App 入口

### 部署依赖

- [Directus 文档](https://directus.io/docs/) - Directus 官方文档
- [Directus 自托管指南](https://directus.io/docs/self-hosting/overview) - 运行时与部署参考
- [Directus GitHub 仓库](https://github.com/directus/directus) - 源码、版本发布和问题追踪
- [Directus 社区](https://community.directus.io/) - 社区支持与讨论

## 实现细节

**架构组件：**

本模板会部署以下资源：

- **Directus StatefulSet**：使用 `directus/directus:11.17.4` 镜像运行 Directus Web 应用和 API，监听 `8055` 端口。
- **PostgreSQL Cluster**：存储 Directus 系统表、用户、角色、权限、集合和应用数据。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `directus` 数据库。
- **Redis Cluster**：为 Directus 提供缓存、限流存储和运行时协同能力。
- **持久化上传卷**：未启用对象存储时，将本地上传文件保存在 `/directus/uploads`。
- **持久化扩展卷**：将 Directus 扩展保存在 `/directus/extensions`。
- **可选 ObjectStorageBucket**：启用 `use_object_storage` 时创建 S3 兼容存储桶，并通过 `sealos` 存储位置配置 Directus。
- **Service 和 Ingress**：通过 Sealos 管理的公网 HTTPS 地址暴露 Directus。
- **Sealos App Resource**：把部署后的 Directus 实例加入 Sealos 应用界面。

**配置：**

模板会要求填写初始管理员邮箱和密码。Directus 的 `SECRET`、公网主机名和应用名称会自动生成。

Directus 通过 KubeBlocks 连接密钥访问 PostgreSQL，并通过 Sealos 集群内 DNS 访问 Redis。启动容器会先等待 PostgreSQL 和 Redis 就绪，再启动 Directus 主容器。

文件存储支持两种模式：

- **本地存储**：默认模式。Directus 将上传文件保存在持久化的 `/directus/uploads` 卷中。
- **对象存储**：可选模式。启用 `use_object_storage` 后，模板会创建 S3 兼容存储桶，并通过 `STORAGE_SEALOS_*` 环境变量配置 Directus。

**默认资源：**

模板为 Directus、初始化容器和数据库组件设置了保守的默认资源：

- CPU limit：`200m`
- Memory limit：`256Mi`
- CPU request：`20m`
- Memory request：`25Mi`

**健康检查：**

Directus 使用 `/server/health` 作为启动、就绪和存活探针。这样可以确保数据库、Redis 和文件存储都可用之后，应用才会对外提供服务。

**许可信息：**

Directus 采用 Business Source License 1.1 分发，并会在对应变更日期后切换为 GNU GPL v3。生产环境使用前，请查看 [Directus 许可证](https://github.com/directus/directus/blob/main/license) 和 [Directus 价格页面](https://directus.io/pricing) 了解具体条款。

## 为什么在 Sealos 上部署 Directus？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统，覆盖从云端开发环境到生产部署和运维的完整应用生命周期。在 Sealos 上部署 Directus，你可以获得：

- **一键部署**：通过一个模板完成 Directus、PostgreSQL、Redis、存储和 HTTPS 访问配置。
- **无需 Kubernetes 经验**：不用编写 YAML，也不用管理集群内部细节，就能使用 Kubernetes 支撑的基础设施。
- **内置持久化存储**：数据库数据、上传文件和扩展在重启后依然保留。
- **可选对象存储**：部署时可选择 S3 兼容对象存储，为生产环境文件存储提供更合适的方案。
- **即时公网访问**：Sealos 会为 Directus 管理后台和 API 自动分配公网 HTTPS 地址。
- **易于自定义**：部署后可在 Sealos Canvas 中调整环境变量、资源、存储和服务设置。
- **AI 辅助运维**：可以通过 Sealos AI 对话描述变更需求，也可以直接编辑资源卡片完成后续调整。
- **按量付费更高效**：先使用轻量资源启动，等业务负载增长后再按需扩容。

在 Sealos 上部署 Directus，把精力放在数据建模、内容管理和 API 构建上，而不是基础设施维护上。

## 部署指南

1. 打开 [Directus 模板](https://sealos.run/products/app-store/directus)，点击 **Deploy Now**。
2. 在弹出的配置窗口中填写参数：
   - **admin_email**：Directus 初始管理员邮箱。
   - **admin_password**：Directus 初始管理员密码。
   - **use_object_storage**：如需将上传文件保存到 S3 兼容对象存储，而不是本地持久卷，请启用该选项。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会进入 Canvas。后续如需修改配置，可以在对话框中描述需求，让 AI 自动应用变更；也可以点击对应资源卡片手动调整设置。
4. 通过提供的 URL 访问应用：
   - **Directus 管理后台**：使用配置好的管理员邮箱和密码登录。
   - **Directus API**：REST 和 GraphQL API 使用同一个公网地址访问。

## 配置

部署完成后，你可以通过以下方式配置 Directus：

- **Directus 管理后台**：管理集合、字段、角色、权限、用户、文件、流程和系统设置。
- **AI 对话**：在 Sealos 中描述想要变更的配置，让 AI 应用到对应资源。
- **资源卡片**：在 Canvas 中打开 StatefulSet、数据库、Redis、存储或 Ingress 卡片进行调整。
- **环境变量**：在工作负载资源中修改 Directus 运行时配置，例如存储、缓存、公网 URL 和安全选项。
- **扩展目录**：需要持久化的 Directus 扩展应放在 `/directus/extensions` 下。

如果是生产环境，并计划使用多个副本或处理大量文件上传，建议启用对象存储，避免上传文件绑定到单个本地卷。

## 扩缩容

如需扩缩容：

1. 打开 Directus 部署对应的 Canvas。
2. 点击 Directus StatefulSet 资源卡片。
3. 在对话框中调整 CPU、内存或副本数量。
4. 应用变更，等待工作负载完成滚动更新。

Directus 使用 PostgreSQL 和 Redis 作为共享后端服务。如果增加 Directus 副本，建议使用对象存储保存上传文件，这样所有副本都能访问同一套文件后端。

## 故障排查

### Directus 一直未就绪

- **原因**：PostgreSQL、Redis 或文件存储尚未就绪。
- **解决方法**：查看 Directus StatefulSet 日志，以及 PostgreSQL 和 Redis 资源卡片。模板已内置启动等待容器和 `/server/health` 探针，因此首次部署时可能需要等待几分钟。

### 初始管理员账号无法登录

- **原因**：部署时填写的管理员邮箱或密码不正确。
- **解决方法**：使用部署配置窗口中填写的值登录。如果填写错误，可以更新部署配置，或使用正确凭据重新创建应用。

### 文件上传失败

- **原因**：本地上传卷不可写，或启用对象存储后对象存储凭据不可用。
- **解决方法**：自定义工作负载时保留模板中的卷权限初始化容器和 `fsGroup` 设置。如果启用了对象存储，请确认 ObjectStorageBucket 和相关密钥已创建。

### 重启后扩展不可用

- **原因**：扩展没有放在持久化扩展路径下。
- **解决方法**：将扩展保存在 `/directus/extensions`，该路径在本模板中由持久化存储卷支持。

### 获取帮助

- [Directus 文档](https://directus.io/docs/)
- [Directus GitHub Issues](https://github.com/directus/directus/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Directus API 参考](https://directus.io/docs/api)
- [Directus 配置参考](https://directus.io/docs/configuration)
- [Directus 自托管概览](https://directus.io/docs/self-hosting/overview)
- [Sealos 应用商店](https://sealos.run/products/app-store)

## 许可证

本 Sealos 模板提供在 Sealos 上运行 Directus 的部署配置。Directus 本身采用 Business Source License 1.1 分发，并会在对应变更日期后切换为 GNU GPL v3。生产环境使用前，请先查看 Directus 许可证。
