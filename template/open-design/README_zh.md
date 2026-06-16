# 在 Sealos 上部署和托管 Open Design

Open Design 是一个本地优先的开源 AI 设计工作区，可生成原型、演示文稿、图片、视频和基于设计系统的可交付产物。此模板会在 Sealos Cloud 上部署 Open Design，并提供持久化工作区卷与 Nginx API 代理。

![Open Design 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/open-design/website-screenshot.webp)

## 关于 Open Design 托管

Open Design 提供由本地 daemon 支撑的浏览器工作区。daemon 会在同一个容器内提供 Web UI、API 路由、项目文件、插件数据和生成产物。部署到 Sealos 后，工作区会持久化到 `/app/.od`，项目、会话、媒体配置和生成结果在重启后仍然保留。

上游 Docker 部署暴露 `7456` 端口，使用 Docker volume 保存运行数据，并在 daemon 绑定公网接口时要求配置 `OD_API_TOKEN`。此模板会在 Open Design 前面运行 Nginx 代理：Nginx 对外暴露 `8080`，将流量转发到 `7456` 端口的 Open Design 服务，并为 `/api` 路由注入内部 bearer token。

## 常见使用场景

- **AI 设计工作区**：基于提示词和设计系统上下文生成 Web、桌面和移动端原型。
- **演示文稿与设计产物生成**：生成 Deck、实时仪表盘、HTML 产物、PDF 和可导出的设计输出。
- **设计系统实验**：在持久化工作区中尝试设计系统、插件和可复用工作流。
- **智能体辅助交付**：先在 Open Design 中形成可视化产物，再交给编码智能体或编辑器继续生产化。

## Open Design 托管依赖

此 Sealos 模板包含 Open Design 运行镜像、轻量 Nginx 代理、公网 HTTPS Ingress 和持久化工作区存储。上游 Docker 部署路径无需 PostgreSQL、MySQL、Redis、SQLite 配置，也无需 S3 兼容对象存储。

### 部署依赖

- [官方网站](https://open-design.ai/) - 产品网站和下载入口
- [源码仓库](https://github.com/nexu-io/open-design) - Open Design 源代码
- [Docker 部署指南](https://github.com/nexu-io/open-design/blob/main/deploy/README.md) - 上游 Docker 部署说明
- [Docker 镜像](https://hub.docker.com/r/vanjayak/open-design) - 已发布的 Open Design 容器镜像

### 实现细节

**架构组件：**

- **Open Design Runtime**：StatefulSet，在 `7456` 端口提供 Web UI 和 daemon API。
- **Nginx Proxy**：公网入口，监听 `8080`，并在转发 API 请求时注入生成的 bearer token。
- **持久化工作区卷**：保存 `/app/.od`，包含项目、会话、生成产物和本地配置。
- **Ingress 与应用入口**：通过 Sealos 生成的域名暴露 Open Design Web 界面。

**配置：**

- Open Design 镜像使用 digest 固定，避免 mutable `latest` 漂移。
- `OD_BIND_HOST=0.0.0.0`、`OD_PORT=7456`、`OD_WEB_PORT=7456` 和生成的 `OD_API_TOKEN` 与上游云端运行要求保持一致。
- `OD_ALLOWED_ORIGINS` 会设置为 Sealos 生成的 HTTPS 域名，让浏览器请求在 Ingress 后正常通过。
- Nginx 会为 `/api/` 请求注入 `Authorization: Bearer <generated token>`，因此浏览器通过 Sealos 公网域名访问时 API 调用仍可正常工作。
- Open Design 上游 Docker 指南建议在共享公网部署前增加认证反向代理、SSH 隧道、VPN 或等效访问层。此模板会在内部保护 daemon API token，最终用户访问控制由你的部署策略决定。

**许可证信息：**

Open Design 使用 Apache-2.0 许可证。

## 为什么在 Sealos 上部署 Open Design？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一了从云端开发到生产部署和管理的完整应用生命周期。在 Sealos 上部署 Open Design 可以获得：

- **一键部署**：无需手写 Kubernetes YAML 即可部署 Open Design。
- **内置持久化存储**：工作区文件和生成产物在容器重启后仍然保留。
- **即时公网访问**：每次部署都会获得自动生成的 HTTPS 入口。
- **易于自定义**：可在 Canvas 中配置允许来源、资源、存储和网络。
- **按量使用资源**：先用小规格启动，工作区增长后再增加 CPU、内存或存储。
- **无需 Kubernetes 专业经验**：直接使用 Kubernetes 托管能力，同时减少底层资源管理成本。

## 部署指南

1. 打开 [Open Design 模板](https://sealos.io/products/app-store/open-design)，点击 **Deploy Now**。
2. 检查默认资源和存储配置。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续调整可以在 AI 对话框中描述需求，也可以点击相关资源卡片修改配置。
4. 从 Canvas 或应用列表打开 Open Design 应用入口。

Open Design 不会创建由模板管理的管理员账号，也没有默认登录页。首次打开时，应用可能显示 onboarding 页面；选择运行方式，或点击 **Skip** 直接进入工作区。进入工作区后，可以在 Open Design 内配置 BYOK 模型提供商、插件、设计系统和本地工作区设置。

此模板已在 Sealos 完成线上测试：Open Design 主容器使用 `100m` CPU / `256Mi` 内存，Nginx 代理使用 `100m` CPU / `128Mi` 内存，并配置 `1Gi` 持久化工作区卷。Smoke test 期间，Open Design 主容器约使用 `30m` CPU 和 `67Mi` 内存，代理约使用 `1m` CPU 和 `22Mi` 内存。

## 配置

部署后，你可以通过以下方式配置 Open Design：

- **AI 对话框**：描述需要调整的内容，例如扩大存储、增加内存或调整访问控制。
- **资源卡片**：在 Canvas 中修改 StatefulSet、代理 Deployment、Service、Ingress 或持久化卷。
- **Open Design UI**：在 Open Design 内配置 BYOK 模型提供商、插件、设计系统和工作区设置。

## 扩缩容

Open Design 会把本地工作区状态保存在单个持久化卷中，因此建议保持单副本运行。多副本部署需要先验证存储和会话策略。

提升容量：

1. 打开该部署的 Canvas。
2. 点击 Open Design StatefulSet 资源卡片。
3. 增加 CPU、内存或持久化存储。
4. 应用修改。

## 故障排查

### 应用已启动但 API 调用失败

此模板使用 Nginx 代理为 `/api/` 路由注入生成的 API token。如果 API 调用失败，请确认代理 Deployment 正在运行，并且仍然挂载了生成的 Nginx 配置。

### 出现 onboarding 页面

Open Design 首次启动会显示 onboarding。选择运行方式，或点击 **Skip** 进入工作区，然后在 UI 中配置模型提供商和插件。

### 重启后生成文件消失

确认 StatefulSet 仍然把持久化卷挂载到 `/app/.od`。工作区数据保存在该目录。

### 获取帮助

- [Open Design GitHub Issues](https://github.com/nexu-io/open-design/issues)
- [Open Design Discussions](https://github.com/nexu-io/open-design/discussions)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Open Design README](https://github.com/nexu-io/open-design/blob/main/README.md)
- [Open Design Docker 部署](https://github.com/nexu-io/open-design/blob/main/deploy/README.md)
- [Open Design Releases](https://github.com/nexu-io/open-design/releases)

## 许可证

此 Sealos 模板遵循仓库许可证。Open Design 使用 Apache-2.0 许可证分发。
