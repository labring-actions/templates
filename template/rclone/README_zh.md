# 在 Sealos 上部署和托管 Rclone

Rclone 是用于跨云存储供应商同步、复制、挂载和服务文件的存储管理工具。此模板在 Sealos Cloud 上以 `rcd` 模式部署 Rclone，并通过 HTTPS 暴露 Web GUI 和 RC API。

![Rclone 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rclone/website-screenshot.webp)

## 关于托管 Rclone

Rclone 以单个 StatefulSet 运行，使用官方 `rclone/rclone` 镜像。模板启动 `rclone rcd`，启用 `--rc-web-gui`，使用部署表单中的 HTTP Basic Auth 凭据，并为 `/config` 和 `/data` 创建持久卷。

Web GUI 和 RC API 使用同一个公网 URL。使用配置的用户名和密码访问浏览器 UI 与 API 端点。

## 常见使用场景

- **云存储管理**：在浏览器中配置和查看 remotes。
- **传输自动化**：通过 RC API 触发 copy、sync、list 等操作。
- **存储迁移**：在支持的供应商之间迁移文件。
- **备份任务**：将 Rclone 配置和缓存保存在 Sealos 持久卷中。

## Rclone 托管依赖

Sealos 模板包含官方 Rclone 容器镜像、持久化配置存储、持久化缓存/数据存储、公开 HTTPS 入口和 Basic Auth 输入。

### 部署依赖

- [Rclone 官网](https://rclone.org/) - 官方文档
- [Rclone Remote Control](https://rclone.org/rc/) - RC API 文档
- [Rclone Web GUI](https://rclone.org/gui/) - Web GUI 文档

## 实现细节

**架构组件：**

- **Rclone rcd**：启用 Web GUI 的远程控制守护进程。
- **持久化配置**：`/config/rclone/rclone.conf` 保存 remotes 和凭据。
- **持久化数据**：`/data` 保存缓存和工作文件。

**配置：**

- `rc_user` 和 `rc_password` 保护 Web GUI 与 RC API。
- 守护进程在集群内监听 `5572` 端口，并通过 HTTPS Ingress 暴露。
- Remotes 可在登录后通过 Web GUI 或 RC API 配置。

**许可证信息：**

Rclone 使用 MIT License。

## 为什么在 Sealos 上部署 Rclone？

Sealos 提供自动 HTTPS、持久化存储，以及面向浏览器访问的 Rclone 控制面一键部署。它适合需要稳定 URL 和持久配置的云存储操作。

## 部署指南

1. 打开 [Rclone 模板](https://sealos.io/products/app-store/rclone)，点击 **Deploy Now**。
2. 在弹窗中配置 RC 用户名和密码。
3. 等待部署完成，通常需要 1-2 分钟。部署完成后会进入 Canvas。
4. 打开生成的应用 URL，使用配置的 Basic Auth 凭据登录。

## 配置

登录后，可通过 Web GUI 创建 remotes。也可以使用相同凭据调用 RC API，例如 `POST /core/version` 和 `POST /config/listremotes`。

## 更多资源

- [Rclone Docs](https://rclone.org/docs/)
- [Rclone Commands](https://rclone.org/commands/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

此模板遵循上游 Rclone MIT License。
