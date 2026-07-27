# 在 Sealos 上部署和托管 Directus

Directus 是一个可组合数据平台和 Headless CMS，可在 SQL 数据库之上提供管理后台、REST 与 GraphQL API、认证、权限、文件和自动化能力。本模板部署 Directus 12 与 Redis，并支持在部署时选择数据库和文件存储拓扑。

![使用 PostgreSQL 和 Sealos S3 的 Directus 集合](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/directus/website-screenshot.webp)

## 模板部署内容

- **Directus `12.1.1`**：以单副本 StatefulSet 运行，监听 `8055` 端口
- **Redis `7.2.7`**：通过 KubeBlocks 部署，用于缓存和限流
- **托管 PostgreSQL `16.4.0`**：默认数据库，也可选择轻量的内嵌 SQLite
- **本地持久化上传卷**：默认文件存储，也可选择私有 Sealos S3 兼容对象存储
- **持久化扩展存储**：挂载到 `/directus/extensions`
- **公网 HTTPS**：由 Sealos 管理 Service 和 Ingress
- **健康探针**：启动、就绪和存活探针统一使用 `/server/ping`

PostgreSQL 和对象存储可以独立选择，支持以下组合：

| 数据库 | 文件存储 | 推荐场景 |
| --- | --- | --- |
| PostgreSQL | 本地持久卷 | 常规单副本部署 |
| PostgreSQL | Sealos S3 | 面向生产的文件存储和后续水平扩容 |
| SQLite | 本地持久卷 | 评估和小型单副本项目 |
| SQLite | Sealos S3 | 轻量数据库与持久对象存储 |

## 常见使用场景

- 网站和应用的 Headless CMS
- 内部数据管理与运营工具
- 带认证和权限的 REST 或 GraphQL 后端
- 结构化内容、用户和文件管理
- 低代码工作流与仪表盘

## 部署

1. 打开 Sealos 应用商店中的 [Directus 模板](https://sealos.io/products/app-store/directus)。
2. 填写高强度的初始管理员邮箱和密码。
3. 选择数据库与文件存储方案。
4. 点击 **部署**，等待 Directus 工作负载就绪。首次使用托管 PostgreSQL 时，KubeBlocks 创建数据库通常需要几分钟。
5. 打开 Sealos 提供的 HTTPS 地址。

### 部署参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `admin_email` | 必填 | 首位 Directus 管理员的邮箱 |
| `admin_password` | 必填 | 首位 Directus 管理员的密码 |
| `use_postgresql` | `true` | 创建托管 PostgreSQL；设为 `false` 时使用 `/directus/database/data.db` 中的 SQLite |
| `use_object_storage` | `false` | 创建私有 Sealos S3 存储桶；设为 `false` 时使用 `/directus/uploads` |

管理员凭据只在 Directus 初始化新数据库时生效。数据库已经存在时，修改这些参数不会重置其中的管理员。

## 首次登录

1. 打开部署后的 Directus 地址。
2. 使用配置的 `admin_email` 和 `admin_password` 登录。
3. 首次运行的许可证页面会提供两种选择：免费且无需密钥的 **Core plan**，以及填写许可证密钥的其他适用方案。
4. 完成或跳过可选的用途调查。
5. 设置项目所有者，或选择 **Remind Later**。

管理后台位于 `/admin`。同一个公网域名也提供 API：

- REST API：`/items`、`/users`、`/files` 等资源路径
- GraphQL API：`/graphql`
- 免认证健康检查：`/server/ping`

Directus 12 会限制 `/server/health` 的访问；外部可用性检查应使用 `/server/ping`。

## 数据库方案

### 托管 PostgreSQL

这是默认方案。模板会创建 KubeBlocks PostgreSQL 集群，并通过幂等初始化 Job 创建 `directus` 数据库。Directus 从 Kubernetes Secret 读取主机、端口、用户名和密码。

生产负载、较大数据集以及计划后续运行多个 Directus 副本的部署应选择 PostgreSQL。

### 内嵌 SQLite

关闭 `use_postgresql` 后，数据库会保存在专用 `1Gi` 持久卷的 `/directus/database/data.db`。SQLite 能降低部署占用，适合评估和小型单副本项目。

SQLite 数据库文件位于 ReadWriteOnce 存储卷，因此该方案应保持一个 Directus 副本。

## 文件存储方案

### 本地持久化存储

关闭 `use_object_storage` 时，上传文件保存在专用 `1Gi` 持久卷的 `/directus/uploads`。

### Sealos S3 对象存储

启用 `use_object_storage` 后，模板会创建私有 `ObjectStorageBucket`。Directus 使用名为 `sealos` 的 S3 兼容存储位置，并将对象保存在 `uploads` 前缀下。存储桶凭据由 Sealos 管理的 Secret 注入。

直接请求私有对象会返回 `403`。用户应通过 Directus 访问文件，由 Directus 执行认证与权限检查。

## 持久化

| 路径或服务 | 用途 | 创建条件 |
| --- | --- | --- |
| PostgreSQL 存储卷 | Directus 系统数据和应用数据 | `use_postgresql=true` |
| `/directus/database` | SQLite 数据库文件 | `use_postgresql=false` |
| `/directus/uploads` | 本地上传文件 | `use_object_storage=false` |
| Sealos S3 存储桶 | 对象存储中的上传文件 | `use_object_storage=true` |
| `/directus/extensions` | Directus 扩展 | 始终创建 |
| Redis 存储卷 | 缓存和限流数据 | 始终创建 |

## 默认资源

Directus 容器采用官方最低内存要求，并选择满足 CPU 要求的 Sealos 资源档位：

| 组件 | CPU limit | Memory limit | CPU request | Memory request |
| --- | ---: | ---: | ---: | ---: |
| Directus | `500m` | `512Mi` | `50m` | `51Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis | `500m` | `512Mi` | `50m` | `51Mi` |
| Redis Sentinel | `500m` | `512Mi` | `50m` | `51Mi` |
| 启动和初始化容器 | `100m` | `128Mi` | `10m` | `12Mi` |

大型 schema、高 API 流量、文件转换或扩展负载需要提高 Directus 内存。

## 扩缩容

模板默认运行一个 Directus 副本。水平扩容前需要完成以下配置：

1. 使用托管 PostgreSQL。
2. 启用 Sealos S3 对象存储，让所有副本共享同一文件后端。
3. 为所有副本分发相同的扩展。
4. 保持 Redis 启用，以共享缓存和限流状态。
5. 在 Sealos Canvas 中调整 StatefulSet 副本数和资源。

## 故障排查

### 应用仍在启动

在 Sealos Canvas 中打开 Directus、PostgreSQL 和 Redis 资源卡片。首次部署时，等待容器会持续检查后端服务，直到它们就绪。PostgreSQL 创建过程可能需要几分钟。

### 初始管理员无法登录

使用部署时填写的邮箱和密码。Directus 只在初始化数据库时使用这些值创建首位管理员；已有数据库会保留其中的用户和密码。

### S3 文件返回 `403`

私有存储桶的直接访问会返回 `403`。请通过 Directus `/assets/{id}` 接口访问，并使用具备对应权限的用户或令牌。

### 日志出现几何功能警告

托管 PostgreSQL 镜像未包含 PostGIS，SQLite 也未包含 SpatiaLite。常规 CMS 和 API 功能可以正常使用。需要几何字段和空间查询时，请使用兼容的空间数据库。

### 自定义后扩展消失

需要持久化的扩展应放在 `/directus/extensions`。运行多个副本时，每个副本都需要使用相同的扩展集合。

## 文档

- [Directus Docker 指南](https://docs.directus.io/self-hosted/docker-guide)
- [Directus 配置选项](https://docs.directus.io/self-hosted/config-options)
- [Directus API 参考](https://directus.io/docs/api)
- [Directus GitHub 仓库](https://github.com/directus/directus)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Directus 12 采用 [Monospace Sustainable Core License 1.0，并附带未来 GPL 许可（MSCL-1.0-GPL）](https://github.com/directus/directus/blob/v12.1.1/license)。生产使用前，请阅读许可证和 [Directus 价格页面](https://directus.io/pricing)。本仓库只提供 Sealos 部署模板，不会改变 Directus 的许可证。
