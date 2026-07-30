# 在 Sealos 上部署和托管 Langfuse

Langfuse 是面向 LLM 应用的开源工程平台，提供追踪、提示词管理、评估和可观测性能力。此模板会部署 Langfuse `3.224.2`、PostgreSQL、Redis、ClickHouse、后台 Worker、私有 Sealos 对象存储和公网 HTTPS 入口。

![Langfuse 提示词管理](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/langfuse/website-screenshot.webp)

## 关于在 Sealos 上托管 Langfuse

Langfuse 为 AI 团队提供统一工作区，用于查看追踪、管理提示词版本、评估输出和监控应用质量。Web 服务负责仪表盘、API 与认证，独立 Worker 负责数据摄取和后台任务。

Sealos 模板会一次性创建全部运行依赖。PostgreSQL 保存关系型元数据，Redis 与 Sentinel 处理队列，ClickHouse 通过持久卷保存分析数据，事件、媒体和批量导出对象则保存到私有 Sealos S3 兼容存储桶。

## 常见使用场景

- **LLM 可观测性**：记录 traces、generations、spans、延迟、成本与模型元数据。
- **提示词管理**：创建带版本的文本或对话提示词，并发布 production 标签。
- **评估工作流**：使用分数、数据集、Evaluator 与人工标注队列。
- **应用调试**：搜索追踪，并比较不同版本和环境下的运行行为。

## Langfuse 托管依赖

模板包含 Langfuse Web 与 Worker 镜像、PostgreSQL、Redis、Redis Sentinel、ClickHouse、对象存储、内部 Service、持久卷和 HTTPS Ingress。

### 部署依赖与参考资料

- [Langfuse 文档](https://langfuse.com/docs) - 产品与 SDK 文档
- [Langfuse 自托管指南](https://langfuse.com/self-hosting) - 官方部署说明
- [Langfuse 配置参考](https://langfuse.com/self-hosting/configuration) - 环境变量说明
- [Langfuse 仓库](https://github.com/langfuse/langfuse) - 源代码与版本
- [Sealos 文档](https://sealos.io/docs) - 平台文档

## 实现细节

### 架构组件

- **Langfuse Web**：1 个 `Deployment`，运行 `docker.io/langfuse/langfuse:3.224.2`，服务端口为 `3000`。
- **Langfuse Worker**：1 个 `Deployment`，运行 `docker.io/langfuse/langfuse-worker:3.224.2`，处理数据摄取和后台队列。
- **PostgreSQL**：1 个 KubeBlocks PostgreSQL `16.4.0` 组件，配有 `1Gi` 持久卷。
- **数据库初始化**：幂等 Job 会在应用迁移前创建 `langfuse` 数据库。
- **Redis**：KubeBlocks Redis `7.2.7` replication 拓扑，包含 1 个 Redis 组件与 1 个 Sentinel 组件。
- **ClickHouse**：1 个持久化 `clickhouse/clickhouse-server:25.4.2` StatefulSet，数据与日志各使用 `1Gi` 持久卷。
- **对象存储**：1 个私有 Sealos `ObjectStorageBucket`，保存事件、媒体与批量导出对象。
- **公网访问**：由 Sealos 托管的 HTTPS Ingress 与 Canvas 应用入口。

### 资源规格

| 组件 | 副本数 | CPU 上限 | 内存上限 | 持久存储 |
| --- | ---: | ---: | ---: | ---: |
| Langfuse Web | 1 | `100m` | `2048Mi` | - |
| Langfuse Worker | 1 | `100m` | `512Mi` | - |
| ClickHouse | 1 | `100m` | `256Mi` | `2Gi` |
| PostgreSQL | 1 | `500m` | `512Mi` | `1Gi` |
| Redis | 1 | `500m` | `512Mi` | `1Gi` |
| Redis Sentinel | 1 | `500m` | `512Mi` | `1Gi` |
| init container 与数据库 Job | 每次启动 | `100m` | `128Mi` | - |

此规格已通过评估环境和轻量工作负载验证。请求量或摄取吞吐上升时提高 Web 与 Worker CPU，追踪数据量和查询并发增加时提高 ClickHouse 资源。

### 模板参数

| 参数 | 必填 | 用途 |
| --- | --- | --- |
| `init_user_email` | 否 | 与密码同时填写时创建首个 Langfuse owner |
| `init_user_name` | 否 | 首个 owner 的显示名称 |
| `init_user_password` | 否 | 首个 owner 的登录密码 |

每次部署所需的 salt、加密密钥、认证 Secret、ClickHouse 凭据、数据库凭据与对象存储凭据都会自动生成或由 Sealos 托管。

### 存储与健康检查

- `/api/public/health` 报告进程健康状态，`/api/public/ready` 报告依赖就绪状态。
- PostgreSQL、Redis、Redis Sentinel 与 ClickHouse 通过持久卷保留数据。
- 事件、媒体和批量导出对象通过 path-style 方式访问私有 Sealos 存储桶。
- 原始对象地址需要授权，Langfuse 会为应用工作流生成签名上传与下载地址。
- 应用删除任务使用兼容 S3 的 MD5 multi-delete checksum 清理关联媒体对象。

## 为什么选择 Sealos 部署 Langfuse？

- **完整运行栈**：一次部署仪表盘、Worker、数据库、分析存储与对象存储。
- **托管凭据**：Sealos 创建服务凭据，并自动注入对应工作负载。
- **持久化数据**：PostgreSQL、Redis、ClickHouse 与对象数据可以跨工作负载重启保留。
- **私有对象存储**：事件、媒体和导出对象保存在独立私有存储桶中。
- **公网 HTTPS 入口**：Sealos 提供域名、Ingress 与 TLS 证书。
- **Canvas 运维**：在同一个部署视图中查看日志、资源健康、存储与配置。

## 部署指南

1. 打开 [Langfuse 模板](https://sealos.io/products/app-store/langfuse)，点击 **Deploy Now**。
2. 选择用户接入方式：
   - 填写 `init_user_email`、`init_user_name` 与 `init_user_password`，自动创建首个 owner。
   - 留空用户参数，通过注册页面创建首个账号。
3. 开始部署，等待 PostgreSQL、Redis、ClickHouse、初始化 Job、Langfuse Web 与 Langfuse Worker 全部进入健康状态。冷启动通常需要几分钟。
4. 打开 Canvas 中显示的 HTTPS 应用地址。

## 登录与注册

### 使用初始化账号

1. 打开应用域名下的 `/auth/sign-in`。
2. 输入部署表单中填写的邮箱与密码。
3. 模板会自动创建 `Sealos Langfuse` 组织。
4. 创建项目后，即可使用 **Prompts**、**Tracing**、**Datasets** 或 **Settings > API Keys**。

### 通过页面注册

1. 打开应用域名下的 `/auth/sign-up`。
2. 创建首个账号。
3. 按 Langfuse 引导创建组织与项目。
4. 连接 SDK 前，前往 **Settings > API Keys** 创建项目 API 密钥。

## 配置说明

项目、提示词、API 密钥、模型定义、Evaluator、数据集与成员都通过 Langfuse 仪表盘管理。工作负载资源、持久卷、日志、域名与环境配置则通过 Sealos Canvas 管理。

私有对象存储桶属于每次部署的固定组成部分，因为 Langfuse `3.224.2` 使用 S3 兼容存储处理事件摄取、媒体和导出。

## 扩缩容

队列延迟增加时提高 Worker CPU 或副本数，仪表盘与 API 流量增加时提高 Web CPU 或副本数，追踪数据量和分析查询增加时提高 ClickHouse CPU、内存与存储。

添加副本前，请先评估 Langfuse 并发要求与数据库容量。扩展无状态 Web 和 Worker 时，应保留当前持久化 ClickHouse StatefulSet 与托管数据服务。

## 故障排查

### 应用地址仍处于启动状态

冷部署会在仪表盘就绪前执行 PostgreSQL 与 ClickHouse 迁移。请在 Canvas 中检查 PostgreSQL 集群、Redis 集群、ClickHouse StatefulSet、初始化 Job 与 Web 日志。

### 无法登录

自动初始化部署请在 `/auth/sign-in` 使用模板表单中的邮箱与密码。交互式接入请在 `/auth/sign-up` 创建首个账号。

### 媒体或事件上传失败

请确认 `ObjectStorageBucket` 已就绪，并确认两个 Langfuse Deployment 都引用了 Sealos 托管的对象存储 Secret。

### Web Pod 以 137 退出

Langfuse Web 启动阶段需要已验证的 `2048Mi` 内存上限。请保留该上限，大型部署可以继续提高内存。

### 获取帮助

- [Langfuse Issues](https://github.com/langfuse/langfuse/issues)
- [Langfuse 自托管文档](https://langfuse.com/self-hosting)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Langfuse 核心产品能力采用 [MIT License](https://github.com/langfuse/langfuse/blob/main/LICENSE)。部分企业功能需要上游商业许可证。此 Sealos 模板按 templates 仓库许可证分发。
