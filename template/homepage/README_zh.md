# 在 Sealos 上部署和托管 Homepage

Homepage 是一个高度可定制的自托管起始页和应用仪表盘，支持服务 API 集成。此模板会在 Sealos Cloud 上部署带持久化配置存储的 Homepage。

![Homepage 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/homepage/website-screenshot.webp)

## 关于 Homepage 托管

Homepage 以 Next.js 应用形式运行在 3000 端口，并从 `/app/config` 读取配置文件。Sealos 模板会自动创建容器、持久化配置卷、服务、HTTPS Ingress 和 App 入口。

此部署遵循官方 Docker 运行方式，并固定使用 `ghcr.io/gethomepage/homepage:v1.13.2`。模板会将 `HOMEPAGE_ALLOWED_HOSTS` 设置为生成的 Sealos 域名，让 Homepage 能通过公网 App URL 正常访问。

## 常见使用场景

- **个人起始页**：把书签、内部工具和服务集中在一个仪表盘中。
- **Homelab 仪表盘**：展示自托管系统的服务卡片、小组件和健康状态。
- **团队入口页**：共享仪表盘、Runbook、文档和工具链接。
- **API 集成总览**：使用 Homepage 小组件展示受支持服务的数据。

## Homepage 托管依赖

Sealos 模板包含 Homepage、持久化配置存储、内部服务和公开 HTTPS Ingress。

### 部署依赖

- [官方网站](https://gethomepage.dev) - 产品主页
- [Docker 安装指南](https://gethomepage.dev/installation/docker/) - 官方 Docker 文档
- [GitHub 仓库](https://github.com/gethomepage/homepage) - 源码和版本发布
- [容器镜像](https://github.com/gethomepage/homepage/pkgs/container/homepage) - 官方 GHCR 镜像

### 实现细节

**架构组件：**

- **Homepage Web 应用**：面向浏览器的仪表盘，服务端口为 3000。
- **配置存储**：挂载到 `/app/config` 的持久化卷。
- **Sealos Ingress**：使用生成的 App 域名提供 HTTPS 访问。

**配置：**

- `HOMEPAGE_ALLOWED_HOSTS` 会设置为生成的 Sealos 域名。
- 模板省略 Docker socket 集成，提供更适合云端的默认部署。
- 可以从 Sealos Canvas 打开存储和工作负载资源来编辑配置文件。

**许可证信息：**

Homepage 使用 GNU General Public License v3.0 许可证。此 Sealos 模板遵循仓库许可证提供。

## 为什么在 Sealos 上部署 Homepage？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从开发、部署到运维的生命周期。在 Sealos 上部署 Homepage 可以获得：

- **一键部署**：从 App Store 部署可用的 Homepage 实例。
- **持久化配置**：把仪表盘设置和服务定义保存在持久化存储中。
- **即时公网访问**：通过自动生成的 HTTPS URL 打开仪表盘。
- **便捷自定义**：从 Sealos 调整资源、环境变量和文件。
- **集中监控**：在 Canvas 中查看发布状态、日志、入口和存储。

## 部署指南

1. 打开 [Homepage 模板](https://sealos.io/products/app-store/homepage)，点击 **Deploy Now**。
2. 在弹窗中确认部署参数。
3. 等待部署完成。部署完成后，你会被重定向到 Canvas。
4. 通过提供的 App URL 访问 Homepage。

## 登录和访问说明

Homepage 默认不会创建登录账号。首次打开会直接进入仪表盘；如果部署中包含私有链接，请通过你偏好的 Ingress、身份认证或网络策略流程增加访问控制。

首次启动后，可以编辑 `/app/config` 下的 Homepage 配置文件来自定义仪表盘。

## 配置

部署完成后，可以通过以下方式配置 Homepage：

- **配置文件**：编辑 `/app/config` 中的文件，定义服务、书签、小组件和布局。
- **AI Dialog**：在 Sealos 中描述环境变量或资源调整需求。
- **资源卡片**：打开 StatefulSet 或存储卡片进行直接编辑。

## 扩缩容

Homepage 将配置保存在单个持久化卷中。常规使用保持 1 个副本；如果仪表盘集成变重，可以从 StatefulSet 卡片增加 CPU 或内存。

## 故障排查

### 公网 URL 返回 allowed-host 错误

- 原因：Homepage 要求 `HOMEPAGE_ALLOWED_HOSTS` 匹配请求域名。
- 解决：确认环境变量与生成的 Sealos App 域名一致。

### 首次启动后仪表盘为空

- 原因：Homepage 使用默认或空配置启动。
- 解决：根据官方配置文档，在 `/app/config` 中添加服务、书签和小组件。

## 其他资源

- [Homepage 文档](https://gethomepage.dev)
- [配置指南](https://gethomepage.dev/configs/)
- [Widgets](https://gethomepage.dev/widgets/)
- [GitHub Discussions](https://github.com/gethomepage/homepage/discussions)

## 许可证

此 Sealos 模板遵循仓库许可证提供。Homepage 本身使用 GNU General Public License v3.0 许可证。
