# 在 Sealos 上部署和托管 EdgeQuake

EdgeQuake 是一个用 Rust 编写的高性能 Graph-RAG 平台，可以将文档转化为知识图谱，并通过向量检索和图检索进行查询。该模板会在 Sealos Cloud 上部署 EdgeQuake Rust API、React/Next.js Web UI，以及带有 pgvector 和 Apache AGE 兼容图存储能力的 PostgreSQL。

## 关于 EdgeQuake 托管

EdgeQuake 将文档导入、实体抽取、关系映射、向量搜索和图遍历整合到一个 Graph-RAG 系统中。它不只依赖向量相似度，还会存储实体与关系，因此用户可以围绕文档提出多跳推理、主题分析和关系探索类问题。

这个 Sealos 模板采用多服务架构。前端提供浏览器界面，用于上传文档、配置工作区、执行查询和查看图谱；API 服务则提供 Graph-RAG 后端能力、健康检查端点和 REST 接口。Sealos 会自动创建 PostgreSQL 16.4.0 和持久化存储，初始化 `edgequake` 数据库，启用 `uuid-ossp` 和 `vector` 扩展，并尝试启用 Apache AGE；如果 AGE 不可用，模板会创建兼容的图存储回退层。

Sealos 还会为 Web UI 和 API 自动配置公开 HTTPS 访问、服务发现、资源限制，并支持通过 Canvas 进行部署后的管理。

## 常见使用场景

- **文档知识库**：上传文档并使用图感知检索进行问答，而不是只依赖关键词或向量搜索。
- **研究与分析工作区**：在技术、法律、金融或研究资料中探索实体、关系、主题和跨文档连接。
- **AI Agent 知识工具**：将 EdgeQuake 作为结构化检索后端，为需要文档依据的 Agent 提供知识支撑。
- **图谱可视化**：通过 React UI 查看生成的知识图谱，理解概念之间的连接方式。
- **RAG API 原型开发**：基于 EdgeQuake REST API 和流式端点构建应用原型。

## EdgeQuake 托管依赖

Sealos 模板包含部署所需的全部组件：EdgeQuake API、EdgeQuake 前端、PostgreSQL、pgvector、数据库初始化、服务发现和 HTTPS Ingress。

### 部署依赖

- [EdgeQuake GitHub 仓库](https://github.com/raphaelmansuy/edgequake) - 源代码和项目文档
- [Docker Quick Start](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/DOCKER_QUICK_START.md) - 上游 Docker 部署参考
- [EdgeQuake Issues](https://github.com/raphaelmansuy/edgequake/issues) - Bug 反馈与社区讨论
- [Sealos 应用商店](https://sealos.run/products/app-store/edgequake) - EdgeQuake 模板页面

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **Web UI**：React/Next.js 前端，通过主公开 URL 访问。
- **API 服务**：Rust 编写的 EdgeQuake 后端，在 `8080` 端口提供 REST、健康检查、文档导入、查询和图谱接口。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4.0 集群，配置 `1Gi` 持久化存储。
- **数据库初始化 Job**：初始化 `edgequake` 数据库、所需扩展，并在必要时创建 Apache AGE 兼容回退视图。
- **Ingress 资源**：为前端和 API 端点提供公开 HTTPS 路由。

**配置：**

模板提供以下部署参数：

- `EDGEQUAKE_LLM_PROVIDER`：可选择 `openai`、`mistral`、`anthropic`、`gemini`、`ollama` 或 `mock`。
- `OPENAI_API_KEY`：选择 OpenAI provider 时使用的 API key。
- `OPENAI_BASE_URL`：可选的 OpenAI 兼容 API base URL，适用于兼容 provider 或代理网关。
- `RUST_LOG`：API 容器的 Rust 日志过滤规则。

前端会在运行时接收生成后的 API URL，因此浏览器会连接到 Sealos 公开 API 端点，而不是本地开发地址。

**许可证信息：**

EdgeQuake 使用 [Apache License 2.0](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/LICENSE) 许可。

## 为什么在 Sealos 上部署 EdgeQuake？

Sealos 是一个基于 Kubernetes 构建的 AI 辅助云操作系统，覆盖从云端 IDE 开发到生产部署和运维管理的完整应用生命周期。它很适合 AI 应用、SaaS 平台和多服务架构。将 EdgeQuake 部署在 Sealos 上，你可以获得：

- **一键部署**：无需手写 Kubernetes 配置，也不用手动编排服务，即可部署 EdgeQuake。
- **多服务统一管理**：将 API、前端、数据库、初始化 Job、Service 和 Ingress 作为一个模板整体部署。
- **内置持久化存储**：PostgreSQL 数据保存在持久卷中，重启后仍然保留。
- **即时公网访问**：自动获得 Web UI 和 API 端点的 HTTPS URL。
- **轻松自定义**：通过 Sealos UI 配置 provider、API key、base URL、日志、资源和部署参数。
- **Canvas + AI 运维**：部署后可通过 Canvas、AI 对话和资源卡片检查或修改资源。
- **按量付费更高效**：默认使用紧凑资源配置，只有在业务负载需要时再扩容。
- **Kubernetes 底座**：无需直接运维 Kubernetes，也能获得服务发现、健康检查、滚动发布和工作负载隔离能力。

在 Sealos 上部署 EdgeQuake，把精力放在文档智能流程上，而不是基础设施运维上。

## 部署指南

1. 打开 [EdgeQuake 模板](https://sealos.io/products/app-store/edgequake)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - 选择 `EDGEQUAKE_LLM_PROVIDER`。
   - 使用 OpenAI 时填写 `OPENAI_API_KEY`。
   - 如需使用 OpenAI 兼容网关，可选填 `OPENAI_BASE_URL`。
   - 除非需要更详细的 API 日志，否则保持 `RUST_LOG` 为 `info`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。之后如需修改配置，可以在对话框中描述需求，让 AI 帮你应用变更，也可以点击对应资源卡片手动调整。
4. 通过生成的 URL 访问部署结果：
   - **Web UI**：从 App 资源中打开 EdgeQuake 应用 URL。
   - **API 端点**：使用生成的 API URL 进行 REST 调用、健康检查、SDK 集成，以及访问应用镜像启用的 `/swagger-ui`。

## 配置

部署完成后，你可以通过以下方式配置 EdgeQuake：

- **AI 对话**：描述想要的变更，例如更新环境变量、调整副本数或修改资源规格。
- **资源卡片**：点击 Deployment、Service、Ingress、Job 或 PostgreSQL 资源卡片，查看并修改设置。
- **Web UI**：在浏览器中配置工作区、上传文档并与生成的图谱交互。
- **API 端点**：通过 EdgeQuake REST API 集成外部工具。

## 扩容

如需扩容 EdgeQuake：

1. 打开当前部署的 Canvas。
2. 点击 API 或 Web UI 的 Deployment 资源卡片。
3. 根据负载调整 CPU、内存或副本数。
4. 在对话框中应用变更，并观察滚动发布状态。

对于更大的文档导入任务，建议优先扩容 API，并持续观察 PostgreSQL 使用情况。随着文档和图数据增长，也要关注数据库存储和备份需求。

## 故障排查

### 常见问题

**Web UI 无法连接 API**
- 原因：前端必须使用生成后的公开 API URL。
- 解决方案：确认前端 Deployment 中的 `EDGEQUAKE_API_URL` 已设置为 API Ingress URL；如果修改过 Ingress 设置，请重启前端。

**图查询失败，提示 Apache AGE 不可用**
- 原因：部分 PostgreSQL 环境可能不提供 Apache AGE 扩展。
- 解决方案：该模板会在 EdgeQuake 创建基础表后安装 AGE 兼容回退视图。如果首次启动阶段图查询失败，请等待初始化完成，并检查 `pgsql-init` Job 日志。

**LLM 请求失败**
- 原因：provider 凭据缺失或无效。
- 解决方案：确认 `EDGEQUAKE_LLM_PROVIDER`、`OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 与你的 provider 配置一致。

### 获取帮助

- [EdgeQuake GitHub 仓库](https://github.com/raphaelmansuy/edgequake)
- [EdgeQuake Issues](https://github.com/raphaelmansuy/edgequake/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [EdgeQuake README](https://github.com/raphaelmansuy/edgequake)
- [Docker Quick Start](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/DOCKER_QUICK_START.md)
- [Apache AGE](https://age.apache.org/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Sealos](https://sealos.run)

## 许可证

该 Sealos 模板遵循 Sealos templates 仓库的许可证。EdgeQuake 本身使用 [Apache License 2.0](https://github.com/raphaelmansuy/edgequake/blob/edgequake-main/LICENSE) 许可。
