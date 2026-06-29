# 在 Sealos 上部署和托管 Grafana

Grafana 是一个开源分析与可视化平台。此模板在 Sealos Cloud 上部署 Grafana，包含持久化存储和可选的托管 PostgreSQL 数据库。

![Grafana 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/grafana/website-screenshot.webp)

## 关于托管 Grafana

Grafana 以单个 StatefulSet 运行，并使用持久化存储保存仪表盘、插件、用户和本地配置。默认情况下，Grafana 使用持久卷上的内置 SQLite 数据库，适合轻量自托管场景。

启用 `use_postgresql` 后，模板会创建托管 PostgreSQL 16.4 数据库，并配置 Grafana 将应用数据写入 PostgreSQL。Sealos 同时提供公网 HTTPS 地址、服务路由和资源控制。

## 常见使用场景

- **指标仪表盘**：从 Prometheus、Graphite、PostgreSQL 等数据源构建仪表盘。
- **运维监控**：跟踪基础设施健康状态、应用指标和告警趋势。
- **日志与链路追踪分析**：连接 Loki、Tempo 等可观测性后端。
- **团队报表**：向运维和产品团队共享面板与仪表盘。

## Grafana 托管依赖

Sealos 模板包含 Grafana 容器、持久化存储、公网 HTTPS Ingress 和可选 PostgreSQL。

### 部署依赖

- [Grafana 文档](https://grafana.com/docs/grafana/latest/) - 官方文档
- [Grafana Docker 镜像](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/) - Docker 部署参考
- [Grafana GitHub 仓库](https://github.com/grafana/grafana) - 源码与发布版本

### 实现细节

**架构组件：**

- **Grafana StatefulSet**：在 `3000` 端口运行 Grafana Web 应用。
- **持久卷**：保存 `/var/lib/grafana` 数据。
- **可选 PostgreSQL**：当 `use_postgresql` 设置为 `true` 时保存 Grafana 元数据。
- **Ingress 与 App**：通过 Sealos 发布 HTTPS Web 界面。

**配置：**

- 管理员用户名为 `admin`。
- 管理员密码自动生成为 `admin_password`。
- 默认关闭用户自注册。
- 默认存储模式为 SQLite；部署选项中可启用 PostgreSQL。

**许可证信息：**

Grafana 使用 AGPL-3.0 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Grafana？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 到生产部署和管理的完整应用生命周期。在 Sealos 上部署 Grafana 可以获得：

- **一键部署**：单击即可部署 Grafana。
- **内置持久化存储**：重启后保留仪表盘和配置。
- **可选托管数据库**：使用 PostgreSQL 作为更持久的元数据存储。
- **即时公网访问**：自动获得 HTTPS 地址。
- **便捷自定义**：从 Canvas 调整资源、环境变量和存储。

## 部署指南

1. 打开 [Grafana 模板](https://sealos.io/products/app-store/grafana)，点击 **Deploy Now**。
2. 选择是否启用 `use_postgresql`。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 打开 Grafana 地址并使用以下信息登录：
   - **用户名**：`admin`
   - **密码**：部署参数中生成的 `admin_password` 值。
5. 首次登录后按 Grafana 提示修改管理员密码。

## 配置

部署后可通过以下方式配置 Grafana：

- **Grafana UI**：添加数据源、仪表盘、文件夹和用户。
- **AI Dialog**：描述资源或环境变量变更，让 Sealos 自动应用。
- **资源卡片**：点击 StatefulSet、Service、Ingress 或 PostgreSQL 卡片更新部署设置。

## 扩缩容

Grafana 部署为单副本，因为默认本地存储和 SQLite 模式为单写入模式。较大规模部署建议启用 PostgreSQL，并结合插件与数据共享需求调整 StatefulSet 的 CPU 和内存。

## 故障排查

### 无法登录

- 原因：生成的管理员密码复制错误。
- 解决方法：检查部署值 `admin_password`，并以 `admin` 用户登录。

### 重启后仪表盘消失

- 原因：持久卷被删除或替换。
- 解决方法：自定义部署时保留 Grafana StatefulSet 卷和 PVC。

## 其他资源

- [Grafana 文档](https://grafana.com/docs/grafana/latest/)
- [Grafana 数据源](https://grafana.com/docs/grafana/latest/datasources/)
- [Grafana 告警](https://grafana.com/docs/grafana/latest/alerting/)

## 许可证

此 Sealos 模板遵循仓库许可证。Grafana 本身使用 AGPL-3.0 许可证。
