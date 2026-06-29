# 在 Sealos 上部署和托管 LiteLLM

LiteLLM 是兼容 OpenAI API 的 AI 网关，可用于模型流量路由、虚拟密钥管理、预算控制和费用追踪。此模板会在 Sealos Cloud 上部署带 PostgreSQL 元数据存储的 LiteLLM，并支持外部 PostgreSQL、可选 S3 兼容配置存储和公网 HTTPS 访问。

![LiteLLM 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/litellm/website-screenshot.webp)

## 关于托管 LiteLLM

LiteLLM 为团队提供一个统一网关端点，用 OpenAI API 格式访问 100 多个模型提供商。管理员可以在 UI 中创建虚拟密钥、添加模型凭据、查看使用量，并设置预算控制。

此 Sealos 模板运行 `litellm/litellm-database:v1.88.1` 镜像，并默认创建 PostgreSQL 16。部署时也可以选择外部 PostgreSQL URL；需要将配置对象放在容器外部时，可以开启 Sealos S3 兼容对象存储。

## 常见使用场景

- **统一 AI 网关**：让应用通过一个兼容 OpenAI 的端点访问多家模型服务。
- **虚拟密钥管理**：为团队、服务或客户创建独立密钥。
- **费用追踪**：在管理 UI 中查看模型调用量和预算消耗。
- **提供商故障切换**：在一个代理后管理多个 LLM 提供商。

## LiteLLM 托管依赖

此模板包含 LiteLLM 应用容器、默认 PostgreSQL 16 资源、可选 ObjectStorageBucket、HTTPS Ingress、Service 和 App 资源。

### 部署依赖

- [LiteLLM 文档](https://docs.litellm.ai/) - 代理、UI 和模型提供商配置
- [LiteLLM GitHub 仓库](https://github.com/BerriAI/litellm) - 源码和问题反馈
- [LiteLLM Docker 镜像](https://hub.docker.com/r/litellm/litellm) - 运行镜像标签

### 实现细节

**架构组件：**

- **LiteLLM Deployment**：在 `4000` 端口提供网关 API 和管理 UI。
- **PostgreSQL Cluster**：保存 LiteLLM 元数据、虚拟密钥、使用量和模型配置。
- **PostgreSQL Init Job**：在默认数据库模式下创建 `litellm` 数据库。
- **可选 ObjectStorageBucket**：当 `config_storage=sealos-s3` 时保存 LiteLLM 配置对象。
- **Ingress 和 App 入口**：通过 Sealos 生成的 HTTPS URL 暴露网关和 UI。

**配置：**

- `ui_username` 和 `ui_password` 设置管理 UI 登录凭据。
- `database_mode` 选择默认 PostgreSQL 或 `external_database_url`。
- `config_storage` 选择本地配置行为或 Sealos S3 兼容存储。
- 模板会自动生成 `LITELLM_MASTER_KEY` 和 `LITELLM_SALT_KEY`。

**许可证信息：**

LiteLLM 使用 MIT License。此 Sealos 模板提供在 Sealos Cloud 上运行 LiteLLM 的部署配置。

## 为什么在 Sealos 上部署 LiteLLM？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署和运维流程。在 Sealos 上部署 LiteLLM，可以获得一键部署、自动 HTTPS、托管数据库、持久化存储、资源控制和基于 Canvas 的更新能力。

## 部署指南

1. 打开 [LiteLLM 模板](https://sealos.io/products/app-store/litellm)，点击 **Deploy Now**。
2. 配置管理 UI 凭据，并选择默认 PostgreSQL 或外部 PostgreSQL。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可以在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 打开生成的公网 URL，使用 `ui_username` 和 `ui_password` 登录。
5. 在 LiteLLM 管理 UI 中添加模型提供商凭据。
6. 创建虚拟密钥，并将生成的 URL 作为兼容 OpenAI 的 base URL 使用。

## 配置

部署后可以通过以下方式配置 LiteLLM：

- **LiteLLM 管理 UI**：添加模型提供商、创建虚拟密钥、查看费用并管理团队。
- **AI 对话**：描述环境变量或资源调整需求，由 Sealos 应用更新。
- **资源卡片**：在 Canvas 中调整 CPU、内存、环境变量和存储。
- **数据库模式**：使用默认 PostgreSQL 完成全量部署，或通过 `external_database_url` 连接已有 PostgreSQL。

## 扩缩容

默认从单个 LiteLLM 副本开始。请求量增长时先在 Canvas 中增加 CPU 和内存；使用量和密钥管理数据增长后，再评估 PostgreSQL 容量。

## 故障排查

### 管理 UI 登录失败

- 原因：输入的凭据与 `ui_username`、`ui_password` 不一致。
- 解决方法：使用部署表单中的值，或在 Canvas 中更新 Deployment 环境变量。

### 网关尚未就绪

- 原因：LiteLLM 仍在连接 PostgreSQL 或执行启动检查。
- 解决方法：在 Canvas 中查看 LiteLLM Deployment 日志和 PostgreSQL Cluster 就绪状态。

### 模型调用失败

- 原因：LiteLLM UI 中缺少模型提供商凭据或模型名称。
- 解决方法：添加提供商凭据，配置模型，并用虚拟密钥测试。

## 更多资源

- [LiteLLM Proxy 文档](https://docs.litellm.ai/docs/simple_proxy)
- [LiteLLM 管理 UI 文档](https://docs.litellm.ai/docs/proxy/ui)
- [LiteLLM GitHub Issues](https://github.com/BerriAI/litellm/issues)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为部署配置提供给 Sealos 用户使用。LiteLLM 本身基于 [MIT License](https://github.com/BerriAI/litellm/blob/main/LICENSE) 授权。
