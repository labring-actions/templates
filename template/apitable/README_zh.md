# 在 Sealos 上部署和托管 APITable

APITable 是一个开源的 API 优先协作表格和数据库平台，可用于构建数据应用。此模板会部署 APITable 社区版服务拓扑，并提供托管 MySQL、托管 Redis、RabbitMQ 和可选的私有 S3 兼容存储。

![APITable 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/apitable/website-screenshot.webp)

## 关于 APITable 托管

APITable 在自托管工作区中提供 datasheet、表单、实时协作、权限、跨表关联和 API。此模板遵循官方 `v1.13.0-beta.1` Docker Compose 拓扑，并将每个应用镜像固定到具体版本或摘要。

全新部署会先执行数据库创建、schema 迁移和模板数据导入，随后 Web 应用进入就绪状态。完整冷启动通常需要数分钟。

## 部署内容

| 组件 | 用途 | 默认限制 |
| --- | --- | --- |
| Backend Server | 认证、工作区 API 和存储集成 | 1 CPU / 1 GiB |
| Room Server | 实时协作和文档通道 | 1 CPU / 1 GiB |
| Web Server | 前端和静态资源 | 200m / 256 MiB |
| Databus Server | Databus API | 200m / 256 MiB |
| Gateway | 公网 HTTPS 路由 | 100m / 128 MiB |
| Image Proxy | 图片读取和转换 | 100m / 128 MiB |
| MySQL | 关系型应用数据 | 500m / 512 MiB，1 GiB 卷 |
| Redis | 缓存和协调 | 500m / 512 MiB，1 GiB 卷 |
| RabbitMQ | 队列任务 | 500m / 512 MiB，1 GiB 卷 |

CPU 和内存请求量设为对应限制的 10%，让部署保持经济的调度基线，同时为 APITable 保留必要的运行余量。

## 存储模式

`enable_s3_storage` 输入控制附件和图片存储。

| 值 | 行为 |
| --- | --- |
| `true`（默认） | 创建私有 Sealos `ObjectStorageBucket`，并把自动生成的 S3 凭据注入 APITable。 |
| `false` | 运行协作和数据库栈，关闭基于对象存储的附件、图片和上传能力。 |

托管桶采用私有策略。APITable 会生成授权资源请求，匿名对象读取会收到 HTTP 403。

## 账号与访问

生成的应用地址会打开 APITable 登录页。社区版注册支持邮箱地址和密码；此模板关闭邮件和短信发送。每个全新部署都会开放密码注册，请在创建预期管理员账号后应用网络或注册策略。

## 部署指南

1. 打开 [APITable 模板](https://sealos.io/products/app-store/apitable)，选择 **Deploy Now**。
2. 需要附件和图片时保留 `enable_s3_storage=true`；数据库工作区可选择 `false`。
3. 启动部署，等待 MySQL、Redis、RabbitMQ、初始化 Job 和六个 APITable 服务全部就绪。
4. 打开生成的 HTTPS 地址，使用邮箱地址和密码注册。
5. 登录后创建工作区和第一张 datasheet。

## 配置

- **APITable UI**：管理工作区、datasheet、表单、权限和 API token。
- **Sealos Canvas**：查看日志、资源指标、Service、数据库和持久化卷。
- **对象存储**：附件和图片工作流需要 `enable_s3_storage=true`。
- **应用注册**：管理员初始化完成后，可按环境要求调整 APITable 注册设置。

## 扩容

请按照观测到的瓶颈扩容对应组件。Backend API 负载主要影响 Backend Server 和 MySQL；协作会话主要影响 Room Server、Redis 和 RabbitMQ；附件流量主要影响 Backend Server、Image Proxy 和对象存储。

经过验证的启动下限为 Backend Server 与 Room Server 各 1 GiB。Room Server 使用 512 MiB 冷启动时发生 OOMKilled，退出码为 137；1 GiB 配置达到就绪状态且重启数为零。

## 运行验证

此模板已通过 Sealos Template API 分别部署两种存储模式。两个分支均达到完整就绪状态且重启数为零。全新用户完成了注册、密码登录、已认证个人信息读取、工作区创建和 datasheet 创建；MySQL 中能够查询到对应工作区和 datasheet 数据行。

托管 S3 分支还完成了已知字节上传、认证下载、预签名下载、SHA-256 对比、匿名访问检查和对象删除。

## 故障排查

### 登录页仍在启动

检查初始化 Job，并等待 MySQL、Redis、RabbitMQ、Backend Server、Room Server、Web Server、Databus Server、Image Proxy 和 Gateway 全部就绪。

### 注册或工作区创建失败

查看 Backend Server 日志，然后检查 MySQL 凭据 Secret、RabbitMQ 就绪状态和 Redis 地址。

### 附件或图片失败

确认已启用 `enable_s3_storage`，并检查 `ObjectStorageBucket` 和自动生成的 `object-storage-key` Secret。

## 资源

- [AITable 官方网站](https://aitable.ai/)
- [APITable GitHub 仓库](https://github.com/apitable/apitable)
- [官方 Docker Compose](https://github.com/apitable/apitable/blob/v1.13.0-beta.1/docker-compose.yaml)
- [开发者中心](https://developers.aitable.ai/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

APITable 使用 GNU Affero General Public License v3.0。此模板遵循 Sealos templates 仓库许可证。
