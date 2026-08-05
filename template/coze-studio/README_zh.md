# 在 Sealos 上部署和托管 Coze Studio

Coze Studio 是一个开源 AI Agent 开发平台，提供工作流、知识库、记忆、插件和聊天能力。此模板会在 Sealos Cloud 上部署 Coze Studio 0.5.1 运行组件，并配套托管数据库、搜索、向量存储、对象存储和 HTTPS 访问入口。

![Coze Studio 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/coze-studio/website-screenshot.webp)

## 关于托管 Coze Studio

模板会在一个 Sealos 部署中维护应用服务和有状态依赖。Coze Studio 使用 KubeBlocks MySQL 保存关系数据，使用 KubeBlocks Redis 提供缓存和会话状态，使用 NSQ 传递消息，使用 Elasticsearch 保存搜索索引，使用 Milvus 提供向量存储，并使用私有 Sealos 对象存储桶保存上传资源。

生成的主机名会同时注入 Web Ingress 和服务端公网地址。etcd、Elasticsearch、Milvus 以及迁移工作区使用持久化卷，Pod 重启后数据仍会保留。

## 常见使用场景

- **Agent 原型开发**：用可视化工作流构建和测试 AI Agent。
- **知识助手**：索引文档，构建带检索能力的对话应用。
- **内部自动化**：组合插件、API 和定时工作流，支持团队运营流程。
- **团队协作试验**：为小型团队提供持久化的 Agent 开发工作区。

## 架构与依赖

部署包含以下运行组件：

- **Coze Studio Web**：Nginx 前端监听 `80` 端口，通过 HTTPS Ingress 和 Sealos App 入口访问。
- **Coze Studio Server**：API 和应用服务监听 `8888`、`8889` 端口。
- **NSQ**：由 `nsqlookupd` 和 `nsqd` 提供内部消息传递。
- **etcd**：Bitnami etcd 为 Milvus 保存协调数据，并使用持久化卷。
- **Elasticsearch**：Bitnami Elasticsearch `9.1.2` 保存 Coze 搜索索引。
- **Milvus**：Milvus `v2.5.10` 提供向量存储，并使用私有对象存储桶。
- **托管数据库**：KubeBlocks MySQL `ac-mysql-8.0.30-1` 和 Redis `redis-7.2.7` 提供应用状态与缓存。
- **初始化流程**：服务端 init 容器会等待依赖就绪，执行 Coze 数据库迁移，把默认图标复制到对象存储，并创建所需 Elasticsearch 索引。

## 为什么在 Sealos 上部署 Coze Studio？

Sealos 是基于 Kubernetes 的 AI 云操作系统。一个模板即可创建多服务运行组件、托管数据库、存储、TLS 和服务发现，让团队把精力放在 Agent 设计上。

- **一键部署**：同时创建 Web、API、消息、搜索、向量、数据库和存储资源。
- **托管运维**：部署后可通过 Canvas 资源卡片和 AI 对话调整环境。
- **持久化数据**：在托管卷中保留 Agent 资源、索引和数据库状态。
- **按需计费**：从紧凑资源配置开始，只为需要扩容的组件增加资源。

## 配置说明

请在部署弹窗中填写以下两项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `api_key` | 默认模型配置使用的 Ark API Key。 | 是 | 无 |
| `model_id` | Coze Studio 使用的 Ark 模型或 Endpoint ID。 | 是 | 无 |

模板会自动生成插件加密密钥和数据库凭据。请妥善保管 Ark 密钥，需要轮换时可通过 Sealos 资源配置进行更新。

## 部署指南

1. 打开 [Coze Studio 模板](https://sealos.io/products/app-store/coze-studio)，点击 **Deploy Now**。
2. 在参数弹窗中填写 Ark `api_key` 和 `model_id`。
3. 等待 Web、Server、NSQ、etcd、Elasticsearch、Milvus、MySQL 和 Redis 全部就绪。Sealos 部署通常需要 2-3 分钟；此多服务组件还要初始化数据库和索引，冷启动可能需要更长时间。部署完成后，Canvas 会展示资源卡片，可用 AI 对话或卡片直接调整。
4. 从 Sealos App 入口打开生成的 URL。
5. 首次访问时打开 `/sign`，填写邮箱和密码后点击 **注册**，新账号会自动进入工作空间；已有账号在同一页面点击 **登录**。
6. 打开 **工作空间**，点击 **创建**，选择 **创建智能体** 并保存一个测试 Agent，验证登录后的工作区流程。Agent 生成回复需要有效的 Ark Key 和模型 Endpoint。

## 存储与运维

Coze Studio 使用私有对象存储桶保存上传文件和默认插件图标。模板还会为 etcd、Elasticsearch、Milvus 和服务端迁移工作区各创建 1 GiB 持久化卷。Sealos 基于 Kubernetes，并按实际资源用量计费；数据量或流量增长后，可在 Canvas 中提高对应资源卡片的资源与存储容量，也可使用 Canvas AI 对话提交环境调整需求。

服务端迁移和索引初始化流程支持幂等执行。重启工作负载会保留数据库和持久化文件；删除部署时，资源按模板配置的托管保留策略处理。

## 故障排查

### Web 页面提前打开

请等待 Server 和 Web 工作负载进入 Ready。Server 会在 MySQL、Redis、NSQ、Elasticsearch 和 Milvus 就绪后再接受流量。

### 搜索或知识库功能失败

在 Canvas 中检查 Elasticsearch 健康状态和索引初始化容器日志。确认 Elasticsearch 已 Ready，并确认 `project_draft`、`coze_resource` 索引已经创建。

### Agent 无法返回结果

检查 `api_key` 和 `model_id` 是否对应有效的 Ark 凭据与 Endpoint。可在 Sealos 配置中更新参数并重启 Server 工作负载。

### 获取帮助

- [Coze Studio 文档](https://www.coze.com/docs)
- [Coze Studio GitHub Issues](https://github.com/coze-dev/coze-studio/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 官方链接

- [Coze Studio GitHub 仓库](https://github.com/coze-dev/coze-studio)
- [Coze Studio 官网](https://www.coze.com/)

## 其他资源

- [Coze Studio 文档](https://www.coze.com/docs)
- [Ark API 文档](https://www.volcengine.com/docs/82379)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。Coze Studio 本身遵循上游项目发布的许可证和使用条款。
