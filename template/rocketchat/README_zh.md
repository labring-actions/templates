# 在 Sealos 上部署和托管 Rocket.Chat

Rocket.Chat 是一个开源通信平台，提供私有团队消息、频道、文件共享和工作区管理功能。此模板会在 Sealos Cloud 上部署 Rocket.Chat 8.6.1，并配置独立的 MongoDB 8.0.4 副本集。

![Rocket.Chat 工作区](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketchat/website-screenshot.webp)

## 功能亮点

- 支持团队频道、私信、文件共享、搜索和工作区管理
- 通过部署参数创建初始管理员账号
- 由 KubeBlocks 管理私有 MongoDB 数据库
- 默认使用 GridFS 存储上传文件，也可选择私有 Sealos 对象存储
- 自动配置 HTTPS、公网域名、健康检查和 Prometheus 指标
- 使用受限的非 root 容器安全上下文

## 常见使用场景

- 分布式团队和受监管组织的私有通信
- 事件响应和日常运营协调频道
- 自托管的团队消息服务
- 具备数据驻留控制的内部社区

## 部署架构

此模板会部署以下资源：

- **Rocket.Chat 8.6.1**：以单体 StatefulSet 运行，提供 Web 界面、REST API、实时消息和管理工具。
- **MongoDB 8.0.4**：以单成员 KubeBlocks 副本集运行，保存用户、房间、消息、设置和 GridFS 上传文件。
- **Sealos 对象存储**：启用 `enable_s3_storage` 后创建，使用私有 S3 兼容存储桶保存上传文件。
- **Sealos Ingress**：通过自动生成的 HTTPS 域名发布工作区。

应用采用经过实测的 200 millicores CPU 和 2 GiB 内存资源下界。MongoDB 使用 500 millicores CPU 和 512 MiB 内存。MongoDB 就绪后，应用冷启动通常需要约两分钟。

## 依赖条件

- Sealos Cloud 账号和工作区
- 用于部署和访问工作区的现代浏览器
- 连接 Rocket.Chat Cloud 时可接收邮件的管理员邮箱

Sealos 会在部署过程中创建 Kubernetes 运行环境、KubeBlocks 数据库、持久卷、网络和可选对象存储。

## 部署参数

| 参数 | 必填 | 用途 |
| --- | --- | --- |
| `admin_username` | 是 | 初始工作区管理员的用户名 |
| `admin_name` | 是 | 初始工作区管理员的显示名称 |
| `admin_email` | 是 | 初始工作区管理员的邮箱地址 |
| `admin_password` | 是 | 初始工作区管理员的密码 |
| `enable_s3_storage` | 否 | 为上传文件创建私有 Sealos 对象存储；默认使用 GridFS |

计划在初始化向导中连接 Rocket.Chat Cloud 时，请填写能够接收确认邮件的邮箱地址。

## 部署指南

1. 打开 [Rocket.Chat 模板](https://sealos.io/products/app-store/rocketchat)，点击 **Deploy Now**。
2. 填写初始管理员的用户名、显示名称、邮箱地址和密码。
3. 保留 GridFS 上传存储，或启用 **S3 storage** 来创建私有 Sealos 对象存储桶。
4. 确认部署。Sealos 会创建应用、MongoDB、存储、HTTPS 域名和控制台入口。
5. 等待部署完成，通常需要 2-3 分钟，然后从 Canvas 打开 Rocket.Chat 应用卡片。

后续调整可在 Canvas 的 AI 对话框中描述需求，也可打开对应资源卡片修改配置和资源。

## 为什么选择 Sealos

- 通过一个模板部署完整的 Rocket.Chat 和 MongoDB 架构
- 使用托管的 KubeBlocks 数据库和可选私有对象存储桶
- 自动获得 HTTPS 域名和应用控制台入口
- 在同一个 Canvas 工作区查看日志、健康状态和资源用量

## 首次登录

1. 打开自动生成的 Rocket.Chat 域名。
2. 使用部署时填写的 `admin_username` 和 `admin_password` 登录。
3. 在初始化向导中填写组织信息。
4. 连接 Rocket.Chat Cloud 时，接受相关条款，并打开管理员邮箱收到的确认链接。
5. 返回工作区，创建频道或邀请团队成员。

管理员后续可继续使用同一用户名或邮箱地址和密码登录。管理员启用工作区注册后，其他用户可通过 **创建账户** 注册。

## 存储选项

### GridFS

GridFS 是默认存储模式。上传文件保存在 MongoDB 中，并跟随数据库生命周期。此模式适合体验环境和小型工作区。

### Sealos 对象存储

部署时启用 `enable_s3_storage`，模板会创建私有 S3 兼容存储桶。Rocket.Chat 通过 Sealos 管理的 Secret 获取存储桶端点和凭据，使用路径式访问，并通过短时效签名链接保护文件。此模式让上传对象与数据库分开管理，适合长期运行的工作区。

## 日常运维

部署完成后，可通过 Sealos Canvas：

- 查看 Rocket.Chat 和 MongoDB 的健康状态、资源用量和日志
- 打开自动生成的 HTTPS 域名
- 管理 MongoDB 数据库和可选对象存储桶
- 调整资源限制和应用设置
- 通过 Sealos 服务备份持久化应用数据

## 相关链接

- [Rocket.Chat 官网](https://rocket.chat/)
- [Rocket.Chat 文档](https://docs.rocket.chat/)
- [Docker 部署指南](https://docs.rocket.chat/deploy-with-docker-docker-compose)
- [Rocket.Chat 源码](https://github.com/RocketChat/Rocket.Chat)
- [Sealos 文档](https://sealos.io/docs/)

## 许可证

Rocket.Chat 8.6.1 采用混合许可证模式。企业目录以外的社区源码使用 MIT 许可证，`apps/meteor/ee/` 和 `ee/` 目录中的源码遵循 Rocket.Chat Enterprise Edition 许可证。用于生产环境前，请查看[官方 8.6.1 许可证](https://github.com/RocketChat/Rocket.Chat/blob/8.6.1/LICENSE)和适用的订阅条款。
