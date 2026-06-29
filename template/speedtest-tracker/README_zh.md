# 在 Sealos 上部署和托管 Speedtest Tracker

Speedtest Tracker 是一个自托管的网络性能监控应用。此模板在 Sealos Cloud 上部署 Speedtest Tracker，并配置 PostgreSQL 存储、持久化配置、HTTPS 入口和初始管理员账号。

![Speedtest Tracker 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/speedtest-tracker/website-screenshot.webp)

## 关于托管 Speedtest Tracker

Speedtest Tracker 会定时运行 Ookla speed tests，并长期保存延迟、下载和上传历史。Web 界面提供图表、阈值和基于 Filament 管理面板的用户管理。

此 Sealos 模板会为 Speedtest Tracker 创建 KubeBlocks PostgreSQL 数据库和持久化 `/config` 卷。Sealos 通过 Canvas 管理公开 HTTPS 入口、存储、数据库生命周期和应用资源。

## 常见使用场景

- **家庭网络监控**：持续跟踪 ISP 性能、故障和延迟趋势。
- **办公网络检查**：为分支机构或办公空间维护轻量网络健康仪表盘。
- **SLA 证据留存**：保存历史测速数据，用于供应商沟通和故障复盘。
- **基础设施基线**：对比网络变更前后的连接质量。

## Speedtest Tracker 托管依赖

Sealos 模板包含 Speedtest Tracker、PostgreSQL、持久化应用存储和 HTTPS 入口。

### 部署依赖

- [官方文档](https://docs.speedtest-tracker.dev/) - 安装、环境变量和用户指南
- [GitHub 仓库](https://github.com/alexjustesen/speedtest-tracker) - 源码和版本发布
- [LinuxServer 镜像](https://docs.linuxserver.io/images/docker-speedtest-tracker/) - 容器镜像文档

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Speedtest Tracker**：基于 Laravel 的 Web 应用，由 LinuxServer 容器在 80 端口提供服务
- **PostgreSQL**：由 KubeBlocks 管理，用于保存测速结果、用户和应用状态
- **持久化存储**：挂载到 `/config` 的 1 Gi 卷
- **Ingress**：面向浏览器 UI 的 Sealos HTTPS 入口

**配置：**

- `APP_URL` 和 `ASSET_URL` 使用生成的 Sealos HTTPS 域名。
- PostgreSQL 凭据来自 KubeBlocks 连接密钥。
- 初始管理员邮箱和密码在部署时配置。
- 默认登录入口是应用根地址，应用会按需跳转到登录页。

**许可证信息：**

Speedtest Tracker 使用 MIT License。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Speedtest Tracker？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、数据库、存储、网络和持续运维。通过 Sealos 部署 Speedtest Tracker，你可以获得：

- **一键部署**：打开模板页、配置凭据并部署，无需编写 Kubernetes YAML。
- **托管 PostgreSQL**：KubeBlocks 为应用创建并运维数据库。
- **内置持久化存储**：`/config` 卷可在重启和升级后保留数据。
- **即时公网访问**：Sealos 自动创建 HTTPS URL。
- **AI Ops 和 Canvas**：通过 Canvas 或 AI 对话调整资源、环境变量和存储。
- **按量使用资源**：从小规格开始，按监控需求增长调整 CPU、内存和存储。

## 部署指南

1. 打开 [Speedtest Tracker 模板](https://sealos.io/products/app-store/speedtest-tracker)，点击 **Deploy Now**。
2. 在弹窗中配置管理员邮箱和密码。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问 Speedtest Tracker，并使用部署时配置的管理员邮箱和密码登录。

## 配置

部署后，你可以通过以下方式配置 Speedtest Tracker：

- **Web UI**：修改个人资料、添加用户、配置阈值并查看结果。
- **AI 对话**：描述测速计划变更或资源调整。
- **资源卡片**：在 Canvas 中修改 CPU、内存、存储和环境变量。

## 扩展

Speedtest Tracker 适合以单 Web 实例配合 PostgreSQL 运行。当定时测速、仪表盘或用户负载增长时，可在 Deployment 或 StatefulSet 资源卡片中增加 CPU 和内存。

## 故障排查

### 无法登录

- 原因：初始管理员配置只在应用首次启动时生效。
- 解决方案：使用首次部署时配置的邮箱和密码。后续账号变更可在 Speedtest Tracker 的个人资料或用户管理页面中完成。

### 没有出现定时测速结果

- 原因：尚未配置测速计划，或所选测速服务器无法访问。
- 解决方案：在 Canvas 环境变量中配置 `SPEEDTEST_SCHEDULE` 和可选服务器设置。

## 其他资源

- [环境变量](https://docs.speedtest-tracker.dev/getting-started/environment-variables)
- [认证指南](https://docs.speedtest-tracker.dev/security/authentication)
- [Speedtest Tracker Releases](https://github.com/alexjustesen/speedtest-tracker/releases)

## License

此 Sealos 模板遵循仓库许可证。Speedtest Tracker 使用 MIT License。
