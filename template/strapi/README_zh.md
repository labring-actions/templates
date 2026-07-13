# 在 Sealos 上部署和托管 Strapi

Strapi 是一款开源无头内容管理系统，可用于创建内容模型、管理内容，并提供 REST API。本模板使用 Node.js 22 构建 Strapi 5.50.1，并在 Sealos 云上以生产模式运行。

![Strapi 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/strapi/website-screenshot.webp)

## 关于 Strapi 托管

Strapi 为内容编辑者提供管理界面，同时为网站、移动应用和其他客户端提供 API。项目文件、SQLite 数据和本地媒体文件共享持久化应用存储，Pod 重启后数据仍会保留。

模板提供两组独立的存储选项。PostgreSQL 16 是默认生产数据库，SQLite 适合精简的单实例部署；媒体文件可存放在本地持久卷中，也可通过 Strapi 的 AWS S3 上传提供商写入 Sealos 私有对象存储桶。

## 常见使用场景

- **网站 CMS**：为前端框架和静态网站管理结构化内容
- **移动应用后端**：通过 REST API 发布内容
- **产品目录**：管理产品、分类、媒体及其关联关系
- **编辑发布平台**：为内容团队提供独立的管理流程
- **内部 API**：构建带有角色权限控制的自定义内容 API

## Strapi 托管依赖

模板包含固定镜像摘要的 Node.js 22 运行时、经过校验的 Strapi 5.50.1 依赖锁文件、持久化应用存储，以及可选的托管 PostgreSQL 和对象存储资源。

### 部署依赖

- [Strapi 文档](https://docs.strapi.io/) - 产品与开发者文档
- [Strapi 部署指南](https://docs.strapi.io/cms/deployment) - 生产部署指南
- [Strapi AWS S3 提供商](https://docs.strapi.io/cms/configurations/media-library-providers#amazon-s3) - S3 上传提供商配置
- [PostgreSQL 文档](https://www.postgresql.org/docs/16/) - PostgreSQL 16 文档

## 实现细节

### 架构组件

- **Strapi 应用**：使用固定镜像摘要的 Node.js 22 和 `npm ci` 安装、构建并启动 Strapi 5.50.1
- **应用存储**：1Gi 持久卷，用于保存项目文件、SQLite 数据和本地上传文件
- **依赖存储**：独立的 1Gi 持久卷，每次冷启动从已校验的依赖归档恢复
- **PostgreSQL 16**：启用 `use_postgresql` 时创建独立的 KubeBlocks 数据库
- **Sealos 对象存储**：启用 `enable_s3_storage` 时创建私有存储桶并注入托管凭据
- **Ingress**：通过 HTTPS 访问管理界面和内容 API

### 配置选项

| 输入项 | 默认值 | 结果 |
| --- | --- | --- |
| `admin_email` | 部署时填写 | 在公网应用启动前创建首位管理员 |
| `admin_password` | 部署时填写 | 设置必填的首位管理员密码 |
| `admin_firstname` | `Admin` | 设置首位管理员名字 |
| `admin_lastname` | `User` | 设置首位管理员姓氏 |
| `use_postgresql` | `true` | 使用托管 PostgreSQL 16 数据库 |
| `use_postgresql` | `false` | 使用持久卷中的 `.tmp/data.db` SQLite 数据库 |
| `enable_s3_storage` | `false` | 将上传文件存入持久卷中的 `public/uploads` |
| `enable_s3_storage` | `true` | 通过 AWS S3 提供商使用 Sealos 私有对象存储桶 |

部署时，模板会生成 Strapi 应用密钥、JWT 密钥、令牌盐值和 `ENCRYPTION_KEY`。构建初始化容器会在公网应用进入就绪状态前创建首位管理员。Strapi 会直接使用 KubeBlocks 管理的 PostgreSQL 连接密钥。最小权限 Job 与 CronJob 会跟踪该密钥版本，并在凭据轮换后只重启 Strapi Pod。对象存储凭据来自 Sealos 托管密钥。

## 为什么在 Sealos 上部署 Strapi？

Sealos 是基于 Kubernetes 的云操作系统，可通过可视化 Canvas 和 AI 辅助运维管理应用资源。本 Strapi 模板提供以下能力：

- **一键部署**：通过同一表单创建应用及所选托管服务
- **数据持久化**：在重启后保留项目文件、SQLite 数据和本地上传文件
- **托管服务**：通过明确选项添加 PostgreSQL 16 和私有对象存储
- **安全公网访问**：自动获得 HTTPS 地址和托管证书
- **资源控制**：通过 Canvas 调整 CPU、内存和存储
- **按量使用资源**：根据所选架构分配对应服务

## 部署指南

1. 打开 [Strapi 模板](https://sealos.io/products/app-store/strapi)，点击 **Deploy Now**。
2. 填写首位管理员邮箱、密码、名字和姓氏。密码需包含大写字母、小写字母、数字和特殊字符。
3. 生产数据库可保留 PostgreSQL；精简单实例可取消该选项并使用持久化 SQLite。
4. 媒体文件需要 S3 存储时启用 Sealos 对象存储；本地模式会使用持久卷。
5. 提交表单并等待部署完成。首次依赖校验安装和管理界面构建可能需要几分钟。
6. 打开 `/admin/auth/login`，使用部署表单中的管理员邮箱和密码登录。

## 登录

模板会在应用 Service 进入就绪状态前创建首位 Strapi 管理员，从而关闭公网首用户注册窗口。请在 `/admin/auth/login` 使用部署时填写的 `admin_email` 和 `admin_password` 登录，并将凭据保存在密码管理器中。后续管理员可在 Strapi 管理界面中维护。

## 配置

部署完成后，可在 Strapi 管理界面维护内容条目、配置角色并生成 API 令牌。Strapi 的内容类型构建器仅在开发模式下运行，生产环境的内容模型调整应在项目代码中完成，并通过受控构建发布。主要端点如下：

| 端点 | 用途 |
| --- | --- |
| `/admin/auth/login` | 登录管理界面 |
| `/admin` | 打开管理界面 |
| `/api` | 访问生成的 REST 端点 |
| `/_health` | 检查应用健康状态 |

后续资源调整可通过 Sealos Canvas 的 AI 对话框或资源卡片完成。SQLite 和本地上传模式共用单个持久卷，建议保持一个 Strapi 副本。

## 故障排查

### 管理页面仍在启动

首次部署会校验内嵌锁文件、运行 `npm ci`、创建首位管理员、打包运行依赖并构建管理界面。请在 Canvas 中查看 `strapi-build` 和 `strapi-runtime-deps` 初始化容器日志，等待两个阶段完成。

### PostgreSQL 启动失败

确认 PostgreSQL 资源已进入运行状态。幂等的 `pg-init` Job 会通过系统生成的连接密钥创建 `strapi` 数据库，`wait-postgresql` 初始化容器会持续等待该数据库就绪后再启动应用。

### 媒体上传失败

本地上传模式下，请确认应用持久卷仍有可用容量。对象存储模式下，请确认存储桶资源及其生成的存储桶密钥已经就绪。

### API 请求返回 403

在 Strapi 管理界面的 **Settings > Users & Permissions plugin > Roles** 中配置所需权限。

### 获取帮助

- [Strapi 文档](https://docs.strapi.io/)
- [Strapi GitHub Issues](https://github.com/strapi/strapi/issues)
- [Strapi 社区论坛](https://forum.strapi.io/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板采用 MIT 许可证。Strapi 使用自身的许可条款，详情请参阅 [Strapi 许可证](https://github.com/strapi/strapi/blob/develop/LICENSE)。
