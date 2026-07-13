# 在 Sealos 上部署和托管 AppFlowy

AppFlowy 是一个开源协作工作空间，支持文档、数据库、看板和团队实时协作。这个模板会在 Sealos 上部署 AppFlowy Cloud 0.16.5 后端组件与 AppFlowy Web 0.15.5。

![AppFlowy 工作空间](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/appflowy/website-screenshot.webp)

## 关于 AppFlowy 托管

AppFlowy 提供类似 Notion 的工作空间体验，支持页面、富文本编辑、团队空间和结构化知识管理。托管版 Web 客户端会连接 AppFlowy Cloud，用于工作空间数据、身份认证、协作 API、WebSocket 同步和后台导入导出任务。

PostgreSQL 通过 KubeBlocks 创建并启用 pgvector，Redis 通过 KubeBlocks 提供缓存和后台任务协调。文件存储默认使用固定版本的私有 MinIO 和持久卷；启用存储选项后会改用 Sealos 托管对象存储桶。

核心运行组件包括 Web、Cloud、Worker、GoTrue、PostgreSQL、Redis 和一个 S3 兼容存储后端。上游 0.16.5 组件包还提供 Search、Admin Frontend 和 AI 服务；这个模板默认关闭这些可选服务，以控制基础资源占用。

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
- 默认部署带 1Gi 持久卷的内置 MinIO，也可选择 Sealos 对象存储

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
- **PostgreSQL**：通过 KubeBlocks 创建并启用 pgvector。
- **Redis**：默认选择外接 Redis，用于缓存和后台任务协调。
- **对象存储**：启用 `use_sealos_objectstorage` 时使用 Sealos 托管的 S3 兼容存储桶。
- **内置 MinIO**：关闭 `use_sealos_objectstorage` 时创建固定版本的 MinIO StatefulSet、持久卷和 HTTPS API 地址。

### 配置方式

AppFlowy Web 客户端启动时会收到三个公开地址：

- `APPFLOWY_BASE_URL`：主应用地址
- `APPFLOWY_GOTRUE_BASE_URL`：独立的 GoTrue 认证公网地址
- `APPFLOWY_WS_BASE_URL`：主应用域名下的 WebSocket 地址

Cloud 和 Worker 服务通过 Kubernetes 内部服务发现连接 PostgreSQL、Redis 和 GoTrue。启动 init container 会等待这些依赖就绪，再启动应用进程。Redis 端点已经指向这个模板创建的 KubeBlocks Redis 数据服务。

启用 Sealos 对象存储时，后端 S3 流量会经过固定版本的私网 OpenResty 兼容代理，浏览器访问的预签名 URL 继续使用公网 HTTPS 端点。代理会为批量清理请求补充 Sealos 对象存储所需的 `Content-MD5` 请求头，然后转发到存储服务。

AppFlowy Cloud 使用 `/api/ready` 作为启动、存活和就绪检查端点。GoTrue 拥有独立公网地址，负责服务管理与身份认证。

### 资源规格

模板经过真实部署测试，并调整到以下最小资源规格：

| 组件 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: |
| AppFlowy Web | 100m | 256Mi | - |
| GoTrue | 100m | 128Mi | - |
| AppFlowy Cloud | 100m | 256Mi | - |
| AppFlowy Worker | 100m | 128Mi | - |
| PostgreSQL | 500m | 512Mi | 1Gi |
| Redis 数据节点 | 500m | 512Mi | 1Gi |
| Redis Sentinel | 500m | 512Mi | 1Gi |
| 内置 MinIO（可选） | 500m | 512Mi | 1Gi |
| Sealos S3 兼容代理（可选） | 100m | 128Mi | - |

注册、页面创建、编辑、重载和 S3 清理实测确定了这些最小档位：Web 与 Cloud 都在 128Mi 档位触及上限，因此使用 256Mi 档位。团队规模扩大后，建议先提高 AppFlowy Cloud 的内存，再根据工作空间规模和访问量调整 PostgreSQL 与 Redis。

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
- **按量付费**：从模板默认规格起步，随着工作空间负载增长逐步扩容。

## 部署指南

1. 打开 [AppFlowy 模板](https://sealos.io/products/app-store/appflowy)，点击 **Deploy Now**。
2. 配置必填参数：
   - **Use Sealos Object Storage**：保持关闭会部署内置 MinIO；启用后会创建 Sealos 托管存储桶。
   - **GoTrue admin email**：GoTrue 初始管理员邮箱。
   - **GoTrue admin password**：GoTrue 初始管理员密码。请在部署时设置并保存这个值。
3. 点击 **Deploy**，等待 2–3 分钟，让 App、PostgreSQL、Redis、存储和公网路由进入就绪状态。完成后 Sealos 会打开 Canvas。
4. 从部署结果或 App 资源卡片打开 AppFlowy 地址。
5. 在 `/login?action=signUpPassword` 注册工作空间用户，然后进入 `/app`。

## 登录和注册

AppFlowy 会从主应用地址进入 `/app`。已有用户可以在 Web 登录页使用工作空间邮箱和密码登录。

新用户通过 `/login?action=signUpPassword` 使用邮箱和密码注册。GoTrue 已启用邮箱自动确认，AppFlowy Cloud 会创建用户资料和默认工作空间，随后打开 `/app`。

部署时填写的 `gotrue_admin_email` 和 `gotrue_admin_password` 会创建独立的 GoTrue 服务管理员。GoTrue 管理使用这组凭据，AppFlowy 工作空间用户通过 Web 注册创建。

## 配置参数

| 参数 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `use_sealos_objectstorage` | `false` | 是 | 启用时使用 Sealos 托管存储桶；关闭时部署固定版本的 MinIO。 |
| `gotrue_admin_email` | 部署时填写 | 是 | GoTrue 服务管理员邮箱。AppFlowy 工作空间用户请通过 Web 注册创建。 |
| `gotrue_admin_password` | 部署时填写 | 是 | GoTrue 服务管理员密码。部署时设置并保存。 |

## 扩缩容

部署后可以按以下方式调整 AppFlowy 资源：

1. 打开 AppFlowy 部署对应的 Canvas。
2. 点击 AppFlowy Cloud、Web、Worker、PostgreSQL 或 Redis 资源卡片。
3. 根据负载需要提高 CPU、内存或存储。
4. 应用修改并等待相关 Pod 重启完成。

多数场景下，建议先提高 AppFlowy Cloud 和 PostgreSQL 资源，再考虑增加 Web 客户端资源。

## 故障排查

### 无法注册或登录

- 在 `/login?action=signUpPassword` 创建工作空间用户，AppFlowy Cloud 会在这个流程中初始化用户资料。
- GoTrue 独立管理界面使用 `gotrue_admin_email` 和 `gotrue_admin_password`。
- 排查认证服务就绪状态时访问 GoTrue `/health`。

### 页面能打开但工作空间操作失败

- 在主应用地址访问 `/api/ready`，检查 AppFlowy Cloud 就绪状态。
- 从 Sealos Canvas 查看 AppFlowy Cloud 日志。
- 确认 PostgreSQL 和 Redis 资源卡片处于运行状态。

### 文件上传或导入失败

- 启用 Sealos 对象存储时，确认存储桶资源和桶级凭据已经就绪。
- 启用 Sealos 对象存储时，确认私网 S3 兼容代理处于就绪状态。
- 关闭 Sealos 对象存储时，确认 MinIO StatefulSet、1Gi 持久卷、Service 和存储 Ingress 已经就绪。

## 相关资源

- [AppFlowy 官网](https://www.appflowy.com/)
- [AppFlowy GitHub](https://github.com/AppFlowy-IO/AppFlowy)
- [AppFlowy Cloud GitHub](https://github.com/AppFlowy-IO/AppFlowy-Cloud)
- [AppFlowy 文档](https://docs.appflowy.io/)
- [Sealos 文档](https://sealos.io/docs)

## 许可

这个 Sealos 模板遵循模板仓库的许可证。AppFlowy 和 AppFlowy Cloud 使用 GNU Affero General Public License v3.0 许可。
