# 在 Sealos 上部署和托管 Flagsmith

Flagsmith 是开源功能开关和远程配置平台。此模板会在 Sealos Cloud 上部署 Flagsmith，并配套 KubeBlocks PostgreSQL 数据库和后台任务处理器。

![Flagsmith 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/flagsmith/website-screenshot.webp)

## 关于托管 Flagsmith

Flagsmith 提供用于管理功能开关、远程配置、基于身份的定向和实验流程的 Dashboard 与 API。组合式 Web/API 服务会从同一个公开入口提供用户界面和 REST API。

该模板会为应用数据和分析数据创建 PostgreSQL，在启动阶段运行数据库迁移，并启动私有任务处理器执行异步任务。Sealos 提供 HTTPS 入口、Kubernetes 编排、持久化数据库存储和 Canvas 运维控制能力。

## 常见使用场景

- **功能灰度发布**：按环境、分群或身份逐步发布功能。
- **远程配置**：无需重新部署代码即可改变应用行为。
- **实验管理**：在同一个 Dashboard 中管理 A/B 测试和功能变体。
- **SDK 管理**：为 Web、移动端和后端 SDK 提供功能开关值。

## Flagsmith 托管依赖

Sealos 模板包含 Flagsmith Web/API 服务、Flagsmith 任务处理器和 KubeBlocks PostgreSQL。

### 部署依赖

- [Flagsmith 文档](https://docs.flagsmith.com/) - 官方文档
- [Docker 托管指南](https://docs.flagsmith.com/deployment-self-hosting/hosting-guides/docker) - 官方 Docker 运行结构
- [环境变量](https://docs.flagsmith.com/deployment-self-hosting/core-configuration/environment-variables) - 配置参考
- [GitHub 仓库](https://github.com/Flagsmith/flagsmith) - 源码和版本发布

### 实现细节

**架构组件：**

此模板会部署三个服务：

- **Flagsmith Web/API**：运行在 8000 端口的 Dashboard 和 REST API。
- **Task Processor**：用于异步任务执行的私有后台 Worker。
- **PostgreSQL**：由 KubeBlocks 管理的核心数据和分析数据库。

**配置：**

Flagsmith 通过 `DATABASE_URL` 和 KubeBlocks 凭据连接 PostgreSQL。公开域名通过 `FLAGSMITH_DOMAIN` 注入，首次设置时允许注册，并由专用任务处理器执行后台任务。官方文档也支持部分企业版和导入导出流程使用外部对象存储；此模板默认把状态保留在 PostgreSQL 中，后续可以按需添加 S3 配置。

**许可证信息：**

Flagsmith 使用 BSD-3-Clause License。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Flagsmith？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维和扩缩容。将 Flagsmith 部署到 Sealos 后，你可以获得：

- **一键部署**：通过一个模板部署 Dashboard、API、任务处理器和数据库。
- **托管 PostgreSQL**：使用带持久化存储的 KubeBlocks PostgreSQL。
- **即时 HTTPS 访问**：自动获得 Flagsmith Dashboard 和 API 的公开 HTTPS URL。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡片调整资源、查看日志并应用变更。
- **按量资源**：用实用资源限制运行 Flagsmith，并随使用增长调整。

## 部署指南

1. 打开 [Flagsmith 模板](https://sealos.io/products/app-store/flagsmith)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续变更可以在对话框中描述需求让 AI 应用更新，或点击对应资源卡片修改设置。
4. 通过系统提供的 URL 访问应用：
   - **Flagsmith Dashboard**：打开 URL，并从 `/signup` 创建第一个账号。
   - **Flagsmith API**：使用同一个基础 URL 进行 SDK 和 REST API 访问。

## 配置

部署后可以通过以下方式配置 Flagsmith：

- **Dashboard**：创建组织、项目、环境、功能开关和分群。
- **SDK 设置**：复制客户端和服务端环境密钥用于应用集成。
- **AI 对话**：描述资源或环境变量变更。
- **资源卡片**：修改 Web/API、任务处理器、入口和数据库资源。

## 扩缩容

调整 Flagsmith 资源：

1. 打开该部署的 Canvas。
2. 点击 Web/API、任务处理器或 PostgreSQL 资源卡片。
3. 调整 CPU、内存、存储或副本设置。
4. 在对话框中应用变更。

## 故障排查

### 注册页面不可用

- 原因：注册设置或启动迁移仍在收敛。
- 解决：等待 Web/API 服务 Ready 后重新打开 `/signup`。

### SDK 客户端无法连接

- 原因：SDK 仍指向托管版 Flagsmith Cloud 端点。
- 解决：把 SDK base URL 配置为 Sealos 提供的 Flagsmith URL。

### 后台任务未执行

- 原因：任务处理器异常或无法访问 PostgreSQL。
- 解决：查看任务处理器资源卡片日志，并确认 PostgreSQL 正常运行。

## 其他资源

- [Flagsmith SDK API](https://docs.flagsmith.com/sdk-api/)
- [自托管概览](https://docs.flagsmith.com/deployment-self-hosting/)
- [Sealos](https://sealos.io)

## 许可证

此 Sealos 模板遵循仓库许可证。Flagsmith 本身使用 BSD-3-Clause License。
