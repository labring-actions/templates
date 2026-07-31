# 在 Sealos 上部署和托管 OpenList

OpenList 是一款由社区驱动的文件列表与存储聚合平台，提供 WebDAV、离线下载和浏览器管理界面。本模板部署 OpenList `v4.2.2-aria2`，开箱即用的本地存储挂载为默认方案，同时支持托管 PostgreSQL 与私有 Sealos S3 存储。

![使用 Sealos S3 存储的 OpenList](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openlist/website-screenshot.webp)

## OpenList 托管方案

OpenList 可将多个存储服务整合到同一个网页界面与 WebDAV 入口。管理员可以添加存储驱动、管理用户和权限、创建分享、配置元信息，并运行离线下载任务。

Sealos 模板通过单个 StatefulSet 运行 OpenList，并挂载 `1Gi` 持久卷。存储初始化 Job 会自动把持久卷挂载到 `/local`，或创建私有 Sealos 对象存储桶并挂载到 `/sealos-s3`。启动、就绪和存活探针统一使用 OpenList 提供的 `/ping` 接口。

数据库和文件存储可以独立组合：

| 数据库 | 文件存储 | 推荐场景 |
| --- | --- | --- |
| SQLite | 本地持久卷 | 评估、个人使用和紧凑型部署 |
| SQLite | Sealos S3 | 轻量元数据与对象文件存储 |
| PostgreSQL | 本地持久卷 | 较大元数据规模与本地文件 |
| PostgreSQL | Sealos S3 | 面向生产的元数据与对象存储 |

## 常见使用场景

- **统一存储门户**：通过一个文件浏览器整合网盘与 S3 兼容服务。
- **私有文件服务**：在自托管界面中上传、整理、预览和分享文件。
- **WebDAV 网关**：让桌面端、移动端、备份工具和媒体应用通过 WebDAV 访问文件。
- **S3 文件访问**：文件存入私有 Sealos 存储桶，并由 OpenList 统一执行认证授权。
- **离线下载**：使用镜像内置的 Aria2 集成完成受支持的传输流程。

## OpenList 托管依赖

模板包含 OpenList 容器、持久化存储、Kubernetes Service、HTTPS Ingress、Sealos App 入口和幂等存储初始化 Job。可选分支会创建 KubeBlocks PostgreSQL 集群或私有 Sealos `ObjectStorageBucket`。

### 部署依赖

- [OpenList 官网](https://oplist.org/) - 产品网站
- [OpenList 文档](https://doc.oplist.org/) - 安装与管理指南
- [Docker 安装指南](https://doc.oplist.org/guide/installation/docker) - 官方容器部署说明
- [S3 驱动指南](https://doc.oplist.org/guide/drivers/s3) - S3 兼容存储配置
- [OpenList GitHub 仓库](https://github.com/OpenListTeam/OpenList) - 源代码与问题跟踪

### 实现细节

**架构组件：**

- **OpenList Web 服务**：运行 `openlistteam/openlist:v4.2.2-aria2`，监听 `5244` 端口。
- **持久卷**：保存 OpenList 配置、SQLite 数据，以及 `/opt/openlist/data` 下的本地文件。
- **存储初始化 Job**：使用初始管理员账号完成认证，并创建 `/local` 或 `/sealos-s3` 挂载。
- **可选 PostgreSQL**：KubeBlocks PostgreSQL `16.4.0` 集群负责保存 OpenList 元数据。
- **可选对象存储**：私有 Sealos S3 兼容存储桶负责保存 `/sealos-s3` 中的文件。
- **公网入口**：Service、Ingress 和 Sealos App 共同提供 HTTPS 访问地址。

**许可证信息：**

OpenList 使用 GNU Affero General Public License v3.0。本仓库提供部署配置，并完整保留上游许可证。

## 在 Sealos 上部署 OpenList 的优势

Sealos 是构建在 Kubernetes 之上的云操作系统，将应用部署与资源运维集中到同一个工作空间。部署 OpenList 后可以获得：

- **一键部署**：通过一个表单创建应用、网络、持久化存储和所选托管服务。
- **存储开箱即用**：OpenList 启动后即可使用本地挂载或 Sealos S3 挂载。
- **托管数据库选项**：一并创建 PostgreSQL 和自动生成的连接凭据。
- **即时 HTTPS 访问**：获得公网地址与托管 TLS 配置。
- **数据持久化**：Pod 重启后继续保留配置、数据库和本地文件。
- **按量使用资源**：从实测通过的 OpenList 最小资源档位起步。
- **Canvas 与 AI 运维**：通过 Sealos Canvas 检查资源，并用自然语言描述后续变更。

## 部署指南

1. 打开 [OpenList 模板](https://sealos.io/products/app-store/openlist)，点击 **Deploy Now**。
2. 填写高强度的 `admin_password`，并将它保存到密码管理器。
3. 选择数据库：
   - 保持 `enable_postgresql` 关闭，使用持久卷中的 SQLite。
   - 开启 `enable_postgresql`，创建独立 PostgreSQL 集群。
4. 选择文件存储：
   - 保持 `enable_s3_storage` 关闭，使用持久卷中的 `/local` 挂载。
   - 开启 `enable_s3_storage`，创建私有 Sealos 存储桶并挂载到 `/sealos-s3`。
5. 等待部署完成。SQLite 通常需要 2-3 分钟，PostgreSQL 首次创建还会增加数据库准备时间。
6. 从 Sealos App 入口打开生成的 OpenList 地址。

### 部署参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `admin_password` | 必填 | 内置 `admin` 账号的初始密码 |
| `enable_postgresql` | `false` | 开启后创建托管 PostgreSQL；`false` 使用 `/opt/openlist/data/data.db` 中的 SQLite |
| `enable_s3_storage` | `false` | 开启后创建私有 Sealos 存储桶并挂载到 `/sealos-s3`；`false` 在持久卷上创建 `/local` |

## 首次登录与用户配置

1. 打开生成的应用地址，OpenList 会跳转到登录页。
2. 用户名填写 `admin`。
3. 密码填写部署时配置的 `admin_password`。
4. 打开 **Manage**，管理存储、设置、分享和索引。
5. 进入 **Manage > Users**，点击 **Add** 为其他用户创建账号。
6. 为每个用户设置基础路径和满足其工作流所需的最小权限。

OpenList 在创建新数据库时使用部署密码初始化 `admin` 账号。SQLite 或 PostgreSQL 已保存数据时，应用更新会继续使用数据库中的管理员密码。

## 存储方案

### 本地持久化存储

当 `enable_s3_storage=false` 时，初始化 Job 会创建挂载到 `/local` 的 Local 驱动。文件保存在 StatefulSet `1Gi` 持久卷的 `/opt/openlist/data/storage`，Pod 替换后仍然保留。

### Sealos S3 对象存储

当 `enable_s3_storage=true` 时，Sealos 会创建私有 `ObjectStorageBucket`。初始化 Job 使用 OpenList 官方 S3 驱动完成 `/sealos-s3` 挂载，采用路径寻址，并从 Sealos 托管 Secret 读取凭据。

匿名直接访问私有桶对象时会收到 `403`。已认证用户通过 OpenList 或 WebDAV 上传和下载文件，OpenList 权限规则会持续生效。

## 数据库方案

### 内嵌 SQLite

SQLite 是默认方案，元数据保存在 `/opt/openlist/data/data.db`。它拥有最小部署占用，适合个人使用和紧凑型单副本部署。

### 托管 PostgreSQL

开启 `enable_postgresql` 后，模板会创建 PostgreSQL 集群和幂等数据库初始化 Job。OpenList 从 Kubernetes Secret 读取自动生成的主机、端口、用户名和密码。

## 持久化

| 路径或服务 | 用途 | 创建条件 |
| --- | --- | --- |
| `/opt/openlist/data/config.json` | OpenList 运行配置 | 始终创建 |
| `/opt/openlist/data/data.db` | SQLite 元数据 | `enable_postgresql=false` |
| `/opt/openlist/data/storage` | `/local` 中的文件 | `enable_s3_storage=false` |
| PostgreSQL 存储卷 | 用户、设置、存储定义、分享和元数据 | `enable_postgresql=true` |
| Sealos S3 存储桶 | `/sealos-s3` 中的文件 | `enable_s3_storage=true` |

## 默认资源

线上部署测试覆盖了管理员登录、管理界面导航、文件上传与下载、Pod 替换后的存储持久化、PostgreSQL 持久化和私有 S3 访问控制。

| 组件 | CPU limit | Memory limit | CPU request | Memory request |
| --- | ---: | ---: | ---: | ---: |
| OpenList | `100m` | `128Mi` | `10m` | `12Mi` |
| PostgreSQL | `500m` | `512Mi` | `50m` | `51Mi` |
| 初始化容器和 Job | `100m` | `128Mi` | `10m` | `12Mi` |

并发传输、媒体预览、索引或持续 API 流量增长时，可以提高 OpenList 资源。

## 扩缩容

模板保留 OpenList 的单实例 StatefulSet 拓扑。SQLite 与本地文件挂载使用 ReadWriteOnce 持久卷，该组合保持单副本运行。

较大规模部署可选择 PostgreSQL 与 Sealos S3，在 StatefulSet 资源卡片中提高 CPU 和内存，并在调整副本数前核对 OpenList 的多实例要求。

## 故障排查

### 应用仍在启动

在 Sealos Canvas 中打开 OpenList 资源卡片，检查 Pod 就绪状态。PostgreSQL 部署会等待数据库和存储初始化 Job 完成后进入完整工作状态。

### 管理员登录排查

用户名使用 `admin`，密码使用当前数据库首次部署时填写的值。已有数据库会保留其中保存的密码。

### 存储挂载排查

在 Canvas 中检查 `<generated-app-name>-storage-init` Job。成功日志会显示 `Local storage mounted at /local` 或 `S3 storage mounted at /sealos-s3`。

### S3 文件返回 `403`

Sealos 存储桶采用私有策略。请通过 OpenList 或 WebDAV 使用已授权账号访问文件。

### 获取帮助

- [OpenList 文档](https://doc.oplist.org/)
- [OpenList GitHub Issues](https://github.com/OpenListTeam/OpenList/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循仓库许可证。OpenList 使用 [GNU Affero General Public License v3.0](https://github.com/OpenListTeam/OpenList/blob/v4.2.2/LICENSE)。
