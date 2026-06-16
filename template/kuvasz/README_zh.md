# 在 Sealos 上部署和托管 Kuvasz

Kuvasz 是一款开源、自托管的在线状态与 SSL 监控服务，支持状态页。此模板会在 Sealos Cloud 上部署 Kuvasz，并配套 Kubeblocks PostgreSQL 数据库和公开 HTTPS 访问入口。

![Kuvasz 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/kuvasz/website-screenshot.webp)

## 关于托管 Kuvasz

Kuvasz 可通过 HTTP、SSL、Push 和 ICMP 检查监控网站与服务。它提供 Web 控制台、REST API、通知集成、指标导出和状态页，适合发布服务健康状态。

此 Sealos 模板将官方 Kuvasz 容器作为单个 Web 服务运行，监听 `8080` 端口。Sealos 会创建 PostgreSQL `postgresql-16.4.0`、初始化 `kuvasz` 数据库、通过 ConfigMap 挂载 `/config/kuvasz.yml`，并通过 HTTPS Ingress 暴露控制台。

认证默认启用。模板会要求配置初始管理员用户名、管理员密码和 API key，其中密码和 API key 提供安全的自动生成默认值。

## 常见使用场景

- **网站在线状态监控**：通过 HTTP 状态检查跟踪公开网站和 API。
- **SSL 证书监控**：在用户受影响前发现无效或即将过期的证书。
- **状态页发布**：向团队、客户或内部系统发布服务可用性。
- **API 驱动监控**：通过 Kuvasz REST API 创建、更新和导出监控项。
- **通知工作流**：连接邮件、Discord、Slack、Telegram、PagerDuty 和 Webhook 告警。

## Kuvasz 托管依赖

此 Sealos 模板包含运行所需的组件：Kuvasz 容器镜像、PostgreSQL 数据库、数据库初始化 Job、用于 `/config/kuvasz.yml` 的 ConfigMap、Kubernetes Service、Ingress 和 Sealos App 入口。

### 部署依赖

- [Kuvasz 官网](https://kuvasz-uptime.dev/) - 官方文档和产品概览
- [Kuvasz GitHub 仓库](https://github.com/kuvasz-uptime/kuvasz) - 源码和版本发布记录
- [Kuvasz 部署指南](https://kuvasz-uptime.dev/setup/installation/) - 官方 Docker 和 Helm 部署指导
- [Kuvasz API 文档](https://api-docs.kuvasz-uptime.dev/) - REST API 参考

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Kuvasz Web 服务**：运行 `kuvaszmonitoring/kuvasz:3.11.0`，监听 `8080` 端口，提供控制台、REST API、健康端点和监控调度器。
- **PostgreSQL**：由 Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0`，用于存储监控项、事件、状态页、集成和应用元数据。
- **PostgreSQL 初始化 Job**：在 PostgreSQL 就绪后，以幂等方式创建 `kuvasz` 数据库。
- **ConfigMap**：挂载 `/config/kuvasz.yml`，用于可选集成、YAML 管理的监控项、状态页和 SMTP 设置。
- **Ingress 与 App 入口**：Sealos 暴露 HTTPS 访问域名，并在控制台中创建应用入口。

**配置：**

模板会配置：

- `DATABASE_HOST`、`DATABASE_PORT`、`DATABASE_USER` 和 `DATABASE_PASSWORD` 来自 Kubeblocks PostgreSQL 连接 Secret。
- `DATABASE_NAME=kuvasz` 作为应用数据库。
- `ENABLE_AUTH=true`，并使用配置的管理员用户名、密码和 API key。
- `APP_LANGUAGE=en` 和 `TZ=UTC`。

部署后，使用配置的管理员用户名和密码登录 Web UI。REST API 请求可在 `X-API-KEY` 请求头中传入 API key，也可以使用 Bearer token。

**许可证信息：**

Kuvasz 使用 Apache License 2.0 发布。此 Sealos 模板只是 Kuvasz 的部署配置，并保持上游应用许可证不变。

## 为什么在 Sealos 上部署 Kuvasz？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖应用部署、运维和资源管理。在 Sealos 上部署 Kuvasz 可以获得：

- **一键部署**：通过一个模板同时部署 Kuvasz、PostgreSQL、网络和控制台入口。
- **Kubernetes 基础能力**：获得 Kubernetes 调度、服务发现、健康检查和滚动更新能力。
- **内置持久化数据库**：监控项、事件和状态页数据会在重启后保留。
- **即时公网访问**：每次部署都会获得 HTTPS URL，可用于控制台、API 和状态页。
- **易于自定义**：可通过 Canvas、AI 对话或资源卡片调整环境变量、资源和挂载配置。
- **按量使用资源**：从紧凑资源配置起步，随着监控规模增长再扩容。

在 Sealos 上部署 Kuvasz，可以把精力放在服务可靠性运营上。

## 部署指南

1. 打开 [Kuvasz 模板](https://sealos.io/products/app-store/kuvasz)，点击 **Deploy Now**。
2. 在弹窗中配置管理员用户名、管理员密码和 API key。自动生成的默认值适合作为首次部署配置。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话框中描述需求，或点击对应资源卡片调整配置。
4. 从 App 入口打开生成的 Kuvasz URL。
5. 使用配置的管理员用户名和密码登录。
6. 在控制台创建第一个监控项，或使用配置的 `X-API-KEY` 值调用 REST API。

## 配置

部署后，你可以通过以下方式配置 Kuvasz：

- **Kuvasz Web UI**：创建 HTTP、SSL、Push 和 ICMP 监控项，管理状态页，并配置支持的集成。
- **REST API**：使用 `X-API-KEY: <your-api-key>` 请求头管理监控项和读取统计数据。
- **ConfigMap**：通过 Canvas 资源卡片编辑 `/config/kuvasz.yml`，用于 YAML 管理的监控项、SMTP 设置、集成和状态页。
- **Sealos AI 对话**：描述环境变量、资源或配置调整需求，让 AI 协助修改。
- **资源卡片**：在 Canvas 中点击 Deployment、PostgreSQL、ConfigMap、Ingress 或 Service 卡片，查看并调整配置。

当监控项定义在 `/config/kuvasz.yml` 中时，Kuvasz 会将该 YAML 文件作为对应监控类型的事实来源。日常编辑推荐使用 Web UI 或 API，并让 YAML 文件保留空的监控段落。

## 扩展

在 Sealos 上扩展 Kuvasz：

1. 打开 Kuvasz 部署对应的 Canvas。
2. 点击 Kuvasz Deployment 资源卡片。
3. 当监控数量、检查频率、API 流量或集成数量需要更多容量时，提高 CPU 或内存。
4. 应用变更并等待 Pod 重新就绪。

默认模板为 Kuvasz 容器配置 `50m` CPU 和 `384Mi` 内存请求，以及 `500m` CPU 和 `512Mi` 内存限制。PostgreSQL 配置 `50m` CPU 和 `51Mi` 内存请求，以及 `500m` CPU 和 `512Mi` 内存限制。

## 故障排查

### 应用打开后进入登录页

这是新部署的预期首屏。使用部署时配置的管理员用户名和密码登录。

### API 请求返回未授权

将 API key 作为 `X-API-KEY: <your-api-key>` 或 `Authorization: Bearer <your-api-key>` 传入。健康端点 `/api/v2/health` 可公开访问。

### 监控项显示为只读

由 `/config/kuvasz.yml` 管理的监控类型会进入只读模式。如需保持 YAML 作为操作来源，请编辑 ConfigMap；如需日常在 UI 或 API 中编辑，请让对应 YAML 监控段落保持空置。

### 获取帮助

- [Kuvasz 文档](https://kuvasz-uptime.dev/)
- [Kuvasz GitHub Issues](https://github.com/kuvasz-uptime/kuvasz/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Kuvasz 配置参考](https://kuvasz-uptime.dev/setup/configuration/)
- [Kuvasz API 指南](https://kuvasz-uptime.dev/features/api/)
- [Kuvasz Docker 镜像](https://hub.docker.com/r/kuvaszmonitoring/kuvasz)
- [Kuvasz GitHub Releases](https://github.com/kuvasz-uptime/kuvasz/releases)

## 许可证

此 Sealos 模板遵循仓库中的模板许可证。Kuvasz 本身使用 Apache License 2.0。
