# 在 Sealos 上部署和托管 Paperclip

Paperclip 是开源 AI 团队运行平台，用于管理智能体公司、任务流、审批、插件和本地编码 Agent。本模板会在 Sealos Cloud 上部署 Paperclip，并自动配置 PostgreSQL、持久化应用存储、可选 S3 兼容对象存储和公网认证访问。

![Paperclip 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/paperclip/website-screenshot.webp)

## 关于 Paperclip 托管

Paperclip 提供 Web 界面和 API，用于围绕公司、项目、Issue、审批、密钥、插件和执行工作区组织 AI Agent。Docker 镜像内置 Codex、Claude、OpenCode 和 Gemini 等本地 Agent CLI，配置好凭据后可在容器内运行对应 Agent。

Sealos 模板会以 Kubernetes StatefulSet 运行 Paperclip。KubeBlocks 会创建 PostgreSQL 保存应用数据，持久卷会保存 Paperclip home 数据、本地加密密钥、工作区、日志和本地文件存储。启用 `use_object_storage` 时，Paperclip 会把附件和公司资产保存到 S3 兼容对象存储。

Sealos 会负责公网 HTTPS 访问、数据库创建、持久化存储、资源配置和应用入口管理。

## 常见使用场景

- **AI 团队运营**：创建公司、分配 Agent，并在项目中协同工作。
- **Issue 与审批流程**：跟踪任务、评论、审批和执行历史。
- **编码 Agent 中心**：从同一个 Web UI 运行 Codex、Claude、OpenCode 或 Gemini Agent。
- **插件平台**：安装和管理 Paperclip 插件及插件健康状态。
- **私有 Agent 工作区**：在 Sealos 托管部署中保存工作区数据和密钥。

## Paperclip 托管依赖

本 Sealos 模板包含以下运行依赖：

- Paperclip 镜像 `ghcr.io/paperclipai/paperclip:sha-b8725c5`
- 通过 KubeBlocks 部署的 PostgreSQL `16.4.0`
- 挂载到 `/paperclip` 的持久化存储
- 用于附件和资产的可选 S3 兼容对象存储
- HTTPS Ingress 和 Sealos App 入口

### 部署依赖

- [Paperclip 官方网站](https://paperclip.ing) - 产品主页
- [Paperclip 官方文档](https://paperclip.ing/docs) - 官方文档
- [Paperclip GitHub 仓库](https://github.com/paperclipai/paperclip) - 源码和版本发布
- [Paperclip Docker 指南](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/docker.md) - Docker 部署参考
- [Paperclip 数据库指南](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/database.md) - PostgreSQL 配置参考
- [Paperclip 存储指南](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/storage.md) - 本地磁盘与 S3 存储参考

## 实现细节

**架构组件：**

- **Paperclip StatefulSet**：使用 `ghcr.io/paperclipai/paperclip:sha-b8725c5` 镜像运行，监听 `3100` 端口。
- **PostgreSQL Cluster**：存储用户、公司、Issue、审批、插件状态和运行时元数据。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `paperclip` 数据库。
- **Paperclip 配置 Init Container**：写入 `/paperclip/instances/default/config.json` 并设置 Agent JWT secret。
- **Paperclip 持久卷**：保存 `/paperclip` 数据、本地密钥、日志、工作区和本地存储。
- **可选 ObjectStorageBucket**：通过 `PAPERCLIP_STORAGE_PROVIDER=s3` 启用 S3 存储。
- **Service、Ingress 和 App Resource**：通过公网 HTTPS 地址暴露 Paperclip。

**配置：**

模板以 `authenticated` 部署模式和 `public` 暴露模式运行 Paperclip，并将 `PAPERCLIP_PUBLIC_URL`、`PAPERCLIP_AUTH_PUBLIC_BASE_URL` 和允许访问的 hostname 设置为 Sealos 公网地址。

模板会在启动阶段写入 Paperclip 首次配置。应用健康后，打开 Paperclip StatefulSet 终端并运行下面的 bootstrap 命令生成首个 CEO 邀请。打开输出的 `Invite URL`，点击 **Sign in / Create account**，创建第一个用户，再回到邀请页点击 **Accept bootstrap invite**。bootstrap 完成后，已登录用户会进入创建第一个公司的 onboarding 流程。

```bash
node cli/node_modules/tsx/dist/cli.mjs cli/src/index.ts auth bootstrap-ceo \
  --config "$PAPERCLIP_CONFIG" \
  --base-url "$PAPERCLIP_PUBLIC_URL" \
  --expires-hours 72
```

部署时可配置可选模型供应商密钥：

- `openai_api_key`：用于 Codex 和 OpenAI 后端 Agent。
- `anthropic_api_key`：用于 Claude 后端 Agent。
- `gemini_api_key`：用于 Gemini 后端 Agent。

对象存储有两种模式：

- **本地存储**：默认模式。Paperclip 将文件保存到 `/paperclip/instances/default/data/storage`。
- **S3 存储**：启用 `use_object_storage` 后创建 S3 兼容存储桶，并配置 `PAPERCLIP_STORAGE_S3_*`。

**默认资源：**

- App CPU limit：`500m`
- App Memory limit：`512Mi`
- PostgreSQL CPU limit：`500m`
- PostgreSQL Memory limit：`512Mi`

**健康检查：**

Paperclip 暴露 `/api/health`。模板使用该端点作为启动、就绪和存活探针。live QA 还需要完成首个用户注册，并打开至少一个公司或 Issue 工作流。

**许可信息：**

Paperclip 使用 MIT License。

## 为什么在 Sealos 上部署 Paperclip？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统，统一应用部署、存储、网络和运维。在 Sealos 上部署 Paperclip 可以获得：

- **一键部署**：通过一个模板部署 Paperclip、PostgreSQL、存储和 HTTPS 访问。
- **持久化 Agent 工作区**：本地密钥、日志、工作区文件和应用状态可在重启后保留。
- **可选对象存储**：将附件和公司资产迁移到 S3 兼容存储。
- **即时公网访问**：Sealos 自动分配公网 HTTPS 入口。
- **易于自定义**：可在 Sealos Canvas 调整 API key、资源和存储。
- **AI 辅助运维**：可通过 Sealos AI 对话或资源卡片修改部署。

## 部署指南

1. 打开 [Paperclip 模板](https://sealos.io/products/app-store/paperclip)，点击 **Deploy Now**。
2. 配置部署参数：
   - **use_object_storage**：启用后将附件和资产保存到 S3 兼容对象存储。
   - **openai_api_key**：用于 OpenAI 后端 Agent 的可选密钥。
   - **anthropic_api_key**：用于 Claude 后端 Agent 的可选密钥。
   - **gemini_api_key**：用于 Gemini 后端 Agent 的可选密钥。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会进入 Canvas。后续如需修改配置，可以在对话框中描述需求，让 AI 自动应用变更；也可以点击对应资源卡片手动调整设置。
4. 通过提供的 URL 访问 Paperclip：
   - **首个管理员**：打开 Paperclip StatefulSet 终端，运行配置章节中的 bootstrap 命令，然后复制生成的 `Invite URL`。
   - **Paperclip Web UI**：打开邀请链接，创建第一个账号，接受 bootstrap 邀请，然后完成 onboarding。
   - **Paperclip API**：使用同一公网地址访问 `/api/*` 路径。

## 配置

部署后可通过以下方式配置 Paperclip：

- **Web UI**：管理公司、Agent、Issue、插件、密钥和审批。
- **环境变量**：通过 StatefulSet 资源卡片新增或轮换供应商 API key。
- **存储设置**：部署时选择本地存储或 S3 兼容存储。
- **资源卡片**：在 Canvas 调整 CPU、内存、持久卷大小或 Ingress 设置。

## 故障排查

### 健康检查显示 bootstrap pending

- **原因**：Paperclip 正在等待第一个管理员账号和 bootstrap 流程。
- **解决方法**：打开 Paperclip StatefulSet 终端，运行配置章节中的 bootstrap 命令，通过输出的邀请链接创建第一个账号，并点击 **Accept bootstrap invite**。

### Agent 运行失败并提示缺少凭据

- **原因**：选中的本地 Agent CLI 需要模型供应商 API key。
- **解决方法**：通过部署参数或 StatefulSet 环境变量添加 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 或 `GEMINI_API_KEY`。

### 文件上传失败

- **原因**：本地存储权限或 S3 凭据不完整。
- **解决方法**：保留模板中的 `/paperclip` 持久卷和权限初始化容器。启用对象存储时，确认 ObjectStorageBucket 和对象存储密钥已经创建。

## 更多资源

- [Paperclip 官方网站](https://paperclip.ing)
- [Paperclip 官方文档](https://paperclip.ing/docs)
- [Paperclip GitHub 仓库](https://github.com/paperclipai/paperclip)
- [Paperclip Docker 指南](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/docker.md)
- [Sealos 上的 Paperclip 模板](https://sealos.io/products/app-store/paperclip)

## 许可证

本 Sealos 模板提供在 Sealos 上运行 Paperclip 的部署配置。Paperclip 本身使用 MIT License。
