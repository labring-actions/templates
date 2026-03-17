# 在 Sealos 上部署和托管 Keystone

Keystone 是一款开源无头 CMS 与应用框架，用于构建基于 GraphQL 的后端服务和管理后台界面。本模板可在 Sealos Cloud 上一键部署 Keystone 及其配套的 PostgreSQL 数据库。

## 关于 Keystone 托管

Keystone 基于 Node.js 运行，根据你定义的 Schema 自动生成功能强大的 Admin UI 和 GraphQL API。底层通过 Prisma ORM 连接 PostgreSQL 数据库，开箱即用地提供关系型数据建模、身份认证和访问控制等核心能力。

Sealos 模板会自动完成 PostgreSQL 数据库创建、Schema 初始化和管理员账号注入等准备工作，同时为应用构建产物提供持久化存储，并处理 SSL 证书签发和域名管理。

## 常见使用场景

- **无头 CMS**：通过 GraphQL API 和直观的 Admin UI，为网站、移动应用或任意前端管理结构化内容。
- **内部工具与管理面板**：无需从零编写前端代码，即可快速搭建自定义管理后台和数据管理界面。
- **多端统一后端**：以 Keystone 的 GraphQL API 作为统一后端，同时驱动 Web、移动端和 IoT 应用。
- **内容驱动型 SaaS 平台**：借助细粒度的访问控制和自定义业务逻辑，将内容管理能力嵌入你的 SaaS 产品。

## Keystone 托管依赖

Sealos 模板已包含所有必要依赖：Node.js 22 运行时、PostgreSQL 16.4 数据库、Keystone 6 框架以及 TypeScript 编译器。

### 相关资源

- [Keystone 官方文档](https://keystonejs.com/docs) - 完整使用文档
- [Keystone GitHub 仓库](https://github.com/keystonejs/keystone) - 源代码与问题追踪
- [Keystone 示例项目](https://github.com/keystonejs/keystone/tree/main/examples) - 示例项目与入门模板

### 实现细节

**架构组成：**

本模板部署以下服务：

- **Keystone 应用**：以 StatefulSet 方式运行的 Node.js 服务，在 3000 端口提供 Admin UI 和 GraphQL API
- **PostgreSQL 16.4**：由 KubeBlocks 托管的数据库集群，存储所有内容、用户账号和 Schema 数据
- **数据库初始化 Job**：一次性任务，等待 PostgreSQL 就绪后创建 `keystone` 数据库
- **Bootstrap 初始化容器**：在主容器启动前，同步应用源文件、安装依赖、构建项目并执行 Prisma 数据库迁移

**配置说明：**

模板内置了一套入门 Schema，包含三种内容类型：用户（Users）、文章（Posts）和标签（Tags）。用户支持邮箱/密码认证，文章支持富文本内容并关联作者和标签，标签提供简单的分类体系。所有内容操作默认需要登录认证。

启动引导流程采用基于哈希的变更检测机制——后续重启时，只有源文件发生变化才会触发重新构建，日常启动速度很快。

**许可证：**

Keystone 采用 MIT 许可证开源。

## 为什么选择在 Sealos 上部署 Keystone？

Sealos 是基于 Kubernetes 构建的 AI 驱动云操作系统，覆盖应用从开发到部署再到运维的完整生命周期，非常适合构建和扩展 AI 应用、SaaS 平台以及复杂的微服务架构。在 Sealos 上部署 Keystone，你将获得：

- **一键部署**：只需点击一下，即可部署 Keystone 及其配套的托管 PostgreSQL 数据库，无需手写 YAML、无需编排容器。
- **内置弹性伸缩**：应用根据流量自动扩缩容，轻松应对突发流量，无需人工干预。
- **便捷配置**：通过直观的表单设置管理员账号、资源配额和存储空间，全程无需编写代码。
- **零 Kubernetes 门槛**：无需成为 Kubernetes 专家，即可享受高可用、服务发现和容器编排带来的全部优势。
- **持久化存储保障**：内置持久化存储方案，确保应用数据和构建产物在部署更新、弹性伸缩时安全可靠。
- **即时公网访问**：每次部署自动分配公网域名并配置 SSL 证书，Admin UI 和 GraphQL API 即刻可用，无需折腾网络配置。
- **自动备份**：数据库自动备份与灾难恢复机制，确保内容数据万无一失。

在 Sealos 上部署 Keystone，让你专注于内容模型的设计，而非基础设施的运维。

## 部署指南

1. 打开 [Keystone 模板页面](https://sealos.io/products/app-store/keystone)，点击 **立即部署**。
2. 在弹出的对话框中配置以下参数：
   - **Admin Name**：初始管理员的显示名称
   - **Admin Email**：用于登录 Admin UI 的邮箱地址
   - **Admin Password**：管理员账号密码
3. 等待部署完成（通常需要 2-3 分钟）。首次部署耗时稍长，因为需要安装 npm 依赖并构建 Keystone 项目。部署完成后会自动跳转至 Canvas 页面。后续如需变更，可在对话框中描述需求让 AI 自动执行，也可点击相应的资源卡片手动修改配置。
4. 通过提供的 URL 访问你的 Keystone 实例，使用部署时配置的邮箱和密码登录 Admin UI。

## 配置说明

部署完成后，你可以通过以下方式配置 Keystone：

- **AI 对话**：在对话框中描述你想要的变更，让 AI 自动执行
- **资源卡片**：点击相应的资源卡片修改配置
- **Admin UI**：通过部署 URL 直接访问 Keystone Admin UI，管理内容、用户和数据

如需自定义内容 Schema（添加新的列表、字段或关系），可通过 ConfigMap 资源卡片修改 Schema 源文件。

## 故障排查

### 常见问题

**首次部署时应用启动时间较长**
- 原因：初始化容器需要安装 npm 依赖并构建 Keystone 项目。
- 解决方案：等待初始化容器执行完毕即可。后续重启会因哈希变更检测机制而大幅加速。

**无法登录 Admin UI**
- 原因：管理员凭据不正确，或初始化注入流程被跳过。
- 解决方案：确认部署时填写的邮箱和密码是否正确，检查应用日志中是否有与账号注入相关的警告信息。

### 获取帮助

- [Keystone 官方文档](https://keystonejs.com/docs)
- [Keystone GitHub Issues](https://github.com/keystonejs/keystone/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Keystone API 参考](https://keystonejs.com/docs/apis)
- [Keystone 使用指南](https://keystonejs.com/docs/guides)
- [GraphQL Playground](https://keystonejs.com/docs/guides/graphql) - 了解如何使用 Keystone 的 GraphQL API