# 在 Sealos 上部署和托管 OpenHands

OpenHands 是 AI 软件开发代理 Web 应用。此模板在 Sealos Cloud 上部署 OpenHands Web UI，并提供持久化 workspace 和状态存储。

![OpenHands 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openhands/website-screenshot.webp)

## 关于托管 OpenHands

OpenHands 以 Web 应用运行在 `3000` 端口，并将 workspace 数据保存到 `/workspace`，将应用状态保存到 `/root/.openhands-state`。模板通过 Sealos HTTPS Ingress 发布 UI，并允许在部署时填写可选 LLM 设置。

OpenHands 完整 Docker sandbox 模式通常需要访问 Docker daemon。此 Sealos 模板提供可访问的 Web 部署路径和持久化 workspace，并验证 UI 与运行时启动路径。需要启动嵌套 sandbox 容器的 agent 执行能力依赖平台级 Docker/runtime 支持。

## 常见使用场景

- **AI 编程工作区**：打开基于浏览器的 OpenHands UI 进行项目自动化。
- **LLM agent 实验**：连接 LLM API Key 并测试 agent 工作流。
- **持久任务状态**：重启后保留 workspace 文件和 OpenHands 状态。
- **云端开发助手**：在其他 Sealos 服务旁运行助手型 Web 应用。

## OpenHands 托管依赖

Sealos 模板包含 OpenHands Web 容器、持久化 workspace 存储、持久化状态存储、公网 HTTPS Ingress 和可选 LLM 配置输入。

### 部署依赖

- [OpenHands 文档](https://docs.openhands.dev/) - 官方文档
- [OpenHands Runtime 文档](https://docs.openhands.dev/openhands/usage/runtimes) - Runtime 与 sandbox 参考
- [OpenHands GitHub 仓库](https://github.com/OpenHands/OpenHands) - 源码与发布版本

### 实现细节

**架构组件：**

- **OpenHands StatefulSet**：运行 `ghcr.io/openhands/openhands:1.8.0`，监听 `3000` 端口。
- **Workspace 卷**：持久化 `/workspace`。
- **状态卷**：持久化 `/root/.openhands-state`。
- **Ingress 与 App**：通过 HTTPS 发布 OpenHands Web UI。

**配置：**

- `llm_api_key` 为可选项，映射到 `LLM_API_KEY`。
- `llm_model` 为可选项，映射到 `LLM_MODEL`。
- `SANDBOX_RUNTIME_CONTAINER_IMAGE` 指向 GHCR 上的匹配版本 OpenHands runtime 镜像。
- 完整嵌套容器执行能力依赖 Sealos 环境中的 Docker/runtime 可用性。

**许可证信息：**

OpenHands 使用 MIT 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 OpenHands？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 到生产部署和管理的完整应用生命周期。在 Sealos 上部署 OpenHands 可以获得：

- **一键 Web UI**：快速启动 OpenHands Web 应用。
- **持久化 Workspace**：重启后保留 workspace 和状态数据。
- **可选 LLM 设置**：部署时填写模型和 API Key。
- **即时公网访问**：通过 HTTPS 地址访问 UI。
- **统一运维**：在 Canvas 中查看日志、重启应用并调整资源。

## 部署指南

1. 打开 [OpenHands 模板](https://sealos.io/products/app-store/openhands)，点击 **Deploy Now**。
2. 可选填写 `llm_api_key` 和 `llm_model`。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 打开 OpenHands 地址。
5. 在 UI 提示时配置 LLM Provider，然后进入主工作区页面。

## 配置

部署后可通过以下方式配置 OpenHands：

- **OpenHands UI**：设置或确认 LLM Provider 和模型。
- **AI Dialog**：描述资源或环境变量变更，让 Sealos 自动应用。
- **资源卡片**：调整 CPU、内存、存储和环境变量。

## Runtime 说明

模板验证 OpenHands Web 应用路径和持久化存储路径。需要启动 sandbox runtime 容器的工作流需要宿主环境提供 Docker 兼容 runtime 访问。代码编辑、UI 设置和状态持久化场景可作为普通 Web 应用运行。

## 故障排查

### Agent 执行无法启动 sandbox

- 原因：宿主环境未向 OpenHands 容器暴露 Docker daemon 或兼容的嵌套 runtime。
- 解决方法：使用无需嵌套 runtime 容器的 OpenHands UI 功能，或按照 OpenHands runtime 文档接入受支持的 runtime 服务。

### LLM 调用失败

- 原因：Provider 凭据缺失或无效。
- 解决方法：部署时设置 `llm_api_key` 和 `llm_model`，或从 StatefulSet 环境变量中更新。

## 其他资源

- [OpenHands 文档](https://docs.openhands.dev/)
- [OpenHands Runtime 指南](https://docs.openhands.dev/openhands/usage/runtimes)
- [OpenHands GitHub 仓库](https://github.com/OpenHands/OpenHands)

## 许可证

此 Sealos 模板遵循仓库许可证。OpenHands 本身使用 MIT 许可证。
