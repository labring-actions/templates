# 在 Sealos 上部署并托管 Open WebUI

Open WebUI 是一个自托管 AI 工作空间，支持 Ollama、OpenAI 兼容 API、RAG、工具和多模态工作流。此模板会在 Sealos Cloud 上部署带 PostgreSQL、持久化应用数据、可选 Sealos 对象存储和公网 HTTPS 入口的 Open WebUI。

![Open WebUI 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/open-webui/website-screenshot.webp)

## 关于托管 Open WebUI

Open WebUI 作为单个应用服务运行，通过 `8080` 端口提供 Web 界面和后端 API。Sealos 模板会创建托管 PostgreSQL 数据库，初始化 `openwebui` 数据库，并将持久化存储挂载到 `/app/backend/data`，用于上传文件、本地缓存和运行时文件。

模板遵循 Open WebUI 的 Kubernetes 指引，主数据库路径使用 PostgreSQL。你也可以启用 Sealos 对象存储，通过 Open WebUI 的 S3 兼容存储提供方保存上传文件。

## 常见使用场景

- **团队 AI 门户**：为聊天、提示词、知识库和模型路由提供共享工作空间。
- **Ollama 前端**：连接可访问的 Ollama API 端点，使用本地或私有模型。
- **OpenAI 兼容网关**：在同一个 Web 界面中使用 OpenAI、vLLM、LiteLLM 或其他兼容 API。
- **RAG 工作空间**：上传文档、构建知识集合，并在聊天中查询。
- **管理员控制访问**：首个注册账号成为管理员，后续用户由管理员审批。

## Open WebUI 托管依赖

此 Sealos 模板包含 Open WebUI 容器、KubeBlocks PostgreSQL 集群、持久化存储、Ingress，以及可选的 Sealos 托管 S3 兼容存储桶。

### 部署依赖

- [Open WebUI 文档](https://docs.openwebui.com/) - 官方文档
- [Open WebUI 快速开始](https://docs.openwebui.com/getting-started/quick-start/) - Docker 与首次登录指引
- [环境变量配置](https://docs.openwebui.com/reference/env-configuration/) - 模型提供方、数据库、S3 和安全变量
- [扩展与高可用](https://docs.openwebui.com/getting-started/advanced-topics/scaling/) - PostgreSQL、存储和生产建议
- [Open WebUI GitHub](https://github.com/open-webui/open-webui) - 源码仓库

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Open WebUI**：使用 `ghcr.io/open-webui/open-webui:v0.10.2` 提供 Web UI 和后端 API。
- **PostgreSQL**：托管 KubeBlocks PostgreSQL `16.4` 集群，用作 Open WebUI 主数据库。
- **PostgreSQL 初始化任务**：在应用启动前幂等创建 `openwebui` 数据库。
- **持久化数据卷**：在 `/app/backend/data` 保存上传文件、缓存和本地运行时文件。
- **可选对象存储**：启用后创建私有 Sealos ObjectStorageBucket，并注入 S3 兼容凭据。

**配置：**

- `WEBUI_URL` 和 `CORS_ALLOW_ORIGIN` 会设置为 Sealos 公网 HTTPS 地址。
- `DATABASE_TYPE`、`DATABASE_HOST`、`DATABASE_PORT`、`DATABASE_USER`、`DATABASE_PASSWORD` 和 `DATABASE_NAME` 会连接到 PostgreSQL。
- `OLLAMA_BASE_URL`、`OPENAI_API_BASE_URL` 和 `OPENAI_API_KEY` 可在部署时填写，也可登录后在管理员面板中配置。
- 启用 `use_sealos_objectstorage` 后，模板会设置 `STORAGE_PROVIDER=s3` 并接入 Sealos 对象存储凭据。

**许可证信息：**

Open WebUI 根据 Open WebUI 项目许可证分发。此 Sealos 模板遵循 Sealos 模板仓库许可证。

## 为什么在 Sealos 上部署 Open WebUI？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一管理部署、扩缩容、存储、网络和运维。在 Sealos 上部署 Open WebUI，你可以获得：

- **一键部署**：通过一个模板启动 Open WebUI、PostgreSQL、存储、Ingress 和 HTTPS。
- **Kubernetes 基础**：运行云原生部署常用的容器与健康探针模型。
- **内置持久化存储**：重启后保留上传文件和运行时文件。
- **托管数据库**：使用 Sealos 托管 PostgreSQL 集群承载主数据库。
- **可选对象存储**：将上传文件保存到私有 S3 兼容 Sealos 存储桶。
- **简化运维**：通过 Canvas、AI 对话和资源卡片完成部署后的变更。
- **按量计费**：从小型单副本部署开始，根据使用量调整资源。

## 部署指南

1. 打开 [Open WebUI 模板](https://sealos.io/products/app-store/open-webui)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `ollama_base_url`：可选的 Ollama API 地址。
   - `openai_api_base_url`：可选的 OpenAI 兼容 API 地址。
   - `openai_api_key`：可选的 OpenAI 兼容 API Key。
   - `use_sealos_objectstorage`：需要将上传文件保存到 Sealos 对象存储时启用。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续变更可以在对话框描述需求，让 AI 应用更新，也可以点击相关资源卡片修改配置。
4. 从 Open WebUI App 卡片打开应用地址。
5. 在注册页面创建第一个账号。Open WebUI 会授予首个账号管理员权限。
6. 使用该管理员账号登录。后续注册账号会进入待审批状态，可在管理员设置中批准。
7. 连接模型提供方：
   - 使用 Ollama 时，打开 **Settings > Connections**，添加可访问的 Ollama Base URL。
   - 使用 OpenAI 兼容 API 时，打开 **Settings > Connections**，添加 API Base URL 和 Key。

## 配置

部署后可通过以下方式配置 Open WebUI：

- **Open WebUI 管理面板**：管理用户、模型提供方、知识库设置和工作空间行为。
- **Sealos AI 对话**：描述配置变更，让 AI 更新部署。
- **资源卡片**：在 Canvas 中调整环境变量、资源限制、存储和副本数。

## 扩缩容

此模板默认以单副本和 PostgreSQL 启动。增加副本前，请先查看 Open WebUI 的扩展指引，评估 Redis、共享存储、外部向量数据库和内容提取配置。

调整资源步骤：

1. 打开当前部署的 Canvas。
2. 点击 Open WebUI StatefulSet 资源卡片。
3. 调整 CPU、内存或副本数。
4. 在对话框中应用变更。

Open WebUI 容器默认使用 `500m` CPU 和 `2G` 内存。现场启动验证中，默认 embedding 模型缓存下载会超过 `1G` 档位，稳定运行后 Pod 约为 `833Mi`。

## 故障排查

### 首个账号已存在

- 原因：数据库中已有来自之前部署或恢复数据的用户。
- 解决方案：使用已有管理员账号登录，或按照 Open WebUI 文档从数据库重置用户。

### 没有可用模型

- 原因：尚未配置 Ollama 或 OpenAI 兼容提供方。
- 解决方案：在 **Settings > Connections** 添加可访问的提供方，或更新部署输入。

### 上传文件需要共享对象存储

- 原因：S3 存储启用前，上传文件保存在本地数据卷。
- 解决方案：部署前启用 `use_sealos_objectstorage`，或先迁移上传文件后再切换存储模式。

### 获取帮助

- [Open WebUI 文档](https://docs.openwebui.com/)
- [Open WebUI GitHub Issues](https://github.com/open-webui/open-webui/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Open WebUI 环境变量配置](https://docs.openwebui.com/reference/env-configuration/)
- [Open WebUI 扩展与高可用](https://docs.openwebui.com/getting-started/advanced-topics/scaling/)
- [Open WebUI Releases](https://github.com/open-webui/open-webui/releases)

## License

此 Sealos 模板遵循 Sealos 模板仓库许可证。Open WebUI 本身遵循 Open WebUI 项目发布的许可证。
