# 在 Sealos 上部署和托管 EaglerCraft Server

EaglerCraft Server 将 EaglercraftX 浏览器客户端、WebSocket 游戏入口、Paper 服务端运行时和基于 RCON 的管理面板打包在一起。这个模板会在 Sealos Cloud 上部署一个带持久化世界数据的 Paper 1.12.2 服务器。

![EaglerCraft Server 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## 关于 EaglerCraft Server 托管

EaglerCraft Server 让玩家直接在浏览器中打开类 Minecraft 游戏客户端，并通过安全的 WebSocket 连接到自托管 Paper 服务器。发布镜像同时包含 1.8 和 1.12 两套运行目录；本模板使用 `MINECRAFT_VERSION=1.12` 启动 Paper 1.12.2 运行时。

Sealos 模板会把 EaglerCraft Server 部署为单个 StatefulSet，并将一个持久卷挂载到 `/eaglerX-1.8-server/server-data`。这个挂载点会保存生成的世界数据，同时保留镜像内置的启动脚本和版本目录。

## 常见使用场景

- **浏览器多人游戏**：为 ChromeOS、平板、学校设备和其他只能使用浏览器的环境提供多人游戏服务器。
- **课堂或社团服务器**：让成员共享一个类 Minecraft 世界，无需分发桌面客户端。
- **私有社区世界**：用托管存储和自动 HTTPS 为小型社群长期运行 Paper 服务器。
- **插件和配置测试**：在隔离、可销毁的部署中测试 Paper 1.12.2 服务端改动。

## EaglerCraft Server 托管依赖

Sealos 模板内置 EaglercraftX 服务端镜像、WebSocket 游戏入口、启用 RCON 的管理面板，以及用于世界数据的持久化存储。

### 部署依赖

- [EaglerCraft Server Docker 镜像](https://github.com/yangchuansheng/eaglercraft-server) - 本模板使用的容器镜像和运行文档
- [已发布的 GHCR 镜像](https://github.com/yangchuansheng/eaglercraft-server/pkgs/container/eaglerx1.8server) - `ghcr.io/yangchuansheng/eaglerx1.8server:1.12.1`
- [上游服务端源码](https://gitee.com/mirrorvim/eaglerX-1.8-server) - 构建镜像所使用的源项目

## 实现细节

### 架构组件

这个模板会部署一个有状态服务：

- **EaglerCraft Server**：在单个容器中运行浏览器客户端、WebSocket 网关、Paper 1.12.2 运行时和管理桥接服务
- **游戏入口**：端口 `5200`，通过部署根 URL 暴露，用于浏览器游戏和多人连接
- **管理面板**：端口 `5201`，通过 `/admin` 暴露，用于基于 RCON 的服务器管理
- **持久化存储**：一个 1 GiB 持久卷挂载到 `/eaglerX-1.8-server/server-data`，保存生成的世界数据

**配置：**

模板会设置 `MINECRAFT_VERSION=1.12`，并自动生成强度足够的 `RCON_PASSWORD`。当 `/admin` 面板提示登录时，使用生成的密码进入管理界面。

Sealos 会在 Ingress 层终止 TLS，并将同一个公网域名路由到两个后端端口：`/` 进入端口 `5200` 的浏览器游戏客户端，`/admin` 进入端口 `5201` 的管理面板。

**许可证信息：**

这个模板基于 MIT License 提供。重新分发前，请同时查看上游 EaglercraftX 和内置服务端组件各自的许可证。

## 为什么在 Sealos 上部署 EaglerCraft Server？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维、扩缩容和管理。在 Sealos 上部署 EaglerCraft Server，你可以获得：

- **一键部署**：直接从 App Store 模板启动可在浏览器中游玩的服务器，无需手写 Kubernetes YAML。
- **世界数据持久化**：用持久卷保存 Paper 生成的世界数据。
- **即时 HTTPS 访问**：游戏入口和管理入口都会获得公网 HTTPS URL。
- **资源可控**：玩家数量或世界规模增长后，可以在 Canvas 中调整 CPU、内存和存储。
- **AI 辅助运维**：部署后可以通过 Canvas AI 对话或资源卡片修改配置。
- **按量使用**：从紧凑资源规格起步，服务器需要更多资源时再扩容。

在 Sealos 上部署 EaglerCraft Server，用托管基础设施运行一个可持久保存的浏览器游戏世界。

## 部署指南

1. 打开 [EaglerCraft Server 模板](https://sealos.io/products/app-store/eaglercraft-server)，点击 **Deploy Now**。
2. 在弹窗中检查生成的应用名称、访问域名和 RCON 密码。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续需要调整时，可以在对话框中描述需求让 AI 修改，也可以点击相关资源卡片修改设置。
4. 通过生成的 URL 访问服务器：
   - **游戏客户端**：打开 `https://[your-app-url]` 加载浏览器客户端并开始游玩。
   - **管理面板**：打开 `https://[your-app-url]/admin`，使用生成的 RCON 密码登录。

## 配置

部署完成后，可以通过以下方式配置 EaglerCraft Server：

- **浏览器客户端**：打开根 URL，使用内置的浏览器游戏客户端。
- **管理面板**：打开 `/admin`，输入生成的 RCON 密码使用管理界面。
- **Canvas AI 对话**：描述 CPU、内存、存储或环境变量调整需求，让 AI 应用变更。
- **资源卡片**：点击 StatefulSet、Service、Ingress 或存储卡片查看并修改设置。

### 玩家连接方式

使用部署根 URL 进行浏览器游戏。如果需要在 EaglercraftX 客户端的多人服务器列表或直接连接流程中填写地址，使用同一主机名的安全 WebSocket 形式：

```text
wss://[your-app-url-host]
```

管理面板使用同一个公网域名加 `/admin`：

```text
https://[your-app-url]/admin
```

## 扩容

扩容服务器：

1. 打开当前部署的 Canvas。
2. 点击 StatefulSet 资源卡片。
3. 根据玩家数量或世界生成负载增加 CPU 和内存。
4. 世界、插件或资源文件增长后，点击存储资源卡片扩容持久卷。

## 故障排查

### 常见问题

**管理面板要求输入密码**

- 原因：管理面板由 `RCON_PASSWORD` 保护。
- 解决方案：使用部署参数中生成的 `rcon_password` 值。

**玩家无法从浏览器客户端连接**

- 原因：客户端需要当前部署域名对应的公网 WebSocket 入口。
- 解决方案：使用根应用 URL 打开内置客户端，或在 EaglercraftX 多人连接流程中输入 `wss://[your-app-url-host]`。

**重启后世界数据消失**

- 原因：世界数据需要存放在配置好的 `SERVER_DATA_DIR` 下。
- 解决方案：保留模板提供的 `/eaglerX-1.8-server/server-data` 持久卷挂载。

### 获取帮助

- [EaglerCraft Server Issues](https://github.com/yangchuansheng/eaglercraft-server/issues)
- [上游服务端源码](https://gitee.com/mirrorvim/eaglerX-1.8-server)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [EaglerCraft Server 文档](https://github.com/yangchuansheng/eaglercraft-server)
- [EaglerCraft Server 博客](https://sealos.io/blog/eaglercraft-server/)
- [已发布的容器镜像](https://github.com/yangchuansheng/eaglercraft-server/pkgs/container/eaglerx1.8server)

## 许可证

这个 Sealos 模板基于 MIT License 提供。EaglerCraft Server 使用 MIT License，内置上游组件保留各自许可证。
