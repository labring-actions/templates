# 在 Sealos 上部署和托管 MockServer

MockServer 是开源 HTTP(S) mock server、代理、录制和请求检查工具。此模板在 Sealos Cloud 上以单个非 root 容器部署 MockServer，并配置 HTTPS 入口。

![MockServer 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mockserver/website-screenshot.webp)

## 关于托管 MockServer

MockServer 让团队可以创建 API expectation、校验请求、代理流量、记录交互并查看日志。它监听 1080 端口，并通过同一个端点提供 HTTP、HTTPS、代理、Dashboard 和 API 流量。

此 Sealos 模板使用官方 MockServer Docker 镜像，配置 Kubernetes 探针和公网 HTTPS URL。默认内存模式无需数据库。

## 常见使用场景

- **API Mock**：为前端、集成测试和契约测试创建稳定响应。
- **流量录制**：捕获真实 API 交互，并在开发过程中回放。
- **代理调试**：转发请求，同时检查 payload 和 header。
- **MCP 测试**：为 agent 测试流程暴露 MockServer MCP 端点。

## MockServer 托管依赖

Sealos 模板包含官方 MockServer 容器镜像、Service、Ingress 和健康探针。

### 部署依赖

- [官方网站](https://www.mock-server.com/) - 产品文档和指南
- [运行 MockServer](https://www.mock-server.com/mock_server/running_mock_server.html) - Docker、Helm 和 CLI 用法
- [GitHub 仓库](https://github.com/mock-server/mockserver-monorepo) - 源码和发布流程

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **MockServer**：官方非 root Java 17 distroless 容器，监听 1080 端口
- **Service**：用于 HTTP 流量的 Kubernetes 内部服务
- **Ingress**：用于 Dashboard 和 API 访问的 Sealos HTTPS 入口

**配置：**

- 容器使用 `SERVER_PORT=1080` 和 `MOCKSERVER_SERVER_PORT=1080`。
- App URL 打开 `/mockserver/dashboard`。
- 健康探针使用 MockServer 文档中的 readiness 和 liveness 端点。
- 默认部署的 MockServer 没有内置登录账号。

**许可证信息：**

MockServer 使用 Apache License 2.0。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 MockServer？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，在一个工作区中处理部署、网络、资源管理和运维。通过 Sealos 部署 MockServer，你可以获得：

- **一键部署**：从 App Store 启动可用的 mock API 服务。
- **即时 HTTPS 端点**：向客户端、测试和团队成员共享安全的 MockServer URL。
- **基于 Kubernetes 的可靠性**：Readiness 和 liveness 探针让服务状态可观测。
- **易于定制**：从 Canvas 调整资源限制、环境变量和启动参数。
- **AI Ops 工作流**：在 AI 对话中描述变更，并由 Sealos 应用到资源。
- **按量运行**：只在需要的环境中运行 MockServer。

## 部署指南

1. 打开 [MockServer 模板](https://sealos.io/products/app-store/mockserver)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问部署：
   - **Dashboard**：打开 `/mockserver/dashboard`
   - **Status API**：发送 `PUT /mockserver/status`
   - **MCP 端点**：当工作流启用 MCP 时使用 `/mockserver/mcp`

## 配置

部署后，你可以通过以下方式配置 MockServer：

- **REST API**：创建、读取、验证和清除 expectations。
- **Dashboard**：检查请求、日志和当前 expectations。
- **AI 对话**：添加环境变量或命令行参数。
- **资源卡片**：在 Canvas 中调整 CPU 和内存。

## 扩展

默认模板运行一个内存模式 MockServer 实例。为了保持 expectation 状态确定，建议保持单副本；横向扩展前可先接入外部持久化或集群模式。

## 故障排查

### Status API 失败

- 原因：MockServer 仍在启动，或请求方法有误。
- 解决方案：使用 `PUT /mockserver/status`，并等待 Canvas 中部署进入 Ready 状态。

### 重启后 expectations 消失

- 原因：默认部署将 expectations 保存在内存中。
- 解决方案：需要持久化 expectations 时，可通过自定义资源更新配置初始化或持久化文件。

## 其他资源

- [MockServer Dashboard](https://www.mock-server.com/mock_server/mockserver_ui.html)
- [配置属性](https://www.mock-server.com/mock_server/configuration_properties.html)
- [Docker 文档](https://www.mock-server.com/where/docker.html)

## License

此 Sealos 模板遵循仓库许可证。MockServer 使用 Apache License 2.0。
