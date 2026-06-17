# 在 Sealos 上部署和托管 mongo-express

mongo-express 是一个基于 Node.js、Express 和 Bootstrap 3 的 MongoDB Web 管理界面。此模板会在 Sealos 上部署 mongo-express，并自动创建 Sealos 托管的 MongoDB、公开 HTTPS 访问入口和默认启用的 Basic Authentication。

## 关于托管 mongo-express

mongo-express 提供浏览器界面，可用于查看 MongoDB 数据库、集合、文档、索引和服务器元数据。它适合开发、测试、内部管理，以及需要图形界面而不是命令行客户端的轻量数据库检查场景。

此 Sealos 模板会创建专用的 MongoDB KubeBlocks 集群和 mongo-express Deployment。Sealos 还会创建 Service、Ingress、SSL 公网 URL 和仪表盘 App 入口，部署完成后即可直接打开管理界面。

Web UI 默认启用 Basic Authentication。默认用户名为 `admin`，密码会在每次部署时自动生成。MongoDB DSN 会由托管 MongoDB 服务和 KubeBlocks root 密码自动组合，默认模板不需要外部 MongoDB 连接字符串。

## 常见使用场景

- **MongoDB 管理**：通过 Web 界面浏览数据库、集合、索引和文档。
- **开发调试**：在构建或测试 MongoDB 应用时检查应用数据。
- **内部运维**：为可信团队成员提供简单的数据库维护界面。
- **结构探索**：无需安装本地工具即可查看文档结构和样例记录。

## mongo-express 托管依赖

此 Sealos 模板包含所有必需运行依赖：mongo-express、托管 MongoDB 数据库、Kubernetes Service、Ingress 和 Sealos App 入口。

### 部署依赖

- [mongo-express GitHub 仓库](https://github.com/mongo-express/mongo-express) - 源代码和项目文档
- [mongo-express Docker 镜像](https://hub.docker.com/_/mongo-express) - 官方容器镜像
- [MongoDB 文档](https://www.mongodb.com/docs/) - MongoDB 使用和管理参考

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **mongo-express**：运行 `mongo-express:1.0.2-20-alpine3.19` 的 Web UI，监听端口 `8081`。
- **MongoDB**：由 Sealos 托管的 KubeBlocks MongoDB `8.0.4` 集群，带持久化存储。
- **Ingress 和 App 入口**：用于访问 UI 的公开 HTTPS 路由和 Sealos 仪表盘入口。

**配置：**

- `ME_CONFIG_MONGODB_URL` 会组合为 `mongodb://root:<托管密码>@<托管-mongodb-service>:27017/admin?authSource=admin`。
- 托管 MongoDB 密码来自 KubeBlocks root 账号 Secret。
- Basic Authentication 使用 `ME_CONFIG_BASICAUTH_USERNAME` 和 `ME_CONFIG_BASICAUTH_PASSWORD`。
- 健康检查使用 mongo-express 暴露的 `/status` 端点。
- 已验证的最小应用资源档位为 `100m` CPU 和 `128Mi` 内存，对应 requests 为 `10m` CPU 和 `12Mi` 内存。

**登录信息：**

部署完成后，从 Sealos App 详情中打开应用 URL。使用以下信息登录：

- **用户名**：`admin`
- **密码**：mongo-express Deployment 环境变量中的 `ME_CONFIG_BASICAUTH_PASSWORD`

请妥善保管此密码。任何拥有 Web 登录信息的人都可以通过 mongo-express 管理 MongoDB 实例。

**MongoDB DSN：**

默认部署不要求外部 MongoDB DSN。模板会创建托管 MongoDB 集群，并通过 `ME_CONFIG_MONGODB_URL` 自动注入内部 DSN。如需连接到其他 MongoDB 服务器，请在部署后编辑 Deployment 环境变量，将 `ME_CONFIG_MONGODB_URL` 替换为你自己的 MongoDB 连接字符串。

**许可证信息：**

mongo-express 使用 MIT License。此 Sealos 模板遵循 Sealos templates 仓库许可证。

## 为什么在 Sealos 上部署 mongo-express？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从部署到运维的生命周期。在 Sealos 上部署 mongo-express 可以获得：

- **一键部署**：打开模板页面，配置部署参数，由 Sealos 自动创建数据库和 Web UI 资源。
- **托管 Kubernetes 运行时**：无需手写 Kubernetes YAML 即可运行 mongo-express。
- **持久化 MongoDB 存储**：托管 MongoDB 集群使用持久化存储保存数据。
- **即时公网访问**：Sealos 会自动创建 HTTPS URL 和仪表盘 App 入口。
- **简单运维**：后续可通过 Canvas、AI 对话和资源卡片调整配置或资源。
- **资源高效**：从已验证的小资源配置开始，需要时可在 Sealos UI 中扩容。

## 部署指南

1. 打开 [mongo-express 模板](https://sealos.io/products/app-store/mongo-express)，点击 **Deploy Now**。
2. 检查生成的默认值。请保存生成的 `ME_CONFIG_BASICAUTH_PASSWORD`，它用于 Web 登录。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需调整，可在对话框中描述需求让 AI 修改，或点击对应资源卡片修改设置。
4. 通过提供的 URL 访问应用：
   - **mongo-express UI**：使用用户名 `admin` 和 Deployment 环境变量中的 `ME_CONFIG_BASICAUTH_PASSWORD` 登录。

## 配置

部署后，可以通过以下方式配置 mongo-express：

- **AI 对话**：描述需要的调整，例如增加 CPU 或内存，让 AI 应用修改。
- **资源卡片**：点击 Deployment、MongoDB、Service 或 Ingress 资源卡片查看并修改设置。
- **环境变量**：高级用户可在 Deployment 资源卡片中调整 `ME_CONFIG_MONGODB_URL`、Basic Auth 凭据、只读模式或编辑器选项。

## 扩容

如需支持更重的数据库检查工作负载，可按以下步骤扩容资源：

1. 打开当前部署的 Canvas。
2. 点击 mongo-express Deployment 资源卡片。
3. 调整 CPU 和内存资源，并在对话框中应用更改。
4. 如果数据库容量也需要提升，点击 MongoDB 资源卡片调整。

## 故障排查

### 常见问题

**打开后立即出现登录弹窗**
- 原因：Basic Authentication 默认启用。
- 解决方案：使用用户名 `admin` 和 Deployment 环境变量中的 `ME_CONFIG_BASICAUTH_PASSWORD` 登录。

**UI 无法连接 MongoDB**
- 原因：MongoDB 集群可能仍在启动，DSN 被修改，或凭据被手动修改。
- 解决方案：在 Canvas 中等待 MongoDB 资源就绪。如果凭据或 DSN 值已修改，请重新部署或更新 `ME_CONFIG_MONGODB_URL` 及相关密码环境变量。

**UI 可访问但数据较少**
- 原因：mongo-express 只显示当前 MongoDB 账号可访问的数据。
- 解决方案：此模板使用托管 root 账号进行管理。请确认目标数据存在于本次部署的 MongoDB 实例中。

### 获取帮助

- [mongo-express GitHub Issues](https://github.com/mongo-express/mongo-express/issues)
- [MongoDB 文档](https://www.mongodb.com/docs/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [mongo-express 配置](https://github.com/mongo-express/mongo-express#usage-docker)
- [MongoDB 连接字符串](https://www.mongodb.com/docs/manual/reference/connection-string/)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循仓库许可证。mongo-express 本身使用 MIT License。
