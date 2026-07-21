# Penpot

面向产品团队协作的开源设计与原型平台。此模板会在 Sealos Cloud 上部署 Penpot 2.16.2，并配置独立的前端、后端、导出器、PostgreSQL 和 Redis 服务。

![Penpot 工作区](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/penpot/website-screenshot.webp)

## 功能亮点

- 支持界面设计、交互原型、设计系统、多人协作和开发交付
- 首次打开即可通过浏览器注册账号并使用密码登录
- 由 KubeBlocks 管理私有 PostgreSQL 数据库和启用认证的 Redis 服务
- 默认使用持久化文件系统，也可选择私有 Sealos 对象存储
- 自动配置 HTTPS、公网域名、健康检查和应用监控

## 部署架构

此模板会部署以下服务：

- **Penpot Frontend**：提供 Web 界面，并代理 API、资源、WebSocket 和导出请求。
- **Penpot Backend**：处理身份验证、项目、文件、协作和资源存储。
- **Penpot Exporter**：在独立服务中渲染可下载的设计导出文件。
- **PostgreSQL**：保存账号、团队、项目、设计文件和应用元数据。
- **Redis**：为消息传递和实时通知提供认证服务。
- **Sealos Object Storage**：仅在启用 `enable_s3_storage` 时创建。

默认文件系统模式会创建一个由前端和后端共享的持久卷，用于保存和交付资源。S3 模式会把上传对象存入私有 Sealos 存储桶，同时保持应用和数据库拓扑一致。

## 部署指南

1. 打开 [Penpot 模板](https://sealos.io/products/app-store/penpot)，点击 **Deploy Now**。
2. 保留默认文件系统，或启用 **S3 storage** 来创建私有 Sealos 对象存储桶。
3. 确认部署。Sealos 会自动创建应用、数据库、存储、HTTPS 域名和控制台入口。
4. 等待部署完成，通常需要 2-3 分钟。资源就绪后，页面会跳转到 Canvas。
5. 从 Canvas 打开 Penpot 应用卡片。

后续调整可直接在 Canvas 的 AI 对话框中描述需求，也可以打开对应资源卡片修改配置和资源。

## 注册与登录

打开 Penpot 后会进入登录页。

1. 点击 **创建账号**。
2. 填写姓名、工作邮箱和至少 8 位的密码。
3. 完成简短的新手引导，进入工作台。
4. 创建项目，再创建一个设计文件即可开始使用。

此自托管模板关闭了邮箱验证，账号注册后会立即生效。再次访问时，使用同一邮箱和密码登录即可。面向公网开放自由注册前，建议在 Penpot 后端配置 SMTP 并启用邮箱验证。

## 存储选项

### 持久化文件系统

默认模式使用一个由前端和后端共享的 1 GiB ReadWriteOnce 持久卷保存上传资源。调度器会把两个工作负载共置在同一节点，并在后端替换时优先沿用该节点。此模式适合个人工作区和体验环境。

### Sealos 对象存储

部署时启用 `enable_s3_storage`，模板会创建私有存储桶，并把兼容 S3 的访问凭据注入 Penpot。此模式让应用资源独立于工作负载调度，适合长期运行和多节点部署。

公网上传链路在 Penpot Frontend、Penpot Backend 和 Sealos Ingress 三层统一使用 32 MiB 单文件上限。

## 日常运维

部署完成后，可通过 Sealos Canvas：

- 查看前端、后端、导出器、PostgreSQL 和 Redis 的运行状态
- 检查各服务日志和健康检查结果
- 通过资源卡片调整资源限制或环境变量
- 打开数据库或对象存储管理界面
- 管理自动生成的 HTTPS 域名

## 相关链接

- [Penpot 官网](https://penpot.app/)
- [Penpot 文档](https://help.penpot.app/)
- [Penpot 源码](https://github.com/penpot/penpot)
- [Sealos 文档](https://sealos.io/docs/)
