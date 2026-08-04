# 在 Sealos 上部署和托管 Harbor

Harbor 是一款开源 OCI 制品仓库，提供基于角色的访问控制、漏洞扫描、复制和制品治理能力。该模板会在 Sealos Cloud 上部署 Harbor v2.15.2、由 KubeBlocks 托管的 PostgreSQL 与 Redis，并支持 Sealos S3 兼容对象存储和 Registry 持久卷两种存储方式。

![Harbor 制品仓库](website-screenshot.webp)

## 关于在 Sealos 上托管 Harbor

Harbor 可以存储和分发容器镜像、Helm Chart、软件物料清单（SBOM）、签名及其他 OCI 制品。项目为团队划分访问边界，机器人账号、保留策略、复制策略和扫描策略则为自动化交付流水线提供支持。

该模板保留 Harbor 的多服务架构，分别部署 `core`、`portal`、`jobservice`、`registry`、`registryctl` 和 `trivy` 工作负载。KubeBlocks 会创建 PostgreSQL 16.4 来保存元数据，并创建带 Sentinel 的 Redis 7.2.7 来承载队列和缓存状态。

同一个 HTTPS 域名同时提供 Web 界面和仓库 API。根路径连接 Portal，`/api/`、`/service/`、`/v2/` 与 `/c/` 连接 Harbor Core。

## 常见使用场景

- **私有容器仓库**：保存研发和生产环境使用的内部镜像与 OCI 制品。
- **软件供应链安全**：通过 Trivy 扫描制品，再将其提升到后续环境。
- **团队权限治理**：使用项目隔离和角色权限管理不同团队。
- **自动化交付**：在 CI/CD 流水线中使用机器人账号。
- **仓库复制**：在 Harbor 与外部仓库之间复制制品。

## Harbor 托管依赖

该模板会创建完整运行环境：

- Harbor v2.15.2 的六个服务：Core、Portal、Jobservice、Registry、Registry Controller 和 Trivy Adapter
- KubeBlocks PostgreSQL 16.4，以及 1 GiB 持久卷
- KubeBlocks Redis 7.2.7 replication 拓扑与 Sentinel
- S3 模式下使用的私有 Sealos ObjectStorageBucket
- 本地文件系统模式下使用的 1 GiB Registry 持久卷
- 持久化的 Jobservice 日志和 Trivy 报告
- HTTPS Ingress 与 Kubernetes 内部服务

### 部署依赖资源

- [Harbor 文档](https://goharbor.io/docs/) - 管理与使用指南
- [Harbor v2.15.2 发布说明](https://github.com/goharbor/harbor/releases/tag/v2.15.2) - 当前模板版本详情
- [Harbor 源码仓库](https://github.com/goharbor/harbor) - 源码与问题追踪
- [Sealos 文档](https://sealos.io/docs) - 平台运维指南

### 实现细节

**架构组件：**

- **Core**（`goharbor/harbor-core:v2.15.2`）：认证、API、令牌服务和控制面逻辑
- **Portal**（`goharbor/harbor-portal:v2.15.2`）：Web 管理界面
- **Jobservice**（`goharbor/harbor-jobservice:v2.15.2`）：扫描、复制、保留和垃圾回收任务
- **Registry**（`goharbor/registry-photon:v2.15.2`）：OCI 分发服务
- **Registry Controller**（`goharbor/harbor-registryctl:v2.15.2`）：Registry 配置与健康控制
- **Trivy Adapter**（`goharbor/trivy-adapter-photon:v2.15.2`）：漏洞扫描服务
- **PostgreSQL**：保存 Harbor 元数据和配置
- **Redis 与 Sentinel**：保存队列、缓存和协调状态

**经过实测的最低资源规格：**

| 组件 | CPU 上限 | 内存上限 | 持久化存储 |
| --- | ---: | ---: | ---: |
| 每个 Harbor 服务 | 100m | 128 MiB | 取决于服务 |
| PostgreSQL | 500m | 512 MiB | 1 GiB |
| Redis | 500m | 512 MiB | 1 GiB |
| Redis Sentinel | 500m | 512 MiB | 1 GiB |
| Jobservice 日志 | 已包含 | 已包含 | 1 GiB |
| Trivy 报告 | 已包含 | 已包含 | 1 GiB |

Trivy 还会为漏洞数据库预留 2 GiB 临时存储。Trivy Pod 重建后的首次扫描需要重新下载数据库，因此耗时可能更长。该最低规格已经通过空闲启动、登录后界面操作、镜像推送与拉取、Pod 重建和漏洞扫描验证；生产流量和大型仓库通常需要更多 CPU、内存与存储。

**许可证信息：**

Harbor 使用 [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 Harbor？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统。在 Sealos 上部署 Harbor 可以获得：

- **一键创建完整环境**：同时创建 Harbor、PostgreSQL、Redis、存储和 Ingress。
- **托管依赖**：由 KubeBlocks 运行数据库与缓存资源。
- **灵活存储选择**：选择私有 S3 兼容 Bucket 或本地持久卷。
- **托管 HTTPS**：自动获得带 TLS 路由的公网域名。
- **Canvas 运维**：通过 AI 对话和资源卡片完成后续配置变更。
- **按量使用资源**：从实测最低规格起步，再根据实际负载扩容。

## 部署指南

1. 打开 [Harbor 模板](https://sealos.io/products/app-store/harbor)，点击 **Deploy Now**。
2. 配置部署参数：
   - `harbor_admin_password`：设置内置 `admin` 账号的初始密码。密码长度至少为 8 个字符，并请妥善保存。
   - `enable_s3_storage`：保留默认值 `true` 会创建私有 Sealos ObjectStorageBucket；选择 `false` 会创建 1 GiB Registry 持久卷。
3. 等待部署完成，通常需要 2-3 分钟。完成后 Sealos 会打开该部署的 Canvas。
4. 打开 Canvas 中显示的 Harbor 地址。
5. 使用用户名 `admin` 和 `harbor_admin_password` 中填写的密码登录。
6. 打开 **Projects**，创建项目，再进入项目管理仓库、成员、机器人账号和策略。

公开自助注册默认关闭。管理员可以从 **Administration > Users** 创建用户，每个项目也可以为自动化客户端创建机器人账号。

Harbor 会在首次初始化数据库时读取 `harbor_admin_password`。已有部署可以从管理员个人资料中修改密码，也可以按官方密码重置流程操作。

## 推送第一个镜像

先在 Harbor 界面中创建项目，再执行：

```bash
export HARBOR_HOST="<你的-Harbor-域名>"

docker login "$HARBOR_HOST" -u admin
docker pull busybox:1.37.0
docker tag busybox:1.37.0 "$HARBOR_HOST/<项目名>/busybox:1.37.0"
docker push "$HARBOR_HOST/<项目名>/busybox:1.37.0"
docker pull "$HARBOR_HOST/<项目名>/busybox:1.37.0"
```

在 `docker login` 提示中输入部署密码。CI/CD 流水线可以使用项目机器人账号及其自动生成的凭据。

## 配置

### 模板参数

| 参数 | 说明 | 必填 | 默认值 |
| --- | --- | --- | --- |
| `harbor_admin_password` | 内置 `admin` 账号的初始密码 | 是 | 无 |
| `enable_s3_storage` | 选择私有 Sealos 对象存储（`true`）或 Registry 持久卷（`false`） | 否 | `true` |

### 存储模式

| 模式 | 制品存储后端 | 推荐场景 |
| --- | --- | --- |
| 启用 S3 | 私有 Sealos ObjectStorageBucket | 长期运行的仓库和持续增长的制品集合 |
| 关闭 S3 | 1 GiB Registry 持久卷 | 小型仓库、开发环境和本地存储流程 |

请在首次推送镜像前确定存储模式。后续切换模式需要单独迁移制品数据。若制品总量接近 1 GiB，请先在 Canvas 中扩展 Registry 持久卷容量。

部署完成后，可以使用：

- **Harbor 管理后台**管理用户、项目、机器人账号、扫描器、复制、保留和垃圾回收
- **Canvas AI 对话**发起基础设施变更
- **Canvas 资源卡片**调整 CPU、内存、存储、工作负载、Service 和 Ingress

## 扩缩容

模板会为每个 Harbor 工作负载启动一个副本，并保留原有组件边界。请根据实际负载从 Canvas 调整资源：

1. 为增长中的制品扩展 Registry 存储，或继续使用 S3 模式。
2. 并发推送和拉取增加时，提升 Registry 与 Core 的资源。
3. 扫描、复制和保留任务增多时，提升 Jobservice 与 Trivy 的资源。
4. 元数据和任务量增长时，提升 PostgreSQL 与 Redis 的容量。

调整副本数前，请先参考 Harbor 的高可用架构，因为部分组件需要共享存储和协同配置。

## 故障排查

### 管理员登录失败

- 确认用户名为 `admin`。
- 使用首次部署时填写的密码。
- 已有数据库应使用 Harbor 当前保存的密码，也可以按官方流程重置密码。

### 首次漏洞扫描耗时较长

- Trivy 会在全新启动后下载漏洞数据库。
- 在 Canvas 中检查 Trivy Pod 状态和日志。
- 为扫描器数据库保留至少 2 GiB 临时存储。

### 推送镜像时达到本地存储容量

- 在 Canvas 中扩展 Registry 持久卷。
- 对于持续增长的制品集合，S3 模式更合适。

### Harbor 地址仍在创建

- 等待部署、DNS 和 TLS 证书完成。
- 资源显示 Ready 后，从 Canvas 重新打开访问地址。

### 获取帮助

- [Harbor 文档](https://goharbor.io/docs/)
- [Harbor GitHub Issues](https://github.com/goharbor/harbor/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Harbor 管理指南](https://goharbor.io/docs/main/administration/)
- [Harbor 漏洞扫描](https://goharbor.io/docs/main/administration/vulnerability-scanning/)
- [Harbor 制品复制](https://goharbor.io/docs/main/administration/configuring-replication/)
- [Harbor 机器人账号](https://goharbor.io/docs/main/working-with-projects/project-configuration/create-robot-accounts/)

## 许可证

本 Sealos 模板遵循模板仓库的许可证策略。Harbor 使用 [Apache License 2.0](https://github.com/goharbor/harbor/blob/main/LICENSE)。
