# 在 Sealos 上部署和托管 Stalwart

Stalwart 是一个开源邮件与协作服务器，支持 SMTP、IMAP、JMAP、CalDAV、CardDAV、WebDAV、垃圾邮件过滤和 Web 管理控制台。此模板会在 Sealos Cloud 上将 Stalwart 0.16.16 部署为单节点持久化服务器。

![Stalwart 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/stalwart/website-screenshot.webp)

## 关于托管 Stalwart

Stalwart 在一个服务器中整合邮件传输、邮箱访问、日历、联系人、共享文件和安全控制。模板会自动执行 Stalwart 官方引导流程，创建主域名和永久管理员，应用部署表单中填写的密码，并启动正常服务器配置。

数据库和 BlobStore 可以独立选择。PostgreSQL 16 是默认托管 DataStore，SQLite 则提供紧凑的单节点持久化选项。邮件正文和其他 Blob 可以存储在所选 DataStore 或私有 Sealos 对象存储桶中。

## 常见使用场景

- **企业邮件托管**：为组织域名提供邮箱和邮件投递服务
- **协作服务器**：提供日历、联系人、共享文件和基于标准的同步
- **邮件传输代理**：使用内置垃圾邮件和网络钓鱼防护处理入站与出站 SMTP
- **JMAP 后端**：通过统一 API 支持现代邮件与协作客户端
- **自托管邮件实验环境**：评估邮件客户端、DNS 记录、策略和投递流程

## Stalwart 托管依赖

模板包含固定摘要的 Stalwart 0.16.16 镜像、1Gi 持久化应用卷、HTTPS Ingress，以及可选的托管 PostgreSQL 和对象存储资源。

### 部署依赖

- [Stalwart 文档](https://stalw.art/docs/) - 安装、管理和协议文档
- [引导模式](https://stalw.art/docs/configuration/bootstrap-mode/) - 官方初始配置流程
- [Kubernetes 部署指南](https://stalw.art/docs/cluster/orchestration/kubernetes/) - 官方 Kubernetes 运行指南
- [PostgreSQL 后端](https://stalw.art/docs/storage/backends/postgresql/) - PostgreSQL DataStore 配置
- [SQLite 后端](https://stalw.art/docs/storage/backends/sqlite/) - SQLite DataStore 配置
- [S3 兼容后端](https://stalw.art/docs/storage/backends/s3/) - S3 BlobStore 配置
- [Stalwart 版本发布](https://github.com/stalwartlabs/stalwart/releases) - 源码和版本历史

## 实现细节

### 架构组件

- **Stalwart StatefulSet**：通过不可变镜像摘要运行一个 `stalwartlabs/stalwart:v0.16.16` 副本
- **引导 Init Container**：使用 Stalwart 管理 API 配置域名、存储、永久管理员、密码和安全监听器默认值
- **应用存储**：在 `/var/lib/stalwart` 挂载 1Gi 持久化卷，用于保存 `config.json`、SQLite 数据、日志和引导状态
- **PostgreSQL 16**：启用后创建独立的 KubeBlocks 集群和数据库初始化 Job
- **Sealos 对象存储**：启用后创建私有存储桶，并将其连接为 Stalwart 的 S3 BlobStore
- **Ingress 和 Service**：通过 HTTPS 发布 Web 界面，并定义内部 SMTP、submission、IMAP、POP3、ManageSieve、HTTP 和 HTTPS 端口

### 配置选项

| 输入项 | 默认值 | 结果 |
| --- | --- | --- |
| `default_domain` | 用户填写 | 创建主邮件域名和管理员身份 |
| `admin_password` | 用户填写 | 设置永久管理员密码 |
| `use_postgresql` | `true` | 使用独立的托管 PostgreSQL 16 DataStore |
| `use_postgresql` | `false` | 使用位于 `/var/lib/stalwart/stalwart.db` 的 SQLite |
| `enable_s3_storage` | `false` | 将 Blob 存储在所选 DataStore 中 |
| `enable_s3_storage` | `true` | 将 Blob 存储在私有 Sealos 对象存储桶中 |

引导流程使用 Stalwart 当前的对象配置模型写入 `/var/lib/stalwart/config.json`。PostgreSQL 凭据和 S3 凭据从 Sealos 托管的 Kubernetes Secret 读取。S3 写入启用 `verifyAfterWrite`，Stalwart 会确认每个上传对象均可读取。

### 网络端口

| 端口 | 协议 | 用途 |
| --- | --- | --- |
| `25` | SMTP | 服务器之间的邮件投递 |
| `465` | TLS 上的 Submissions | 经过身份认证的邮件提交 |
| `993` | IMAPS | 通过 TLS 访问邮箱 |
| `995` | POP3S | 通过 TLS 进行 POP3 邮箱访问 |
| `4190` | ManageSieve | Sieve 脚本管理 |
| `8080` | HTTP | 健康检查和 Ingress 后端 |
| `443` | HTTPS | Stalwart 原生 HTTPS 监听器 |

Sealos Ingress 通过生成的 HTTPS 应用 URL 发布 HTTP 监听器。生产邮件流量需要为所选邮件协议端口配置公网 L4 映射，并配套合适的服务商策略和反向 DNS。

## 为什么在 Sealos 上部署 Stalwart？

Sealos 是基于 Kubernetes 的云操作系统，通过可视化 Canvas 和 AI 辅助操作管理应用资源。此 Stalwart 部署提供：

- **一键引导**：通过一个表单创建域名、管理员、数据库和所选 Blob 存储
- **持久化状态**：在 Pod 重启后保留配置和本地数据
- **托管存储选项**：可独立选择 PostgreSQL 或 SQLite，以及本地或 S3 Blob 存储
- **安全 Web 访问**：获得 HTTPS 管理端点和托管证书
- **资源控制**：通过 Canvas 调整 CPU、内存和存储
- **按量资源成本**：仅创建工作负载所选的数据库和对象存储

## 部署指南

1. 打开 [Stalwart 模板](https://sealos.io/products/app-store/stalwart)，点击 **Deploy Now**。
2. 输入主邮件域名，例如 `example.com`。
3. 输入至少八个字符的强管理员密码。
4. 保持启用 PostgreSQL 以使用托管数据库，或清除该选项以使用持久化 SQLite。
5. 启用 S3 存储以创建私有 Blob 存储桶，或将 Blob 保存在所选 DataStore 中。
6. 提交表单并等待 Stalwart StatefulSet 进入 Ready 状态。PostgreSQL 部署在数据库集群启动期间可能需要几分钟。
7. 打开应用 URL 的 `/admin`，使用 `admin@<default_domain>` 和部署表单中填写的密码登录。

## 登录与首次设置

模板会在引导期间创建永久管理员。域名输入为 `example.com` 时，使用 `admin@example.com` 作为用户名。登录后可以在 **Directory > Accounts** 中创建新邮件用户。

首次登录后：

1. 打开 **Management > Directory > Domains**，选择主域名。
2. 查看生成的 DNS 记录和 DKIM 公钥。
3. 在 **Directory > Accounts** 中创建邮件账户。
4. 为客户端所需的邮件协议端口配置公网 L4 访问。
5. 在生产投递前发布 MX、SPF、DKIM、DMARC、MTA-STS 和反向 DNS 记录。

## 端点

| 端点 | 用途 |
| --- | --- |
| `/admin` | 打开 Web 管理控制台 |
| `/jmap/session` | 获取经过身份认证的 JMAP 会话 |
| `/jmap` | 发送 JMAP 和 Stalwart 管理请求 |
| `/healthz/live` | 检查进程存活状态 |
| `/healthz/ready` | 检查服务就绪状态 |

后续资源调整可以使用 Sealos Canvas AI 对话或资源卡片。此模板的持久化应用卷和引导状态面向单服务器设计，请保持一个 Stalwart 副本。

## 故障排查

### 管理员登录失败

使用完整管理员地址 `admin@<default_domain>` 和部署表单中填写的准确密码。登录前确认 StatefulSet 已进入 Ready 状态。

### PostgreSQL 启动需要几分钟

等待 KubeBlocks PostgreSQL 集群和 `pg-init` Job 完成。Stalwart Init Container 会阻止引导继续，直至 `stalwart` 数据库能够接受查询。

### S3 Blob 上传失败

确认 ObjectStorageBucket 及其生成的存储桶 Secret 已就绪。Stalwart 会在引导期间验证 S3 端点，并验证每次成功的对象写入。

### 邮件客户端无法连接

为所需邮件协议端口创建公网 L4 映射，并配置匹配的 DNS 记录。生成的应用 URL 用于 Web 管理端点。

### 获取帮助

- [Stalwart 文档](https://stalw.art/docs/)
- [Stalwart GitHub Issues](https://github.com/stalwartlabs/stalwart/issues)
- [Stalwart 支持](https://stalw.art/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循仓库许可证。Stalwart Community Edition 使用 AGPL-3.0 许可证；详情请参阅 [Stalwart 许可证](https://github.com/stalwartlabs/stalwart/blob/main/LICENSES/AGPL-3.0-only.txt)。
