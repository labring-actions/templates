# 在 Sealos 上部署和托管 DocuSeal

DocuSeal 是一个开源平台，可在线创建、填写和签署 PDF 表单。此模板会在 Sealos Cloud 上部署 DocuSeal，并配套 PostgreSQL、持久化文件存储和公开 HTTPS 访问入口。

![DocuSeal 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/docuseal/website-screenshot.webp)

## 关于托管 DocuSeal

DocuSeal 提供一套自托管文档流程，用于上传 PDF、添加可填写字段、收集签名并管理已完成的提交记录。对于希望把电子签名数据保留在自有部署环境中的团队，它很适合用于搭建可控的签署系统。

此 Sealos 模板会将 DocuSeal 作为单个 Web 服务运行，并创建一个 Kubeblocks PostgreSQL 数据库存储应用数据。上传的文档和生成的文件会保存在挂载到 `/data/docuseal` 的持久化卷中，重启或滚动更新后仍会保留。

Sealos 会自动配置公网 HTTPS 路由、服务发现、持久化存储和资源限制。模板还会把 DocuSeal 的公开 `APP_URL` 设置为生成的 Sealos 域名，因此初始化页面、邮件链接、Webhook URL 和 Open Graph 元数据都会使用正确的外部地址。

## 常见使用场景

- **内部文件审批**：准备 PDF 表单，收集员工、外包人员或合作伙伴的签名。
- **客户协议签署**：发送服务协议、入驻文件和授权表单，让客户在线签署。
- **运营纸质流程数字化**：将交接单、检查清单、确认书等高频文件转成在线流程。
- **API 驱动的签署流程**：使用 DocuSeal API 和 Webhook，把文件签署能力接入已有产品。
- **自托管电子签名系统**：把签署数据和文件保存在自己的 Sealos 工作区，而不只依赖托管 SaaS 账号。

## DocuSeal 托管依赖

此 Sealos 模板包含运行所需的组件：DocuSeal 容器镜像、PostgreSQL `postgresql-16.4.0` 数据库、用于创建 `docuseal` 数据库的初始化 Job、应用持久化存储、Kubernetes Service、Ingress 和 Sealos App 入口。

### 部署依赖

- [DocuSeal 官网](https://www.docuseal.com/) - 产品概览和官方云服务
- [DocuSeal GitHub 仓库](https://github.com/docusealco/docuseal) - 源码、Docker 镜像和版本发布记录
- [DocuSeal 文档](https://www.docuseal.com/docs) - 产品与集成文档
- [DocuSeal API 参考](https://www.docuseal.com/docs/api) - 自动化和集成所需的 API 端点

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **DocuSeal Web 服务**：运行 `docuseal/docuseal:3.0.1`，监听 `3000` 端口，提供 Web UI、API、嵌入式签署页面和后台任务。
- **PostgreSQL**：由 Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0`，用于存储用户、账号、模板、提交记录和应用元数据。
- **PostgreSQL 初始化 Job**：在 PostgreSQL 就绪后，以幂等方式创建 `docuseal` 数据库。
- **持久化存储**：挂载到 `/data/docuseal` 的 `1Gi` 卷，用于保存 DocuSeal 运行文件和上传附件。
- **Ingress 与 App 入口**：Sealos 暴露 HTTPS 访问域名，并在仪表盘中创建应用入口。

**配置：**

模板会自动配置：

- `APP_URL` 为 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。
- `HOST` 为生成的 Sealos 主机名。
- `FORCE_SSL=true`，让 DocuSeal 按 HTTPS 公网路由运行。
- `SECRET_KEY_BASE` 为自动生成的密钥。
- `DATABASE_URL` 来自 Kubeblocks PostgreSQL 连接 Secret。

部署时不需要填写必填参数。SMTP、对象存储、SSO 或许可证相关设置可在部署后通过 DocuSeal UI 配置，也可以在 Sealos Canvas 中编辑工作负载环境变量。

**许可证信息：**

DocuSeal 使用 AGPLv3 License，并附带 DocuSeal LLC 的额外条款。此 Sealos 模板只是 DocuSeal 的部署配置，不改变上游应用许可证。

## 为什么在 Sealos 上部署 DocuSeal？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖从云端开发到生产部署和运维管理的完整应用生命周期。在 Sealos 上部署 DocuSeal 可以获得：

- **一键部署**：通过一个模板同时部署 DocuSeal、PostgreSQL、存储、网络和仪表盘入口。
- **无需 Kubernetes 经验**：不用手写清单，也能获得 Kubernetes 的可靠性。
- **内置持久化存储**：上传文档、生成文件和数据库数据会在重启后保留。
- **即时公网访问**：每次部署都会获得 HTTPS URL，可用于初始化、签署页面和 API 回调。
- **易于自定义**：可通过 Sealos Canvas 和 AI 对话调整环境变量、资源和存储。
- **按量使用资源**：从紧凑资源配置起步，随着签署业务增长再扩容。

在 Sealos 上部署 DocuSeal，可以把精力放在文档流程本身，而不是基础设施维护上。

## 部署指南

1. 打开 [DocuSeal 模板](https://sealos.run/products/app-store/docuseal)，点击 **Deploy Now**。
2. 除非需要自定义生成名称或访问域名，否则保留默认参数即可。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话框中描述需求，或点击对应资源卡片调整配置。
4. 从 App 入口打开生成的 DocuSeal URL。
5. 完成首次初始化表单：
   - 输入首个管理员的名字和姓氏。
   - 输入管理员邮箱地址。
   - 输入公司或工作区名称。
   - 设置管理员密码。
   - App URL 字段保持生成的 Sealos HTTPS URL；除非你已经配置了自定义域名。
   - 选择界面语言并提交表单。
6. 初始化完成后，后续可在登录页使用同一个邮箱和密码登录。

## 配置

部署后，你可以通过以下方式配置 DocuSeal：

- **初始化页面**：创建首个管理员账号，并保存公开 App URL。
- **DocuSeal 账号设置**：管理用户、品牌、签署偏好、Webhook、API Token 和账号级选项。
- **Sealos AI 对话**：描述环境变量或资源调整需求，让 AI 协助修改。
- **资源卡片**：在 Canvas 中点击 StatefulSet、PostgreSQL、Ingress 或存储卡片，查看并调整配置。

如果需要发送站内邀请或签署邮件，请先配置 SMTP 相关环境变量。若后续修改公网域名，也应在 DocuSeal 账号设置中同步更新 App URL，确保生成的签署链接继续使用正确主机名。

## 扩展

在 Sealos 上扩展 DocuSeal：

1. 打开 DocuSeal 部署对应的 Canvas。
2. 点击 DocuSeal StatefulSet 资源卡片。
3. 当大 PDF、频繁上传或高签署流量需要更多容量时，提高 CPU 或内存资源。
4. 应用变更并等待 Pod 重新就绪。

默认模板使用适合评估和轻量使用的紧凑资源配置。若用于更重的生产工作负载，请提高应用资源，并考虑为大量附件启用外部对象存储。

## 故障排查

### 应用打开后进入初始化页面

这是新部署的正常行为。请在初始化页面创建首个管理员账号。首个用户创建后，未登录访问会跳转到登录页。

### 生成链接使用了错误域名

进入 DocuSeal 账号设置，将 App URL 更新为当前 Sealos HTTPS URL 或你的自定义域名。模板会为新部署自动设置 `APP_URL`，但手动更换域名后，也需要在 DocuSeal 内同步更新。

### 邀请邮件或签署邮件无法发送

DocuSeal 需要 SMTP 配置才能发送外部邮件。请在 StatefulSet 资源卡片中添加所需 SMTP 环境变量，重启工作负载，然后在 DocuSeal 设置中测试邮件发送。

### 获取帮助

- [DocuSeal 文档](https://www.docuseal.com/docs)
- [DocuSeal GitHub Issues](https://github.com/docusealco/docuseal/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [DocuSeal API 参考](https://www.docuseal.com/docs/api)
- [DocuSeal Docker 镜像](https://hub.docker.com/r/docuseal/docuseal)
- [DocuSeal GitHub Releases](https://github.com/docusealco/docuseal/releases)

## 许可证

此 Sealos 模板遵循仓库中的模板许可证。DocuSeal 本身使用 AGPLv3，并附带 DocuSeal LLC 的额外条款。
