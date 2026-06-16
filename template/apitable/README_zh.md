# 在 Sealos 上部署和托管 APITable

APITable 是一个开源的 API 优先协作表格和数据库平台，可用于构建无代码数据应用。此模板会在 Sealos 上以多服务架构部署 APITable，并包含 MySQL、Redis、RabbitMQ 和 S3 兼容对象存储。

![APITable 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/apitable/website-screenshot.webp)

## 关于 APITable 托管

APITable 将类电子表格界面、实时协作、表单、权限、跨表关联和 API 能力组合在一起。团队可以用它搭建自托管的 Airtable 风格工作区，并保留开源后端。

此 Sealos 模板遵循 APITable 官方 Docker Compose 的服务布局，同时用 Sealos 托管资源替换本地 MySQL、Redis 和对象存储容器。部署后会自动获得公网 HTTPS 访问、服务发现、持久化数据库存储，以及可选的外部 S3 兼容存储。

APITable 首次冷启动会执行数据库初始化和模板数据导入。MySQL、Redis、RabbitMQ、迁移任务和应用服务启动完成前，应用 URL 可能需要等待数分钟。

## 常见使用场景

- **协作数据库**：用类表格体验管理结构化业务数据，并支持实时更新。
- **内部工具**：通过表格、表单、视图、权限和 API 构建轻量业务应用。
- **数据收集**：发布表单，将提交结果收集到结构化工作区。
- **API 优先工作流**：把 APITable 数据连接到脚本、组件、集成和自动化系统。
- **自托管 Airtable 替代方案**：在自己的基础设施边界内运行开源协作数据库栈。

## APITable 托管依赖

Sealos 模板包含社区版部署所需的运行依赖：

- APITable web server、backend server、room server、databus server、image proxy 和 gateway
- KubeBlocks MySQL，用于 APITable 关系型数据库
- KubeBlocks Redis，用于缓存和实时协作协调
- RabbitMQ，用于 APITable 队列任务
- 默认创建 Sealos ObjectStorageBucket，同时支持外部 S3 兼容桶

### 部署依赖

- [APITable GitHub 仓库](https://github.com/apitable/apitable) - 源码和官方 Docker Compose 部署文件
- [AITable 官方网站](https://aitable.ai) - 产品网站和托管服务
- [开发者中心](https://developers.aitable.ai/) - API、Widget 和脚本文档
- [REST API 文档](https://developers.aitable.ai/api/introduction/) - APITable API 参考
- [GitHub 安装指南](https://github.com/apitable/apitable#installation) - 官方自托管安装说明

## 实现细节

**架构组件：**

此模板部署以下服务：

- **Gateway**：基于 Nginx 的 HTTP 网关，保留 APITable 官方 web、API、room、notification、document 和 asset 路由。
- **Web Server**：提供 APITable 前端和静态资源。
- **Backend Server**：运行 APITable Java API 服务、认证、工作区 API 和对象存储集成。
- **Room Server**：运行实时协作、socket、fusion、notification 和 document 通道。
- **Databus Server**：提供 APITable databus API 服务。
- **Image Proxy**：代理和处理由 S3 兼容存储支撑的图片资源。
- **MySQL**：由 KubeBlocks 管理，保存 APITable 数据和迁移状态。
- **Redis**：由 KubeBlocks 管理，处理缓存和实时协作协调。
- **RabbitMQ**：为 APITable room 和 backend 工作流提供队列能力。
- **Object Storage**：使用 Sealos ObjectStorageBucket 或外部 S3 兼容桶存储附件和图片资源。

**配置：**

- 默认存储提供方会创建一个私有 Sealos ObjectStorageBucket。
- 选择 `external-s3` 后，可让 APITable 使用已有的 S3 兼容桶。
- 社区版部署启用注册，可通过密码创建第一个账号。
- 默认关闭邮件和短信发送，因此请使用内置注册/登录流程，通过邮箱地址和密码登录。
- APITable 上游文档建议 Docker 部署主机使用 4 CPU 和 8 GB 内存。此模板采用更小的组件级资源起步，业务增长后可在 Sealos Canvas 中扩容。

**许可证信息：**

APITable 使用 GNU Affero General Public License v3.0 许可证。此 Sealos 模板遵循 Sealos templates 项目的仓库许可证条款。

## 为什么在 Sealos 上部署 APITable？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一应用部署、数据库供应、存储、网络和运维。将 APITable 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单，即可部署完整 APITable 栈。
- **托管数据库**：通过 KubeBlocks 创建带持久化存储的 MySQL 和 Redis。
- **内置对象存储**：使用私有 S3 兼容桶保存上传文件和附件。
- **即时 HTTPS 访问**：每个部署都会获得自动 TLS 的公网 URL。
- **Canvas 运维**：在 Sealos Canvas 中调整资源、查看日志并更新环境变量。
- **按量资源使用**：先用较小配置启动，再按真实负载扩容单个服务。

在 Sealos 上部署 APITable，把精力集中在数据工作流上。

## 部署指南

1. 打开 [APITable 模板](https://sealos.io/products/app-store/apitable)，点击 **Deploy Now**。
2. 选择存储提供方：
   - `sealos-objectstorage`：创建并使用私有 Sealos ObjectStorageBucket。
   - `external-s3`：填写已有 S3 兼容 endpoint、public endpoint、access key、secret key、bucket 和 region。
3. 点击 **Deploy** 并等待栈初始化。部署开始后会进入 Canvas；APITable 冷启动和数据库导入可能需要数分钟。
4. 打开生成的 APITable URL。
5. 在登录或注册页面使用邮箱地址和密码创建第一个账号。
6. 使用该账号登录，然后从 APITable workbench 创建或打开工作区。

## 配置

部署完成后，可通过以下方式配置 APITable：

- **APITable UI**：在 Web 界面中管理工作区、datasheet、表单、权限和 API token。
- **Sealos Canvas**：打开资源卡片查看日志、编辑环境变量或调整服务资源。
- **AI Dialog**：在 Canvas 对话框中描述运维变更，让 Sealos 应用支持的更新。
- **对象存储输入**：当需要把 APITable 资源保存到已有桶时，使用 `external-s3` 重新部署。

## 扩容

APITable 由多个服务组成，请按瓶颈服务扩容：

1. 打开 APITable 部署对应的 Canvas。
2. 查看 backend-server、room-server、MySQL、Redis 和 RabbitMQ 的指标与日志。
3. API 请求变慢时，提高 backend-server 的 CPU 或内存。
4. 协作会话、websocket 流量或 fusion API 用量增长时，提高 room-server 资源。
5. 大量附件元数据或 datasheet 负载增长前，提高 MySQL 存储容量。

## 故障排查

**首次启动需要数分钟**

APITable 冷启动会执行数据库创建、schema 迁移和应用数据导入。请等待 MySQL、Redis、RabbitMQ、init-db、init-appdata、backend-server、room-server、web-server、databus-server、imageproxy-server 和 gateway 都进入健康状态。

**登录页能打开，但注册失败**

优先查看 backend-server 日志。数据库迁移、对象存储凭据或 RabbitMQ 连接错误通常会在这里暴露。

**上传或图片加载失败**

检查选择的 S3 提供方。使用 `external-s3` 时，确认 endpoint、public endpoint、access key、secret key、bucket 和 region 有效，并且 APITable 可以访问。

### 获取帮助

- [APITable GitHub Issues](https://github.com/apitable/apitable/issues)
- [开发者中心](https://developers.aitable.ai/)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [AITable 官方网站](https://aitable.ai)
- [APITable GitHub 仓库](https://github.com/apitable/apitable)
- [REST API 文档](https://developers.aitable.ai/api/introduction/)
- [Widget SDK](https://developers.aitable.ai/widget/introduction/)
- [Scripting Widget](https://developers.aitable.ai/script/introduction/)

## 许可证

此 Sealos 模板遵循 Sealos templates 项目的许可证。APITable 本身使用 GNU Affero General Public License v3.0 许可证。
