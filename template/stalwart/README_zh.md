# 在 Sealos 上部署和托管 Stalwart

Stalwart 是一个开源邮件与协作服务器，支持 SMTP、IMAP、JMAP、CalDAV、CardDAV、WebDAV、垃圾邮件过滤和 Web 管理控制台。此模板会在 Sealos Cloud 上部署使用 PostgreSQL 数据存储的 Stalwart。

![Stalwart 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/stalwart/website-screenshot.webp)

## 关于托管 Stalwart

Stalwart 以单节点邮件与协作服务器运行，并使用 Sealos 托管的 PostgreSQL 数据库作为后端。模板遵循 Stalwart 官方 Kubernetes 运行模型：StatefulSet 使用 `/etc/stalwart/config.json` 启动容器，使用 PostgreSQL 作为外部 DataStore，并通过 Sealos Ingress 暴露 HTTP 管理入口。

部署会自动创建 PostgreSQL、初始化 `stalwart` 数据库，并在数据库就绪后启动 Stalwart 容器。Web 管理控制台位于 `/admin`，生产邮件投递还需要额外的 L4 端口暴露和 DNS 记录。

## 常见使用场景

- **企业邮件托管**：为托管域名提供 SMTP、IMAP、POP3 和 submission 服务。
- **协作服务器**：提供日历、联系人、文件共享和 JMAP 兼容访问。
- **邮件安全网关**：使用 Stalwart 的垃圾邮件和钓鱼防护处理收发邮件。
- **自托管邮件实验环境**：测试邮件服务器配置、DNS 记录和客户端兼容性。

## Stalwart 托管依赖

Sealos 模板包含 Stalwart、PostgreSQL 16.4 KubeBlocks 集群、数据库初始化 Job、Kubernetes StatefulSet、Service、Ingress 和 Sealos App 链接。

### 部署依赖

- [官方网站](https://stalw.art/) - Stalwart 产品信息
- [官方文档](https://stalw.art/docs/) - 安装和配置指南
- [Kubernetes 部署指南](https://stalw.art/docs/cluster/orchestration/kubernetes/) - 官方 Kubernetes 运行模型
- [GitHub 仓库](https://github.com/stalwartlabs/stalwart) - 源码和版本发布

### 实现细节

**架构组件：**

此模板部署以下服务：

- **Stalwart StatefulSet**：运行 `stalwartlabs/stalwart:v0.16.7`，并使用官方 `--config /etc/stalwart/config.json` 启动契约。
- **PostgreSQL**：使用官方 PostgreSQL DataStore 配置存储 Stalwart 主数据。
- **数据库初始化 Job**：在 PostgreSQL 可访问后创建 `stalwart` 数据库。
- **Sealos Ingress**：通过 HTTPS 发布 Web 管理控制台和健康检查端点。
- **可选对象存储**：启用后创建 Sealos ObjectStorageBucket，并注入 S3 兼容凭据，供后续在 WebUI 中配置 BlobStore。

**配置：**

- 使用部署时配置的引导密码和用户名 `admin` 登录 `/admin`。
- 健康检查端点为 `/healthz/live` 和 `/healthz/ready`。
- 使用 Stalwart WebUI 配置域名、DNS 记录、DKIM、TLS 证书、账号和存储后端。
- 如需 S3 Blob 存储，部署时启用对象存储，然后在 **Settings > Storage > Blob Store** 中用注入的凭据配置 S3 兼容 BlobStore。

**邮件 DNS 和端口：**

Sealos Ingress 暴露 HTTPS 管理入口。SMTP、submission、IMAP、POP3 和 ManageSieve 属于 L4 协议，生产邮件托管还需要显式暴露所需 TCP 端口，配置 MX/SPF/DKIM/DMARC、反向 DNS，并确认服务商出站邮件策略。

**许可证信息：**

Stalwart 使用 AGPL-3.0 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Stalwart？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 开发到生产部署和管理的应用生命周期。在 Sealos 上部署 Stalwart，你可以获得：

- **一键部署**：通过 App Store 模板部署 Stalwart 和 PostgreSQL。
- **Kubernetes 基础设施**：以托管 Kubernetes 工作负载运行 Stalwart，并使用持久化数据库存储。
- **易于自定义**：在 Canvas 中调整环境变量、资源和存储。
- **公开 HTTPS 访问**：通过自动 HTTPS URL 访问 WebUI。
- **按量资源成本**：从紧凑资源配置起步，并在邮件量增长时扩容。

## 部署指南

1. 打开 [Stalwart 模板](https://sealos.io/products/app-store/stalwart)，点击 **Deploy Now**。
2. 配置引导管理员密码，并选择是否创建 Sealos 对象存储。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续修改可以在对话框中描述需求让 AI 应用更新，也可以点击相关资源卡片修改设置。
4. 通过提供的 URL 访问应用：
   - **Web 管理端**：打开 `https://[your-stalwart-url]/admin`，使用用户名 `admin` 和引导密码登录。
   - **健康检查**：使用 `/healthz/live` 和 `/healthz/ready` 做 Web 健康监控。

## 配置

部署后，在 Stalwart WebUI 中完成邮件服务器设置：

- **Domains**：添加邮件域名并查看生成的 DNS 记录。
- **Accounts**：创建邮件用户和管理员账号。
- **DNS**：发布 MX、SPF、DKIM、DMARC、MTA-STS 等真实邮件投递需要的记录。
- **Ports**：通过合适的 L4 路径暴露 SMTP、submission、IMAP、POP3 和 ManageSieve 所需 TCP 端口。
- **Object Storage**：部署时启用对象存储后，在 WebUI 中配置 S3 兼容 Blob 存储。
- **Canvas**：使用 Sealos Canvas、AI 对话和资源卡片调整资源与环境变量。

## 扩展

默认单节点部署适合初始化和评估。生产邮件托管前，需要审查 CPU、内存、数据库容量、TCP 端口暴露、DNS 信誉和备份要求。

调整资源：

1. 打开部署对应的 Canvas。
2. 点击 Stalwart StatefulSet 或 PostgreSQL 资源卡片。
3. 调整 CPU、内存、存储或运行参数。
4. 在对话框中应用更改。

## 故障排查

### 管理员登录

- 原因：引导密码输入错误。
- 解决方案：使用用户名 `admin` 和部署时配置的密码登录。

### 健康检查端点

- 原因：PostgreSQL 仍在启动，或数据库初始化 Job 尚未完成。
- 解决方案：等待 PostgreSQL 和 Stalwart StatefulSet 就绪后，再访问 `/healthz/ready`。

### 邮件投递

- 原因：Web HTTPS 访问已可用，邮件协议端口或 DNS 记录仍未完整配置。
- 解决方案：发送生产邮件前，配置 L4 TCP 暴露并发布 Stalwart 生成的 DNS 记录。

### 获取帮助

- [官方文档](https://stalw.art/docs/)
- [GitHub Issues](https://github.com/stalwartlabs/stalwart/issues)
- [Stalwart 社区](https://github.com/stalwartlabs/stalwart#community)

## 更多资源

- [Docker 安装指南](https://stalw.art/docs/install/platform/docker/)
- [PostgreSQL 后端文档](https://stalw.art/docs/storage/backends/postgresql/)
- [S3 兼容后端文档](https://stalw.art/docs/storage/backends/s3/)
- [DNS 设置指南](https://stalw.art/docs/install/dns/)

## 许可证

此 Sealos 模板遵循仓库许可证。Stalwart 本身使用 AGPL-3.0 许可证。
