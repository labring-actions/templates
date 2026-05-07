# 在 Sealos 上部署和托管 Harbor

Harbor 是一个开源 OCI 制品仓库，通过访问控制、镜像签名和漏洞扫描帮助你强化软件供应链安全。该模板会在 Sealos Cloud 上部署 Harbor v2.14.0，并集成托管 PostgreSQL、托管 Redis 与对象存储。

![Harbor Logo](logo.png)

## 关于在 Sealos 上托管 Harbor

Harbor 提供私有容器镜像与 OCI 制品的存储和分发能力，支持基于角色的访问控制、项目隔离和策略治理。它还内置漏洞扫描与复制能力，适用于生产级软件交付流程。

该 Sealos 模板将 Harbor 部署为多组件架构：`core`、`portal`、`jobservice`、`registry`、`registryctl` 和 `trivy`。平台会通过 KubeBlocks 自动创建 PostgreSQL 与 Redis，创建用于制品后端存储的 ObjectStorage Bucket，并通过 HTTPS Ingress 对外暴露 Harbor。

部署采用同一公网域名下的路径路由：UI 流量进入 portal，API/Registry 相关路径进入 Harbor core。部署完成后，你可在 Canvas 中通过 AI 对话和资源卡片继续进行运维操作。

## 常见使用场景

- **私有容器仓库**：托管研发和生产流水线所需的内部镜像与 OCI 制品。
- **供应链安全治理**：结合 Trivy 扫描结果和项目策略进行制品准入控制。
- **多团队权限管理**：通过项目隔离和 RBAC 为不同团队提供细粒度权限控制。
- **仓库复制分发**：在 Harbor 实例之间或与外部仓库进行复制，支撑混合云和多地域交付。
- **SBOM 与签名制品管理**：集中存储和管理签名镜像及相关制品。

## Harbor 托管依赖

该 Sealos 模板已包含生产可用 Harbor 所需的全部核心依赖：

- Harbor 组件服务（`core`、`portal`、`jobservice`、`registry`、`registryctl`、`trivy`）
- KubeBlocks 托管 PostgreSQL `16.4.0`
- KubeBlocks 托管 Redis `7.2.7`（replication + sentinel 拓扑）
- Sealos ObjectStorage Bucket 与凭证注入（用于 registry blob 存储）
- Kubernetes Ingress、Service 与持久化存储卷

### 部署依赖资源

- [Harbor 官方网站](https://goharbor.io/) - 产品概览与项目入口
- [Harbor 文档](https://goharbor.io/docs/) - 安装、管理与运维说明
- [Harbor GitHub 仓库](https://github.com/goharbor/harbor) - 源码与问题追踪
- [Sealos 文档](https://sealos.run/docs) - 平台使用与运维指南

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Harbor Core**（`goharbor/harbor-core:v2.14.0`）：API、认证、令牌服务与控制面逻辑
- **Harbor Portal**（`goharbor/harbor-portal:v2.14.0`）：Web UI 前端
- **Harbor Jobservice**（`goharbor/harbor-jobservice:v2.14.0`）：后台任务服务（复制、扫描、GC 相关流程）
- **Harbor Registry**（`goharbor/registry-photon:v2.14.0`）：OCI Registry 服务，使用 S3 兼容后端
- **Harbor Registry Controller**（`goharbor/harbor-registryctl:v2.14.0`）：Registry 控制平面辅助服务
- **Harbor Trivy Adapter**（`goharbor/trivy-adapter-photon:v2.14.0`）：漏洞扫描服务
- **PostgreSQL 集群**：存储 Harbor 元数据与业务数据
- **Redis 集群 + Sentinel**：提供任务队列、缓存与协调能力
- **对象存储 Bucket**：持久化镜像层与制品数据

**配置：**

- 必填部署参数：
  - `harbor_admin_password`：Harbor `admin` 初始登录密码
- 自动生成默认值：
  - `app_name`、`app_host` 以及 Harbor/Registry 内部密钥
- 公网入口：
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- 路径路由规则：
  - `/` 路由到 Harbor portal
  - `/api/`、`/service/`、`/v2/`、`/c/` 路由到 Harbor core

**许可证信息：**

Harbor 使用 [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 Harbor？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可简化从部署到日常运维的完整流程。将 Harbor 部署到 Sealos，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单，即可快速启动完整 Harbor 多组件架构。
- **Kubernetes 原生可靠性**：基于成熟 Kubernetes 资源模型，配套托管 Ingress 与服务发现。
- **内置持久化存储**：元数据、队列状态、任务日志和扫描缓存可在重启后保持持久。
- **托管 HTTPS 访问**：自动获得公网访问地址与 TLS 证书能力。
- **便捷 Day-2 运维**：通过 Canvas 的 AI 对话与资源卡片持续调整配置。
- **按量计费更高效**：按实际负载使用资源，避免不必要的基础设施开销。

将 Harbor 部署在 Sealos 上，把精力聚焦在制品治理，而不是底层基础设施管理。

## 部署指南

1. 打开 [Harbor 模板](https://sealos.io/products/app-store/harbor) 并点击 **Deploy Now**。
2. 在弹窗中配置必填参数：
   - `harbor_admin_password`（用于初始 `admin` 登录）
3. 等待部署完成（通常 2-3 分钟）。部署完成后会自动跳转到 Canvas。后续如需调整，可在 AI 对话中描述需求，或通过资源卡片修改具体配置。
4. 访问 Harbor：
   - **Web UI**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
   - **Registry API**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`
5. 使用以下凭据登录：
   - 用户名：`admin`
   - 密码：部署时填写的 `harbor_admin_password`

## 配置

部署完成后，你可通过以下方式管理 Harbor：

- **AI 对话**：直接描述所需变更，由 AI 生成并应用调整。
- **资源卡片**：修改 Deployment/StatefulSet、Service、Ingress 和存储配置。
- **Harbor 管理后台**：管理项目、用户、机器人账号、保留策略与复制规则。

### 模板参数

| 参数 | 说明 | 必填 |
| --- | --- | --- |
| `harbor_admin_password` | Harbor `admin` 初始登录密码 | 是 |

## 扩缩容

如需调整 Harbor 资源规模：

1. 在 Canvas 中打开当前部署。
2. 在对应组件卡片中调整资源（如 `core`、`jobservice`、`registry`、`trivy`）。
3. 提交变更并观察滚动更新状态。
4. 高吞吐场景下，优先提升 `registry` 与 `jobservice` 的 CPU/内存，再按需调整 `core` 与 `redis`/`postgresql` 容量。

## 故障排查

### 常见问题

**问题：部署后无法使用 `admin` 登录**
- 原因：初始密码输入错误，或忘记部署时设置的密码值。
- 解决方案：核对部署时填写的 `harbor_admin_password`，必要时按 Harbor 恢复流程重置管理员凭据。

**问题：推送镜像时报请求体大小/代理限制错误**
- 原因：镜像层较大，超出当前 Ingress 代理参数配置。
- 解决方案：在 Canvas 资源卡片中调整 Ingress/body-size 等相关设置后重试。

**问题：漏洞扫描任务延迟或卡住**
- 原因：Trivy 数据库同步慢，或扫描组件在资源不足时出现堆积。
- 解决方案：检查 `trivy` Pod 日志，确认外网连通性，并按需提升扫描组件资源。

**问题：Harbor 域名部署后短时间不可访问**
- 原因：Ingress 生效或 DNS 传播尚未完成。
- 解决方案：等待几分钟后从 Canvas 重新打开访问地址。

### 获取帮助

- [Harbor 文档](https://goharbor.io/docs/)
- [Harbor GitHub Issues](https://github.com/goharbor/harbor/issues)
- [Sealos 文档](https://sealos.run/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Harbor 安装与配置](https://goharbor.io/docs/main/install-config/)
- [Harbor 管理指南](https://goharbor.io/docs/main/administration/)
- [Harbor 制品复制](https://goharbor.io/docs/main/administration/configuring-replication/)
- [Harbor 漏洞扫描](https://goharbor.io/docs/main/administration/vulnerability-scanning/)

## 许可证

本 Sealos 模板遵循模板仓库的许可证策略。Harbor 项目本身使用 [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE)。
