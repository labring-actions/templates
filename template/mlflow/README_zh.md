# 在 Sealos 上部署和托管 MLflow

MLflow 是一个开源平台，用于跟踪机器学习实验、整理模型元数据并存储模型产物。此模板会在 Sealos Cloud 上部署 MLflow，并配置 PostgreSQL 元数据存储和 S3 兼容产物存储。

## 关于托管 MLflow

MLflow 以 Web 服务形式运行，在 5000 端口提供实验跟踪界面和 REST API。Sealos 模板会自动创建 PostgreSQL 作为 backend store，并创建 Object Storage 存储桶保存 artifacts，因此实验元数据和上传文件在重启后仍会保留。

此部署模式下，MLflow 默认不包含内置登录或用户认证。请将生成的 Sealos URL 视为工作区内的应用入口；如果需要多人或公网访问保护，请额外添加认证代理或网络访问控制。

## 常见使用场景

- **实验跟踪**：记录模型训练运行的参数、指标、标签和产物。
- **模型注册流程**：整理模型版本和元数据，用于评审和发布流程。
- **产物存储**：保存训练输出、图表、模型文件和评估报告。
- **团队机器学习运维**：为 notebooks、脚本和 CI 任务共享一个中心化 tracking server。

## MLflow 托管依赖

Sealos 模板包含所需运行依赖：MLflow server 容器、用于元数据的 KubeBlocks PostgreSQL 16.4 集群，以及用于 artifacts 的私有 Object Storage 存储桶。

### 部署依赖

- [MLflow 文档](https://mlflow.org/docs/latest/) - 官方文档
- [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) - Tracking UI 和 API 指南
- [MLflow GitHub 仓库](https://github.com/mlflow/mlflow) - 源代码和问题反馈

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **MLflow Server**：在 5000 端口提供 Web UI 和 REST API。
- **PostgreSQL**：保存实验、运行记录、参数、指标和模型元数据。
- **Object Storage**：通过 S3 API 保存 MLflow artifacts。
- **Ingress 和 App Link**：提供由 Sealos 管理的公网 HTTPS 入口。

**配置：**

服务启动时会将 `--backend-store-uri` 指向 PostgreSQL，并将 `--default-artifact-root` 指向生成的 S3 存储桶。Sealos 通过托管 Secret 注入数据库和对象存储凭据，部署时无需手动填写私有凭据。

**访问与认证：**

部署完成后，可以通过生成的 HTTPS URL 直接访问 MLflow。此模板不会创建用户名或密码，因为上游 MLflow tracking server 在该模式下没有内置登录页。如果 tracking server 不应公开访问，请使用 Sealos 工作区控制、私有分享策略或外部认证代理。

**许可证信息：**

MLflow 使用 Apache License 2.0。此 Sealos 模板遵循 Sealos templates 仓库的许可证。

## 为什么在 Sealos 上部署 MLflow？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一管理应用部署、网络、存储和后续运维。在 Sealos 上部署 MLflow，你可以获得：

- **一键部署**：通过一个模板部署 MLflow、PostgreSQL、对象存储、Service、Ingress 和 App 入口。
- **持久化元数据与产物**：使用 PostgreSQL 保存 MLflow 元数据，并使用托管 S3 兼容存储保存 artifacts。
- **即时公网访问**：部署后获得 HTTPS 入口，无需手动配置 Ingress 或证书。
- **易于调整**：部署后可在 Sealos Canvas 中调整 CPU、内存、环境变量和存储配置。
- **Kubernetes 基础能力**：无需直接维护原始 Kubernetes YAML，也能运行在 Kubernetes 之上。
- **按量资源使用**：先使用模板默认资源，之后再按工作负载增长进行扩容。

## 部署指南

1. 打开 [MLflow 模板](https://sealos.io/products/app-store/mlflow)，点击 **Deploy Now**。
2. 除非需要自定义应用名称或域名前缀，否则保留默认参数。
3. 等待部署完成，通常需要 2-3 分钟。部署后会进入 Canvas。后续如需修改，可在 AI 对话框描述需求，或点击对应资源卡片调整设置。
4. 通过生成的 URL 访问应用：
   - **MLflow UI**：打开生成的 HTTPS 应用地址。系统不会创建默认用户名或密码。
   - **Tracking API**：在 MLflow 客户端中将同一个生成地址设置为 `MLFLOW_TRACKING_URI`。

## 配置

部署后，可以通过以下方式配置 MLflow：

- **AI 对话框**：描述需要修改的内容，让 Sealos 应用变更。
- **资源卡片**：打开 Deployment、PostgreSQL、Object Storage 或 Ingress 卡片调整资源和设置。
- **MLflow 客户端**：在 notebooks、训练脚本或 CI 任务中将 `MLFLOW_TRACKING_URI` 设置为生成的应用地址。
- **外部访问控制**：如果 tracking server 包含敏感实验数据，请添加认证代理或限制访问范围。

## 扩容

如需扩展 MLflow 资源：

1. 打开该部署对应的 Canvas。
2. 点击 MLflow Deployment 资源卡片。
3. 根据请求量、artifact 活动和 UI 使用情况调整 CPU 与内存。
4. 在对话框中应用变更，并等待新 Pod 进入 ready 状态。

## 故障排查

### MLflow URL 打开后没有登录页

MLflow tracking server 在此部署模式下没有内置登录功能。这是预期行为。如需保护入口，请使用工作区访问规则、私有分享或外部认证代理。

### 客户端无法写入运行记录

确认 `MLFLOW_TRACKING_URI` 使用生成的 HTTPS URL。如果运行记录需要上传 artifacts，也请确认部署状态健康，并且 Canvas 中存在 Object Storage 存储桶。

### 部署耗时超过预期

PostgreSQL 和 MLflow 容器初始化需要一定时间。如果几分钟后应用仍未 ready，请在 Canvas 中检查 Deployment 和 PostgreSQL 资源卡片。

### 获取帮助

- [MLflow 文档](https://mlflow.org/docs/latest/)
- [MLflow GitHub Issues](https://github.com/mlflow/mlflow/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [MLflow Tracking API](https://mlflow.org/docs/latest/api_reference/rest-api.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循 Sealos templates 仓库的许可证。MLflow 本身使用 Apache License 2.0。
