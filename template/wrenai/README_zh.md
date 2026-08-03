# 在 Sealos 上部署和托管 WrenAI

WrenAI 是一个开源 GenBI Agent，可通过数据对话生成 Text-to-SQL、图表、电子表格、报告和 BI 洞察。此模板会在 Sealos Cloud 上部署 WrenAI `0.29.3` AI 服务、`0.24.6` 引擎、`0.25.0` Ibis 服务、`0.32.2` UI、Qdrant `v1.18.2` 和 PostgreSQL。

![WrenAI 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/wrenai/website-screenshot.webp)

## 关于托管 WrenAI

模板会把 WrenAI 运行组件作为一个 Sealos 应用部署。UI 提供公网 HTTPS 入口，AI Service 负责模型和向量嵌入调用，Wren Engine 与 Ibis Server 执行 SQL，Qdrant 保存向量，PostgreSQL 保存项目和配置数据。

AI Service 从挂载的 ConfigMap 读取生成配置。部署需要分别提供文本生成和向量嵌入的 OpenAI 密钥。所有内部服务使用集群 DNS，运行组件会在 Sealos 命名空间内协同工作。

## 常见使用场景

- **自然语言分析**：让团队用日常语言询问已连接的数据源。
- **SQL 加速**：在分析过程中生成、解释和修正 SQL。
- **语义建模**：索引数据表结构和业务描述，提升重复问答的一致性。
- **自托管 BI 试验**：把元数据和向量索引保存在 Sealos 工作区中。

## 架构与依赖

- **Wren UI `0.32.2`**：监听 `3000` 端口，通过 HTTPS Ingress 和 App 入口提供访问。
- **Wren AI Service `0.29.3`**：监听 `5555` 端口，负责模型和嵌入网关。
- **Wren Engine `0.24.6`**：监听 `8080`、`7432` 端口，包含 bootstrap 初始化容器。
- **Wren Ibis Server `0.25.0`**：监听 `8000` 端口，提供 Ibis 查询服务。
- **Qdrant `v1.18.2`**：使用存储、快照和初始化卷保存向量数据。
- **PostgreSQL `16.4.0`**：由 KubeBlocks 管理，为 `wrenai` 应用数据库提供服务。
- **PostgreSQL 初始化 Job**：等待数据库就绪并幂等创建 `wrenai` 数据库。

## 为什么在 Sealos 上部署 WrenAI？

Sealos 是基于 Kubernetes 的 AI 云操作系统。一个可复用的部署即可创建 WrenAI 服务、托管 PostgreSQL、持久化向量存储、TLS 和服务发现。

- **一键搭建 GenBI 栈**：同时创建 UI、模型网关、SQL 服务、向量检索和 PostgreSQL。
- **托管运维**：部署后使用 Canvas 资源卡片和 AI 对话调整环境。
- **分析状态持久化**：重启后保留表结构、嵌入、项目和查询元数据。
- **按需计费**：根据数据集规模和查询量，为需要的组件扩容。

## 配置说明

请在部署弹窗中填写以下凭据：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `openai_api_key` | WrenAI 文本生成使用的 OpenAI Key。 | 是 | 无 |
| `embedder_openai_api_key` | `text-embedding-3-large` 使用的 OpenAI Key。 | 是 | 无 |
| `openai_api_base` | 文本生成使用的 OpenAI 兼容 API Base。 | 否 | `https://api.openai.com/v1` |
| `embedder_openai_api_base` | 向量嵌入使用的 OpenAI 兼容 API Base。 | 否 | `https://api.openai.com/v1` |
| `generation_model` | WrenAI 使用的默认聊天模型名称。 | 否 | `gpt-4.1-nano-2025-04-14` |

模板会自动生成应用名称、主机名和用户遥测标识。请将 API Key 保存在 Sealos 管理的输入项中，需要轮换时通过工作负载配置更新。

## 部署指南

1. 打开 [WrenAI 模板](https://sealos.io/products/app-store/wrenai)，点击 **Deploy Now**。
2. 在参数弹窗中填写 `openai_api_key` 和 `embedder_openai_api_key`。
3. 公共 OpenAI API 可保留默认 Base；使用 OpenAI 兼容服务时，同时填写两个 API Base，并将 `generation_model` 设置为该服务支持的模型。
4. 等待 PostgreSQL、初始化 Job、AI Service、Engine、Ibis Server、Qdrant 和 UI 进入 Ready。Sealos 部署通常需要 2-3 分钟；此运行组件还要初始化数据库和向量存储，冷启动可能需要更长时间。部署完成后，Canvas 会提供 AI 对话和资源卡片，便于继续调整。
5. 从 Sealos App 入口打开生成的 URL。
6. 在 `/setup/connection` 完成 WrenAI 首次设置，然后添加数据源或选择内置 E-commerce 样例。
7. WrenAI OSS 会直接进入设置流程，此模板没有邮箱密码注册和登录页；Sealos App 访问权限与工作区权限构成访问边界。
8. 样例数据完成索引后，可打开 Modeling 或 Home 并运行示例问题。语义索引和问答需要同时提供可用的文本生成端点与 embedding 端点。

## 存储与运维

Qdrant 使用持久化卷保存向量、快照和初始化标记。Wren Engine 使用持久化 `/app/data` 卷保存 bootstrap 数据，PostgreSQL 使用 1 GiB 托管数据卷。Sealos 基于 Kubernetes，并按实际资源用量计费。数据集或查询历史增长后，可在 Canvas 中扩展对应资源卡片，也可通过 Canvas AI 对话提交环境调整需求。

WrenAI 会使用填写的密钥向配置的 OpenAI 兼容 API Base 发起模型和嵌入请求。导入大型数据表结构前，请检查供应商配额和集群出网策略。

## 故障排查

### UI 可以打开，但数据查询失败

检查 AI Service、Engine 和 Ibis Server 日志。确认两个 OpenAI Key 均已填写，并确认 UI 能访问内部服务 DNS。

### 向量索引失败

检查 Qdrant Ready 状态和 AI Service 日志。确认 Qdrant 存储卷与快照卷已绑定，并确认嵌入 Key 有权调用 `text-embedding-3-large`。

### 提问一直停留在“Understanding question”

检查 AI Service 日志中的 embedding 供应商响应。`/embeddings` 返回 `503` 表示当前 OpenAI 兼容服务没有提供配置的 embedding 模型；请改用支持 embedding 的供应商和模型，然后重启 AI Service 配置。

### PostgreSQL 初始化一直等待

等待 PostgreSQL Cluster 进入 Ready，并确认 `wrenai-pg-init` Job 已完成。UI 启动门会等待 `wrenai` 数据库创建完成后再接受请求。

### 获取帮助

- [WrenAI 文档](https://docs.getwren.ai/)
- [WrenAI GitHub Issues](https://github.com/Canner/WrenAI/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 官方链接

- [WrenAI 官网](https://getwren.ai/)
- [WrenAI 源码仓库](https://github.com/Canner/WrenAI)

## 其他资源

- [WrenAI OSS 文档](https://docs.getwren.ai/oss/introduction)
- [WrenAI 部署指南](https://docs.getwren.ai/oss/deployment)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。WrenAI 及其组件遵循各自上游项目的许可证。
