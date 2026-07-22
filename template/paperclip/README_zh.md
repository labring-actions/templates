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
- **首个管理员 Bootstrap Helper**：等待 Paperclip 健康端点，为 setup code 创建或轮换邀请，并在初始化成功后放行就绪探针。
- **持久卷**：保存 `/paperclip` 下的配置、密钥、日志、工作区和本地上传文件。
- **可选 ObjectStorageBucket**：通过 Paperclip S3 provider 保存附件和公司资产。
- **Service、两个 Ingress 资源和 App 入口**：提供公网 HTTPS 地址，并保留指向 setup code 邀请的兼容入口。

Paperclip 使用 `authenticated` 部署模式和 `public` 暴露模式。该模式要求配置 `DATABASE_URL`，模板会始终创建独立 PostgreSQL 集群。Paperclip Pod 及其 Init Container 使用 UID/GID `1000` 运行，同时关闭权限提升、移除全部 Linux capabilities，并启用 runtime-default seccomp profile。PostgreSQL 初始化 Job 同样关闭权限提升并移除全部 Linux capabilities。

部署时可填写以下模型服务商密钥：

- `openai_api_key`：用于 Codex 和 OpenAI 后端 Agent
- `anthropic_api_key`：用于 Claude 后端 Agent
- `gemini_api_key`：用于 Gemini 后端 Agent

存储模式：

- **本地存储**：默认选项。文件保存在持久卷的 `/paperclip/instances/default/data/storage` 目录。
- **S3 存储**：启用 `use_object_storage` 后，模板会创建私有存储桶并自动配置 Paperclip S3 provider。

**已验证的资源限制：**

- Paperclip 应用：`100m` CPU 和 `1024Mi` 内存
- Init Container：`100m` CPU 和 `128Mi` 内存
- PostgreSQL：`500m` CPU 和 `512Mi` 内存

Paperclip 暴露 `/api/health`。启动与存活探针直接检查该端点；就绪探针还会检查 `/tmp/paperclip-bootstrap-ready`，该标记会在首个管理员邀请准备完成或实例已有管理员后生成。

## 为什么在 Sealos 上部署 Paperclip？

- **基于 Kubernetes 的一键部署**：通过一个模板创建 Paperclip、PostgreSQL、存储和 HTTPS 入口。
- **持久化工作区**：重启后继续保留加密密钥、日志、工作区和应用状态。
- **托管对象存储**：可选择私有 S3 兼容存储桶保存上传资产。
- **公网 HTTPS 访问**：自动获得 Sealos 托管的公网地址。
- **AI 辅助 Canvas 运维**：在 AI 对话框中描述部署后的变更，或通过资源卡片调整模型密钥、资源、存储和网络配置。
- **按量付费资源**：个人部署可采用已验证的资源档位，并按实际使用的 Sealos 资源付费。

## 部署指南

1. 打开 [Paperclip 模板](https://sealos.io/products/app-store/paperclip)，点击 **Deploy Now**。
2. 确认部署前记录预填的 `first_admin_setup_code`。你可以将其替换为 32-128 位 URL-safe 字符，内容需同时包含大写字母、小写字母和数字。
3. 选择存储模式。保持 `use_object_storage` 关闭即可使用本地持久化存储；启用后会创建私有 Sealos 对象存储桶。
4. 填写 Agent 所需的模型服务商 API key。
5. 等待约 2-3 分钟，让 PostgreSQL 完成迁移、Paperclip 启动并完成首个管理员初始化。随后 Sealos 会打开本次部署的 Canvas。
6. 复制 Sealos 中显示的 Paperclip 公网域名，然后打开 `https://<你的-Paperclip-域名>/invite/<first_admin_setup_code>`。Sealos App 入口会继续指向同一个邀请 URL，作为兼容快捷入口。
7. 后续需要调整部署时，可在 Canvas AI 对话框中描述变更，或打开对应的资源卡片。

## 首次登录与注册

1. 使用部署前记录的 code 打开 `https://<你的-Paperclip-域名>/invite/<first_admin_setup_code>`。
2. 点击 **Sign in / Create account**，选择 **Create account**，填写姓名、邮箱和密码，然后点击 **Create account and continue**。
3. 已有账号时，选择 **I already have an account**，完成登录后返回同一个邀请 URL。
4. 完成身份验证后，Paperclip 会继续处理邀请。如果邀请仍处于待确认状态，请重新打开同一个邀请 URL，然后点击 **Accept bootstrap invite**。
5. 创建第一家公司，完成 onboarding。
6. 打开公司看板，即可创建任务、添加评论、调整优先级和配置 Agent。

首个管理员邀请从最近一次成功准备开始计算 72 小时有效期，并且只能认领一次。Pod 重启会使用同一个 setup code 刷新尚未认领的邀请。首个管理员接受邀请后，可通过公网域名根路径正常登录。邀请有效期间请将 setup code 作为 bearer credential 妥善保管。兼容 App 入口会保存邀请路径，访问后浏览器历史和 Paperclip 请求日志也会记录该路径；请将 Sealos 工作空间和 Paperclip 日志的访问权限控制在可信运维边界内。

## 配置

- **Web UI**：管理公司、Agent、任务、插件、密钥和审批。
- **AI 对话框**：在 Sealos Canvas 中描述部署后的变更，由 AI 更新相关资源。
- **环境变量**：通过 StatefulSet 资源卡片添加或轮换模型服务商 API key。
- **首个管理员 Setup Code**：部署前记录，并在邀请被认领前妥善保管。
- **存储**：部署时选择本地持久化存储或 S3 兼容对象存储。
- **资源卡片**：通过 Sealos Canvas 调整 CPU、内存、持久卷大小或 Ingress 设置。

## 故障排查

### Setup code 丢失或过期

在 Sealos 中打开现有 Paperclip 部署，设置新的合法 `first_admin_setup_code`，然后重新部署。Bootstrap Helper 会撤销旧的有效邀请，并创建一个有效期为 72 小时的新邀请。确认重新部署前请记录新的 code。

### Agent 运行时提示缺少凭据

通过部署参数或 StatefulSet 环境变量，为所选 Agent CLI 添加 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 或 `GEMINI_API_KEY`。

### 文件上传失败

使用本地存储时，确认 `/paperclip` 持久卷已经挂载，并允许 UID `1000` 写入。使用 S3 存储时，检查 ObjectStorageBucket 状态及其自动生成的凭据，然后确认 Paperclip Pod 处于 Ready 状态。

## 许可证

本 Sealos 模板提供 Paperclip 的部署配置。Paperclip 使用 MIT License。
