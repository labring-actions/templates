# 在 Sealos 上部署和托管 Postiz

Postiz 是一款开源社交媒体排程与管理平台，用于规划、发布和跟踪社交媒体内容。此模板会在 Sealos Cloud 上部署 Postiz，并配套 PostgreSQL、Redis、Temporal、Elasticsearch 和持久化存储。

![Postiz 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/postiz/website-screenshot.webp)

## 关于 Postiz 托管

Postiz 为社交媒体团队提供自托管工作区，可用于排程内容、管理渠道并协同发布流程。此 Sealos 模板运行 Postiz `v2.21.8`，主应用容器内包含前端、后端 API、orchestrator 和 Nginx 网关。

部署时还会创建 PostgreSQL、Redis、Temporal、Elasticsearch 以及持久化卷。PostgreSQL 用于保存 Postiz 应用数据和 Temporal 元数据；Redis 提供缓存和队列能力；Temporal 负责后台工作流；Elasticsearch 存储 Temporal visibility 数据；持久化卷用于保存上传文件和运行配置。Sealos 会自动创建公网 HTTPS 入口、服务发现、数据库资源和存储资源。

此模板默认采用最简单的首次使用方式：启用本地邮箱和密码注册。创建首个账号不需要 OAuth、Resend、邮件验证码或密码重置邮件服务。

## 常见使用场景

- **社交媒体排程**：在一个自托管仪表盘中规划并发布多个社交渠道的内容。
- **团队内容运营**：在私有工作区中协同管理内容日历、草稿和发布流程。
- **代理机构发布流程**：为多个客户管理社交账号，同时将数据保存在自己的 Sealos 工作区。
- **自托管社交工具**：首次登录不依赖托管版 SaaS 账号或外部身份提供商。

## Postiz 托管依赖

此 Sealos 模板包含运行 Postiz 所需的依赖：Postiz 应用镜像、PostgreSQL 16.4、Redis 7.2、Temporal 1.28、Elasticsearch 7.17、上传文件持久化存储和配置持久化存储。

### 部署依赖

- [Postiz 官网](https://postiz.com/) - 产品介绍与概览
- [Postiz 文档](https://docs.postiz.com/introduction) - 官方文档与配置指南
- [Postiz 源码仓库](https://github.com/gitroomhq/postiz-app) - 源码与问题跟踪
- [Sealos 文档](https://sealos.io/docs) - Sealos Cloud 文档

## 实现细节

**架构组件：**

此模板会部署以下服务：

- **Postiz 应用**：运行 `ghcr.io/gitroomhq/postiz-app:v2.21.8`，通过 `5000` 端口提供 Web UI、API、Nginx 网关和 orchestrator。
- **PostgreSQL 16.4**：存储 Postiz 应用数据和 Temporal 元数据。初始化 Job 会在应用启动前创建 `postiz` 数据库。
- **Redis 7.2**：为 Postiz 提供缓存和队列支撑。
- **Temporal 1.28**：运行 Postiz 后台任务所需的工作流处理能力。
- **Temporal Elasticsearch 7.17**：以 256 MiB heap 存储 Temporal visibility 数据。
- **持久化卷**：将上传文件保存到 `/uploads`，将应用配置保存到 `/config`。

**配置：**

模板会自动生成应用名称、公网域名和 JWT 密钥。应用默认使用本地存储，并设置 `DISABLE_REGISTRATION=false`，因此首个用户可以在部署完成后直接用邮箱和密码注册。

服务之间通过 Kubernetes DNS 和 Sealos 自动生成的数据库凭据连接。PostgreSQL 连接数采用保守配置，确保 Postiz 与 Temporal 可以共享默认数据库资源基线。

**资源配置：**

| 组件 | CPU 限制 | 内存限制 | 说明 |
| --- | ---: | ---: | --- |
| Postiz 应用 | `500m` | `4096Mi` | 一个容器内包含 Nginx、前端、后端和 orchestrator；冷启动生成工作流 bundle 需要 4 GiB 内存。 |
| PostgreSQL | `500m` | `512Mi` | 使用 Sealos PostgreSQL 数据库基线。 |
| Redis | `500m` | `512Mi` | 使用 Sealos Redis 与 Sentinel 数据库基线。 |
| Temporal | `500m` | `512Mi` | 运行 Temporal 服务和默认 namespace 初始化。 |
| Temporal Elasticsearch | `500m` | `1024Mi` | 以 256 MiB heap 运行 Elasticsearch，供 Temporal visibility 使用。 |

**许可证信息：**

此 Sealos 模板作为 Sealos templates 仓库的一部分提供。Postiz 本身采用 GNU Affero General Public License v3.0 许可证。

## 为什么在 Sealos 上部署 Postiz？

Sealos 是基于 Kubernetes 的 AI 云操作系统，覆盖从云端 IDE 开发到生产部署和运维管理的完整应用生命周期。它适合运行现代 SaaS 工具、工作流系统和多服务应用。在 Sealos 上部署 Postiz，你可以获得：

- **一键部署**：通过一个模板部署 Postiz、PostgreSQL、Redis、Temporal、Elasticsearch、访问入口和存储。
- **无需运维 Kubernetes**：直接使用 Kubernetes 支撑的工作负载、服务发现、持久化存储和健康检查，无需手写 YAML。
- **即时公网访问**：Sealos 会为 Postiz Web 界面生成公网 HTTPS 地址。
- **易于调整配置**：可通过 Canvas、AI 对话或资源卡片调整环境变量、资源和存储。
- **内置持久化存储**：上传媒体和应用配置会在重启或重新部署后保留。
- **按量使用资源**：根据实际负载调整 CPU、内存和存储。
- **运维可观测**：可在 Sealos 控制台查看日志、工作负载状态和资源使用情况。

在 Sealos 上部署 Postiz，可以把精力放在社交内容发布流程上，而不是底层基础设施管理。

## 部署指南

1. 打开 [Postiz 模板](https://sealos.io/products/app-store/postiz)，点击 **Deploy Now**。
2. 在弹窗中配置参数。最简单的部署方式是保持默认值。
3. 等待部署完成。通常需要 2-3 分钟，但首次启动可能更久，因为 PostgreSQL、Redis、Temporal、Elasticsearch 和 Postiz 都需要初始化。部署开始或完成后会进入 Canvas。后续如果要调整配置，可在 AI 对话中描述需求让 Sealos 应用变更，也可以点击相关资源卡片手动修改。
4. 通过生成的公网地址访问 Postiz，并创建第一个本地账号。

## 首次登录与注册

Postiz 是 Web 应用，使用前需要用户账号。此模板默认启用本地注册，因此首个账号只需要邮箱和密码即可创建。

1. 部署完成后打开生成的 Postiz 地址。
2. 全新部署会打开本地注册页面 `/auth`。如果进入的是登录页，请手动打开 `/auth`，或使用界面中的注册入口。
3. 首个账号不需要 OAuth。即使页面显示 OAuth 按钮，也请使用分隔线下方的本地注册表单。
4. 输入邮箱、密码和工作区或公司名称，然后点击 **Create Account**。
5. 默认模板没有配置邮件服务或邮件验证，因此账号会立即激活。
6. 如果注册后页面要求登录，请打开 `/auth/login`，使用同一个邮箱和密码登录。

用户名请使用邮箱地址。该邮箱在当前部署中尚未注册前，直接登录会返回 `Invalid user name or password`。注册页面是 `/auth`，`/auth/register` 不是 Postiz 路由。GitHub OAuth、Google OAuth、X/Twitter API 凭据、Resend 和邮件验证码都是后续可选集成，不是首次登录的前置条件。

## 配置说明

部署后可以通过以下方式配置 Postiz：

- **AI 对话**：描述你希望修改的内容，让 Sealos 应用变更。
- **资源卡片**：点击 StatefulSet、Deployment、数据库、缓存、Ingress 或存储等资源卡片修改设置。
- **Postiz UI**：在 Postiz 内连接社交渠道并配置发布集成。
- **环境变量**：只有在准备启用 OAuth、邮件或社交平台集成时，才需要添加对应凭据。

关键默认环境变量：

| 配置 | 默认值 | 作用 |
| --- | --- | --- |
| `DISABLE_REGISTRATION` | `false` | 允许本地用户注册。 |
| `IS_GENERAL` | `true` | 启用通用自托管 Postiz 使用体验。 |
| `STORAGE_PROVIDER` | `local` | 将上传文件保存到 `/uploads` 持久化卷。 |
| `TEMPORAL_NAMESPACE` | `default` | 使用部署时创建的默认 Temporal namespace。 |

## 扩容与资源调整

如需扩容或调优 Postiz：

1. 打开当前部署的 Canvas。
2. 点击相关资源卡片，例如 Postiz StatefulSet、Temporal Deployment、PostgreSQL 集群、Redis 集群或 Elasticsearch StatefulSet。
3. 根据负载调整 CPU、内存、存储或副本设置。
4. 在对话中应用变更，并从 Sealos 控制台观察工作负载就绪状态。

小型自托管工作区建议保留默认单副本拓扑。连接大量渠道、处理大体积媒体上传或运行高频发布流程前，建议先增加资源。

## 故障排查

### 部署后页面没有立即就绪

等待所有组件进入 Running 状态。冷启动时，Temporal 和 Elasticsearch 可能比主 Web 容器更慢。

### 登录提示 `Invalid user name or password`

请先在 `/auth` 创建账号。只有该邮箱已经存在于当前 Postiz 部署中，才能直接登录。

### 注册时要求邮件激活

检查部署后是否额外添加了邮件服务或验证配置。使用默认模板时，本地用户会立即激活。

### 社交平台发布失败

确认已配置对应社交平台凭据，并已在 Postiz UI 中完成渠道连接。

### 上传失败

检查 `/uploads` 持久化卷和可用存储容量。

### 获取帮助

- [Postiz 文档](https://docs.postiz.com/introduction)
- [Postiz GitHub Issues](https://github.com/gitroomhq/postiz-app/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Postiz 官网](https://postiz.com/)
- [Postiz 源码仓库](https://github.com/gitroomhq/postiz-app)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为 Sealos templates 仓库的一部分提供。Postiz 本身采用 [GNU Affero General Public License v3.0](https://github.com/gitroomhq/postiz-app/blob/main/LICENSE) 许可证。
