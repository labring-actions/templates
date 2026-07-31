# 在 Sealos 上部署和托管 Budibase

Budibase 是一个开源低代码平台，可用于构建内部工具、表单、门户和工作流应用。此模板会在 Sealos Cloud 上部署 Budibase 3.41.1，并配套部署应用服务、Worker、Proxy、CouchDB 兼容数据库、Redis 和私有 S3 兼容对象存储。

![Budibase 应用构建器](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/budibase/website-screenshot.webp)

## Budibase 托管架构

Budibase 将可视化构建器、数据连接、自动化工具、用户管理和 API 集成在同一个工作区中。公网 Proxy 负责把浏览器和 API 流量转发给应用及 Worker 服务，Redis 负责协调运行时任务，Budibase Database 则保存工作区元数据。

Budibase 依赖对象存储来保存应用资源、附件、插件、模板、临时文件和备份。此模板会创建一个私有 Sealos Object Storage 存储桶，并通过 S3 兼容 API 接入 Budibase。文件下载使用签名 URL，存储桶保持私有访问策略。

CouchDB 数据统一持久化到独立存储卷的 `/data` 目录。Redis 和 Redis Sentinel 分别使用 KubeBlocks 持久化存储。Sealos 还会自动创建 HTTPS 入口、公网域名、服务发现和运行时凭据。

## 常见使用场景

- **内部运营工具**：构建管理后台、审批工具和运营看板。
- **表单与门户**：创建数据录入流程、客户门户和员工自助应用。
- **数据库前端**：为业务数据库和 API 提供权限可控的可视化界面。
- **工作流自动化**：通过应用事件触发操作、通知和第三方集成。
- **快速原型验证**：先用可运行的应用验证业务流程，再推进更大规模的实现。

## Budibase 托管依赖

模板已包含 Budibase 所需的全部运行依赖：

- Budibase Apps、Worker 和 Proxy 3.41.1
- 带持久化存储的 Budibase Database 2.1.0
- 由 KubeBlocks 管理的 Redis 7.2.7 和 Redis Sentinel
- 私有 Sealos S3 兼容对象存储
- Kubernetes Service、Ingress 和自动 TLS

### 部署资料

- [Budibase 文档](https://docs.budibase.com/docs) - 产品与构建器文档
- [自托管指南](https://docs.budibase.com/docs/hosting-methods) - 官方托管方案
- [Budibase 源码仓库](https://github.com/Budibase/budibase) - 源码和版本发布
- [3.41.1 官方 Helm Values](https://github.com/Budibase/budibase/blob/3.41.1/charts/budibase/values.yaml) - 上游拓扑和对象存储配置

## 实现细节

### 架构组件

此模板会部署以下组件：

- **Proxy**：监听 `10000` 端口的公网入口，负责在 Budibase 服务之间转发构建器和 API 流量，并承载官方外部对象存储上游配置。
- **Apps**：在 `4002` 端口提供 Budibase 构建器、工作区 API、身份认证和应用运行时。
- **Worker**：在 `4003` 端口处理后台工作和运行时任务。
- **Budibase Database**：运行官方 `budibase/database:2.1.0` 镜像，并把全部数据库状态持久化到 `/data`。
- **Redis**：通过 KubeBlocks 托管服务提供缓存、队列和协调能力。
- **Redis Sentinel**：监控 Redis 服务，并提供托管数据库集群所需的拓扑。
- **Object Storage**：使用一个私有 Sealos 存储桶承载 Budibase 的全部对象存储类别。

Apps 和 Worker 会等待 Redis 与 Budibase Database 就绪后再启动。运行时凭据和服务地址来自 Sealos 托管值、KubeBlocks 账户 Secret 和 Object Storage Secret。

### 实测最低资源

| 组件 | 副本数 | CPU 上限 | 内存上限 | 持久化存储 |
|---|---:|---:|---:|---:|
| Apps | 1 | `200m` | `1Gi` | - |
| Worker | 1 | `100m` | `256Mi` | - |
| Proxy | 1 | `100m` | `128Mi` | - |
| Budibase Database | 1 | `200m` | `1Gi` | `1Gi` |
| Redis | 1 | `500m` | `512Mi` | `1Gi` |
| Redis Sentinel | 1 | `500m` | `512Mi` | `1Gi` |

这些配置已通过全新部署的冷启动、登录后构建器操作、对象上传下载和持久化检查。随着应用数量、用户、自动化任务和附件流量增长，生产环境可以逐步提高资源上限。

## 配置

在部署窗口中配置以下参数：

| 参数 | 用途 | 是否必填 | 默认值 |
|---|---|---:|---|
| `admin_email` | 初始管理员邮箱和登录名 | 是 | 用户填写 |
| `admin_password` | 初始管理员密码，至少 8 个字符 | 是 | 用户填写 |
| `enable_analytics` | 启用 Budibase 分析功能 | 否 | `false` |
| `smtp_enabled` | 启用邮件发送 | 否 | `false` |
| `smtp_host` | SMTP 服务器地址 | 启用 SMTP 时填写 | 空 |
| `smtp_port` | SMTP 服务器端口 | 启用 SMTP 时填写 | `587` |
| `smtp_user` | SMTP 用户名和发件地址 | 启用 SMTP 时填写 | 空 |
| `smtp_password` | SMTP 密码 | 启用 SMTP 时填写 | 空 |

Sealos 会为每次部署生成内部 API Key、JWT Secret、API 加密密钥、CouchDB 凭据和数据库 Cookie。

## 在 Sealos 上部署 Budibase 的优势

- **一键部署**：通过一个部署窗口创建完整的多服务拓扑。
- **依赖统一托管**：KubeBlocks Redis、持久化存储卷、私有 S3 兼容存储、网络和 TLS 会协同创建。
- **Kubernetes 基础能力**：每个组件都配有明确的健康检查、服务发现和独立资源配置。
- **Canvas 运维**：部署完成后，可以通过 AI 对话或资源卡片检查和更新应用。
- **按量使用资源**：从实测最低资源起步，再随业务增长扩容。
- **私有应用存储**：Budibase 资源和附件保存在私有存储桶中，并通过签名方式访问。

## 部署指南

1. 打开 [Budibase 模板](https://sealos.io/products/app-store/budibase)，点击 **Deploy Now**。
2. 填写初始管理员邮箱和至少 8 个字符的密码，并按需配置分析功能或 SMTP。
3. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开新应用的 Canvas。
4. 打开 Budibase 应用卡片上显示的公网地址。根地址会进入 Budibase 构建器。

## 登录并开始构建

部署过程会根据 `admin_email` 和 `admin_password` 创建初始管理员。

1. 打开生成的公网地址，浏览器会进入 `/builder`。
2. 输入部署时填写的管理员邮箱和密码。
3. 点击 **Create**，选择 **App**，填写应用名称和 URL 路径。
4. 在构建器中点击 **Add component**，创建第一个页面。

管理员登录后，可以通过 **Invite users** 添加更多创建者和应用用户。

## 部署后运维

- **AI 对话**：在 Canvas 对话框中描述资源或配置变更。
- **资源卡片**：打开 Apps、Worker、Proxy、Database、Redis 或 Object Storage 卡片查看设置。
- **SMTP**：部署时启用 SMTP，以支持邮件邀请和通知。
- **应用备份**：使用 Budibase 备份功能，备份对象会保存到私有 Sealos 存储桶。
- **监控**：在 Canvas 中查看组件日志、重启次数和资源消耗。

## 扩容

模板会按照既有拓扑为每个 Budibase 服务启动 1 个副本。根据实际流量增加 Apps、Worker 和 Proxy 容量；调整有状态副本时，需要同步规划数据库和队列的一致性。

调整资源的步骤：

1. 打开部署对应的 Canvas。
2. 选择相关资源卡片。
3. 调整 CPU、内存、存储或副本数。
4. 应用变更，并确认全部健康检查恢复为 Ready。

## 故障排查

### 构建器仍在启动

Apps 和 Worker 会等待 Redis 与 Budibase Database。先查看这两个资源卡片，等待有状态服务进入 Ready。

### 管理员登录失败

使用部署时填写的 `admin_email` 和 `admin_password`。登录页面位于 `/builder/auth/login`。

### 邮件邀请功能不可用

更新应用，将 `smtp_enabled` 设置为 `true`，并填写 SMTP 地址、端口、用户名和密码。

### 附件上传失败

确认 Object Storage 存储桶及其自动生成的访问 Secret 已进入 Ready。Budibase 会使用该存储桶保存附件和其他全部对象存储内容。

### 获取帮助

- [Budibase 文档](https://docs.budibase.com/docs)
- [Budibase GitHub Issues](https://github.com/Budibase/budibase/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Budibase 整体采用 GPLv3。客户端与组件库采用 MPL 2.0，付费功能采用 Business Source License，详情参阅 [Budibase 许可说明](https://github.com/Budibase/budibase/blob/3.41.1/LICENSE)。
