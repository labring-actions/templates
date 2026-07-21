# 在 Sealos 上部署和托管 Flowise

Flowise 是一款用于构建 AI 智能体与大语言模型（LLM）工作流的可视化平台。此模板会在 Sealos 上部署 Flowise 3.1.2，并提供持久化存储、自动 HTTPS，以及可选的托管 PostgreSQL 和私有 S3 兼容对象存储。

![Flowise 应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/flowise/website-screenshot.webp)

## 关于 Flowise 托管

Flowise 提供拖拽式画布，可以连接语言模型、工具、记忆、文档加载器与向量数据库。你可以在同一个 Web 界面中构建对话流、智能体工作流、助手，管理 API 与可复用凭据。

默认部署使用 SQLite，并将应用数据保存在 1 GiB 持久卷中。部署时可以启用 PostgreSQL 16.4 托管数据库，也可以启用 Sealos 对象存储来保存上传文件；两项存储能力可以独立选择。

## 常见使用场景

- **AI 助手**：构建具备工具调用、记忆与检索能力的对话式助手。
- **RAG 流程**：加载和切分文档，并连接向量数据库。
- **智能体工作流**：通过可视化多步骤流程编排模型与工具。
- **API 后端**：通过 Flowise API 将已保存的流程提供给其他应用调用。

## Flowise 托管依赖

此模板包含 Flowise 应用、1 GiB 持久卷、HTTPS 公网入口和自动生成的认证密钥。启用可选能力后，Sealos 会一并创建对应的托管服务。

### 部署依赖

- [Flowise 文档](https://docs.flowiseai.com/) - 产品与 API 文档
- [Flowise 源码](https://github.com/FlowiseAI/Flowise) - 上游代码仓库
- [Sealos 应用商店](https://sealos.io/products/app-store/flowise) - 模板部署页面

### 实现细节

**架构组件：**

- **Flowise 3.1.2**：单个 StatefulSet，通过 3000 端口提供 Web 界面和 API。
- **持久卷**：保存 SQLite 数据、密钥、日志和本地上传文件。
- **PostgreSQL 16.4**：可选的 KubeBlocks 托管数据库，配备 1 GiB 数据卷。
- **Sealos 对象存储**：可选的私有 S3 兼容存储桶，用于保存上传文件。
- **Ingress**：提供自动生成的公网域名并终止 TLS。

**部署选项：**

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `USE_POSTGRESQL` | `false` | 使用托管 PostgreSQL 保存应用数据；默认使用 SQLite。 |
| `USE_S3_STORAGE` | `false` | 使用私有 Sealos 对象存储保存上传文件。 |

应用资源上限为 100m CPU 和 1 GiB 内存。持久卷会在 Pod 重启后继续保存账户与工作流数据。

**许可证信息：**

Flowise 的开源组件采用 Apache 2.0 许可证，另行标注的企业组件遵循上游商业许可证。

## 为什么在 Sealos 上部署 Flowise？

- **一键创建**：一次部署即可创建应用、存储、网络和已选择的托管服务。
- **独立选择存储方案**：通过部署表单选择 SQLite 或 PostgreSQL、本地文件或 S3 存储。
- **数据持久化**：账户、工作流、凭据和上传内容会在重启后继续保留。
- **托管公网访问**：自动获得已配置 Ingress 与 TLS 的 HTTPS 地址。
- **资源可控**：通过 Sealos 资源卡片调整 CPU、内存和存储空间。

## 部署指南

1. 打开 [Flowise 模板](https://sealos.io/products/app-store/flowise)，点击 **Deploy Now**。
2. 根据业务需要选择 PostgreSQL 与 S3 存储，然后确认部署。
3. 等待 StatefulSet 和已选择的托管服务进入就绪状态。Flowise 首次启动需要初始化数据库，通常需要几分钟。
4. 打开应用卡片中显示的访问地址。

## 创建账户并登录

首次访问会进入 Flowise 账户设置页面。填写姓名、电子邮件地址和高强度密码，即可创建管理员账户。

后续访问会进入登录页面。使用同一电子邮件地址和密码登录。账户数据保存在持久卷或 PostgreSQL 中，Pod 重启后仍会保留。

## 配置

在 Flowise 界面中添加模型凭据、创建对话流或智能体工作流，并配置文档存储。部署时生成的密钥会用于加密凭据。

需要调整基础设施时，请打开部署 Canvas，通过 AI 对话或资源卡片修改配置。更新现有部署时，请保持自动生成的认证密钥稳定。

## 故障排查

### 应用仍在启动

Flowise 会在开放 3000 端口前初始化节点并执行数据库迁移。请检查 StatefulSet 日志，并等待出现 `Flowise Server is listening at :3000`。

### S3 上传失败

请确认已经启用 `USE_S3_STORAGE`，且对象存储桶处于就绪状态。模板会自动注入存储桶端点与凭据。

### 获取帮助

- [Flowise 文档](https://docs.flowiseai.com/)
- [Flowise GitHub Issues](https://github.com/FlowiseAI/Flowise/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Flowise 的许可证详情见[上游许可证文件](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md)。
