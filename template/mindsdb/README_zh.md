# 在 Sealos 上部署和托管 MindsDB

MindsDB 是一个开源 AI 查询引擎和自动化平台，用于在已连接数据之上构建可控的 AI 系统。此模板会在 Sealos Cloud 上部署带有 PostgreSQL 元数据存储、持久化应用存储、认证和可选 Sealos 对象存储的 MindsDB。

![MindsDB 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mindsdb/website-screenshot.webp)

## 关于托管 MindsDB

MindsDB 提供 Web 编辑器、REST API、MySQL 兼容 API、SQL 执行层、数据集成、智能体、任务和知识库工作流。用户可以连接数据源，用 SQL 查询数据，并基于这些数据构建 AI 自动化能力。

此 Sealos 模板以 StatefulSet 运行 MindsDB，并为 MindsDB 元数据创建 KubeBlocks PostgreSQL 16 数据库。模板会在应用启动前创建 `mindsdb` 和 `kb` 两个数据库，对齐上游 Compose 部署中使用 PostgreSQL 存储应用状态和知识库向量数据的运行方式。

MindsDB 默认通过官方 `MINDSDB_USERNAME` 和 `MINDSDB_PASSWORD` 环境变量启用认证。部署完成后，使用配置的凭据登录 Web UI 或调用 REST API。

## 常见使用场景

- **AI 查询引擎**：连接业务数据源，并通过 MindsDB SQL 查询。
- **自动化智能体**：构建能够在已连接数据之上回答问题或执行工作流的智能体。
- **知识库**：通过 MindsDB 知识库 API 存储和查询结构化或非结构化内容。
- **数据集成网关**：通过统一的 SQL 和 REST 接口暴露已连接的数据系统。
- **自托管 AI 平台**：在自己的云环境中运行带托管 Kubernetes 原语的 MindsDB。

## MindsDB 托管依赖

Sealos 模板包含 MindsDB、PostgreSQL 16、持久化存储、Kubernetes Service、HTTPS Ingress 和 Sealos App 入口。启用对象存储时，模板会为 MindsDB 永久文件存储创建 Sealos Object Storage。

### 部署依赖

- [MindsDB 文档](https://docs.mindsdb.com/) - 官方文档
- [Docker 部署指南](https://docs.mindsdb.com/setup/self-hosted/docker/) - 官方 Docker 部署指南
- [环境变量](https://docs.mindsdb.com/setup/environment-vars) - 官方运行时配置参考
- [自定义配置](https://docs.mindsdb.com/setup/custom-config) - 官方存储和 API 配置指南
- [REST API 查询参考](https://docs.mindsdb.com/rest/sql) - SQL 执行 API
- [Minds Platform 仓库](https://github.com/mindsdb/minds-platform) - 源代码和上游部署文件

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **MindsDB 应用**：运行 `mindsdb/mindsdb:v26.1.0`，提供 Web UI、REST API 和 MySQL 兼容 API。
- **PostgreSQL**：由 KubeBlocks 管理的 PostgreSQL 16.4 数据库，用于 MindsDB 元数据和知识库存储。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并幂等创建 `mindsdb` 和 `kb` 数据库。
- **持久卷**：挂载到 `/mindsdb/var` 的 `1Gi` 卷，用于 local 文件存储模式下的运行时文件、静态 GUI 资产、缓存、日志和上传内容。
- **可选对象存储**：选择 `sealos-objectstorage` 时，为 MindsDB 永久文件存储创建 Sealos `ObjectStorageBucket`。
- **Ingress 和 App 入口**：Sealos 通过 HTTPS URL 暴露 MindsDB，并创建可直接访问的仪表盘入口。

**配置：**

模板会要求填写：

- `admin_username`：Web UI 和 REST API 的管理员用户名。
- `admin_password`：Web UI 和 REST API 的管理员密码。
- `file_storage`：选择 `local` 使用持久卷文件存储，或选择 `sealos-objectstorage` 使用 S3 兼容永久存储。

MindsDB 以 `MINDSDB_APIS=http,mysql` 运行，因此 Web UI 和 REST API 暴露在 `47334` 端口，MySQL 兼容 API 可通过同命名空间内 Service 的 `47335` 端口访问。PostgreSQL 凭据来自 Sealos 管理的 KubeBlocks 连接密钥。

启用对象存储时，容器会在启动时使用 Sealos bucket、access key、secret key 和内部 S3 endpoint 生成 MindsDB 配置文件。

**许可证信息：**

Minds Platform 是开源项目，遵循上游仓库许可证。此 Sealos 模板是用于在 Sealos Cloud 上运行 MindsDB 的部署配置。

## 为什么在 Sealos 上部署 MindsDB？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一了从部署到生产运维的应用生命周期。在 Sealos 上部署 MindsDB，你可以获得：

- **一键部署**：通过一个模板部署 MindsDB、PostgreSQL、持久化存储、网络和 App 入口。
- **Kubernetes 原生运行时**：在带内部服务发现的托管 Kubernetes 原语上运行 MindsDB。
- **内置持久化存储**：让应用文件和元数据在重启后继续保留。
- **托管数据库初始化**：自动创建 PostgreSQL 资源和所需数据库。
- **可选对象存储**：为 MindsDB 永久文件存储使用 Sealos 管理的 S3 兼容 bucket。
- **即时公网访问**：自动获得 Web 编辑器和 REST API 的 HTTPS URL。
- **按量资源**：以经过实测的资源配置起步，并随工作负载增长扩展。

在 Sealos 上部署 MindsDB，可以运行自托管 AI 查询和自动化平台，同时减少手写 Kubernetes 清单的工作。

## 部署指南

1. 打开 [MindsDB 模板](https://sealos.io/products/app-store/mindsdb)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `admin_username`：MindsDB 登录用户名。
   - `admin_password`：MindsDB 登录密码。
   - `file_storage`：选择 `local` 或 `sealos-objectstorage`。
3. 等待部署完成，通常需要 2-3 分钟。首次冷启动时，PostgreSQL 初始化、MindsDB 数据库迁移和 Web GUI 资产准备会带来更长等待时间。部署后会跳转到 Canvas。后续变更可以在 AI 对话框中描述需求，或点击相关资源卡片修改设置。
4. 通过生成的 URL 访问应用：
   - **MindsDB Web UI**：打开公网 URL，并使用配置的凭据登录。
   - **REST API**：使用同一个公网 URL 调用 `/api/login`、`/api/status` 和 `/api/sql/query` 等端点。
   - **MySQL 兼容 API**：同命名空间内工作负载可通过内部 Service 的 `47335` 端口访问。

## 配置

部署后，你可以通过以下方式配置 MindsDB：

- **MindsDB Web UI**：使用管理员凭据登录，连接数据源、安装集成、运行 SQL 并管理知识库。
- **REST API**：调用 `/api/login` 获取 token，然后使用 `/api/sql/query` 等认证端点。
- **Sealos AI 对话框**：描述环境变量、存储或资源变更，让 AI 应用更新。
- **资源卡片**：在 Canvas 中点击 StatefulSet、PostgreSQL Cluster、Ingress、Service、持久卷或 Object Storage 卡片进行检查和调整。

## 扩展

MindsDB 在冷启动时会执行迁移、启动多个 API，并准备 Web GUI，因此对内存较敏感。此模板基于 Sealos 现场冷启动测试使用 `1Gi` 内存限制。

1. 打开 MindsDB 部署所在的 Canvas。
2. 点击 MindsDB StatefulSet 资源卡片。
3. 当启动、集成安装或查询负载变重时，优先增加内存。
4. 当并发 SQL 查询、智能体或 API 流量增加时，再增加 CPU。
5. 通过对话框应用变更，并在 Canvas 中观察就绪状态。

对于包含大量集成、大文件上传或活跃知识库的生产工作负载，请规划更多内存和存储容量。

## 故障排查

### 登录失败

- 原因：输入的凭据与 `admin_username` 和 `admin_password` 不一致。
- 解决：使用部署时填写的值，或在 StatefulSet 上更新 `MINDSDB_USERNAME` 和 `MINDSDB_PASSWORD` 后重启 Pod。

### `/api/databases` 或 `/api/projects` 发生跳转

- 原因：MindsDB 会将部分集合端点规范化为带尾部斜杠的路径。
- 解决：直接调用 `/api/databases/` 和 `/api/projects/`。

### 启动需要数分钟

- 原因：首次冷启动会执行 PostgreSQL 初始化、数据库创建、MindsDB 迁移和 GUI 资产准备。
- 解决：等待 StatefulSet Pod 变为 ready。启动期间发生 OOMKilled 时增加内存。

### 知识库向量存储

- 原因：上游 Compose 使用支持 pgvector 的 PostgreSQL 为 `KB_PGVECTOR_URL` 提供存储。
- 解决：模板会创建 PostgreSQL 16.4 和 `kb` 数据库。依赖大量向量能力的知识库工作负载，请先确认你的 Sealos PostgreSQL 环境支持 pgvector 扩展。

### 获取帮助

- [MindsDB 文档](https://docs.mindsdb.com/)
- [Minds Platform GitHub Issues](https://github.com/mindsdb/minds-platform/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [MindsDB REST API](https://docs.mindsdb.com/rest/overview)
- [MindsDB SQL Query API](https://docs.mindsdb.com/rest/sql)
- [MindsDB 自定义配置](https://docs.mindsdb.com/setup/custom-config)
- [MindsDB Docker 镜像](https://hub.docker.com/r/mindsdb/mindsdb)

## 许可证

此 Sealos 模板遵循仓库模板许可证。Minds Platform 本身遵循上游项目许可证。
