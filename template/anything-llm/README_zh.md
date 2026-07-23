# 在 Sealos 上部署和托管 AnythingLLM

AnythingLLM 是一款自托管 AI 工作空间，支持私有对话、文档摄取、Agent 和检索增强生成（RAG）。此模板会在 Sealos 上部署 AnythingLLM 1.15.0，提供持久化存储，并可按需启用由 Sealos 托管的 PGVector 数据库。

![AnythingLLM 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/anything-llm/website-screenshot.webp)

## 关于托管 AnythingLLM

AnythingLLM 将 Web 界面、API 服务、文档采集器和 Agent 运行时整合在一个容器中。模板会持久保存应用数据、上传文档和采集器输出，应用重启后数据依然保留。

LanceDB 是默认向量后端，向量数据保存在应用存储卷中。选择 PGVector 后，模板会通过 KubeBlocks 创建 PostgreSQL 16.4 集群，初始化 `anythingllm` 数据库，启用 `vector` 扩展，并在数据库就绪后启动 AnythingLLM。

## 常见使用场景

- **私有 AI 对话**：连接常用模型供应商，在自托管工作空间中保存对话。
- **文档问答**：上传文件、生成向量，并在对话中检索相关内容。
- **Agent 工作流**：在同一界面中使用内置工具、Agent 技能和定时任务。
- **团队知识空间**：按工作区整理文档、提示词和对话记录。

## AnythingLLM 托管依赖

模板包含 AnythingLLM 容器、HTTPS 入口和三个持久卷。启用 PGVector 后，还会创建由 Sealos 托管的 PostgreSQL 集群和幂等初始化任务。

### 部署依赖

- [AnythingLLM 文档](https://docs.anythingllm.com/) - 产品与配置文档
- [AnythingLLM GitHub 仓库](https://github.com/Mintplex-Labs/anything-llm) - 源代码与版本发布
- [Docker 部署指南](https://github.com/Mintplex-Labs/anything-llm/blob/v1.15.0/docker/HOW_TO_USE_DOCKER.md) - 官方容器部署说明

## 实现细节

**架构组件：**

- **AnythingLLM**：提供 Web 界面和 API，处理文档、运行 Agent，并连接选定的向量后端。
- **持久化存储**：在 `/app/server/storage` 保存服务端状态，在 `/app/collector/hotdir` 和 `/app/collector/outputs` 保存采集器数据。
- **LanceDB**：通过 AnythingLLM 存储卷提供默认的嵌入式向量后端。
- **可选 PGVector**：选择 `pgvector` 时，通过 KubeBlocks 创建 PostgreSQL 并启用 `vector` 扩展。

**身份验证：**

模板启用 AnythingLLM 单用户密码认证。部署时设置 **Single-user password**，随后在 AnythingLLM 登录页输入同一密码。账户注册属于 AnythingLLM 多用户模式，此模板采用单用户登录流程。

**配置：**

- `vector_database` 可选择 `lancedb` 或托管的 `pgvector` 分支。
- `pgvector_table_name` 用于设置 PGVector 的向量表名。
- `openai_api_key` 可预先配置 OpenAI API Key，也可登录后再设置模型供应商。

**许可证信息：**

AnythingLLM 使用 MIT License。

## 为什么在 Sealos 上部署 AnythingLLM？

Sealos 提供一键部署、自动 HTTPS、持久卷和基于 Kubernetes 的生命周期管理。PGVector 条件选项会自动创建并连接数据库，平台会将数据库凭据直接注入工作负载；按量付费的资源模式也适合个人使用。

## 部署指南

1. 打开 [AnythingLLM 模板](https://sealos.io/products/app-store/anything-llm)，点击 **Deploy Now**。
2. 设置 **Single-user password**。使用嵌入式存储时保留 **Vector Database** 为 `lancedb`；需要 Sealos 托管的 PostgreSQL 向量后端时选择 `pgvector`。需要立即使用 OpenAI 时可同时填写 API Key。
3. 等待部署完成。LanceDB 通常需要 2-3 分钟；PGVector 会先初始化 PostgreSQL，耗时可能增加几分钟。部署完成后页面会进入 Canvas。
4. 打开生成的 AnythingLLM 地址，使用第 2 步设置的单用户密码登录。
5. 在 AnythingLLM 中配置大语言模型供应商、创建工作区并上传文档。

## 配置

登录后，可在 **Settings** 中配置大语言模型和 Embedding 供应商、Agent 工具、外观与安全选项。后续如需调整计算资源、存储、环境变量和网络，可使用 Sealos Canvas 的 AI 对话框或资源卡片。

## 更多资源

- [AnythingLLM 配置文档](https://docs.anythingllm.com/configuration)
- [GitHub Issues](https://github.com/Mintplex-Labs/anything-llm/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

此模板遵循上游 AnythingLLM MIT License。
