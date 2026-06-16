# 在 Sealos 上部署并托管 Appwrite

Appwrite 是一个开源后端平台，提供认证、数据库、存储、函数和 API。本模板会在 Sealos Cloud 上部署 Appwrite 1.9.0，并自动配置 MongoDB、Redis、持久化存储、可选 S3 兼容对象存储和 HTTPS Ingress。

![Appwrite 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/appwrite/website-screenshot.webp)

## 关于在 Sealos 上托管 Appwrite

Appwrite 提供自托管后端控制台和 API，适合需要用户认证、文档数据库、文件存储、函数能力和统一 API 的项目。

这个 Sealos 模板会创建 Appwrite Web/API 服务、KubeBlocks 管理的 MongoDB 和 Redis 集群、挂载到 `/storage` 的持久化存储，以及公开 HTTPS 地址。模板还提供可选的 Sealos S3 兼容对象存储桶，用于用户上传文件。

## 常见使用场景

- **应用后端**：为 Web 或移动应用提供认证、数据库 API 和文件上传。
- **自托管 BaaS**：把后端平台掌控在自己的 Sealos 工作区内。
- **快速 API 原型**：通过 Appwrite Console 快速创建项目 API。
- **团队开发**：统一管理项目、用户、集合和存储桶。

## Appwrite 托管依赖

本模板包含 Appwrite、MongoDB、Redis、持久化存储、可选对象存储、Service、Ingress 和 App 启动入口。

### 部署依赖

- [Appwrite Documentation](https://appwrite.io/docs) - 官方文档
- [Self-hosting Installation](https://appwrite.io/docs/advanced/self-hosting/installation) - 官方 Docker Compose 安装指南
- [Appwrite GitHub Repository](https://github.com/appwrite/appwrite) - 源码与发布记录

## 实现细节

### 架构组成

- **Appwrite**：在端口 `80` 提供 Console 和 API
- **MongoDB**：Appwrite 1.9 的默认数据库后端
- **Redis**：缓存和队列依赖
- **持久化存储**：在 `/storage` 保存 Appwrite 运行时文件
- **可选对象存储**：为上传文件启用 S3 兼容存储

### 资源配置

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Appwrite | 20m | 200m | 25Mi | 256Mi |
| MongoDB | 50m | 500m | 51Mi | 512Mi |
| Redis | 50m | 500m | 51Mi | 512Mi |
| Redis Sentinel | 50m | 500m | 51Mi | 512Mi |

### 配置说明

Sealos 会自动生成公网域名、应用名、OpenSSL key 和 executor secret。MongoDB 和 Redis 凭据通过 KubeBlocks 管理的 Secret 注入。模板会关闭 Appwrite router protection，使 Sealos Ingress 流量和 Kubernetes 内部健康检查都能访问服务。

### 许可证信息

Appwrite 使用 [BSD 3-Clause License](https://github.com/appwrite/appwrite/blob/master/LICENSE)。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么在 Sealos 上部署 Appwrite？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可以简化完整部署生命周期。部署 Appwrite 后，你可以获得：

- **一键部署**：从一个模板页面启动 Appwrite、MongoDB、Redis、存储和 HTTPS。
- **托管运行依赖**：使用 KubeBlocks 管理 MongoDB 和 Redis。
- **数据持久化**：Appwrite 存储和数据库数据在重启后保留。
- **公网 HTTPS 访问**：通过自动生成的安全 URL 打开 Appwrite Console。
- **简单运维**：通过 Sealos Canvas 和资源卡调整资源。

## 部署指南

1. 打开 [Appwrite 模板页面](https://sealos.io/products/app-store/appwrite)，点击 **Deploy Now**。
2. 在弹窗中配置参数。上传文件需要使用 Sealos S3 兼容存储时，开启对象存储选项。
3. 等待部署完成。MongoDB 和 Redis 初始化后，Appwrite 会启动。
4. 打开生成的 Appwrite 地址，在注册页面创建第一个 root 账号。
5. 登录 Appwrite Console，创建项目，再创建集合或存储桶。

## 配置

部署后，通过 Sealos Canvas 调整 CPU、内存、存储或公网域名。通过 Appwrite Console 管理项目配置、认证提供商、数据库集合、存储桶、API key 和平台设置。

## 扩缩容

本模板按单实例 Appwrite Web/API 服务优化。优先通过增加 Appwrite StatefulSet 的 CPU 和内存做纵向扩容。随着项目数据增长，再扩展 MongoDB、Redis 或存储容量。

## 故障排查

**问题：Appwrite 需要几分钟才 Ready**
- 原因：MongoDB 和 Redis 需要先初始化。
- 处理方法：等待数据库 Pod 就绪，再查看 Appwrite StatefulSet 日志。

**问题：上传文件需要对象存储**
- 原因：默认部署使用本地持久化存储。
- 处理方法：部署时开启对象存储选项。

## 更多资源

- [Appwrite Self-Hosting](https://appwrite.io/docs/advanced/self-hosting)
- [Appwrite API Reference](https://appwrite.io/docs/references)
- [Appwrite GitHub Issues](https://github.com/appwrite/appwrite/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Appwrite 本身使用 BSD 3-Clause License。
