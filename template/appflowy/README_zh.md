# 在 Sealos 上部署和托管 AppFlowy

AppFlowy 是一个开源协作工作空间，支持文档、数据库、看板和团队实时协作。这个 Sealos 模板会部署 AppFlowy Web 客户端、AppFlowy Cloud API、后台 Worker、GoTrue 认证、PostgreSQL、Redis，以及 S3 兼容对象存储，组成一套可自托管的工作空间服务。

## 关于 AppFlowy 托管

AppFlowy 提供类似 Notion 的工作空间体验，支持页面、富文本编辑、团队空间和结构化知识管理。托管版 Web 客户端会连接 AppFlowy Cloud，用于工作空间数据、身份认证、协作 API、WebSocket 同步和后台导入导出任务。

这个模板尽量使用 Sealos 托管能力。PostgreSQL 通过 KubeBlocks 创建并启用 pgvector，Redis 通过 KubeBlocks 提供缓存和后台任务协调，文件存储默认使用 Sealos 对象存储。如果你已经有 S3 兼容存储桶，也可以在部署时切换为外部 S3。

模板保持最小运行形态：只包含必需的 Web、Cloud、Worker、GoTrue、PostgreSQL、Redis 和对象存储服务，不部署可选的 AI、搜索、管理前端或 MinIO 容器。

## 常见使用场景

- **团队知识库**：创建共享文档、项目笔记和内部手册。
- **个人效率工作空间**：运行私有笔记、任务和规划空间。
- **自托管协作平台**：把工作空间数据保存在自己的 Sealos 环境中。
- **数据库驱动的项目管理**：用 AppFlowy 数据库组织任务、内容和结构化记录。
- **轻量工作空间替代方案**：部署一个开源的在线工作空间替代品。

## AppFlowy 托管依赖

这个 Sealos 模板包含以下运行依赖：

- AppFlowy Web 客户端
- AppFlowy Cloud API 和 WebSocket 服务
- AppFlowy Worker 后台任务服务
- GoTrue 认证服务
- 启用 pgvector 的 KubeBlocks PostgreSQL
- KubeBlocks Redis
- 默认使用 Sealos 对象存储，也可选择外部 S3 兼容存储桶

### 部署依赖

- [AppFlowy GitHub 仓库](https://github.com/AppFlowy-IO/AppFlowy) - AppFlowy 主项目
- [AppFlowy Cloud 仓库](https://github.com/AppFlowy-IO/AppFlowy-Cloud) - 自托管云端后端
- [AppFlowy 文档](https://docs.appflowy.io/) - 产品和自托管文档
- [Sealos 应用市场](https://sealos.io/products/app-store) - 一键应用部署

## 实现细节

### 架构组件

这个模板会部署以下服务：

- **AppFlowy Web**：浏览器端 UI，通过主应用地址访问。
- **AppFlowy Cloud**：工作空间、文档、协作和文件元数据的 API 与 WebSocket 后端。
- **AppFlowy Worker**：处理导入、文件相关任务等异步后台任务。
- **GoTrue**：AppFlowy 使用的邮箱和密码认证服务。
- **PostgreSQL**：默认选择外接数据库而不是 SQLite，通过 KubeBlocks 创建并启用 pgvector。
- **Redis**：默认选择外接 Redis，用于缓存和后台任务协调。
- **对象存储**：S3 兼容存储。默认创建 Sealos 对象存储桶，也可按条件选择外部 S3 存储桶。

### 配置方式

AppFlowy Web 客户端启动时会收到三个公开地址：

- `APPFLOWY_BASE_URL`：主应用地址
- `APPFLOWY_GOTRUE_BASE_URL`：独立的 GoTrue 认证公网地址
- `APPFLOWY_WS_BASE_URL`：主应用域名下的 WebSocket 地址

Cloud 和 Worker 服务通过 Kubernetes 内部服务发现连接 PostgreSQL、Redis 和 GoTrue。Redis 端点已经指向这个模板创建的 KubeBlocks Redis 数据服务。

### 资源规格

模板经过真实部署测试，并调整到以下最小资源规格：

| 组件 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: |
| AppFlowy Web | 100m | 128Mi | - |
| GoTrue | 100m | 128Mi | - |
| AppFlowy Cloud | 200m | 256Mi | - |
| AppFlowy Worker | 100m | 128Mi | - |
| PostgreSQL | 500m | 512Mi | 1Gi |
| Redis 数据节点 | 500m | 512Mi | 1Gi |
| Redis Sentinel | 500m | 512Mi | 1Gi |

如果团队规模更大，建议先提高 AppFlowy Cloud 的内存，再根据工作空间规模和访问量调整 PostgreSQL 与 Redis。

### 许可信息

AppFlowy 和 AppFlowy Cloud 使用 GNU Affero General Public License v3.0 许可。这个 Sealos 模板只提供部署配置。

## 为什么在 Sealos 上部署 AppFlowy？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端开发到生产部署和运维管理的完整应用生命周期。在 Sealos 上部署 AppFlowy 可以获得：

- **一键部署**：从应用市场部署完整的多服务 AppFlowy 栈。
- **托管依赖**：PostgreSQL、Redis、公网入口、TLS 和对象存储一起创建。
- **持久化存储**：数据库和对象存储数据可在应用重启后保留。
- **公网 HTTPS 访问**：Sealos 自动提供公网地址和 TLS 证书。
- **简单配置**：通过部署表单和 Canvas 配置存储后端、账号密码和资源规格。
- **Kubernetes 原生运维**：不用手写 Kubernetes 清单，也可以调整资源、查看日志和管理服务。

## 部署指南

1. 打开 [AppFlowy 模板](https://sealos.io/products/app-store/appflowy)，点击 **Deploy Now**。
2. 配置必填参数：
   - **S3 provider**：保留 `sealos-objectstorage` 会创建内置 Sealos 对象存储桶；如果已有 S3 兼容存储桶，可以选择 `external-s3`。
   - **GoTrue admin email**：GoTrue 初始管理员邮箱。
   - **GoTrue admin password**：GoTrue 初始管理员密码。请在部署时设置并保存这个值。
   - **External S3 fields**：仅在选择 `external-s3` 时需要填写。
3. 点击 **Deploy**，等待模板完成 App、PostgreSQL、Redis、对象存储和公网路由创建。
4. 从 Sealos Canvas 或部署结果中打开 AppFlowy 应用地址。
5. 在 AppFlowy 登录页登录或注册用户账号。

## 登录和注册

AppFlowy 会从主应用地址跳转到 `/app`。在登录页输入邮箱，然后继续使用密码登录。

新用户可以在登录页点击 **Create account** 创建账号，并使用邮箱和密码注册。这个模板启用了 GoTrue 邮箱自动确认，因此首次登录不需要额外配置 SMTP。注册完成后，AppFlowy 会创建默认工作空间并进入主界面。

部署时填写的 `gotrue_admin_email` 和 `gotrue_admin_password` 会创建 GoTrue 服务管理员账号。不要把这个管理员账号作为普通 AppFlowy Web 工作空间账号使用；请在 Web 登录页新建普通用户，让 AppFlowy Cloud 自动初始化对应的用户资料和默认工作空间。

## 配置参数

| 参数 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `appflowy_s3_provider` | `sealos-objectstorage` | 是 | 选择 Sealos 对象存储或外部 S3 兼容存储桶。 |
| `gotrue_admin_email` | `admin@example.com` | 是 | GoTrue 服务管理员邮箱。AppFlowy 工作空间用户请通过 Web 注册创建。 |
| `gotrue_admin_password` | 空 | 是 | GoTrue 服务管理员密码。部署时设置并保存。 |
| `external_s3_endpoint` | 空 | 条件必填 | 选择 `external-s3` 时填写 S3 API 端点。 |
| `external_s3_public_endpoint` | 空 | 条件必填 | 用于预签名 URL 的公网 S3 端点。 |
| `external_s3_access_key` | 空 | 条件必填 | 外部 S3 Access Key。 |
| `external_s3_secret_key` | 空 | 条件必填 | 外部 S3 Secret Key。 |
| `external_s3_bucket` | 空 | 条件必填 | 已存在的外部 S3 存储桶名称。 |
| `external_s3_region` | `us-east-1` | 条件必填 | 外部 S3 区域。 |

## 扩缩容

部署后可以按以下方式调整 AppFlowy 资源：

1. 打开 AppFlowy 部署对应的 Canvas。
2. 点击 AppFlowy Cloud、Web、Worker、PostgreSQL 或 Redis 资源卡片。
3. 根据负载需要提高 CPU、内存、存储或副本数。
4. 应用修改并等待相关 Pod 重启完成。

多数场景下，建议先提高 AppFlowy Cloud 和 PostgreSQL 资源，再考虑增加 Web 客户端资源。

## 故障排查

### 无法注册或登录

- 请在 Web 登录页创建普通 AppFlowy 用户，不要直接使用 GoTrue 管理员账号登录工作空间。管理员账号可以通过 GoTrue 认证，但可能没有 AppFlowy 工作空间资料。
- 如果是在检查 GoTrue 管理能力，确认部署时已经设置 `gotrue_admin_password`。
- 如需排查，可打开 GoTrue 公网地址并访问 `/health`。
- 确认用户是通过 AppFlowy Web 登录页注册，而不是访问内部服务地址。

### 页面能打开但工作空间操作失败

- 在主应用地址访问 `/api/health`，检查 AppFlowy Cloud 健康状态。
- 从 Sealos Canvas 查看 AppFlowy Cloud 日志。
- 确认 PostgreSQL 和 Redis 资源卡片处于运行状态。

### 文件上传或导入失败

- 如果使用默认存储，确认 Sealos 对象存储桶已经创建。
- 如果使用外部 S3，确认 endpoint、公网 endpoint、bucket、access key、secret key 和 region 均正确。
- 模板设置了 `APPFLOWY_S3_CREATE_BUCKET=false`，因此外部 S3 存储桶需要提前创建。

## 相关资源

- [AppFlowy 官网](https://www.appflowy.com/)
- [AppFlowy GitHub](https://github.com/AppFlowy-IO/AppFlowy)
- [AppFlowy Cloud GitHub](https://github.com/AppFlowy-IO/AppFlowy-Cloud)
- [AppFlowy 文档](https://docs.appflowy.io/)
- [Sealos 文档](https://sealos.io/docs)

## 许可

这个 Sealos 模板遵循模板仓库的许可证。AppFlowy 和 AppFlowy Cloud 使用 GNU Affero General Public License v3.0 许可。
