# 在 Sealos 上部署和托管 EaglerCraft Server

EaglerCraft Server 将 EaglercraftX 浏览器客户端、WebSocket 游戏网关、Paper 服务端和基于 RCON 的管理面板打包在一个镜像中。本模板在 Sealos Cloud 上部署 EaglercraftX Server 2.2.3，并持久化世界和插件数据。

![EaglerCraft Server 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## 关于 EaglerCraft Server 托管

EaglerCraft Server 让玩家直接在浏览器中打开类 Minecraft 客户端，并通过安全的 WebSocket 连接到自托管 Paper 世界。2.2.3 镜像包含 EaglercraftX 1.8 和 1.12 客户端，以及 Paper 1.8.8 和 1.12.2 运行时；`minecraft_version` 参数会在启动时选择运行时。

Sealos 模板运行一个 StatefulSet，并配置一个持久卷。持久卷挂载到 `/eaglerx-data`，镜像运行时初始化在 `/eaglerx-data/runtime` 下，`PERSISTENT_DATA_ROOT` 会在重启后保留世界数据和按版本隔离的插件仓库。

## 常见使用场景

- **浏览器多人游戏**：为浏览器、ChromeOS 设备、平板和学校电脑运行多人世界。
- **课堂或社团服务器**：让成员共享一个类 Minecraft 世界，无需分发桌面客户端。
- **私有社区世界**：用持久化存储和自动 HTTPS 长期运行小型社区服务器。
- **插件和配置测试**：在隔离部署中测试 Paper 1.8.8 或 1.12.2 的改动。

## EaglerCraft Server 托管依赖

Sealos 模板内置 EaglercraftX 服务端镜像、浏览器游戏入口、管理 API、Paper 运行时和持久化存储。

### 部署依赖

- [EaglerXserver 源码和文档](https://github.com/yangchuansheng/eaglerXserver) - 官方源码和运行指南
- [已发布的 GHCR 镜像](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server) - `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.3`
- [Sealos Discord](https://discord.gg/wdUn538zVP) - 社区支持

## 实现细节

### 架构组件

模板部署一个有状态服务、两个公网路由和一个持久卷：

- **EaglerCraft Server**：在一个容器中运行浏览器客户端、WebSocket 网关、Paper 运行时和管理桥接服务
- **游戏入口**：端口 `5200`，通过 HTTPS 根路径暴露，用于浏览器客户端和 Multiplayer 服务器入口
- **管理入口**：端口 `5201`，通过 `/admin`、`/admin.css`、`/admin.js`、`/api` 和 `/dynmap` 暴露
- **内部 Paper 和 RCON**：端口 `25565` 和 `25575` 保留在容器内，由管理桥接服务访问
- **持久化存储**：1 GiB 持久卷挂载到 `/eaglerx-data`，保存 `/eaglerx-data/runtime/server-data` 和插件仓库

**配置：**

`minecraft_version` 输入接受 `1.8` 或 `1.12`，并设置 `MINECRAFT_VERSION`。默认的 `1.12` 选项启动 Paper 1.12.2，`1.8` 启动 Paper 1.8.8。`rcon_password` 输入设置 `RCON_PASSWORD`，保护 `/api/login` 和 `/admin` 面板。实测起始规格为 100m CPU、1 GiB 内存和 1 GiB 存储；世界和玩家数量增长后，可在 Canvas 中增加资源。

Sealos 会在 Ingress 层终止 TLS，并将一个公网 HTTPS 域名路由到游戏和管理端口。游戏路由保留 WebSocket 支持和较长的代理超时；管理路由将 API、面板资源和 Dynmap 流量发送到端口 `5201`。

**许可证信息：**

这个 Sealos 模板基于 MIT License 提供。重新分发前，请查看 EaglercraftX 项目和内置服务端组件各自适用的许可证。

## 为什么在 Sealos 上部署 EaglerCraft Server？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维、扩缩容和管理。在 Sealos 上部署 EaglerCraft Server，你可以获得：

- **一键部署**：直接从 App Store 模板启动可在浏览器中游玩的服务器。
- **世界数据持久化**：用托管存储保存 Paper 世界和插件仓库。
- **即时 HTTPS 访问**：游戏和管理入口都会获得公网 HTTPS URL。
- **资源可控**：使用 Canvas 根据实际使用量调整 CPU、内存和存储。
- **AI 辅助运维**：通过 Canvas AI 对话或资源卡片应用变更。
- **按量使用**：从紧凑规格开始，随着需求扩容。

在 Sealos 上部署 EaglerCraft Server，用托管基础设施运行可持久保存的浏览器游戏世界。

## 部署指南

1. 打开 [EaglerCraft Server 模板](https://sealos.io/products/app-store/eaglercraft-server)，点击 **Deploy Now**。
2. 在弹窗中检查生成的应用名称和访问域名，选择 `1.12` 或 `1.8`，并填写 RCON 密码。这个密码用于管理面板登录和基于 RCON 的操作。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续需要调整时，可以在对话框中描述需求让 AI 修改，也可以点击相关资源卡片修改设置。
4. 通过生成的 HTTPS URL 访问服务器：
   - **游戏客户端**：打开 `https://[your-app-url]` 加载浏览器客户端。
   - **Multiplayer 服务器入口**：在 EaglercraftX Multiplayer 对话框中填写公网主机名，例如 `[your-app-url-host]`。
   - **管理面板**：打开 `https://[your-app-url]/admin`，使用部署时填写的 RCON 密码登录。

## 配置

部署完成后，可以通过以下方式配置 EaglerCraft Server：

- **浏览器客户端**：打开根 URL，使用内置的浏览器游戏客户端。
- **管理面板**：打开 `/admin`，输入部署表单中的 RCON 密码，使用服务器控制功能。
- **Canvas AI 对话**：描述 CPU、内存、存储或环境变量调整需求，让 AI 辅助应用变更。
- **资源卡片**：点击 StatefulSet、Service、Ingress 或存储卡片查看并编辑资源。

### 管理员登录和玩家注册

管理面板使用部署时填写的 `rcon_password`。管理员使用现有密码登录：打开 `/admin`，输入密码，浏览器会为管理 API 保存一个短期会话令牌。

玩家加入公网主机名后，在游戏内创建账号。打开游戏聊天框并执行：

```text
/register <你的密码>
```

在 Multiplayer 中使用同一个公网主机名，保留纯主机名形式，不添加 `https://` 或 `wss://`：

```text
[your-app-url-host]
```

## 扩容

扩容服务器：

1. 打开当前部署的 Canvas。
2. 打开 StatefulSet 资源卡片。
3. 根据玩家数量或世界生成负载增加 CPU 和内存。
4. 世界、插件或资源文件增长后扩展存储资源。

## 故障排查

### 常见问题

**管理面板要求输入密码**

- **原因**：管理面板由 `RCON_PASSWORD` 保护。
- **解决方案**：使用部署参数中的 `rcon_password` 值。

**浏览器客户端无法连接**

- **原因**：Multiplayer 输入框需要主机名。
- **解决方案**：只填写 `[your-app-url-host]`，不要在输入框中加入 `https://` 或 `wss://` 前缀。

**首次服务器操作仍在启动**

- **原因**：首次启动会初始化 Paper 和所选的 EaglercraftX 运行时。
- **解决方案**：等待 2-3 分钟的首次启动窗口结束，再重试管理操作。

**重启后缺少世界数据**

- **原因**：世界数据路径需要位于持久卷上。
- **解决方案**：保留模板提供的 `/eaglerx-data` 挂载，使 `/eaglerx-data/runtime/server-data` 中的运行时数据持续保存。

### 获取帮助

- [EaglerXserver Issues](https://github.com/yangchuansheng/eaglerXserver/issues)
- [EaglerXserver 文档](https://github.com/yangchuansheng/eaglerXserver)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [EaglerXserver 源码和运行文档](https://github.com/yangchuansheng/eaglerXserver)
- [Sealos EaglerCraft Server 博客](https://sealos.io/blog/eaglercraft-server/)
- [已发布的容器镜像](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server)

## 许可证

这个 Sealos 模板基于 MIT License 提供。EaglerCraft Server 及其内置上游组件保留各自适用的许可证。
