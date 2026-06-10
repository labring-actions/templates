# 在 Sealos 上部署并托管 Joplin Server

Joplin Server 是 Joplin 笔记、用户、共享和发布功能的开源同步后端。本模板会在 Sealos Cloud 上部署 Joplin Server 3.7.1，并自动配置 PostgreSQL 和 HTTPS Ingress。

![Joplin 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/joplin/website-screenshot.webp)

## 关于在 Sealos 上托管 Joplin Server

Joplin Server 为 Joplin 桌面端和移动端保存笔记元数据、笔记内容、附件、用户、会话、共享和发布状态。它在同一个 HTTP 服务上提供管理界面和同步 API。

这个 Sealos 模板会创建 PostgreSQL 集群、用于创建 `joplin` 数据库的初始化 Job、Joplin Server 容器、HTTPS Ingress 和 App 启动入口。模板遵循 Joplin 官方 Docker Compose 示例中的 server profile，并使用外接 PostgreSQL。

## 常见使用场景

- **个人笔记同步**：在 Joplin 桌面端和移动端之间同步笔记与资源。
- **团队笔记托管**：创建用户，并集中管理团队笔记同步。
- **自托管发布**：从自己的工作区托管共享笔记和发布内容。
- **私有知识库**：把笔记数据保存在可控的 Sealos 环境中。

## Joplin Server 托管依赖

本模板包含运行所需依赖：Joplin Server、PostgreSQL、数据库初始化 Job、Service、Ingress 和 App 启动入口。

### 部署依赖

- [Joplin Server Documentation](https://github.com/laurent22/joplin/blob/dev/packages/server/README.md) - 官方服务端设置指南
- [Joplin Docker Compose Example](https://raw.githubusercontent.com/laurent22/joplin/dev/docker-compose.server.yml) - 官方 Compose 拓扑
- [Joplin GitHub Repository](https://github.com/laurent22/joplin) - 源码与发布记录

## 实现细节

### 架构组成

- **Joplin Server**：在端口 `22300` 提供 Web 管理界面和同步 API
- **PostgreSQL**：保存用户、笔记、条目元数据、会话和同步状态
- **数据库初始化 Job**：在应用启动前创建 `joplin` 数据库
- **Ingress**：通过 HTTPS 暴露服务，并让 `APP_BASE_URL` 对齐 Sealos URL

### 资源配置

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Joplin Server | 20m | 200m | 25Mi | 256Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### 配置说明

Joplin Server 使用 `DB_CLIENT=pg`、Sealos 公网 `APP_BASE_URL`，以及 KubeBlocks 管理的 PostgreSQL Secret。容器健康检查使用 TCP 探针，因为 Joplin 对 HTTP 请求执行 origin 校验。

### 许可证信息

Joplin 使用 [AGPL-3.0 License](https://github.com/laurent22/joplin/blob/dev/LICENSE)。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么在 Sealos 上部署 Joplin Server？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可以简化部署和运维。部署 Joplin Server 后，你可以获得：

- **一键部署**：从一个模板页面启动 Joplin Server、PostgreSQL 和 HTTPS。
- **托管 PostgreSQL**：使用 KubeBlocks PostgreSQL 保存笔记同步数据。
- **公网同步地址**：把生成的 HTTPS URL 作为 Joplin 同步目标。
- **简单运维**：通过 Sealos Canvas 调整资源和查看日志。

## 部署指南

1. 打开 [Joplin 模板页面](https://sealos.io/products/app-store/joplin)，点击 **Deploy Now**。
2. 检查弹窗中的生成参数并部署。
3. 等待 PostgreSQL、初始化 Job 和 Joplin Server 就绪。
4. 打开生成的 URL，并使用默认管理员账号登录：
   - Email: `admin@localhost`
   - Password: `admin`
5. 打开个人资料菜单并修改管理员密码。然后创建普通同步用户供 Joplin 客户端使用。

## 配置

通过 Joplin 管理界面创建用户和管理账户。通过 Sealos Canvas 调整 CPU、内存、域名或数据库存储。

在 Joplin 客户端中，将同步目标设置为 **Joplin Server**，并填写生成的 Sealos HTTPS URL。

## 扩缩容

本模板按单实例 Joplin Server 设计。同步流量增长时，先增加 Deployment 的 CPU 和内存。随着笔记和附件数据增长，再扩展 PostgreSQL 存储。

## 故障排查

**问题：登录使用默认凭据**
- 原因：Joplin Server 首次启动会创建 `admin@localhost` / `admin`。
- 处理方法：首次登录后立即修改管理员密码。

**问题：同步客户端无法连接**
- 原因：客户端同步 URL 或用户凭据填写错误。
- 处理方法：同步 URL 使用生成的 Sealos HTTPS URL，并使用已创建的 Joplin 用户账号。

## 更多资源

- [Joplin Server README](https://github.com/laurent22/joplin/blob/dev/packages/server/README.md)
- [Joplin Help](https://joplinapp.org/help/)
- [Joplin GitHub Issues](https://github.com/laurent22/joplin/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Joplin 本身使用 AGPL-3.0。
