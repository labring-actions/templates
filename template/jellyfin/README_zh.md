# 在 Sealos 上部署并托管 Jellyfin

Jellyfin 是自由开源媒体系统，用于管理、串流和共享电影、剧集、音乐与照片。本模板会在 Sealos Cloud 上部署 Jellyfin 10.10.7，并自动配置持久化配置、缓存、媒体存储和 HTTPS Ingress。

![Jellyfin 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/jellyfin/website-screenshot.webp)

## 关于在 Sealos 上托管 Jellyfin

Jellyfin 提供基于浏览器的媒体服务器界面和流媒体 API。你可以通过初始化向导创建第一个管理员，添加媒体库，扫描内容，并通过 Sealos 生成的 URL 播放媒体。

这个 Sealos 模板遵循官方容器部署模型，持久化 `/config`、`/cache` 和 `/media` 路径。默认卷从 `1Gi` 开始；导入较大媒体库前，可以在 Sealos Canvas 中扩容。

## 常见使用场景

- **个人媒体服务器**：整理并串流播放个人媒体库。
- **家庭媒体库**：创建用户，并通过一个 Web 界面共享媒体库。
- **私有视频归档**：在 Sealos 持久化存储中保存并浏览自管理视频。
- **音乐和照片浏览**：通过一个应用管理混合媒体集合。

## Jellyfin 托管依赖

本模板包含 Jellyfin、配置/缓存/媒体持久卷、Service、Ingress 和 App 启动入口。

### 部署依赖

- [Jellyfin Documentation](https://jellyfin.org/docs/) - 官方文档
- [Jellyfin Container Guide](https://jellyfin.org/docs/general/installation/container/) - 官方容器部署指南
- [Jellyfin GitHub Repository](https://github.com/jellyfin/jellyfin) - 源码与发布记录

## 实现细节

### 架构组成

- **Jellyfin Server**：在端口 `8096` 提供 Web 界面和串流服务
- **配置存储**：持久化 `/config`，容量 `1Gi`
- **缓存存储**：持久化 `/cache`，容量 `1Gi`
- **媒体存储**：持久化 `/media`，容量 `1Gi`
- **Ingress**：通过 HTTPS 暴露 Jellyfin

### 资源配置

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Jellyfin | 20m | 200m | 25Mi | 256Mi |

### 配置说明

模板会把 `JELLYFIN_PublishedServerUrl` 设置为 Sealos 生成的 HTTPS URL。媒体文件可以在后续通过 Sealos 存储工作流或自定义卷管理加入 `/media`。

### 许可证信息

Jellyfin 使用 [GNU General Public License v2.0](https://github.com/jellyfin/jellyfin/blob/master/LICENSE)。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么在 Sealos 上部署 Jellyfin？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可以简化部署和运维。部署 Jellyfin 后，你可以获得：

- **一键部署**：从一个模板页面启动 Jellyfin、持久化存储和 HTTPS。
- **持久化媒体路径**：配置、缓存和媒体存储在重启后保留。
- **公网 Web 访问**：通过自动生成的安全 URL 打开 Jellyfin。
- **资源调整简单**：通过 Sealos Canvas 调整 CPU、内存和存储。

## 部署指南

1. 打开 [Jellyfin 模板页面](https://sealos.io/products/app-store/jellyfin)，点击 **Deploy Now**。
2. 检查弹窗中的生成参数并部署。
3. 等待 Jellyfin 就绪。
4. 打开生成的 URL，完成首次运行向导：
   - 选择显示语言
   - 创建管理员账号
   - 使用 `/media` 添加媒体库
   - 确认远程访问设置
5. 使用管理员账号登录，扫描媒体库，并按需创建另一个用户。

## 配置

通过 Jellyfin dashboard 管理媒体库、用户、元数据、插件、转码设置和访问策略。通过 Sealos Canvas 扩展持久卷或更新资源限制。

## 扩缩容

本模板按单实例 Jellyfin 和本地持久化存储设计。媒体库扫描或串流会话需要更多余量时，提高 CPU 和内存。随着媒体库增长，扩展 `/media` 存储。

## 故障排查

**问题：Jellyfin 需要更多媒体库或缓存空间**
- 原因：媒体元数据、海报图和转码缓存增长较快。
- 处理方法：在 Sealos Canvas 中扩容 `/config`、`/cache` 或 `/media`。

**问题：初始化后没有媒体内容**
- 原因：媒体库路径中还没有文件。
- 处理方法：把媒体加入 `/media`，然后在 Jellyfin dashboard 中重新扫描媒体库。

## 更多资源

- [Jellyfin Documentation](https://jellyfin.org/docs/)
- [Jellyfin Container Guide](https://jellyfin.org/docs/general/installation/container/)
- [Jellyfin GitHub Issues](https://github.com/jellyfin/jellyfin/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Jellyfin 本身使用 GPL-2.0。
