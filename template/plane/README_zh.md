# 在 Sealos 上部署和托管 Plane

Plane 是一款开源项目管理平台，可用于跟踪任务、迭代、模块、页面和产品路线图。该模板会在 Sealos Cloud 上部署完整的 Plane 多服务架构，并集成托管 PostgreSQL、托管 Redis 与对象存储。

![Plane Logo](logo.png)

## 关于在 Sealos 上托管 Plane

Plane 适合软件、产品和运营团队把工作统一放到一个平台中管理。它将 issue 跟踪、迭代规划、模块管理、页面协作和工作区协同整合在一起，并支持通过 HTTPS 对外提供安全访问。

该 Sealos 模板会在同一个公网域名下，通过路径路由方式部署 Plane 的 Web、API、后台 Worker、管理后台和 Spaces 应用。同时，平台还会自动创建由 KubeBlocks 托管的 PostgreSQL 集群用于存储业务数据，创建由 KubeBlocks 托管的 Redis 集群用于队列与协调，并创建一个私有对象存储 Bucket 用于上传文件和资源。

在主服务对外提供访问前，模板还会自动执行数据库初始化和迁移任务。部署完成后，你可以继续在 Canvas 中通过 AI 对话和资源卡片完成后续运维操作。

## 常见使用场景

- **任务与迭代管理**：适合工程团队管理缺陷、需求、待办列表和交付周期。
- **产品路线规划**：用于组织 epic、module 和版本路线图。
- **跨团队项目协作**：帮助产品、设计、研发和运营团队围绕同一项目协同推进。
- **团队知识与规格沉淀**：借助 Plane 的 pages 和 spaces，把规划文档与执行过程放在一起管理。
- **自托管工作管理平台**：在自有基础设施上运行私有项目管理系统，自主掌控数据和访问权限。

## Plane 托管依赖

该 Sealos 模板已包含生产可用 Plane 部署所需的全部核心依赖：

- Plane 应用组件（`web`、`api`、`worker`、`beat-worker`、`admin`、`space`）
- KubeBlocks 托管 PostgreSQL 集群，用于 Plane 业务数据存储
- KubeBlocks 托管 Redis 集群（含 Sentinel），用于队列和服务协调
- Sealos ObjectStorage Bucket 与凭证注入，用于文件上传
- Kubernetes Job，用于数据库初始化与迁移
- Kubernetes Service 与 Ingress 资源，用于内部路由和公网 HTTPS 访问

### 部署依赖资源

- [Plane 官方网站](https://plane.so/) - 产品概览与服务介绍
- [Plane 文档](https://docs.plane.so/) - 官方使用与管理文档
- [Plane GitHub 仓库](https://github.com/makeplane/plane) - 源码、版本和问题追踪
- [Sealos 文档](https://sealos.run/docs) - 平台使用与运维说明

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Plane Web**（`makeplane/plane-frontend:v0.22-dev`）：主 Web 应用，挂载在 `/`
- **Plane API**（`makeplane/plane-backend:v0.22-dev`）：后端 API 与认证服务，对外暴露 `/api` 和 `/auth`
- **Plane Worker**（`makeplane/plane-backend:v0.22-dev`）：负责异步任务处理的后台 Worker
- **Plane Beat Worker**（`makeplane/plane-backend:v0.22-dev`）：负责周期性任务调度的调度器服务
- **Plane Admin**（`makeplane/plane-admin:v0.22-dev`）：实例管理后台，挂载在 `/god-mode`
- **Plane Space**（`makeplane/plane-space:v0.22-dev`）：Space 前端应用，挂载在 `/spaces`
- **PostgreSQL 集群**：由 KubeBlocks 托管，用于持久化 Plane 业务数据
- **Redis 集群 + Sentinel**：提供队列、缓存和服务协调能力
- **对象存储 Bucket**：用于持久化上传文件和静态资源
- **初始化任务**：一个 Job 负责创建 `plane` 数据库，另一个 Job 负责执行后端迁移

**配置：**

- 公网入口：
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- 路径路由规则：
  - `/` 路由到 Plane Web
  - `/api` 和 `/auth` 路由到 Plane API
  - `/spaces` 路由到 Plane Space
  - `/god-mode` 路由到 Plane Admin
- PostgreSQL、Redis 和对象存储凭证会通过 Kubernetes Secret 自动注入。
- 文件上传默认限制为 `5242880` 字节。
- 所有核心应用组件默认都以单副本方式启动。

**许可证信息：**

Plane 使用 [GNU Affero General Public License v3.0](https://github.com/makeplane/plane/blob/preview/LICENSE.txt)。

## 为什么在 Sealos 上部署 Plane？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可简化从部署到日常运维的完整流程。将 Plane 部署到 Sealos，你可以获得：

- **一键部署**：无需手工编排 PostgreSQL、Redis、对象存储、Ingress 和后台 Worker，即可快速拉起完整 Plane 栈。
- **Kubernetes 原生可靠性**：基于成熟的 Kubernetes 资源模型运行，并内置服务发现与 HTTPS Ingress。
- **托管数据服务**：直接使用 KubeBlocks 提供的 PostgreSQL 和 Redis，无需自行维护这些依赖。
- **便捷 Day-2 运维**：通过 Canvas 的 AI 对话和资源卡片持续调整配置与资源。
- **内置持久化存储**：数据库数据、Redis 状态和上传文件在服务重启后仍可保留。
- **公网访问开箱即用**：自动获得带 TLS 的公网访问地址。
- **按量使用更高效**：按实际工作负载使用云资源，避免基础设施浪费。

将 Plane 部署在 Sealos 上，把精力放在项目协作和交付推进上，而不是底层基础设施管理。

## 部署指南

1. 打开 [Plane 模板](https://sealos.run/products/app-store/plane) 并点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - `app_host`：Plane 对外访问域名的前缀
   - `app_name`：Kubernetes 资源名前缀
3. 等待部署完成（通常 2-3 分钟）。部署完成后会自动跳转到 Canvas。后续如需调整，可在 AI 对话中描述需求，或点击相关资源卡片修改设置。
4. 使用生成的公网地址访问 Plane：
   - **主工作区界面**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/`
   - **Spaces 界面**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/spaces`
   - **管理后台**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/god-mode`
   - **API 基础路径**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/api`
5. 如果是全新部署，请先在 Web 界面完成 Plane 初始化，并创建第一个工作区账号。

## 配置

部署完成后，你可以通过以下方式管理 Plane：

- **AI 对话**：直接描述所需变更，由 AI 生成并应用调整。
- **资源卡片**：在 Canvas 中直接修改 Deployment、Service、Ingress、数据库、Redis 或存储资源。
- **Plane Admin UI**：通过 `/god-mode` 路径进入实例级管理界面。

### 模板参数

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `app_host` | 用于生成 Plane 公网访问地址的域名前缀 | `plane-<random>` |
| `app_name` | 当前部署对应的 Kubernetes 资源名前缀 | `plane-<random>` |

### 运维说明

- 如果要调整同一公网域名下的路径结构，需要同步修改相关应用基础 URL 配置。
- Plane 的后台任务依赖 Redis 以及 `worker` / `beat-worker` 两个 Deployment 正常运行。
- 文件上传能力依赖平台创建的对象存储 Bucket 及其注入的访问凭证。

## 扩缩容

如需调整 Plane 的资源规模：

1. 在 Canvas 中打开当前部署。
2. 点击需要调整的资源卡片。
3. 根据实际需求修改 CPU、内存、存储或副本数。
4. 提交变更并观察滚动更新状态。

对大多数部署场景，建议优先扩容 `api`、`worker`、PostgreSQL 和 Redis，再考虑调整前端组件。除非你已经验证过当前 Plane 版本的调度策略，否则建议 `beat-worker` 继续保持单副本。

## 故障排查

### 常见问题

**问题：部署完成后，Plane 地址暂时无法访问**
- 原因：Ingress 配置或 DNS 传播尚未完成。
- 解决方案：等待几分钟后，再从 Canvas 重新打开公网地址。

**问题：后台任务或通知处理延迟**
- 原因：Redis 尚未就绪，或 `worker` / `beat-worker` 部署状态异常。
- 解决方案：检查 Redis 集群状态，并查看后台 Worker 相关 Deployment 的日志。

**问题：文件上传失败**
- 原因：对象存储凭证、Bucket 绑定或 endpoint 配置未正确注入后端服务。
- 解决方案：检查对象存储相关 Secret，并确认 API Deployment 已获得预期的 S3 环境变量。

**问题：应用已启动，但初始化不完整**
- 原因：PostgreSQL 初始化任务或迁移任务未成功执行。
- 解决方案：查看数据库初始化 Job 和 API 迁移 Job 的日志，并确认 PostgreSQL 集群状态正常。

### 获取帮助

- [Plane 文档](https://docs.plane.so/)
- [Plane GitHub Issues](https://github.com/makeplane/plane/issues)
- [Plane GitHub Discussions](https://github.com/makeplane/plane/discussions)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Plane 产品文档](https://docs.plane.so/)
- [Plane Releases](https://github.com/makeplane/plane/releases)
- [Plane 自托管仓库](https://github.com/makeplane/plane)

## 许可证

本 Sealos 模板遵循模板仓库的许可证策略。Plane 项目本身使用 [GNU Affero General Public License v3.0](https://github.com/makeplane/plane/blob/preview/LICENSE.txt)。
