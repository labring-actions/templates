# 在 Sealos 上部署和托管 Uptime Kuma

Uptime Kuma 是一个易用的自托管监控工具，可用于监控网站、API、TCP 端口、Ping 检查和状态页。此模板会在 Sealos Cloud 上部署 Uptime Kuma v2，默认使用独立 MySQL 兼容数据库，并为 `/app/data` 运行时目录配置持久化存储。

![Uptime Kuma 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/uptime-kuma/website-screenshot.webp)

## 关于托管 Uptime Kuma

Uptime Kuma 在 `3001` 端口提供 Web 控制台。Sealos 模板默认使用 Uptime Kuma v2 与独立 MySQL 兼容数据库，并保留 `/app/data` 持久卷用于运行时文件。

仅在需要更轻量的 SQLite 文件模式时，将 `USE_MARIADB` 设置为 `false`。SQLite 路径仍会使用 `/app/data` 持久卷，更适合轻量单节点部署。

## 常见使用场景

- **网站可用性监控**：跟踪公网网站，在检查失败时发送告警。
- **API 健康检查**：监控 HTTP 端点、JSON 响应和延迟。
- **内部服务检查**：监控 TCP 端口、DNS、Ping 和关键词匹配结果。
- **公开状态页**：为用户或内部团队发布服务状态页。
- **通知路由**：将告警发送到 Slack、Discord、Telegram、邮件、Webhook 和其他支持渠道。

## Uptime Kuma 托管依赖

Sealos 模板包含所需运行资源：

- **Uptime Kuma StatefulSet**：运行控制台和监控 Worker。
- **独立 MySQL 兼容数据库**：在 `USE_MARIADB=true` 时保存监控项、用户、状态页、事件和通知配置。
- **持久化 `/app/data` 卷**：保存运行时文件，并在 `USE_MARIADB=false` 时保存 SQLite 数据库。
- **Service 和 Ingress**：通过 Sealos 网关以 HTTPS 暴露控制台。
- **App 入口**：在 Sealos 桌面中创建可点击的 Uptime Kuma 入口。

### 部署依赖

- [官方网站](https://uptime.kuma.pet/) - 产品首页
- [官方安装指南](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install) - Docker 安装和存储说明
- [Docker 标签指南](https://github.com/louislam/uptime-kuma/wiki/Docker-Tags) - 镜像标签和 v2 存储后端说明
- [GitHub 仓库](https://github.com/louislam/uptime-kuma) - 源码和 issue 跟踪

## 实现细节

**架构组件：**

此模板部署一个应用组件：

- **Uptime Kuma**：基于 Node.js 的监控控制台，监听 `3001` 端口。
- **MySQL 兼容数据库**：在 `USE_MARIADB=true` 时通过 Kubeblocks 创建。
- **持久卷**：挂载到 `/app/data`，保存运行时文件和 SQLite 模式数据。
- **Ingress**：通过 Sealos 托管 TLS，将控制台发布到 `https://<app-host>.<your-sealos-domain>`。

**配置：**

- 应用访问域名前缀使用 `uptime-kuma-` 自动生成。
- 运行时使用固定镜像 `louislam/uptime-kuma:2.4.0-slim`。
- `USE_MARIADB=true` 会创建独立 MySQL 兼容数据库，并注入 `UPTIME_KUMA_DB_TYPE=mariadb` 与生成的连接凭据。
- `USE_MARIADB=false` 会把 SQLite 文件数据库保存在持久化存储中。

**许可证信息：**

Uptime Kuma 使用 MIT License。此 Sealos 模板遵循 templates 仓库的许可证条款。

## 首次运行设置

部署完成后，从 Sealos App 入口或生成的 Ingress URL 打开 Uptime Kuma。

1. 在首次打开的页面中创建第一个管理员账号，填写用户名和密码。
2. 创建账号后，使用该管理员账号登录。
3. 点击 **Add New Monitor**。
4. 选择监控类型，例如 **HTTP(s)**、**Ping** 或 **TCP Port**。
5. 填写目标 URL 或主机，设置心跳间隔，然后点击 **Save**。
6. 打开 **Settings** 配置通知渠道、语言、状态页和其他实例选项。

## 为什么在 Sealos 上部署 Uptime Kuma？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、存储、网络和运维能力。在 Sealos 上部署 Uptime Kuma 可以获得：

- **一键部署**：从应用商店部署，无需手写 Kubernetes 清单。
- **内置持久化存储**：监控数据和用户设置可跨重启保留。
- **即时公网访问**：自动获得带 Sealos 托管证书的 HTTPS 地址。
- **按量资源配置**：从较小资源规格开始，并可在 Canvas 中按需调整。
- **AI 运维和资源卡片**：通过 Canvas AI 对话或资源卡片调整 CPU、内存、存储和运行配置。

## 部署指南

1. 打开 [Uptime Kuma 模板](https://sealos.io/products/app-store/uptime-kuma)，点击 **Deploy Now**。
2. 检查自动生成的应用名称和访问域名。
   - 保持 `USE_MARIADB=true` 使用默认独立数据库部署。
   - 设置 `USE_MARIADB=false` 使用 SQLite 单节点模式。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，Sealos 会跳转到 Canvas。
4. 访问应用：
   - **Uptime Kuma 控制台**：打开 App 入口或生成的公网 URL。
   - **首次设置**：创建第一个管理员账号，登录后添加第一个监控项。

## 扩缩容

部署后调整资源：

1. 打开 Uptime Kuma 部署对应的 Canvas。
2. 点击 StatefulSet 资源卡片。
3. 根据监控项数量和检查频率调整 CPU、内存或存储。
4. 在对话框中应用变更。

## 故障排查

### 创建账号后仍回到首次运行页面

- 原因：应用数据目录缺少持久化或写入异常。
- 解决方案：确认 StatefulSet 已挂载 `/app/data` 持久卷，并且 Pod 运行日志中没有存储错误。

### SQLite 存储告警

- 原因：SQLite 需要支持 POSIX 文件锁的文件系统。
- 解决方案：保持 `/app/data` 使用 Sealos 持久卷，并使用支持文件锁的存储。

### WebSocket 或控制台实时更新延迟

- 原因：反向代理设置会影响实时更新。
- 解决方案：保留模板中的 Ingress 注解，并通过生成的 HTTPS URL 访问 Uptime Kuma。

## 更多资源

- [Uptime Kuma 文档 Wiki](https://github.com/louislam/uptime-kuma/wiki)
- [反向代理说明](https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy)
- [Uptime Kuma Releases](https://github.com/louislam/uptime-kuma/releases)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。Uptime Kuma 本身使用 MIT License。
