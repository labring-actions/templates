# 在 Sealos 上部署和托管 Payload

Payload 是一个原生集成 Next.js 的无头内容管理系统，提供可扩展的管理后台、REST 与 GraphQL API、认证能力以及媒体文件管理。本模板会在 Sealos Cloud 上为你部署 Payload、PostgreSQL、持久化媒体存储，以及可直接访问的 HTTPS 入口。

## 关于在 Sealos 上托管 Payload

Payload 本质上是一个 Node.js 应用，把内容建模、后台管理和 API 交付整合在同一套服务里。如果你希望用一个 CMS 同时支撑网站、应用、内部工具或自定义产品，又不想把管理后台和 API 层拆开，它会是一个很合适的选择。

这个 Sealos 模板会自动创建 PostgreSQL 数据库集群，用来保存结构化内容数据；同时还会运行一次性的初始化任务，自动创建 `payload` 数据库，并挂载一个持久化卷到 `/app/src/media`，专门存放上传的媒体文件。应用会通过 Ingress 对外暴露，默认带 SSL，并预置适合生产环境启动的关键环境变量和上传相关代理配置。

## 常见使用场景

- **网站无头 CMS**：为 Next.js、Nuxt、Astro 或任意前端项目提供结构化内容管理与 API 能力。
- **API 优先的产品后端**：把 Payload 用作 Web 或移动应用的内容层与认证层。
- **内容编辑工作流**：让团队通过统一后台管理草稿、媒体资源和正式发布内容。
- **内部门户系统**：基于自定义 collections 构建内部工具、知识库或运营后台。
- **富媒体内容平台**：在内容模型和 API 之外，同时管理图片、文档等上传资源。

## Payload 托管依赖

这个 Sealos 模板已经包含所需的全部组件：Payload 应用本体、PostgreSQL 16.4 数据库集群、数据库初始化任务、持久化媒体存储，以及 HTTPS Ingress。

### 部署依赖

- [Payload 官方文档](https://payloadcms.com/docs) - Payload 的官方使用文档，涵盖配置、Collections、API 等内容
- [Payload GitHub 仓库](https://github.com/payloadcms/payload) - 源码、版本发布与问题跟踪
- [Payload 官网](https://payloadcms.com/) - 产品介绍与生态资源
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/) - 数据库参考资料与运维指南

### 实现细节

**架构组件：**

本模板会部署以下服务与资源：

- **Payload 应用**：以 StatefulSet 形式运行，对外提供 `3000` 端口服务，同时承载管理后台和 API 层
- **PostgreSQL 数据库**：由 KubeBlocks 管理的 PostgreSQL 16.4 集群，默认附带 1Gi 持久化存储
- **数据库初始化任务**：一次性 Job，会等待 PostgreSQL 就绪后自动创建 `payload` 数据库
- **媒体存储卷**：一个 1Gi 的持久化卷，挂载到 `/app/src/media`，用于保存上传文件
- **Ingress 与应用入口**：通过 Sealos 自动生成 HTTPS 公网入口，并在应用卡片中提供访问链接

**配置说明：**

应用默认以 `NODE_ENV=production` 启动，并通过 `DATABASE_URL` 连接 PostgreSQL。Payload 相关配置通过 `PAYLOAD_SECRET` 和 `PAYLOAD_CONFIG_PATH=src/payload.config.ts` 注入；上传的媒体文件则会写入挂载的持久化卷，而不是容器临时文件系统。

模板默认只启用单副本运行。这是本地文件上传场景下更稳妥的做法，因为媒体目录依赖单个 `ReadWriteOnce` 卷。如果你要做多副本横向扩容，建议先把上传文件迁移到共享对象存储或其他共享文件系统。

**平台说明：**

- 公网地址：`https://<app-host>.<domain>`
- 管理后台：通常位于 `/admin`
- 上传大小限制：`32m`
- 默认媒体存储：`1Gi`

**许可证说明：**

请以 [Payload 仓库](https://github.com/payloadcms/payload) 中当前上游许可证说明为准。

## 为什么在 Sealos 上部署 Payload？

Sealos 是一个构建在 Kubernetes 之上的 AI 辅助云操作系统，把部署、运维和扩缩容整合进同一套工作流。将 Payload 部署到 Sealos 后，你可以获得：

- **一键部署**：Payload 和 PostgreSQL 一起拉起，无需手写 Kubernetes YAML，也不用自己串联服务依赖。
- **数据库自动就绪**：PostgreSQL 会自动创建、初始化，并与 Payload 完成连接。
- **媒体持久化存储**：上传文件保存在独立存储卷中，重启或升级后依然保留。
- **自动 HTTPS 访问**：Sealos 会自动分配公网地址并签发 SSL 证书，开箱即可安全访问。
- **AI 辅助运维**：部署完成后，你可以通过对话描述修改需求，或在 Canvas 中点击资源卡片完成调整。
- **按量使用更省成本**：可以先用较小的 CPU、内存、存储配置启动，后续根据实际负载再逐步扩容。
- **享受 Kubernetes 能力但不用直接管理 Kubernetes**：服务发现、工作负载隔离和基础设施编排都由平台处理。

把 Payload 部署到 Sealos 后，你可以把精力集中在内容模型和业务设计上，而不是底层基础设施。

## 部署指南

1. 打开 [Payload 模板页面](https://sealos.run/products/app-store/payload)，点击 **Deploy Now**。
2. 在弹出的参数配置窗口中填写以下信息：
   - **App Name**：部署资源使用的应用名称
   - **App Host**：公网访问域名的子域名前缀
   - **Payload Secret**：Payload 用于应用安全的密钥
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会自动跳转到 Canvas。后续如果需要修改配置，可以直接在对话框中描述需求，让 AI 帮你更新；也可以点击对应资源卡片手动调整。
4. 通过以下地址访问你的应用：
   - **主访问地址**：`https://<app-host>.<domain>`
   - **管理后台**：`https://<app-host>.<domain>/admin`
   - **API 地址**：Payload 配置的 API 路由会通过同一个公网地址对外提供服务

## 配置说明

部署完成后，你可以通过以下方式配置 Payload：

- **AI 对话框**：直接描述基础设施或运行参数变更需求，由 AI 代你修改
- **资源卡片**：在 Canvas 中修改算力、存储、网络和环境变量等配置
- **Payload 管理后台**：创建 collections、globals、访问控制规则、用户和媒体配置

如果需要调整 Payload 的 schema 级配置，请更新 Payload 项目配置后重新部署应用资源。

## 扩缩容

如需扩缩容，可按以下步骤操作：

1. 打开该部署对应的 Canvas。
2. 点击 Payload 对应的资源卡片。
3. 如果后台操作或 API 请求量上升，可适当提高 CPU 与内存。
4. 如果上传文件逐渐增多，可扩大媒体存储卷，超过默认的 `1Gi` 时尤其建议处理。
5. 在没有切换到共享存储前，建议保持单副本运行，不要直接扩到多实例。

## 故障排查

### 常见问题

**问题 1：应用地址已经能打开，但管理后台暂时不可用**
- 原因：Payload 容器可能仍在启动过程中，尚未完全就绪。
- 解决方案：在 Canvas 中查看应用日志，等待容器通过就绪检查。

**问题 2：启动时报数据库连接错误**
- 原因：PostgreSQL 可能还在初始化，或者数据库初始化任务尚未完成。
- 解决方案：先确认 PostgreSQL 集群状态正常，再检查 `pg-init` 任务是否执行成功，必要时再重启应用。

**问题 3：大文件上传失败**
- 原因：Ingress 默认配置了 `32m` 的上传限制。
- 解决方案：控制上传文件大小，或通过对应资源卡片调整 Ingress 配置。

**问题 4：横向扩容后媒体文件表现不一致**
- 原因：上传文件默认写入单个 `ReadWriteOnce` 卷，多副本场景下不适合直接共享。
- 解决方案：先改成共享存储后端，再考虑把副本数扩到 1 个以上。

### 获取帮助

- [Payload 官方文档](https://payloadcms.com/docs)
- [Payload GitHub Issues](https://github.com/payloadcms/payload/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Payload 配置总览](https://payloadcms.com/docs/configuration/overview)
- [Payload REST API](https://payloadcms.com/docs/rest-api/overview)
- [Payload GraphQL API](https://payloadcms.com/docs/graphql/overview)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)

## 许可证

本 Sealos 模板用于在 Sealos 上部署应用。Payload 本身遵循其上游许可证条款，具体请参考 [Payload 仓库](https://github.com/payloadcms/payload) 中的最新说明。
