# 在 Sealos 上部署和托管 Clouisle

Clouisle 是开源 AI 智能体平台，提供可视化工作流、RAG 知识库、工具集成和团队管理。本模板会部署 Clouisle `v0.3.0-beta.4`，并配置 PostgreSQL、Redis、Qdrant、后台任务、可选沙箱任务进程和可选的 Sealos S3 兼容对象存储。

![Clouisle 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/clouisle/website-screenshot.webp)

## 关于托管 Clouisle

Clouisle 由 React Web 界面、FastAPI 后端、Celery 任务、PostgreSQL 元数据与词法检索、Redis 队列和 Qdrant 向量检索组成。默认部署提供核心知识库和智能体平台；可选沙箱任务进程会独立运行代码与命令作业。

本模板保留官方 Compose 的单实例拓扑，并使用 KubeBlocks 托管 PostgreSQL 和 Redis。上传文件默认写入共享持久卷；启用 S3 存储后，模板会创建私有 Sealos ObjectStorageBucket，并在数据库迁移完成后写入 Clouisle 存储设置。

## 常见使用场景

- **AI 智能体工作空间**：创建团队级智能体，并接入获准使用的模型服务商和工具。
- **可视化工作流自动化**：组合 LLM、工具、条件和 HTTP 节点；启用沙箱后可增加隔离的代码与命令执行。
- **RAG 知识库**：上传文档，使用词法、向量或混合检索。
- **多团队管理**：管理用户、角色、模型权限、配额、审计日志和站点设置。

## Clouisle 托管依赖

模板包含所选官方版本使用的全部运行依赖：

- Clouisle 前端、API、任务进程和 Beat 调度器 `0.3.0-beta.4`，以及同版本的可选沙箱任务进程
- KubeBlocks PostgreSQL 16.4.0，以及 `pg_search` 0.24.3 和 `pg_stat_statements`
- 带 Sentinel 的 KubeBlocks Redis 7.2.7
- 带持久化存储的 Qdrant 1.18.3
- 共享 1 GiB 上传卷或私有 Sealos ObjectStorageBucket
- Sealos Service、HTTPS Ingress 和 App 入口

### 部署依赖

- [Clouisle 官网](https://clouisle.asia/) - 官方产品网站
- [Clouisle GitHub 仓库](https://github.com/clouisle/clouisle) - 源码与版本发布
- [Clouisle v0.3.0-beta.4](https://github.com/clouisle/clouisle/releases/tag/v0.3.0-beta.4) - 本模板部署的版本
- [Clouisle 用户指南](https://github.com/clouisle/clouisle/tree/v0.3.0-beta.4/docs/guide) - 产品与管理文档

### 实现细节

**架构组件：**

- **前端**：在 `3000` 端口提供浏览器界面。
- **API**：运行 FastAPI 应用、数据库迁移、认证上传代理和 `8000` 端口的公共 API。
- **Worker 和 Beat**：执行 Celery 后台任务与定时任务。
- **沙箱任务进程**：按部署选项通过 rootless Bubblewrap 运行隔离的代码与制品作业。
- **PostgreSQL**：保存账户、团队、智能体、工作流、知识元数据、站点设置和 BM25 词法索引。
- **Redis 和 Sentinel**：提供队列、缓存与协调能力。
- **Qdrant**：保存语义检索与混合检索所需的向量嵌入。
- **上传存储**：部署时选择共享本地 PVC 或私有 S3 兼容存储桶。

KubeBlocks 当前提供 PostgreSQL 16.4.0。本模板安装 ParadeDB 官方 PostgreSQL 16 版 `pg_search` 0.24.3 软件包，校验其 SHA-256 摘要，将 `pg_search` 和 `pg_stat_statements` 加入 `shared_preload_libraries`，创建两个扩展，并等待 Clouisle BM25 迁移完成。这一兼容边界已经通过 Clouisle `v0.3.0-beta.4` 运行验证，其中包括 `knowledge_lexical_chunks_bm25_idx` 索引。

S3 分支会验证私有存储桶，再写入 Clouisle 存储设置。本地分支会在 API 和 Worker 中挂载同一份上传持久卷；启用沙箱后，该进程也会挂载此卷。这些进程会调度到 API 卷所在节点。

Sealos HTTP Ingress 约定使用 `32m` 请求体上限。本模板把 Clouisle 知识库文档上限初始化为 31 MiB，为 multipart 请求预留空间，让超限请求由应用清晰返回。上游 Helm 使用 `100m`；当前较窄上限属于 Sealos 平台约定边界。

**许可证信息：**

Clouisle 使用 [GNU General Public License v3.0](https://github.com/clouisle/clouisle/blob/v0.3.0-beta.4/LICENSE)。

## 为什么在 Sealos 上部署 Clouisle？

Sealos 在一个 Canvas 中整合 Kubernetes 应用编排、托管数据库、对象存储、HTTPS 网络和生命周期管理。本模板把官方多服务拓扑整合为一次可配置部署，并让每项服务保持独立资源卡片。

- **一键部署拓扑**：通过一个应用商店表单创建完整 Clouisle 技术栈。
- **存储选项**：选择持久化本地卷或私有 Sealos 对象存储。
- **托管数据服务**：通过 KubeBlocks 资源卡片管理 PostgreSQL 和 Redis。
- **即时 HTTPS 访问**：就绪检查完成后打开自动生成的公共地址。
- **AI 辅助运维**：在 Canvas 对话框中描述配置变更，也可以直接编辑资源卡片。

## 部署指南

1. 打开 [Clouisle 模板](https://sealos.io/products/app-store/clouisle)，点击 **Deploy Now**。
2. 需要私有 Sealos ObjectStorageBucket 时启用 **Enable S3 Storage**；默认选项使用本地持久化上传卷。
3. 标准 Sealos 工作空间保持 **Enable Sandbox** 关闭。工作空间允许 `Unconfined` seccomp 或提供等效且已安装的 `Localhost` 配置时可以启用该选项。
4. 等待资源就绪。核心资源通常会在 2-3 分钟内出现，首次 PostgreSQL `pg_search` 初始化可能会增加几分钟。
5. 从 Canvas 打开生成的 Clouisle HTTPS 地址。

## 注册和登录

本模板使用 Clouisle 的首次注册引导流程。初始凭据由你在浏览器中创建：

1. 打开生成的 Clouisle 地址，选择 **Register**。
2. 输入唯一用户名、邮箱地址和密码。当前版本的默认策略要求至少 8 个字符、一个大写字母和一个数字；特殊字符为可选项。
3. 提交表单。首个注册账户会自动激活、标记邮箱已验证，并获得 **Super Admin** 角色。
4. 使用相同的用户名或邮箱及密码登录。
5. 创建团队，然后进入 **Knowledge Bases** 或 **Workflows** 开始使用。

后续注册会遵循首位管理员配置的审核、邮箱验证、验证码、默认团队和角色策略。智能体模型调用和向量嵌入需要先在管理端模型设置中配置服务商凭据。

## 配置

- **AI 对话框**：在 Canvas 中描述资源或环境变量调整需求。
- **资源卡片**：调整单个工作负载、存储、网络设置或数据库资源。
- **上传存储**：在首次部署时选择存储后端，升级时保留对应存储桶或上传 PVC。
- **上传大小**：Sealos `32m` Ingress 范围内的知识库文档上限为 31 MiB。
- **代码与命令沙箱**：工作空间安全策略支持 rootless Bubblewrap 的命名空间和挂载隔离时启用沙箱选项。
- **模型服务商**：使用 Super Admin 登录，打开模型管理页面，添加服务商凭据、测试连接，并向目标团队授权模型。
- **站点安全**：在 Clouisle 站点设置中配置注册审核、邮箱验证、验证码、密码策略和 SSO。

## 资源配置

默认部署的核心角色通过了冷启动、注册、团队与知识库创建、文件上传和下载、检索以及 60 秒稳定窗口验证，活动故障和容器重启均为零。下表保留兼容工作空间使用的可选沙箱任务进程档位：

| 组件 | CPU | 内存 |
| --- | ---: | ---: |
| API | `100m` | `1024Mi` |
| Worker | `100m` | `1024Mi` |
| 沙箱任务进程 | `100m` | `256Mi` |
| Beat 调度器 | `100m` | `256Mi` |
| 前端 | `100m` | `128Mi` |
| Qdrant | `100m` | `128Mi` |
| PostgreSQL | `500m` | `512Mi` |
| Redis | `500m` | `512Mi` |
| Redis Sentinel | `500m` | `512Mi` |

稳定状态下的实测内存约为：API 297 MiB、Worker 607 MiB、沙箱任务进程 212 MiB、Beat 212 MiB、前端 70 MiB、Qdrant 16 MiB。API 的 512 MiB 候选配置在接收 40 MiB 超限回归请求时触发 OOM，因此 1024 MiB 是当前上传边界下的最低稳定档位。Worker 和 Beat 的实测工作负载也已超过下一档更低内存。沙箱档位来自任务进程观测；Bubblewrap 实际执行需要兼容工作空间，当前 baseline 准入策略未覆盖此项验证。PostgreSQL 与 Redis 保持 KubeBlocks 数据库资源约定。

## 故障排查

### 首次部署耗时较长

PostgreSQL 初始化会下载并验证固定版本的 `pg_search` 软件包，更新托管 PostgreSQL 配置，并等待扩展与 BM25 迁移完成。保留 PostgreSQL 数据卷后，后续 Pod 替换会复用已经验证的软件包。

### 注册状态显示等待审核

首个账户会立即获得 Super Admin 权限。后续账户遵循 **Site Settings → Security** 中的注册和审核策略。

### 知识处理需要模型

在模型管理页面添加支持嵌入的服务商，测试连接，并将该模型授权给知识库所属团队。

### 代码或命令沙箱工具持续排队

Clouisle `v0.3.0-beta.4` 会通过 rootless Bubblewrap 启用用户、PID、IPC、UTS、命名空间和挂载隔离。标准 Sealos 工作空间执行 PodSecurity `baseline:v1.25`，因此模板默认关闭 **Enable Sandbox**。允许任务进程使用文档规定的 `Unconfined` seccomp 配置，或提供等效且已安装的 `Localhost` 配置后，可以使用启用分支。当前版本没有远程沙箱后端。

### 上传失败

确认文件大小处于 31 MiB 知识库上限内。使用本地存储时，确认 API 上传 PVC 已绑定，Worker 已经随 API 卷完成调度；启用沙箱后还需检查沙箱任务进程。使用 S3 存储时，确认 ObjectStorageBucket 和一次性 S3 配置 Job 已就绪。

### 获取帮助

- [Clouisle GitHub Issues](https://github.com/clouisle/clouisle/issues)
- [Clouisle 文档](https://github.com/clouisle/clouisle/tree/v0.3.0-beta.4/docs)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Clouisle 使用 GPL-3.0 许可证。本模板包含在 Sealos 上运行该上游软件所需的部署元数据和文档。
