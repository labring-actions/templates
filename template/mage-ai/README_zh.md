# 在 Sealos 上部署和托管 Mage AI

Mage AI 是一个开源的数据管道工具，用于构建和运行数据工作流。本模板在 Sealos 云平台上部署 Mage AI，同时配置 PostgreSQL 数据库和持久化存储。

## 关于托管 Mage AI

Mage AI 提供类似笔记本的交互环境，用于构建、调度和监控数据管道。该模板自动配置专用的 PostgreSQL 集群用于存储元数据，并为 `/home/src` 路径提供持久化卷来存放项目文件。

部署完成后，系统会自动配置公网 HTTPS 入口、SSL 证书自动签发以及网络管理，无需触碰任何 YAML 配置。你可以直接在 App Launchpad 中管理资源和环境变量。

## 常见应用场景

- **ETL/ELT 数据管道**——从多个数据源提取、转换和加载数据
- **定时数据工作流**——利用内置调度器运行周期性任务
- **特征工程**——为机器学习管道构建可复用的数据转换流程
- **API 数据采集**——从第三方 API 拉取数据并标准化
- **数据质量检查**——在管道中验证和监控数据完整性

## Mage AI 托管依赖

Sealos 模板已包含所有必需的依赖：Mage AI 运行时、PostgreSQL 数据库和持久化存储。

### 部署相关资源

- [Mage AI 官方文档](https://docs.mage.ai/)——权威文档和使用指南
- [Mage AI GitHub 仓库](https://github.com/mage-ai/mage-ai)——源代码和版本发布
- [Mage AI GitHub 议题](https://github.com/mage-ai/mage-ai/issues)——社区支持和问题跟踪
- [Sealos 云平台](https://sealos.run)——部署平台和应用启动器

### 实现细节

**架构组件：**

本模板会部署以下服务：

- **Mage AI**——通过 `mage start magic` 命令运行 StatefulSet，监听端口 `6789`
- **PostgreSQL 集群**——KubeBlocks 管理的 PostgreSQL `16.4.0`，用于存储管道元数据
- **PostgreSQL 初始化任务**——首次启动时创建 `mage` 数据库
- **Service + Ingress**——内部服务，提供公网 HTTPS 访问
- **持久化卷**——1Gi 存储空间，挂载到 `/home/src` 用于存放项目文件

**配置说明：**

- **管理员凭据**——部署时设置 `DEFAULT_OWNER_EMAIL` 和 `DEFAULT_OWNER_PASSWORD`
- **数据库**——连接详情自动注入，数据库名称为 `mage`
- **连接字符串**——`MAGE_DATABASE_CONNECTION_URL` 会根据 PostgreSQL 凭据自动组装

**许可证信息：**

Mage AI 遵循其上游开源许可证。详情请查看 Mage AI GitHub 仓库。

## 为何选择在 Sealos 上部署 Mage AI？

Sealos 是一个基于 Kubernetes 的云操作系统，通过 AI 辅助实现了从开发到生产的全生命周期统一管理。在 Sealos 上部署 Mage AI，你将获得：

- **一键部署**——几分钟内即可启动包含 PostgreSQL 和存储的 Mage AI
- **自动弹性伸缩**——根据工作负载自动调整资源，无需人工编排
- **灵活定制**——在 App Launchpad 中轻松配置环境变量和存储
- **零 Kubernetes 门槛**——享受托管 Kubernetes 的优势，无需深入理解其复杂性
- **内置持久化存储**——数据和配置随持久化卷保存，重启不丢失
- **即刻公网访问**——自动配置 HTTPS 端点和 SSL 证书
- **按量计费**——根据实际使用灵活调整资源，优化成本

在 Sealos 上部署 Mage AI，专注于构建数据工作流，而非管理基础设施。

## 部署指南

1. 访问 [Mage AI 模板页面](https://sealos.io/products/app-store/mage-ai)
2. 点击"立即部署"按钮
3. 在弹出对话框中配置参数：
   - **默认所有者邮箱**——管理员登录邮箱
   - **默认所有者密码**——管理员登录密码
4. 等待部署完成（通常 0-1 分钟）。部署完成后会自动跳转到 Canvas。后续如需修改，可在对话框中描述需求让 AI 自动应用更新，或点击相关资源卡片手动调整设置。
5. 通过提供的 URL 访问你的 Mage AI 实例：
   - **Mage AI Web 界面**——使用默认所有者凭据登录

## 配置

部署后，你可以通过以下方式配置 Mage AI：

- **AI 对话**——描述你想要的变更，让 AI 直接应用更新
- **资源卡片**——点击相关资源卡片修改设置
- **Web 界面**——通过提供的 URL 使用默认所有者凭据登录
- **存储**——项目存储在持久化卷的 `/home/src` 路径

## 扩缩容

本模板默认运行单个 Mage AI 副本。如需调整资源：

1. 在 Sealos 中打开 App Launchpad
2. 选择你的 Mage AI 部署
3. 调整 CPU/内存限制并点击"更新"

## 故障排查

### 常见问题

**问题：无法登录 Mage AI**
- 原因：默认所有者邮箱或密码错误
- 解决方案：在部署配置中验证凭据，如需要可在 App Launchpad 中更新

**问题：数据库连接失败**
- 原因：PostgreSQL 仍在初始化，或初始化任务尚未完成
- 解决方案：等待几分钟后检查 PostgreSQL 集群和初始化任务的日志

**问题：502 错误/Ingress 未就绪**
- 原因：Mage AI 服务仍在启动中
- 解决方案：等待 StatefulSet 进入就绪状态，然后刷新 URL

### 获取帮助

- [Mage AI 官方文档](https://docs.mage.ai/)
- [Mage AI GitHub 议题](https://github.com/mage-ai/mage-ai/issues)

## 更多资源

- [Mage AI GitHub 仓库](https://github.com/mage-ai/mage-ai)
- [Mage AI 官网](https://www.mage.ai/)

## 许可证

本 Sealos 模板遵循代码仓库的许可条款。Mage AI 本身受其上游许可证约束；详情请查看 Mage AI GitHub 仓库。
