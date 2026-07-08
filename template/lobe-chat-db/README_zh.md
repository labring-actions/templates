# 在 Sealos 上部署和托管 Lobe Chat 数据库版

Lobe Chat 数据库版是一款带服务端持久化能力的开源 LLM 聊天界面。本模板会在 Sealos Cloud 上部署 Lobe Chat、PostgreSQL 和 Sealos 托管的 S3 兼容对象存储。

![Lobe Chat 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/lobe-chat-db/website-screenshot.webp)

## 关于托管 Lobe Chat 数据库版

Lobe Chat 提供精致的 Web 界面，用于使用 OpenAI 兼容模型、多模态对话、助手工作流和共享团队状态。数据库版将应用数据存储在 PostgreSQL 中，适合需要账号登录、多设备同步和服务端持久化的场景。

此 Sealos 模板会创建 Lobe Chat 数据库版镜像、由 Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0` 集群、用于创建 `lobechat` 数据库的幂等初始化 Job、私有 ObjectStorageBucket、Service、Ingress 和 Sealos App 入口。Logto 作为独立身份服务使用，因为 Lobe Chat 部署时需要 OAuth Client ID、Client Secret 和 Issuer URL。

## 常见使用场景

- **个人 AI 工作台**：运行带持久化历史记录的私有聊天界面，并接入 OpenAI 兼容模型。
- **团队 AI 入口**：为团队成员提供带登录能力的统一入口，并由 PostgreSQL 保存状态。
- **多模态助手界面**：通过 S3 兼容对象存储保存图片和生成资产。
- **LLM 产品原型**：在接入更大系统前测试提示词、智能体和工作流。

## Lobe Chat 数据库版托管依赖

Sealos 模板包含运行容器、PostgreSQL、对象存储、Kubernetes Service、Ingress 和 App 入口。部署 Lobe Chat 前需要先准备 Logto 应用，因为模板需要 Logto OAuth 凭证。

### 部署依赖

- [Lobe Chat 文档](https://lobehub.com/docs) - 官方产品和自托管文档
- [Lobe Chat GitHub 仓库](https://github.com/lobehub/lobe-chat) - 源码和发布记录
- [Logto 文档](https://docs.logto.io/) - 身份提供方和应用配置
- [Sealos 应用商店](https://sealos.io/products/app-store/lobe-chat-db) - 一键部署入口

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Lobe Chat**：Web 应用容器，通过 `3210` 端口提供聊天 UI 和 API。
- **PostgreSQL**：Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0`，用于保存账号、会话、设置和应用元数据。
- **PostgreSQL 初始化 Job**：等待 PostgreSQL 就绪后创建 `lobechat` 数据库，数据库已存在时会正常退出。
- **对象存储**：Sealos 托管的私有 ObjectStorageBucket，通过 S3 兼容环境变量注入应用。
- **Ingress 和 App 入口**：为 Lobe Chat UI 提供公开 HTTPS 路由和 Sealos 控制台入口。
- **Logto**：独立部署的身份提供方，用于注册和登录。

**配置：**

模板会通过 Kubeblocks Secret 字段组合 `DATABASE_URL`，并从 Sealos 对象存储 Secret 注入 S3 凭证。Sealos 托管 ObjectStorageBucket 是此模板的默认存储路径。高级运维场景可以在部署后参考 Lobe Chat 官方 S3 文档评估外部 S3 迁移方案。

**许可证信息：**

Lobe Chat 使用 Apache-2.0 许可证发布。此 Sealos 模板作为 Sealos 模板仓库中的部署配置提供。

## 为什么在 Sealos 上部署 Lobe Chat 数据库版？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、存储、网络和生命周期管理。在 Sealos 上部署 Lobe Chat 数据库版，你可以获得：

- **一键部署**：从应用商店部署 Lobe Chat，无需手写 Kubernetes YAML。
- **托管数据库和存储**：模板会同时创建 PostgreSQL 和 S3 兼容对象存储。
- **即时公网访问**：Ingress 会自动提供 HTTPS 访问地址。
- **Canvas 运维**：部署后可通过 Canvas、AI 对话框和资源卡片调整资源或环境变量。
- **资源效率**：按量使用资源，适合小团队和原型项目运行数据库版。

## 部署前准备

先准备 Logto：

1. 打开 [Logto 模板](https://sealos.io/products/app-store/logto)，点击 **Deploy Now**。
2. 等待 Logto 部署完成，然后打开 Logto 控制台 URL。
3. 注册第一个 Logto 管理员账号。
4. 在 Logto 中创建新应用，应用类型选择 **Next.js (App Router)**。
5. 复制 Logto Client ID 和 Client Secret，并将 Logto OpenID Connect issuer 填入 `AUTH_LOGTO_ISSUER`。issuer 通常带 `/oidc` 后缀，例如 `https://<your-logto-domain>/oidc`。

## 部署指南

1. 打开 [Lobe Chat 数据库版模板](https://sealos.io/products/app-store/lobe-chat-db)，点击 **Deploy Now**。
2. 配置必填的 Logto 参数：
   - `AUTH_LOGTO_ID`：Logto 应用 Client ID
   - `AUTH_LOGTO_SECRET`：Logto 应用 Client Secret
   - `AUTH_LOGTO_ISSUER`：Logto OpenID Connect issuer，通常是 `https://<your-logto-domain>/oidc`
3. 按需配置 OpenAI 兼容模型访问：
   - `OPENAI_API_KEY`
   - `OPENAI_PROXY_URL`
   - `OPENAI_MODEL_LIST`
   - `ACCESS_CODE`
4. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续修改可以在 AI 对话框中描述需求，或点击相关资源卡片调整设置。
5. 从 Canvas 复制 Lobe Chat 公网 URL。

## Logto 回调配置

Lobe Chat 获得公网 URL 后，回到 Logto 应用设置并添加以下 URL：

- Redirect URI：`https://<your-lobe-chat-domain>/api/auth/callback/logto`
- Post sign-out redirect URI：`https://<your-lobe-chat-domain>`

保存 Logto 设置后，打开 Lobe Chat 公网 URL，点击账号头像，选择 **Log in / Sign up**，然后通过 Logto 注册或登录。

## 扩展

扩展部署：

1. 打开 Lobe Chat 部署所在的 Canvas。
2. 点击 Lobe Chat Deployment 或 PostgreSQL 资源卡片。
3. 调整 CPU、内存、存储或副本数。
4. 在对话框中应用变更，并等待资源就绪。

## 故障排查

### Logto 登录失败

- 原因：Redirect URI 或 Post sign-out redirect URI 缺失，或域名与 Lobe Chat 公网地址不一致。
- 解决方案：重新打开 Logto 应用设置，保存上方列出的精确回调 URL。

### 模型请求失败

- 原因：`OPENAI_API_KEY`、`OPENAI_PROXY_URL` 或 `OPENAI_MODEL_LIST` 与模型服务商配置不匹配。
- 解决方案：通过 Canvas 更新这些值，然后重启 Lobe Chat Deployment。

### 上传失败

- 原因：部署后对象存储配置被拆散或改动。
- 解决方案：保持 Sealos 托管 ObjectStorageBucket 和注入的 S3 环境变量一起使用。

## 更多资源

- [Lobe Chat 自托管指南](https://lobehub.com/docs/self-hosting/start)
- [Lobe Chat 环境变量](https://lobehub.com/docs/self-hosting/environment-variables)
- [Logto Applications](https://docs.logto.io/docs/recipes/integrate-logto/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证提供。Lobe Chat 使用 Apache-2.0 许可证。
