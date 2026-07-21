# 在 Sealos 上部署和托管 Paperclip

Paperclip 是一个开源的 AI Agent 公司控制平台，可在同一个 Web 应用中管理公司、Agent、项目、任务、审批、插件、密钥和执行历史。本模板会在 Sealos Cloud 上部署 Paperclip，并配置托管 PostgreSQL、持久化应用存储、可选 S3 兼容对象存储和公网认证访问。

![Paperclip 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/paperclip/website-screenshot.webp)

## 关于 Paperclip 托管

Paperclip 围绕实际工作组织 AI Agent。你可以通过 Web 界面和 API 创建公司、定义 Agent 职责、管理项目与任务、处理审批，并查看 Agent 活动。官方容器内置 Codex、Claude、OpenCode 和 Gemini 等本地 Agent CLI。

Sealos 模板使用 Kubernetes StatefulSet 运行 Paperclip。KubeBlocks 为公网认证部署提供 PostgreSQL，持久卷用于保存配置、加密密钥、工作区、日志和本地上传文件。启用 `use_object_storage` 后，模板会创建私有 Sealos 对象存储桶，用于保存附件和公司资产。

## 常见使用场景

- **AI 团队运营**：创建公司、分配 Agent，并协调项目工作。
- **任务与审批流程**：跟踪任务、评论、优先级、审批和执行历史。
- **编码 Agent 中心**：通过同一个 Web UI 运行 Codex、Claude、OpenCode 或 Gemini Agent。
- **插件运维**：安装插件并监控插件健康状态。
- **私有 Agent 工作区**：在 Sealos 托管部署中保存工作区数据和密钥。

## 依赖项

- Paperclip `v2026.720.0`，镜像固定为 digest `sha256:30237caad0ca3625fd10436a833c3b40809fe54b84debd702896e801d02c584e`
- 通过 KubeBlocks 部署的 PostgreSQL `16.4.0`
- 挂载到 `/paperclip` 的持久化存储
- 可选的私有 S3 兼容对象存储
- Sealos HTTPS Ingress 和 App 入口

### 官方参考资料

- [Paperclip 官网](https://paperclip.ing)
- [Paperclip 文档](https://docs.paperclip.ing)
- [Paperclip GitHub 仓库](https://github.com/paperclipai/paperclip)
- [Docker 部署指南](https://github.com/paperclipai/paperclip/blob/v2026.720.0/doc/DOCKER.md)
- [数据库指南](https://docs.paperclip.ing/deploy/database)
- [存储指南](https://docs.paperclip.ing/deploy/storage)

## 实现细节

**架构组件：**

- **Paperclip StatefulSet**：使用固定版本镜像运行 Paperclip，监听 `3100` 端口。
- **PostgreSQL Cluster**：存储用户、公司、任务、审批、插件和运行时元数据。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `paperclip` 数据库。
- **配置 Init Container**：根据选定的存储模式写入 `/paperclip/instances/default/config.json`。
- **Bootstrap CEO Job**：创建 Sealos App 入口使用的首个管理员邀请。
- **持久卷**：保存 `/paperclip` 下的配置、密钥、日志、工作区和本地上传文件。
- **可选 ObjectStorageBucket**：通过 Paperclip S3 provider 保存附件和公司资产。
- **Service、Ingress 和 App Resource**：提供公网 HTTPS 地址和首个管理员入口。

Paperclip 使用 `authenticated` 部署模式和 `public` 暴露模式。该模式要求配置 `DATABASE_URL`，模板会始终创建独立 PostgreSQL 集群。应用 Pod 和辅助 Job 使用 UID/GID `1000` 运行，同时关闭权限提升、移除全部 Linux capabilities，并启用 runtime-default seccomp profile。

部署时可填写以下模型服务商密钥：

- `openai_api_key`：用于 Codex 和 OpenAI 后端 Agent
- `anthropic_api_key`：用于 Claude 后端 Agent
- `gemini_api_key`：用于 Gemini 后端 Agent

存储模式：

- **本地存储**：默认选项。文件保存在持久卷的 `/paperclip/instances/default/data/storage` 目录。
- **S3 存储**：启用 `use_object_storage` 后，模板会创建私有存储桶并自动配置 Paperclip S3 provider。

**已验证的资源限制：**

- Paperclip 应用：`100m` CPU 和 `512Mi` 内存
- Init Container 与 Bootstrap Container：`100m` CPU 和 `128Mi` 内存
- PostgreSQL：`500m` CPU 和 `512Mi` 内存

Paperclip 暴露 `/api/health`，模板使用该端点作为启动、就绪和存活探针。

## 为什么在 Sealos 上部署 Paperclip？

- **一键部署**：通过一个模板创建 Paperclip、PostgreSQL、存储和 HTTPS 入口。
- **持久化工作区**：重启后继续保留加密密钥、日志、工作区和应用状态。
- **托管对象存储**：可选择私有 S3 兼容存储桶保存上传资产。
- **公网 HTTPS 访问**：自动获得 Sealos 托管的公网地址。
- **Canvas 运维**：通过资源卡片调整模型密钥、资源、存储和网络配置。

## 部署指南

1. 打开 [Paperclip 模板](https://sealos.io/products/app-store/paperclip)，点击 **Deploy Now**。
2. 选择存储模式。保持 `use_object_storage` 关闭即可使用本地持久化存储；启用后会创建私有 Sealos 对象存储桶。
3. 填写 Agent 所需的模型服务商 API key。
4. 等待约 2-3 分钟，让 PostgreSQL 完成迁移、Paperclip 启动并创建 Bootstrap 邀请。
5. 从 Sealos 打开 Paperclip 应用入口，该入口会直接进入首个管理员邀请页面。

## 首次登录与注册

1. 在邀请页面点击 **Sign in / Create account**。
2. 选择 **Create account**，填写姓名、邮箱和密码，然后提交表单。
3. 返回邀请页面，点击 **Accept bootstrap invite**。
4. 创建第一家公司，完成 onboarding。
5. 打开公司看板，即可创建任务、添加评论、调整优先级和配置 Agent。

首个管理员接受邀请后，可通过公网域名根路径正常登录。Bootstrap 邀请有效期为 72 小时。Bootstrap Job 完成后会保留五分钟，可在这段时间内通过日志查看生成的 `Invite URL`。

## 配置

- **Web UI**：管理公司、Agent、任务、插件、密钥和审批。
- **环境变量**：通过 StatefulSet 资源卡片添加或轮换模型服务商 API key。
- **存储**：部署时选择本地持久化存储或 S3 兼容对象存储。
- **资源**：通过 Sealos Canvas 调整 CPU、内存、持久卷大小或 Ingress 设置。

## 故障排查

### 邀请页面已过期

在 Paperclip StatefulSet 终端中生成新的首个管理员邀请：

```bash
node cli/node_modules/tsx/dist/cli.mjs cli/src/index.ts auth bootstrap-ceo \
  --config "$PAPERCLIP_CONFIG" \
  --base-url "$PAPERCLIP_PUBLIC_URL" \
  --expires-hours 72
```

### Agent 运行时提示缺少凭据

通过部署参数或 StatefulSet 环境变量，为所选 Agent CLI 添加 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 或 `GEMINI_API_KEY`。

### 文件上传失败

使用本地存储时，确认 `/paperclip` 持久卷已经挂载，并允许 UID `1000` 写入。使用 S3 存储时，检查 ObjectStorageBucket 状态及其自动生成的凭据，然后确认 Paperclip Pod 处于 Ready 状态。

## 许可证

本 Sealos 模板提供 Paperclip 的部署配置。Paperclip 使用 MIT License。
