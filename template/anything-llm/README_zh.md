# 在 Sealos 上部署和托管 AnythingLLM

AnythingLLM 是一个集私有聊天、文档摄取、Agent 和工作区知识库于一体的 AI 应用。此模板在 Sealos Cloud 上部署带持久化存储的 AnythingLLM。

![AnythingLLM 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/anything-llm/website-screenshot.webp)

## 关于托管 AnythingLLM

AnythingLLM 以单个 Web 服务运行，包含应用服务、文档摄取流水线、本地工作区存储和向量存储配置。模板会为 `/app/server/storage`、`/app/collector/hotdir`、`/app/collector/outputs` 创建持久卷，用于保存上传文件、工作区数据和处理结果。

默认向量后端是应用存储卷内的 LanceDB。使用外部 PGVector 时，将 **Vector Database** 设为 `pgvector`，并填写 PostgreSQL 连接串和表名。

## 常见使用场景

- **私有 AI 聊天**：为不同工作区创建连接自有模型供应商的助手。
- **文档问答**：上传文件并通过工作区知识库提问。
- **Agent 工作流**：在浏览器中运行工具和 Agent 操作。
- **团队知识库**：集中保存项目上下文、文档和对话。

## AnythingLLM 托管依赖

Sealos 模板包含 AnythingLLM 容器镜像、持久化存储、公开 HTTPS 入口和可选 PGVector 参数。

### 部署依赖

- [官方网站](https://anythingllm.com/) - 产品网站
- [GitHub 仓库](https://github.com/Mintplex-Labs/anything-llm) - 源代码
- [Docker 指南](https://github.com/Mintplex-Labs/anything-llm/tree/master/docker) - 上游容器部署说明

## 实现细节

**架构组件：**

- **AnythingLLM**：Web UI、API 服务、工作区管理、文档摄取和向量后端客户端。
- **持久化存储**：保存服务端数据、collector hotdir 和 collector outputs。
- **可选 PGVector**：使用启用 pgvector 扩展的外部 PostgreSQL 作为向量存储。

**配置：**

- `auth_token` 设置单用户登录密码。
- `openai_api_key` 可用于初始化和后续模型配置。
- `vector_database` 默认是 `lancedb`；选择 `pgvector` 后填写外部 PGVector 字段。

**许可证信息：**

AnythingLLM 使用 MIT License。

## 为什么在 Sealos 上部署 AnythingLLM？

Sealos 提供一键部署、自动 HTTPS、持久化存储和基于 Kubernetes 的生命周期管理。通过 App Store 表单即可获得带可配置存储和模型参数的 AnythingLLM 公网服务。

## 部署指南

1. 打开 [AnythingLLM 模板](https://sealos.io/products/app-store/anything-llm)，点击 **Deploy Now**。
2. 在弹窗中配置参数。设置 **Single-user password** 作为首次登录密码。内置存储保留 **Vector Database** 为 `lancedb`；使用外部向量库时选择 `pgvector` 并填写 PGVector 字段。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。
4. 打开生成的应用 URL，使用配置的单用户密码登录。

## 配置

部署后，可在 AnythingLLM UI 中配置模型供应商、Embedding 供应商、工作区和文档上传设置。资源和环境变量可在 Sealos Canvas 的资源卡片中调整。

## 更多资源

- [AnythingLLM 文档](https://docs.anythingllm.com/)
- [GitHub Issues](https://github.com/Mintplex-Labs/anything-llm/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

此模板遵循上游 AnythingLLM MIT License。
