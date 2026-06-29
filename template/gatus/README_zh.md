# 在 Sealos 上部署和托管 Gatus

Gatus 是面向开发者的在线状态监控工具，支持可配置检查、告警和状态仪表盘。此模板会在 Sealos 上部署带 KubeBlocks PostgreSQL 存储的 Gatus。

![Gatus 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gatus/website-screenshot.webp)

## 关于托管 Gatus

Gatus 作为单个仪表盘服务运行在 `8080` 端口。模板会把 ConfigMap 挂载到 `/config/config.yaml`，使用官方 PostgreSQL 存储模式，并把监控状态保存在 KubeBlocks PostgreSQL 数据库中。

默认配置包含 Gatus 自身的内部健康检查，以及一个 Sealos 外部可用性检查。你可以在 Sealos Canvas 中编辑 ConfigMap，添加服务、告警渠道、端点分组或安全设置。

## 常见使用场景

- **服务在线状态监控**：检查 HTTP、TCP、ICMP、DNS 等端点类型。
- **状态仪表盘**：展示服务当前可用性和故障状态。
- **提前告警**：在客户反馈前发现故障。
- **合成检查**：对 API 和 Web 服务执行轻量验收检查。

## Gatus 托管依赖

此 Sealos 模板包含运行所需依赖：Gatus、KubeBlocks PostgreSQL `postgresql-16.4.0`、用于创建 `gatus` 数据库的初始化 Job、ConfigMap、Service、Ingress 和 App 入口。

### 部署依赖

- [官方文档](https://github.com/TwiN/gatus#configuration) - 配置参考
- [PostgreSQL 存储示例](https://github.com/TwiN/gatus/tree/master/.examples/docker-compose-postgres-storage) - 官方 compose 示例
- [Sealos](https://sealos.io) - 基于 Kubernetes 的应用托管平台

### 实现细节

**架构组件：**

- **Gatus Web 服务**：运行 `twinproduction/gatus:v5.36.0`，监听 `8080` 端口。
- **PostgreSQL**：KubeBlocks 托管的 `postgresql-16.4.0`，用于保存端点检查结果。
- **ConfigMap**：提供 `/config/config.yaml`，包含 PostgreSQL 存储和初始检查项。
- **Service 与 Ingress**：通过 HTTPS 暴露仪表盘。

**配置：**

ConfigMap 使用官方 Gatus 配置格式中的环境变量连接 PostgreSQL。数据库凭据从 KubeBlocks 连接 Secret 注入。

**许可证信息：**

此 Sealos 模板遵循仓库许可证。Gatus 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 Gatus？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、公开访问和运维。通过 Sealos 部署 Gatus，你可以获得：

- **一键部署**：从 App Store 启动带 PostgreSQL 的监控仪表盘。
- **持久化监控状态**：KubeBlocks PostgreSQL 保存检查历史。
- **即时公开访问**：Sealos 自动创建 HTTPS 仪表盘 URL。
- **便捷自定义**：从 Canvas 更新 ConfigMap 和资源设置。

## 部署指南

1. 打开 [Gatus 模板](https://sealos.io/products/app-store/gatus)，点击 **Deploy Now**。
2. 检查生成的应用名称和访问域名，然后开始部署。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续需要修改时，可以在对话框描述需求让 AI 应用更新，或点击相关资源卡片修改设置。
4. 通过提供的 App URL 访问 Gatus 仪表盘。默认模板会直接打开仪表盘。

## 配置

通过 ConfigMap 资源卡编辑 `/config/config.yaml`，可以添加端点、告警渠道、仪表盘设置或 Basic Auth。Gatus 会自动重新加载有效的配置更新。

## 更多资源

- [Gatus README](https://github.com/TwiN/gatus)
- [配置参考](https://github.com/TwiN/gatus#configuration)
- [安全配置](https://github.com/TwiN/gatus#security)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循仓库许可证。Gatus 使用 Apache License 2.0。
