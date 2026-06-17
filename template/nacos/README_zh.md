# 在 Sealos 上部署和托管 Nacos

Nacos 是用于动态服务发现、配置管理和服务管理的平台。此模板会在 Sealos Cloud 上部署 Nacos 3.2.2，并包含调优后的 Nacos JVM 内存、独立控制台、单节点 Nacos Server、持久化存储和 Sealos 托管的 MySQL 数据库。

## 关于 Nacos 托管

Nacos 为微服务平台提供命名服务、服务发现、配置管理、命名空间隔离和控制台运维能力。此 Sealos 模板将 Nacos 控制台和服务端拆分为两个 StatefulSet：控制台通过公网 HTTPS 访问，Nacos 服务端通过集群内服务提供给客户端使用。

模板还会创建 KubeBlocks MySQL 8.0 集群，并在应用启动前执行 Nacos 数据库表结构初始化任务。Nacos 日志和运行数据会写入持久化卷，避免 Pod 重启后丢失。

## 常见使用场景

- **微服务服务发现**：注册服务实例，并让应用发现健康实例。
- **集中式配置管理**：维护共享配置、发布变更并追踪配置历史。
- **环境隔离**：使用命名空间区分开发、测试和生产环境的服务元数据。
- **AI 与插件注册实验**：使用 Nacos 3.x 的注册能力管理插件、提示词和 Agent 相关元数据。

## Nacos 托管依赖

此 Sealos 模板包含所需运行依赖：两个 Nacos 应用组件、MySQL 数据库、表结构初始化、持久化卷、内部 Service、控制台 HTTPS Ingress 以及 Sealos App 入口。

### 部署依赖

- [Nacos 文档](https://nacos.io/docs/latest/overview/) - Nacos 官方文档
- [Nacos Docker 仓库](https://github.com/nacos-group/nacos-docker) - 官方镜像与 Compose 示例
- [Nacos GitHub 仓库](https://github.com/alibaba/nacos) - 源代码与版本发布说明

### 实现细节

**架构组件：**

此模板部署四个主要组件：

- **Nacos Console**：运行在 8080 端口的 Web 控制台，通过 Sealos Ingress 对外暴露。
- **Nacos Server**：运行在 8848 和 9848 端口的集群内 Nacos 服务端，用于服务发现和客户端 RPC。
- **MySQL**：由 KubeBlocks 管理的 MySQL 8.0 数据库，用于保存配置、用户、角色和元数据。
- **初始化 Job**：在应用组件完成启动前，将 Nacos MySQL 表结构写入 `nacos_devtest` 数据库。

**配置说明：**

- 控制台和服务端 API 均启用认证。
- 控制台和服务端使用 `JVM_XMS=512m`、`JVM_XMX=512m` 和 `JVM_XMN=256m`；经过验证的单节点配置中，每个 Nacos 组件内存上限为 1024Mi。
- 首次访问控制台时会初始化固定管理员用户名 `nacos`；在页面中设置密码后，再使用 `nacos` 和该密码登录。
- `auth_token` 会自动生成为 Nacos 认证使用的 JWT 签名密钥。如部署后修改该值，请确保两个 Nacos 组件保持一致。
- 控制台访问地址为 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。

**许可信息：**

Nacos 使用 Apache License 2.0。此 Sealos 模板遵循 Sealos 模板仓库的许可证。

## 为什么在 Sealos 上部署 Nacos？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一管理部署、网络、存储和应用生命周期。在 Sealos 上部署 Nacos 可以获得：

- **一键部署**：通过一个模板创建 Nacos、MySQL、持久化存储、HTTPS 路由和应用入口。
- **托管 Kubernetes 运行环境**：无需手写 StatefulSet、Service、Ingress 或数据库资源。
- **内置持久化存储**：Pod 重启后仍保留 Nacos 日志和运行数据。
- **集成数据库能力**：使用 Sealos 托管的 MySQL 集群，无需单独维护数据库。
- **公网控制台访问**：部署完成后通过生成的 HTTPS 地址打开 Nacos 控制台。

## 部署指南

1. 打开 [Nacos 模板](https://sealos.io/products/app-store/nacos)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数。模板会自动生成 Nacos 认证令牌。
3. 等待部署完成，通常需要 2-3 分钟。部署后会进入 Canvas。后续如需调整配置，可以在对话框描述需求让 AI 修改，也可以点击相关资源卡片进行设置。
4. 通过生成的公网地址访问 Nacos 控制台。
5. 首次访问时，为固定用户名 `nacos` 设置管理员密码。
6. 初始化完成后，使用用户名 `nacos` 和刚设置的密码登录。

## 配置

部署后可以通过以下方式配置 Nacos：

- **Nacos 控制台**：管理命名空间、配置、服务、用户、角色和权限。
- **AI 对话框**：描述资源或环境变量调整需求，由 Sealos 执行修改。
- **资源卡片**：在 Canvas 中点击 StatefulSet、数据库或 Ingress 卡片调整配置。
- **客户端配置**：集群内客户端连接 Nacos Server Service 的 8848 端口。

## 扩缩容

此模板按单节点 Nacos 部署调优，并配套持久化存储与 MySQL。如需提升资源，在 Canvas 中打开对应 StatefulSet 资源卡片并调整 CPU 或内存。若要改为高可用 Nacos 集群，请先参考官方 Nacos 集群文档，再调整副本数。

## 故障排查

### 首次登录跳转到初始化页面

这是没有全局管理员用户时的正常行为。请为用户名 `nacos` 设置密码并提交，然后回到登录页使用该密码登录。

### 修改 JWT 密钥后无法登录

所有 Nacos 组件必须使用相同的 `auth_token`。如果部署后修改自动生成的令牌，请确保两个应用组件保持一致。

### Nacos 无法连接数据库

检查 MySQL 集群是否运行正常，并确认表结构初始化 Job 已成功完成。如果 Job 失败，请在 Canvas 或 kubectl 中查看该 Job 的日志。

## 其他资源

- [Nacos 快速开始](https://nacos.io/docs/latest/quickstart/quick-start-docker/)
- [Nacos 认证指南](https://nacos.io/docs/latest/manual/admin/auth/)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Nacos 本身使用 Apache License 2.0。
