# 在 Sealos 上部署和托管 Dashy

Dashy 是一个可自托管的个人仪表盘，支持小组件、状态检查、主题、图标包和内置 UI 编辑器。此模板会在 Sealos Cloud 上部署带持久化 user-data 存储的 Dashy。

![Dashy 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/dashy/website-screenshot.webp)

## 关于 Dashy 托管

Dashy 运行一个 Node.js Web 服务，监听 8080 端口，并从 `/app/user-data/conf.yml` 读取仪表盘配置。Sealos 模板会自动创建容器、初始配置文件、持久化存储、服务、HTTPS Ingress 和 App 入口。

此部署遵循官方 Docker 运行方式，并固定使用 `lissy93/dashy:4.3.11`。模板内置一个 Sealos 起始分区，确保首次启动时拥有有效的仪表盘配置。

## 常见使用场景

- **个人仪表盘**：把工具、书签、备注和链接集中在一个页面。
- **服务状态页**：用 Dashy 状态检查监控内部应用和公开端点。
- **Homelab 入口页**：组织自托管应用和基础设施链接。
- **团队导航中心**：为运维、支持或工程团队发布精选仪表盘。

## Dashy 托管依赖

Sealos 模板包含 Dashy、持久化 user-data 存储、初始配置、公开 HTTPS Ingress 和仪表盘 App 入口。

### 部署依赖

- [官方网站](https://dashy.to) - 产品主页
- [部署文档](https://dashy.to/docs/deployment) - 官方部署指南
- [GitHub 仓库](https://github.com/Lissy93/dashy) - 源码和版本发布
- [Docker 镜像](https://hub.docker.com/r/lissy93/dashy) - 官方容器镜像

### 实现细节

**架构组件：**

- **Dashy Web 应用**：面向浏览器的仪表盘，服务端口为 8080。
- **初始配置**：通过 ConfigMap 挂载的 `conf.yml`，用于首次启动。
- **持久化用户数据**：挂载到 `/app/user-data`，用于保存自定义配置和资产。

**配置：**

- 模板会创建包含 Sealos 分区的初始 `conf.yml`。
- 可以通过 UI 编辑器或编辑 `/app/user-data/conf.yml` 自定义 Dashy。
- 健康检查使用官方 `node /app/services/healthcheck.js` 命令。

**许可证信息：**

Dashy 使用 MIT License。此 Sealos 模板遵循仓库许可证提供。

## 为什么在 Sealos 上部署 Dashy？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从开发、部署到运维的生命周期。在 Sealos 上部署 Dashy 可以获得：

- **一键部署**：从 App Store 快速启动 Dashy。
- **持久化用户数据**：重启后保留配置和仪表盘资产。
- **即时公网访问**：通过自动生成的 HTTPS URL 打开 Dashy。
- **便捷自定义**：从 Sealos 编辑资源、存储和配置。
- **集中运维**：在一个 Canvas 中查看发布状态、日志、入口和存储。

## 部署指南

1. 打开 [Dashy 模板](https://sealos.io/products/app-store/dashy)，点击 **Deploy Now**。
2. 在弹窗中确认部署参数。
3. 等待部署完成。部署完成后，你会被重定向到 Canvas。
4. 通过提供的 App URL 访问 Dashy。

## 登录和访问说明

Dashy 默认不会创建登录账号。App URL 会直接打开仪表盘；如果需要私有仪表盘，可以后续通过 Dashy 配置添加认证。

首次启动后，可以使用 UI 编辑器，或更新 `/app/user-data/conf.yml` 来添加分区、条目、图标、小组件和状态检查。

## 配置

部署完成后，可以通过以下方式配置 Dashy：

- **Dashy UI 编辑器**：在浏览器中更新仪表盘内容。
- **配置文件**：编辑 `/app/user-data/conf.yml`，维护可版本化的仪表盘设置。
- **AI Dialog**：在 Sealos 中描述资源或环境变量调整需求。
- **资源卡片**：打开 StatefulSet 或存储卡片进行直接编辑。

## 扩缩容

Dashy 将配置保存在单个持久化卷中。常规使用保持 1 个副本；如果小组件或状态检查变重，可以从 StatefulSet 卡片增加 CPU 或内存。

## 故障排查

### 仪表盘显示配置错误

- 原因：`conf.yml` 可能包含无效 YAML 或不受支持的字段。
- 解决：按 Dashy 配置文档校验文件，然后重启 StatefulSet。

### UI 编辑器改动消失

- 原因：仪表盘可能仍在使用通过 ConfigMap 挂载的初始文件。
- 解决：将改动保存到 `/app/user-data/conf.yml`，并保持持久化卷挂载。

## 其他资源

- [Dashy 文档](https://dashy.to/docs)
- [配置指南](https://dashy.to/docs/configuring)
- [管理指南](https://dashy.to/docs/management)
- [GitHub Issues](https://github.com/Lissy93/dashy/issues)

## 许可证

此 Sealos 模板遵循仓库许可证提供。Dashy 本身使用 MIT License。
