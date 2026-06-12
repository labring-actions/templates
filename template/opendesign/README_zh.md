# 在 Sealos 上部署和托管 OpenDesign

OpenDesign 是一个本地优先的开源 AI 设计工作区，可用于生成原型、仪表盘、演示文稿、图片、视频和基于设计系统的可交付产物。此模板会在 Sealos 上以单个持久化服务部署官方 OpenDesign Docker 运行时。

![OpenDesign 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/opendesign/website-screenshot.webp)

## 关于 OpenDesign 托管

OpenDesign 提供由本地 daemon 支撑的浏览器工作区。daemon 会在同一个容器内提供 Web UI、API 路由、项目文件、插件数据和生成产物。此 Sealos 模板会将 OpenDesign 工作区持久化到 `/app/.od`，确保项目、会话、媒体配置和生成结果在重启后仍然保留。

上游 Docker 部署默认暴露 `7456` 端口，并把运行时数据保存到 `/app/.od`。当 daemon 绑定到公网接口时，上游要求配置 API Token。此 Sealos 模板采用上游云部署模式，在 OpenDesign 前运行 Nginx 代理：Nginx 对外暴露 `8080`，再转发到 `7456` 端口的 OpenDesign 服务，并为 `/api` 路由注入内部 bearer token。

## 常见使用场景

- **AI 设计工作区**：基于提示词和设计系统上下文生成 Web、桌面和移动端原型。
- **演示文稿与设计产物生成**：生成 Deck、实时仪表盘、HTML 产物、PDF 和可导出的设计输出。
- **设计系统实验**：在持久化工作区中尝试设计系统、插件和可复用工作流。
- **智能体辅助交付**：先在 OpenDesign 中形成可视化产物，再交给编码智能体或编辑器继续生产化。

## OpenDesign 托管依赖

此 Sealos 模板把运行时依赖都包含在 OpenDesign Docker 镜像中，并为工作区数据创建持久化存储。

### 部署依赖

- [官方网站](https://open-design.ai/) - 产品网站和下载入口
- [源码仓库](https://github.com/nexu-io/open-design) - OpenDesign 源代码
- [Docker 部署指南](https://github.com/nexu-io/open-design/blob/main/deploy/README.md) - 上游 Docker 部署说明
- [Docker 镜像](https://hub.docker.com/r/vanjayak/open-design) - 已发布的 OpenDesign 容器镜像

### 实现细节

**架构组件：**

- **OpenDesign Runtime**：在 `7456` 端口提供 Web UI 和 daemon API 的主容器。
- **Nginx Proxy**：公网入口，监听 `8080`，并在转发 API 请求时注入生成的 bearer token。
- **持久化工作区卷**：保存 `/app/.od`，包含项目、会话、生成产物和本地配置。
- **Ingress 与应用入口**：通过 Sealos 生成的域名暴露 OpenDesign Web 界面。

**配置：**

- 镜像使用 digest 固定，避免 mutable `latest` 漂移。
- `OD_BIND_HOST=0.0.0.0`、`OD_PORT=7456`、`OD_WEB_PORT=7456` 和生成的 `OD_API_TOKEN` 与上游云端运行要求保持一致。
- `OD_ALLOWED_ORIGINS` 会设置为 Sealos 生成的 HTTPS 域名，让 OpenDesign 在 Ingress 后接受同源浏览器请求。
- Nginx 会为 `/api/` 请求注入 `Authorization: Bearer <生成的 token>`，因此浏览器通过 Sealos 公网域名访问时 API 调用仍可正常工作。
- 代理会保留浏览器访问域名对应的 Host 与转发头，因此同源浏览器请求可以通过 Sealos 域名访问 daemon。
- OpenDesign 上游 Docker 指南提示，远程部署应放在认证反向代理、SSH 隧道、VPN 或等效访问层之后。此模板会保护 daemon API token 不直接暴露给浏览器，但不会给 Web UI 增加终端用户登录。不要在未增加访问控制的情况下把它当作安全的多人公网服务。

**许可证信息：**

OpenDesign 使用 Apache-2.0 许可证。

## 为什么在 Sealos 上部署 OpenDesign？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一了从云端开发到生产部署和管理的完整应用生命周期。在 Sealos 上部署 OpenDesign 可以获得：

- **一键部署**：无需手写 Kubernetes YAML 即可部署 OpenDesign。
- **内置持久化存储**：工作区文件和生成产物在容器重启后仍然保留。
- **即时 HTTPS 访问**：每次部署都会获得自动生成的 HTTPS 入口。
- **易于自定义**：可在 Sealos 中配置允许来源、资源、存储和网络。
- **无需 Kubernetes 专业经验**：直接使用 Kubernetes 托管能力，而不用手动管理底层资源。

## 部署指南

1. 打开 [OpenDesign 模板](https://sealos.io/products/app-store/opendesign)，点击 **Deploy Now**。
2. 检查默认资源和存储配置。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 从 Canvas 或应用列表打开 OpenDesign 应用入口。

OpenDesign 不会创建由模板管理的管理员账号，也没有默认登录页。部署后的应用会直接进入工作区，你可以在 OpenDesign 内配置 BYOK 模型提供商、插件、设计系统和本地工作区设置。

此模板已按最小运行资源完成测试：OpenDesign 主容器请求 `20m` CPU 和 `128Mi` 内存，代理容器请求 `20m` CPU 和 `25Mi` 内存，并使用 `1Gi` 持久化工作区卷。如果你会生成大型媒体资源，或在同一个工作区保留大量项目，建议增加内存或存储。

## 配置

部署后，你可以通过以下方式配置 OpenDesign：

- **AI 对话框**：描述需要调整的内容，例如扩大存储、增加内存或调整访问控制。
- **资源卡片**：在 Canvas 中修改 StatefulSet、Service、Ingress 或持久化卷。
- **OpenDesign UI**：在 OpenDesign 内配置 BYOK 模型提供商、插件、设计系统和工作区设置。

## 扩缩容

OpenDesign 会把本地工作区状态保存在单个持久化卷中，因此除非你已经验证过自己的多副本存储和会话策略，否则应保持单副本运行。

提升容量：

1. 打开该部署的 Canvas。
2. 点击 OpenDesign StatefulSet 资源卡片。
3. 增加 CPU、内存或持久化存储。
4. 应用修改。

## 故障排查

### 应用已启动但 API 调用失败

此模板使用 Nginx 代理为 `/api/` 路由注入生成的 API token。如果 API 调用失败，请确认代理 Deployment 正在运行，并且仍然挂载了生成的 Nginx 配置。

### 重启后生成文件消失

确认 StatefulSet 仍然把持久化卷挂载到 `/app/.od`。工作区数据保存在该目录。

### 获取帮助

- [OpenDesign GitHub Issues](https://github.com/nexu-io/open-design/issues)
- [OpenDesign Discussions](https://github.com/nexu-io/open-design/discussions)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [OpenDesign README](https://github.com/nexu-io/open-design/blob/main/README.md)
- [OpenDesign Docker 部署](https://github.com/nexu-io/open-design/blob/main/deploy/README.md)
- [OpenDesign Releases](https://github.com/nexu-io/open-design/releases)

## 许可证

OpenDesign 使用 Apache-2.0 许可证分发。最新许可证和第三方声明请以其上游仓库为准。
