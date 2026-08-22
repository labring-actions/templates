# 在 Sealos 上部署和托管 RocketRide Server

RocketRide Server 是开源 AI 开发工作流和可移植 pipeline 执行的运行时引擎。此模板在 Sealos Cloud 上部署官方 RocketRide engine 容器，并配置 HTTPS 端点。

![RocketRide Server 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketride-server/website-screenshot.webp)

## 关于托管 RocketRide Server

RocketRide 可以把 AI 和数据 pipeline 变成可移植运行时进程，这些 pipeline 可在 IDE 中设计，并在自有基础设施上运行。Server 通过 HTTP 暴露 engine，使客户端、SDK 和开发工具可以连接到共享运行时。

此 Sealos 模板会部署官方 `ghcr.io/rocketride-org/rocketride-engine` 镜像、托管的 KubeBlocks PostgreSQL 数据库和 pgvector 扩展。Sealos 通过 Canvas 提供 HTTPS 入口、资源管理和生命周期控制。

## 常见使用场景

- **AI Pipeline 运行时**：在托管云端点运行 RocketRide pipelines。
- **IDE 驱动开发**：将本地 IDE 工作流连接到托管运行时。
- **SDK 集成**：通过稳定 Server URL 使用 Python 或 TypeScript 客户端。
- **内部 AI 服务**：为团队实验和原型托管后端运行时。

## RocketRide Server 托管依赖

Sealos 模板包含官方 RocketRide engine 镜像、启用 pgvector 的 KubeBlocks PostgreSQL、Service、Ingress 和健康探针。

### 部署依赖

- [RocketRide 网站](https://rocketride.org/) - 产品概览和生态链接
- [RocketRide 文档](https://docs.rocketride.org/) - Quickstart、协议和 SDK 指南
- [GitHub 仓库](https://github.com/rocketride-org/rocketride-server) - 源码和版本发布

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **RocketRide Engine**：官方运行时容器，监听 5565 端口
- **PostgreSQL**：用于 engine 运行时的 KubeBlocks PostgreSQL 数据库，并启用 pgvector
- **Service**：用于内部 HTTP 路由的 Kubernetes Service
- **Ingress**：用于外部访问的 Sealos HTTPS 入口

**配置：**

- 官方镜像入口会启动 `./engine ./ai/eaas.py --host=0.0.0.0`。
- `POSTGRES_URL` 会从 KubeBlocks PostgreSQL 连接密钥生成。
- 数据库初始化 Job 会创建 `rocketride` 数据库并启用 `vector` 扩展。
- `ROCKETRIDE_APIKEY` 会在部署时生成，并供 RocketRide 客户端使用。
- 健康探针使用镜像提供的公开 `/version` 端点。
- App URL 指向 `/version`，首次访问即可确认运行时可用。
- 此运行时模板中的 RocketRide Server 没有内置 Web 登录。

**许可证信息：**

RocketRide Server 使用 MIT License。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 RocketRide Server？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，用于部署、运维和扩展应用。通过 Sealos 部署 RocketRide Server，你可以获得：

- **一键部署**：从 App Store 启动运行时，并获得生成的 HTTPS URL。
- **云原生运维**：在一个 Canvas 中管理探针、资源、Ingress 和日志。
- **便捷 SDK 访问**：将本地工具或 SDK 连接到 Sealos 端点。
- **AI Ops 工作流**：在 AI 对话中描述运行时变更，并由 Sealos 应用。
- **资源效率**：从小规格运行时开始，按工作负载增长调整 CPU 或内存。

## 部署指南

1. 打开 [RocketRide Server 模板](https://sealos.io/products/app-store/rocketride-server)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问运行时：
   - **健康检查**：打开 `/version`
   - **Runtime API**：在 RocketRide 客户端和 SDK 中使用同一 host，并传入生成的 `ROCKETRIDE_APIKEY`

## 配置

部署后，你可以通过以下方式配置 RocketRide Server：

- **AI 对话**：添加环境变量或调整运行时设置。
- **资源卡片**：在 Canvas 中调整 CPU、内存和副本设置。
- **客户端配置**：将 IDE 工具或 SDK 客户端指向生成的 Sealos HTTPS URL。

## 扩展

验证 pipeline 行为时先使用单个运行时实例。增加副本前优先提升 CPU 和内存，因为每类工作负载都需要评估 pipeline 运行时状态和客户端协调方式。

## 故障排查

### `/ping` 无响应

- 原因：`/ping` 属于已认证运行时 API。
- 解决方案：使用 `/version` 进行匿名健康检查，通过 RocketRide 客户端和生成的 API key 调用运行时。

### 客户端无法连接

- 原因：客户端可能使用了内部 URL、HTTP scheme 或错误路径。
- 解决方案：使用生成的 Sealos HTTPS host，并先确认 `/ping` 成功。

## 其他资源

- [Quickstart](https://docs.rocketride.org/quickstart)
- [Self-Hosting](https://docs.rocketride.org/self-hosting)
- [RocketRide Releases](https://github.com/rocketride-org/rocketride-server/releases)

## License

此 Sealos 模板遵循仓库许可证。RocketRide Server 使用 MIT License。
