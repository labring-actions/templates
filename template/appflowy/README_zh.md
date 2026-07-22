# 在 Sealos 上部署和托管 AppFlowy

AppFlowy 是一个开源协作工作空间，支持文档、数据库、看板和团队实时协作。这个模板会在 Sealos 上部署 AppFlowy Cloud 0.16.5、Admin Frontend 0.16.5、AppFlowy Web 0.15.5、AppFlowy Search 0.16.3 及其托管依赖。

![AppFlowy 工作空间](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/appflowy/website-screenshot.webp)

## 关于 AppFlowy 托管

AppFlowy 提供类似 Notion 的工作空间体验，支持页面、富文本编辑、团队空间和结构化知识管理。托管版 Web 客户端会连接 AppFlowy Cloud，用于工作空间数据、身份认证、协作 API、WebSocket 同步和后台导入导出任务。

PostgreSQL 通过 KubeBlocks 创建并启用 pgvector，Redis 通过 KubeBlocks 提供缓存和后台任务协调。文件存储使用 Sealos 托管对象存储桶，并通过私网 S3 兼容代理访问。

运行组件包括 Web、Admin Frontend、Cloud、Worker、Search、GoTrue、PostgreSQL、Redis 和 S3 兼容对象存储。Sealos 会为工作空间和系统管理界面分别创建 Canvas 入口，并通过同一个主应用域名进行路由。可选的 AppFlowy AI 服务保持在本次部署范围之外。

## 常见使用场景

- **团队知识库**：创建共享文档、项目笔记和内部手册。
- **个人效率工作空间**：运行私有笔记、任务和规划空间。
- **自托管协作平台**：把工作空间数据保存在自己的 Sealos 环境中。
- **数据库驱动的项目管理**：用 AppFlowy 数据库组织任务、内容和结构化记录。
- **轻量工作空间替代方案**：部署一个开源的在线工作空间替代品。

## AppFlowy 托管依赖

这个 Sealos 模板包含以下运行依赖：

- AppFlowy Web 客户端
- 用于系统管理的 AppFlowy Admin Frontend
- AppFlowy Cloud API 和 WebSocket 服务
- AppFlowy Worker 后台任务服务
- AppFlowy Search 关键词索引和查询服务
- GoTrue 认证服务
- 启用 pgvector 的 KubeBlocks PostgreSQL
- KubeBlocks Redis
- Sealos 托管对象存储和私网兼容代理

### 部署依赖

- [AppFlowy GitHub 仓库](https://github.com/AppFlowy-IO/AppFlowy) - AppFlowy 主项目
- [AppFlowy Cloud 仓库](https://github.com/AppFlowy-IO/AppFlowy-Cloud) - 自托管云端后端
- [AppFlowy 文档](https://docs.appflowy.io/) - 产品和自托管文档
- [Sealos 应用市场](https://sealos.io/products/app-store) - 一键应用部署

## 实现细节

### 架构组件

这个模板会部署以下服务：

- **AppFlowy Web**：浏览器端 UI，通过主应用地址访问。
- **AppFlowy Admin Frontend**：系统管理界面，通过主应用域名下的 `/console/login` 访问。
- **AppFlowy Cloud**：工作空间、文档、协作和文件元数据的 API 与 WebSocket 后端。
- **AppFlowy Worker**：处理导入、文件相关任务等异步后台任务。
- **AppFlowy Search**：提供持久化关键词索引和搜索查询。
- **GoTrue**：AppFlowy 使用的邮箱和密码认证服务。
- **PostgreSQL**：通过 KubeBlocks 创建并启用 pgvector。
- **Redis**：通过 KubeBlocks 提供缓存和后台任务协调。
- **对象存储**：使用 Sealos 托管的 S3 兼容存储桶和私网 OpenResty 代理。

### 公网入口与路由

Sealos 会创建两个 Canvas App 入口。主域名采用基于路径的 Ingress 路由，因此多个 Ingress 可以共用一个公网域名，并把不同路径转发到对应服务。

| 入口或路由 | URL 形式 | 用途 |
| --- | --- | --- |
| AppFlowy | `https://<app-host>/` | 工作空间注册、登录和 Web 应用 |
| AppFlowy Admin | `https://<app-host>/console/login` | 系统管理界面 |
| Cloud API | `https://<app-host>/api` | AppFlowy Web 和 Admin 的 API 请求 |
| WebSocket | `wss://<app-host>/ws` | 文档与工作空间实时同步 |
| GoTrue | `https://<auth-host>/` | AppFlowy Web 和 Admin 使用的认证 API |

精确路径 `/api/admin/health/postgresql` 是 Admin 健康页使用的兼容接口，会把请求转发到 AppFlowy Cloud 的 PostgreSQL 健康检查处理器。

### 配置方式

AppFlowy Web 客户端启动时会收到应用、认证和 WebSocket 公网地址。Admin Frontend 会收到主应用公网地址与 GoTrue 内部服务地址，并在 Cloud 和 GoTrue 独立完成初始化期间直接提供登录页面。

Cloud、Worker 和 Search 服务通过 Kubernetes 内部服务发现连接 PostgreSQL、Redis 和 GoTrue。它们的 init container 会等待所需数据服务和迁移状态就绪，再启动应用进程。Redis 端点已经指向这个模板创建的 KubeBlocks Redis 数据服务。

后端 S3 流量会经过固定版本的私网 OpenResty 兼容代理，浏览器访问的预签名 URL 使用公网 HTTPS 端点。代理会为批量清理请求补充 Sealos 对象存储所需的 `Content-MD5` 请求头，然后转发到存储服务。Search 复用现有托管桶并关闭建桶动作，实时关键词 Worker 保持运行；最小资源配置关闭可选后台索引任务。

AppFlowy Cloud 使用 `/api/ready` 作为启动、存活和就绪检查端点。GoTrue 是独立的认证 API，同时提供客户端公网端点和集群内部服务端点。

### 资源规格

模板经过真实部署测试，并调整到以下最小资源规格：

| 组件 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: |
| AppFlowy Web | 100m | 256Mi | - |
| AppFlowy Admin | 100m | 128Mi | - |
| GoTrue | 100m | 128Mi | - |
| AppFlowy Cloud | 100m | 256Mi | - |
| AppFlowy Worker | 100m | 128Mi | - |
| AppFlowy Search | 100m | 128Mi | 1Gi |
| PostgreSQL | 500m | 512Mi | 1Gi |
| Redis 数据节点 | 500m | 512Mi | 1Gi |
| Redis Sentinel | 500m | 512Mi | 1Gi |
| Sealos S3 兼容代理 | 100m | 128Mi | - |

工作空间注册、管理员登录、用户搜索、服务健康检查、页面创建、编辑、搜索、鉴权对象上传/读取/删除和 60 秒稳定窗口实测确定了这些最小档位：Web 与 Cloud 都在 128Mi 档位触及上限，因此使用 256Mi 档位。团队规模扩大后，建议先提高 AppFlowy Cloud 的内存，再根据工作空间规模和访问量调整 PostgreSQL 与 Redis。

### 许可信息

AppFlowy 和 AppFlowy Cloud 使用 GNU Affero General Public License v3.0 许可。这个 Sealos 模板只提供部署配置。

## 为什么在 Sealos 上部署 AppFlowy？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端开发到生产部署和运维管理的完整应用生命周期。在 Sealos 上部署 AppFlowy 可以获得：

- **一键部署**：从应用市场部署完整的多服务 AppFlowy 栈。
- **托管依赖**：PostgreSQL、Redis、公网入口、TLS 和对象存储一起创建。
- **持久化存储**：数据库和对象存储数据可在应用重启后保留。
- **公网 HTTPS 访问**：Sealos 自动提供公网地址和 TLS 证书。
- **简单配置**：通过部署表单设置管理员凭据，再通过 Canvas AI 对话或资源卡片调整资源。
- **Kubernetes 原生运维**：不用手写 Kubernetes 清单，也可以调整资源、查看日志和管理服务。
- **按量付费**：从模板默认规格起步，随着工作空间负载增长逐步扩容。

## 部署指南

1. 打开 [AppFlowy 模板](https://sealos.io/products/app-store/appflowy)，点击 **Deploy Now**。
2. 配置必填参数：
   - **GoTrue admin email**：AppFlowy Admin 使用的系统管理员邮箱。
   - **GoTrue admin password**：AppFlowy Admin 使用的系统管理员密码。请在部署时设置并保存这个值。
3. 点击 **Deploy**，等待 2–3 分钟，让 App、Search、PostgreSQL、Redis、对象存储和公网路由进入就绪状态。完成后 Sealos 会打开 Canvas。
4. 根据操作目标选择 Canvas 入口：
   - **AppFlowy** 打开工作空间 Web 应用。
   - **AppFlowy Admin** 打开 `/console/login` 系统管理界面。
5. 从 AppFlowy Web 登录页注册工作空间用户，或使用第 2 步填写的凭据登录 AppFlowy Admin。

## 登录和注册

AppFlowy 提供两套账号流程，对应两个入口：

| 用途 | 入口 | 凭据 |
| --- | --- | --- |
| 创建和使用工作空间 | `https://<app-host>/` 对应的 **AppFlowy** | 通过 AppFlowy Web 注册的工作空间账号 |
| 管理用户和查看服务状态 | `https://<app-host>/console/login` 对应的 **AppFlowy Admin** | 部署时填写的 `gotrue_admin_email` 和 `gotrue_admin_password` |

### 工作空间用户

已有用户可以在 AppFlowy Web 登录页使用工作空间邮箱和密码登录。新用户在登录页选择密码注册，对应路径为 `/login?action=signUpPassword`。GoTrue 已启用邮箱自动确认，AppFlowy Cloud 会创建用户资料和默认工作空间，随后打开 `/app`。

### 系统管理员

`gotrue_admin_email` 和 `gotrue_admin_password` 会创建系统管理员账号。使用这组凭据登录 **AppFlowy Admin**，可以管理用户、邀请、服务健康状态、SAML SSO、AI 设置和环境信息。文档与工作空间的日常使用通过 AppFlowy Web 注册工作空间账号。

独立的 GoTrue 公网域名是 AppFlowy 客户端调用的认证 API。浏览器端管理功能从 Canvas 中的 **AppFlowy Admin** 入口进入。

## 配置参数

| 参数 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `gotrue_admin_email` | 部署时填写 | 是 | AppFlowy Admin 登录页使用的系统管理员邮箱。工作空间用户通过 Web 注册。 |
| `gotrue_admin_password` | 部署时填写 | 是 | AppFlowy Admin 登录页使用的系统管理员密码。部署时设置并保存。 |

部署完成后，可以在 Canvas AI 对话中描述配置修改，也可以打开对应资源卡片调整环境变量和资源。AppFlowy Admin 健康页会显示 PostgreSQL、Redis、S3、Search、GoTrue、AI Embedding 和邮件服务状态；配置 OpenAI 与 SMTP 后，对应检查会转为 Healthy。

## 扩缩容

部署后可以按以下方式调整 AppFlowy 资源：

1. 打开 AppFlowy 部署对应的 Canvas。
2. 点击 AppFlowy Cloud、Web、Worker、PostgreSQL 或 Redis 资源卡片。
3. 根据负载需要提高 CPU、内存或存储。
4. 应用修改并等待相关 Pod 重启完成。

多数场景下，建议先提高 AppFlowy Cloud 和 PostgreSQL 资源，再考虑增加 Web 客户端资源。

## 故障排查

### 不清楚应该打开哪个 URL

- **AppFlowy** Canvas 入口用于工作空间注册、登录、文档和数据库。
- **AppFlowy Admin** Canvas 入口用于用户管理和服务健康检查。
- `/`、`/console`、`/api` 和认证路径分别使用独立 Ingress，让每条路径进入对应服务。

### 初次部署时 Admin 页面显示 404

- 打开以 `/console/login` 结尾的完整 **AppFlowy Admin** 地址。
- 在 Canvas 中确认 AppFlowy Admin Deployment 和公网路由已经就绪。
- 模板会立即启动 Admin 登录页面，公网路由首次同步仍可能需要几秒钟。

### 无法登录 AppFlowy Admin

- 使用部署时填写的 `gotrue_admin_email` 和 `gotrue_admin_password`。
- 在 Canvas 中检查 GoTrue 和 AppFlowy Cloud 资源卡片。

### 无法注册或登录工作空间

- 从 Web 登录页或 `/login?action=signUpPassword` 创建工作空间用户；AppFlowy Cloud 会在这个流程中初始化用户资料和默认工作空间。
- 排查认证服务就绪状态时访问 GoTrue `/health`。

### 页面能打开但工作空间操作失败

- 在主应用地址访问 `/api/ready`，检查 AppFlowy Cloud 就绪状态。
- 从 Sealos Canvas 查看 AppFlowy Cloud 日志。
- 确认 PostgreSQL 和 Redis 资源卡片处于运行状态。

### 文件上传或导入失败

- 确认 Sealos 存储桶资源、共享对象存储凭据和桶名 Secret 已经就绪。
- 确认私网 S3 兼容代理处于就绪状态。
- 确认 Cloud、Worker 和 Search 引用了共享对象存储 Secret，以及这个部署创建的桶名 Secret。

## 相关资源

- [AppFlowy 官网](https://www.appflowy.com/)
- [AppFlowy GitHub](https://github.com/AppFlowy-IO/AppFlowy)
- [AppFlowy Cloud GitHub](https://github.com/AppFlowy-IO/AppFlowy-Cloud)
- [AppFlowy 文档](https://docs.appflowy.io/)
- [Sealos 文档](https://sealos.io/docs)

## 许可

这个 Sealos 模板遵循模板仓库的许可证。AppFlowy 和 AppFlowy Cloud 使用 GNU Affero General Public License v3.0 许可。
