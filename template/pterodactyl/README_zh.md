# 在 Sealos 上部署和托管 Pterodactyl Panel

Pterodactyl Panel 是开源游戏服务器管理面板。本模板在 Sealos Cloud 上部署 Panel、KubeBlocks MySQL、KubeBlocks Redis、持久化应用存储和 HTTPS Ingress。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pterodactyl/website-screenshot.webp)

## 关于托管 Pterodactyl Panel

Pterodactyl Panel 是用于通过 Pterodactyl Wings 管理游戏服务器的 Web 控制面。官方 Docker 拓扑使用 Panel 容器、MySQL 兼容数据库、Redis 缓存，以及用于应用状态和日志的持久化存储。

Sealos 模板使用 KubeBlocks 创建 MySQL 和 Redis，初始化 Panel 数据库，创建第一个管理员账号，并通过 Sealos HTTPS URL 暴露 Panel。

## 常见使用场景

- **游戏服务器控制面板**：管理用户、节点、分配和服务器。
- **Minecraft 与游戏托管**：配合 Wings 节点托管游戏服务器。
- **团队管理**：为员工和用户提供受控的服务器操作权限。
- **自托管基础设施**：在 Kubernetes 管理的云资源上运行 Panel。

## Pterodactyl Panel 托管依赖

Sealos 模板包含 Panel 容器、KubeBlocks MySQL、KubeBlocks Redis、数据库引导、管理员引导、持久化存储和 HTTPS Ingress。

### 部署依赖

- [Pterodactyl 文档](https://pterodactyl.io/panel/1.0/getting_started.html) - 官方 Panel 文档
- [Pterodactyl Docker Compose](https://github.com/pterodactyl/panel/blob/v1.12.4/docker-compose.example.yml) - 官方容器拓扑
- [Pterodactyl GitHub 仓库](https://github.com/pterodactyl/panel) - 源码与发布记录

### 实现细节

**架构组件：**

- **Panel**：`ghcr.io/pterodactyl/panel:v1.12.4` 中的 PHP、nginx、supervisor 和定时任务
- **MySQL**：KubeBlocks MySQL `ac-mysql-8.0.30-1`
- **Redis**：KubeBlocks Redis `redis-7.2.7`
- **Bootstrap Job**：执行迁移、种子数据和管理员创建
- **持久化存储**：挂载 `/app/var` 与 `/app/storage/logs`

**配置：**

模板把 `APP_URL` 设置为生成的 HTTPS 地址，使用 Redis 作为缓存、会话和队列后端，把邮件投递设置为日志模式，并使用部署时填写的参数创建初始管理员。

**许可证：**

Pterodactyl Panel 使用 MIT License。

## 为什么在 Sealos 上部署 Pterodactyl Panel？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用从开发到生产部署和管理的完整生命周期。在 Sealos 上部署 Pterodactyl Panel 可以获得：

- **一键部署**：一次部署 Panel、MySQL、Redis、存储、Ingress 和 SSL。
- **托管数据库**：使用 KubeBlocks MySQL 和 Redis 提供持久化应用服务。
- **管理员引导**：部署时创建第一个 Panel 管理员。
- **即时公网访问**：部署完成后打开生成的 HTTPS URL。
- **运维控制**：在 Sealos Canvas 中调整资源和环境变量。

在 Sealos 上部署 Pterodactyl Panel，以云原生基础设施管理控制面。

## 部署指南

1. 打开 [Pterodactyl Panel 模板](https://sealos.io/products/app-store/pterodactyl)，点击 **Deploy Now**。
2. 在弹窗中配置管理员邮箱、用户名、姓名、密码和可选 S3 备份。
3. 等待部署完成。部署完成后会跳转到 Canvas。后续修改可在对话框中描述需求让 AI 执行，或点击对应资源卡片调整配置。
4. 通过提供的 URL 访问 Panel。
5. 使用部署时配置的管理员邮箱和密码登录。

## 配置

第一个管理员账号由 bootstrap Job 在迁移和种子数据完成后通过 Pterodactyl 的 `p:user:make` 命令创建。部署后需要在 Panel 中添加 Wings 节点，才能运行实际游戏服务器。

S3 兼容备份可通过 **Use S3-compatible object storage for Pterodactyl server backups** 开关启用。启用后，模板会创建 Sealos 对象存储 bucket，并用 path-style S3 设置配置 `APP_BACKUP_DRIVER=s3`。MySQL 和 Redis 均作为外接 KubeBlocks 服务创建。

## 扩缩容

调整 Pterodactyl Panel 资源：

1. 打开当前部署的 Canvas。
2. 点击 Panel StatefulSet、MySQL 或 Redis 资源卡片。
3. 调整 CPU、内存、副本数或存储。
4. 在对话框中应用变更。

## 故障排查

**管理员登录失败**

- 原因：bootstrap Job 可能仍在执行迁移和用户创建。
- 解决：等待 bootstrap Job 完成后，使用配置的管理员邮箱和密码登录。

**Panel 已加载但队列或会话异常**

- 原因：Redis 可能仍在初始化。
- 解决：等待 Redis 就绪后，从 Canvas 重启 Panel 工作负载。

**无法创建游戏服务器**

- 原因：Pterodactyl 需要 Wings 节点执行服务器。
- 解决：Panel 部署完成后，在 Panel 中添加并配置 Wings 节点。

## 更多资源

- [Pterodactyl Panel 文档](https://pterodactyl.io/panel/1.0/getting_started.html)
- [Pterodactyl Wings 文档](https://pterodactyl.io/wings/1.0/installing.html)
- [Pterodactyl GitHub](https://github.com/pterodactyl/panel)

## License

本 Sealos 模板遵循仓库许可证。Pterodactyl Panel 本身使用 MIT License。
