# 在 Sealos 上部署和托管 Uptime Kuma

Uptime Kuma 是一款自托管监控面板，可用于监控网站、API、网络服务与基础设施。此模板会在 Sealos Cloud 上部署 Uptime Kuma 2.4.0，并配置持久化存储以及可选的独立 MySQL 兼容数据库。

![Uptime Kuma 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/uptime-kuma/website-screenshot.webp)

## Uptime Kuma 托管说明

Uptime Kuma 提供基于浏览器的管理面板，支持 HTTP、TCP、DNS、Ping、数据库、WebSocket 和证书监控。它可以记录心跳历史、统计响应时间、发送通知，并发布公开状态页。

Sealos 模板会创建单副本 Uptime Kuma StatefulSet、1 GiB 持久化数据卷、支持 WebSocket 的公网 HTTPS 入口和健康检查。SQLite 是轻量级默认方案；需要独立数据库服务时，可以启用部署选项，由模板创建 KubeBlocks MySQL 兼容数据库。

## 常见使用场景

- **网站与 API 监控**：检查可用性、延迟、状态码、证书和响应内容。
- **网络服务监控**：持续关注 TCP 端口、DNS 记录、Ping 目标和 WebSocket 端点。
- **故障通知**：通过邮件、聊天工具、Webhook 等渠道发送告警。
- **公开状态页**：向客户或内部团队发布服务健康状态和故障进展。

## 托管 Uptime Kuma 所需依赖

模板包含 Uptime Kuma 容器、持久化存储、Service、支持 WebSocket 的 Ingress、健康检查与 Sealos 应用入口。启用独立数据库后，还会创建 KubeBlocks MySQL 和数据库初始化 Job。

### 部署依赖

- [Uptime Kuma 文档](https://github.com/louislam/uptime-kuma/wiki) - 安装、配置和功能说明
- [Uptime Kuma 源码](https://github.com/louislam/uptime-kuma) - 源代码、版本发布和问题追踪
- [环境变量](https://github.com/louislam/uptime-kuma/wiki/Environment-Variables) - 数据库和服务端配置参考

### 实现细节

**架构组件：**

- **Uptime Kuma**：单副本 StatefulSet，通过 3001 端口提供管理面板并执行监控任务。
- **持久化存储**：挂载到 `/app/data` 的 1 GiB 数据卷，用于保存配置、用户、监控历史和 SQLite 数据。
- **公网入口**：由 Sealos 管理的 HTTPS Ingress，已经配置 Socket.IO 与 WebSocket 流量支持。
- **可选数据库**：通过 `enable_external_database` 启用的 KubeBlocks MySQL 兼容 Cluster 与初始化 Job。

关闭 `enable_external_database` 时，应用使用 SQLite。启用后，模板会注入由 Sealos 管理的数据库凭据，并在 Uptime Kuma 启动前创建 `uptime_kuma` 数据库。

Uptime Kuma 使用 MIT 许可证。

## 为什么在 Sealos 上部署 Uptime Kuma？

- **一键部署**：通过一个模板创建应用、存储、网络和可选数据库。
- **监控数据持久保存**：应用重启后，用户、监控项、设置和心跳历史仍然完整保留。
- **自动配置 HTTPS**：部署后立即获得公网域名、TLS 证书和 WebSocket 路由。
- **Kubernetes 运维能力**：通过 Sealos Canvas、AI 对话框和资源卡片查看并调整部署。
- **资源利用高效**：从经过个人低负载验证的 CPU 和内存配置起步，并随监控规模增长逐步扩容。

## 部署指南

1. 打开 [Uptime Kuma 模板](https://sealos.io/products/app-store/uptime-kuma)，点击 **Deploy Now**。
2. 使用 SQLite 时保持 **Enable a dedicated MySQL-compatible database** 关闭；需要独立数据库服务时启用该选项。
3. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开 Canvas，后续可以通过 AI 对话框或资源卡片修改配置。
4. 打开 Sealos 中显示的 Uptime Kuma 应用地址。

## 注册与登录

首次访问时，Uptime Kuma 会打开账户初始化页面：

1. 选择管理面板语言。
2. 输入管理员用户名和高强度密码。
3. 再次输入密码并点击 **Create**。

创建完成后，Uptime Kuma 会自动登录新管理员并进入 Dashboard。以后访问时，在登录页面输入同一组用户名和密码。这组凭据由你创建和管理，请妥善保管。

## 配置

登录后点击 **Add New Monitor**，选择监控类型、填写目标并保存。通知渠道可在 **Settings > Notifications** 中配置，公开服务状态可通过 **Status Pages** 创建。

调整部署参数时，可以使用 Sealos Canvas 的 AI 对话框，也可以直接打开 StatefulSet、存储、网络和数据库资源卡片。

## 扩缩容

随着监控数量或检查频率增长，可以通过 Uptime Kuma StatefulSet 资源卡片增加 CPU 和内存。应用保持单副本运行，以符合持久化 SQLite 与任务调度拓扑；可选独立数据库会拆分数据库存储，Uptime Kuma 调度器依然保持单副本。

## 故障排查

### 初始化页或登录页无法打开

等待 StatefulSet 进入 Ready 状态后刷新应用地址。检查 Uptime Kuma Pod 日志，并确认 Service 已经生成可用端点。

### 监控项持续显示异常

确认 Uptime Kuma Pod 可以访问目标地址，并逐项检查 URL、端口、DNS、TLS、认证信息和允许的状态码。

### 获取帮助

- [Uptime Kuma Issues](https://github.com/louislam/uptime-kuma/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循模板仓库的许可证条款。Uptime Kuma 使用 [MIT 许可证](https://github.com/louislam/uptime-kuma/blob/2.4.0/LICENSE)。
