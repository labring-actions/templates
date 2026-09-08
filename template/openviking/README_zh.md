# 在 Sealos 上部署和托管 OpenViking

OpenViking 是面向 AI 智能体的上下文数据库，通过文件系统接口组织记忆、资源和技能。此模板在 Sealos Cloud 上部署 OpenViking API 服务和 Web Studio，提供持久化存储，并支持按需启用托管 S3 和 Redis。

![OpenViking 官网](./website-screenshot.webp)

## 关于托管 OpenViking

OpenViking 使用 `viking://` URI 管理上下文，并生成摘要和向量以支持语义检索。智能体可以通过 HTTP API 或 SDK 维护知识、记录会话和检索相关上下文。Web Studio 提供浏览器界面，可管理资源、检索、会话和账号。

模板使用官方镜像 `ghcr.io/volcengine/openviking:v0.4.18`，以单个应用实例在 `1933` 端口提供 API 和 Studio，并通过 Sealos 的 HTTPS 地址对外开放。持久卷保存配置、本地向量索引、身份验证数据和应用状态。部署时需要另外提供兼容 OpenAI 的嵌入模型与语言模型服务。

上下文文件默认保存在本地存储中，也可以选择私有 Sealos S3 存储。QueueFS 可独立选择托管 Redis。启用任一选项后，应用都会继续使用持久卷。

## 常见使用场景

- **智能体知识库**：导入文档，使用自然语言查询相关上下文。
- **智能体持久记忆**：跨会话组织用户和智能体上下文。
- **技能库**：将可复用指令与相关资源一起保存。
- **上下文检查**：通过 Studio 查看文件、检索结果、会话和处理任务。

## OpenViking 托管依赖

模板包含 OpenViking、Web Studio、持久化存储及选中的托管存储服务。部署前请准备兼容 OpenAI 的嵌入 API，以及视觉或语言模型 API 的访问凭据。模型调用由相应服务商单独计费；处理图片时需要选择支持视觉输入的模型。

- [官方网站](https://www.openviking.ai/)
- [部署指南](https://github.com/volcengine/OpenViking/blob/v0.4.18/docs/en/guides/03-deployment.md)
- [配置参考](https://github.com/volcengine/OpenViking/blob/v0.4.18/docs/en/guides/01-configuration.md)
- [身份验证指南](https://github.com/volcengine/OpenViking/blob/v0.4.18/docs/en/guides/04-authentication.md)
- [GitHub 问题反馈](https://github.com/volcengine/OpenViking/issues)

### 实现细节

**架构组件：**

| 组件 | 配置 |
| --- | --- |
| OpenViking 服务和 Studio | 单副本 StatefulSet；CPU 上限 `100m`、内存上限 `512Mi`；CPU 请求 `10m`、内存请求 `51Mi` |
| 应用存储 | 挂载到 `/app/.openviking` 的 `1Gi` 持久卷，包含本地向量索引 |
| 上下文文件存储 | 默认使用本地文件，可选私有 Sealos S3 存储桶 |
| QueueFS | 默认使用持久化 SQLite，可选 KubeBlocks Redis 7.2.7，包含一个 Redis 组件和一个 Sentinel 组件 |
| 可选 Redis 资源 | 每个托管组件的 CPU 上限为 `500m`、内存上限为 `512Mi`，各配置 `1Gi` 数据卷 |
| 公网访问 | HTTPS 地址；Studio 路径为 `/studio/`，API 路径为 `/api/v1/` |

当前应用资源配置面向个人使用和少量串行操作。处理大型文件、批量导入或多个并发用户时，请增加 CPU、内存和存储。模型并发数初始设为一。官方部署采用单副本，本地向量索引需要独占访问其数据目录。

## 为什么在 Sealos 上部署 OpenViking？

- **统一部署表单**：一次配置应用及其可选托管服务。
- **持久化存储**：Pod 重启后保留应用数据。
- **托管 HTTPS 访问**：为 Studio 和 API 客户端提供公网地址。
- **资源调整和日志查看**：通过部署 Canvas 及其资源卡片管理应用。

## 部署指南

1. 打开 [OpenViking 模板](https://sealos.io/products/app-store/openviking)，点击 **Deploy Now（立即部署）**。
2. 在部署对话框中填写模型配置并选择存储选项：

   | 参数 | 填写内容 |
   | --- | --- |
   | `embedding_api_key` | 嵌入模型服务的 API 密钥 |
   | `embedding_api_base` | 兼容 OpenAI 的 API 基础地址；服务商要求时应包含 `/v1` |
   | `embedding_model` | 该嵌入服务提供的模型，默认 `text-embedding-3-small` |
   | `embedding_dimension` | 与模型返回的向量长度一致的正整数，默认 `1536` |
   | `vlm_api_key` | 视觉或语言模型服务的 API 密钥 |
   | `vlm_api_base` | 该模型服务的 API 基础地址 |
   | `vlm_model` | 用于摘要生成和记忆提取的模型，默认 `gpt-4o-mini` |
   | `enable_s3_storage` | 启用私有 Sealos S3 存储来保存上下文文件，默认 `false` |
   | `enable_redis_queue` | 启用托管 Redis 作为 QueueFS 后端，默认 `false` |

   每个 API 密钥应搭配对应服务商的接口地址使用。部署前请确认嵌入模型实际返回的向量维度，并准确填写。
3. 等待部署完成，通常需要 **2-3 分钟**。首次拉取镜像或创建数据库时可能耗时更长，就绪检查还会访问嵌入服务。部署后 Sealos 会打开 Canvas；后续调整可通过 AI 对话框或对应资源卡片完成。
4. 打开应用的公网地址，进入 `/studio/` 下的 **Web Studio**，按下方步骤完成首次访问。API 客户端使用同一 HTTPS 域名和 `/api/v1/` 路径。

### 首次访问：创建账号并登录

此模板启用 API 密钥认证。管理员负责创建账号并分发用户 API 密钥，Studio 使用这些密钥完成身份验证。

1. 在部署 Canvas 中打开 OpenViking 应用资源卡片，找到自动生成的 `OPENVIKING_ROOT_API_KEY` 环境变量，妥善保管根密钥。
2. 打开 Studio，点击 **EN** 切换为英文界面，然后进入 **Connection Settings**。将 **Server URL** 保持为应用的 HTTPS 域名，在 **Root or Admin API Key** 中填入根密钥。设置会自动保存。
3. 打开左上角账号选择器，选择 **Create account**。填写 **Account**（账号名）和 **Initial admin user**（首位管理员），点击 **Create and switch**。Studio 会创建工作区、获取用户密钥并切换账号。在 **New API key** 对话框显示密钥时，将其复制并安全保存。
4. 确认 Studio 已显示新账号和用户。打开 **Sessions**，创建会话并添加消息。导入或写入资源后，可通过 **Retrieval** 执行检索。
5. 在其他浏览器登录或为普通用户配置访问时，请向账号管理员获取 **User Management** 中的用户密钥，再填入 **Connection Settings** 的 **User API Key**。用户密钥用于访问对应账号的数据，根密钥用于管理操作。

[身份验证指南](https://github.com/volcengine/OpenViking/blob/v0.4.18/docs/en/guides/04-authentication.md) 还提供了通过管理 API 创建账号和用户的方法。API 客户端可通过 `X-API-Key: <user-key>` 或 `Authorization: Bearer <user-key>` 认证。

## 配置与扩容

模型设置通过应用环境变量和 `/app/.openviking/ov.conf` 提供。使用对应 Canvas 资源卡片修改后，重启应用以加载新配置。嵌入模型与向量维度应始终匹配现有索引；更换时请规划索引重建。

建议在首次部署前确定 S3 和 Redis 选项。S3 将上下文文件保存在私有存储桶中，下载请求经由 OpenViking API 完成认证。Redis 保存 QueueFS 状态，本地向量索引及其他应用状态继续使用持久卷。更换已有部署的存储后端时，需要规划数据迁移。

通过资源卡片调整 CPU、内存和存储，进行垂直扩容。应用应保持一个副本，以符合本地向量索引的部署要求。升级或迁移前，请备份持久卷和已选择的外部存储。

## 故障排查

- **应用持续未就绪**：检查日志，以及嵌入服务的地址、密钥、模型可用性和向量维度。`/ready` 会实际检查嵌入服务连通性。
- **Studio 返回 401 或要求填写用户密钥**：检查 Connection Settings 中的密钥。数据操作使用所选账号的用户密钥，管理凭据填入 root 或 admin 字段。
- **上下文处理失败**：检查模型服务的额度和兼容性，并查看任务与应用日志。较大工作负载需要增加资源。
- **直接打开私有 S3 对象返回 403**：使用账号的用户 API 密钥，通过 OpenViking 下载文件。

## 许可证

OpenViking 使用 [GNU Affero General Public License v3.0](https://github.com/volcengine/OpenViking/blob/v0.4.18/LICENSE)。
