# 在 Sealos 上部署和托管 copyparty

copyparty 是一个便携式文件服务器，支持浏览器上传、下载、媒体索引、缩略图和共享权限控制。此模板在 Sealos Cloud 上部署带持久化存储的 copyparty。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/copyparty/website-screenshot.webp)

## 关于托管 copyparty

copyparty 作为单个 Web 服务运行，使用官方 `copyparty/ac` 镜像，该镜像包含 FFmpeg 和媒体缩略图支持。Sealos 模板会为共享文件、配置和运行状态创建持久化卷，确保上传内容和索引在重启后保留。

部署会通过自动管理的 HTTPS 域名暴露浏览器界面。模板会使用部署时设置的密码创建 `admin` 账号，默认共享的 `/w` 卷对该账号开放写入权限。

## 常见使用场景

- **私有文件投递**：通过浏览器接收可信用户上传的文件。
- **媒体浏览**：浏览上传的音频、视频和图片文件，并显示缩略图。
- **团队文件共享**：为小团队托管轻量级共享文件区。
- **临时传输中心**：创建带持久化存储的短期文件传输服务。

## copyparty 托管依赖

Sealos 模板包含 copyparty 应用容器和持久化存储卷。

### 部署依赖

- [copyparty GitHub 仓库](https://github.com/9001/copyparty) - 源码和文档
- [Docker 使用指南](https://github.com/9001/copyparty/tree/v1.20.16/scripts/docker) - 官方容器说明
- [copyparty CLI 帮助](https://copyparty.eu/cli/) - 账号、卷和权限选项

### 实现细节

**架构组件：**

此模板部署一个服务：

- **copyparty**：监听 `3923` 端口的 Web 文件服务器
- **持久化存储**：挂载到 `/w`、`/cfg` 和 `/state` 的存储卷

**配置：**

- 默认账号为 `admin`。
- 部署时设置 `admin_password`，并保存该值用于登录。
- 上传文件保存在 `/w` 下。
- copyparty 运行状态和历史记录保存在 `/state` 下。
- 大文件上传场景可在部署后通过 Canvas 调整 Ingress body size。

**许可证信息：**

copyparty 使用 MIT License。

## 为什么在 Sealos 上部署 copyparty？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一提供部署、存储、网络和后续运维能力。在 Sealos 上部署 copyparty 可以获得：

- **一键部署**：通过应用商店部署 copyparty，无需编写 Kubernetes YAML。
- **内置持久化存储**：上传文件和索引可在重启后保留。
- **即时公网访问**：部署完成后直接使用生成的 HTTPS URL。
- **AI 辅助运维**：通过 Canvas AI 对话调整资源、域名和存储。
- **按量付费效率**：以小资源起步，并按工作负载增长扩容。

## 部署指南

1. 打开 [copyparty 模板](https://sealos.io/products/app-store/copyparty)，点击 **Deploy Now**。
2. 在弹窗中配置 `admin_password` 参数。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续修改可在对话框中描述需求，让 AI 应用变更，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问 copyparty，并使用以下信息登录：
   - **用户名**：`admin`
   - **密码**：你配置的 `admin_password`

## 配置

部署后可以通过以下方式配置 copyparty：

- **AI 对话**：描述你想要的存储、资源或域名变更。
- **资源卡片**：调整 CPU、内存、存储和 Ingress 设置。
- **copyparty 配置文件**：在 `/cfg` 卷中添加 `.conf` 文件进行高级配置。

## 扩展

如需调整资源，打开 Canvas，点击 copyparty StatefulSet 资源卡片，调整 CPU 或内存并应用。除非已经为多实例设计共享存储和会话行为，否则建议保持单副本。

## 故障排查

**登录失败**

使用用户名 `admin` 和部署时填写的 `admin_password`。

**大文件上传被拒绝**

通过 Canvas 资源卡片提高 Ingress body size。

## 更多资源

- [copyparty 文档](https://github.com/9001/copyparty)
- [copyparty Docker 指南](https://github.com/9001/copyparty/tree/v1.20.16/scripts/docker)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证。copyparty 本身使用 MIT License。
