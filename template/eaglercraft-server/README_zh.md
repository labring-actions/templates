# 在 Sealos 上部署和托管 EaglerCraft Server

EaglerCraft Server 集成浏览器游戏客户端、安全 WebSocket 网关、Paper 服务端和网页管理面板。本模板在 Sealos 上部署 **2.2.4** 版本，提供持久化世界，以及支持 English 和简体中文的管理面板。

![EaglerCraft Server 管理面板](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## 关于 EaglerCraft Server 托管

玩家打开浏览器客户端后，通过安全 WebSocket 连接加入 Paper 世界。首次部署前选择游戏版本：`1.12` 对应 Paper 1.12.2，`1.8` 对应 Paper 1.8.8。每个 Minecraft 版本应使用独立的实例和持久卷。

一个 StatefulSet 运行游戏网关、Paper 和管理桥接服务。Sealos 自动配置 1 GiB 持久卷、公网 HTTPS 地址，以及游戏和管理面板的访问路由。Pod 替换后，世界文件、服务端配置、玩家账号和按版本隔离的插件仓库会继续保留。

## 常见使用场景

- **小型社区世界**：通过浏览器链接共享持久化多人世界。
- **课堂和社团活动**：让成员直接通过浏览器进入共同的游戏世界。
- **服务器管理**：在网页面板中管理天气、时间、玩家和插件。
- **插件测试**：在独立实例中试用可信来源的 Paper 插件。

## EaglerCraft Server 托管依赖

镜像包含两套浏览器客户端、Paper 运行时、WebSocket 网关、管理桥接服务和内置插件。部署采用本地持久化存储，其中包括 LoginSecurity 插件的 SQLite 账号数据。

### 部署依赖

- [上游运行文档](https://github.com/yangchuansheng/eaglerXserver/tree/v2.2.4)
- [2.2.4 版本发布说明](https://github.com/yangchuansheng/eaglerXserver/releases/tag/v2.2.4)
- [已发布的容器镜像](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server)

### 实现细节

**架构组件：**

- **StatefulSet**：单副本运行 `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.4`，并固定到已发布的 SHA-256 摘要。
- **游戏路由**：HTTPS 根路径 `/` 和安全 WebSocket 连接访问端口 `5200`。
- **管理路由**：同一域名下的 `/admin`、`/api`、`/admin.css`、`/admin.js`、`/admin-i18n.js` 和 `/dynmap` 访问端口 `5201`。Service 在游戏初始化期间就发布 Pod 端点，管理页和浏览器客户端各自的 HTTP 服务启动后即可访问。
- **内部服务**：Paper 端口 `25565` 和 RCON 端口 `25575` 保持在 Pod 内部。
- **持久卷**：`/eaglerx-data` 保存完整运行目录、世界和配置。`PERSISTENT_DATA_ROOT=/eaglerx-data/runtime/server-data` 保存按版本隔离的插件仓库。
- **运行目录初始化**：初始化容器会为新持久卷写入完整运行目录，并刷新已有持久卷中由镜像提供的脚本和浏览器资源，同时保留 Paper 配置、世界及插件数据。

主容器的 CPU 上限为 `200m`、内存上限为 `1024Mi`；初始化容器使用 `100m` CPU 和 `128Mi` 内存。验证中，`100m` CPU 配额下的区块保存触发了 Paper 1.8 看门狗，`512Mi` 内存档位在启动时触发了 OOM。Pod 就绪检查会等待游戏、HTTP、Paper 和 RCON 端口，以及所选世界的 `level.dat` 文件。启动探针会确认 RCON 命令响应，并立即保存新生成的世界。Service 通过 `publishNotReadyAddresses: true` 在这一过程期间提前开放管理页和浏览器客户端，进入世界需要等待 Paper 启动完成。

`PUBLIC_GAME_URL` 自动使用生成的 HTTPS 地址。管理面板的 Overview 会显示对应的 `wss://` 地址和 **Open and join game** 链接。通过本模板入口上传的插件大小上限为 **32 MiB**。

## 为什么在 Sealos 上部署 EaglerCraft Server？

[Sealos](https://sealos.io) 基于 Kubernetes 提供一键部署、托管 HTTPS 访问和持久化存储。按量付费和资源配置功能支持小型服务器从已验证的资源规格起步。部署后，可以通过 Canvas 的 AI 对话框或资源卡片调整 CPU、内存和存储。

## 部署指南

1. 打开 [EaglerCraft Server 模板页面](https://sealos.io/products/app-store/eaglercraft-server)，点击 **Deploy Now**。
2. 选择 `minecraft_version`，默认值为 `1.12`；将 `rcon_password` 设置为强度足够的非空单行密码，并保存好这个管理员登录密码。
3. 游戏完整启动通常需要 **2-3 分钟**，具体取决于世界生成和插件加载。在 Canvas 点击应用链接会直接打开 `/admin`，管理 HTTP 服务启动后即可访问该页面。
4. 输入部署时的 RCON 密码，点击 **Confirm**。游戏初始化期间即可完成管理员登录；StatefulSet 进入 Ready 状态后，世界数据和游戏控制功能可用。可通过页眉的 **Language** 选择 English 或简体中文。
5. 等待 StatefulSet 进入 Ready 状态后，在 **Overview** 中点击 **Open and join game**，或将 WebSocket 地址复制到浏览器客户端的 Multiplayer 服务器列表。进入世界后，按照下文完成玩家注册或登录。

## 管理员登录与玩家注册

### 管理员访问

管理面板使用部署时设置的 `rcon_password` 登录。登录成功后，管理令牌保存在当前浏览器标签页的 `sessionStorage` 中，有效期为 8 小时。关闭标签页会清除该标签页的会话；点击 **Log out** 也会清除已保存的登录状态。

游戏进入 Ready 状态后，可在 **Operation control** 中点击天气按钮 **sunny** 和时间按钮 **noon**。世界状态卡片和命令控制台会显示操作结果。面板同时提供玩家管理、世界保存和插件管理功能。

### 玩家访问

选择一个长度为 3-16 个字符的玩家名，通过生成的地址连接服务器：

```text
wss://[your-app-url-host]
```

进入世界后，按 `T` 打开聊天窗口，并在 30 秒登录窗口内完成注册。玩家密码长度为 6-32 个字符：

```text
/register <password>
```

以后访问时，使用相同的玩家名和密码登录：

```text
/login <password>
```

玩家密码属于 LoginSecurity 账号。管理员 RCON 密码用于服务器管理，请分别保管。

## 配置与升级

通过 Canvas 的 AI 对话框或 StatefulSet 资源卡片调整资源。共享世界保持 **一个副本**，并随着玩家活动增加 CPU 或内存。

升级期间保留 `/eaglerx-data` 持久卷。每次 Pod 启动都会刷新内置脚本和浏览器资源，世界目录、Paper 配置和插件仓库保留已有内容。自定义服务端配置应放在持久化的 Paper 目录下。切换 Minecraft 运行版本前，先备份持久卷。

管理面板支持上传可信来源的 JAR 插件，通过本模板上传的大小上限为 32 MiB。上传、启用或停用插件后，使用 **Restart the server** 受控重启 Paper，使变更生效。

Minecraft 1.8 的初始化流程会关闭 Dynmap 的玩家生命值和护甲显示，以兼容旧版 Paper API。地图瓦片和玩家位置功能继续可用。

## 故障排查

- **管理页面已打开，游戏控制仍在加载**：在 Canvas 查看 StatefulSet 的 Ready 状态。浏览器客户端 `/` 和管理页 `/admin` 提前开放，进入世界及游戏控制需要等待 Paper 和 RCON。`[start]` 日志描述入口脚本的配置过程，Paper 的实际初始化进度保存在容器内的 `/eaglerx-data/runtime/server/logs/latest.log`。
- **管理员登录失败**：使用已保存的 `rcon_password`。同一来源连续输错 5 次会锁定 10 分钟；通过同一反向代理访问的客户端可能共享这一窗口。
- **玩家加入后很快断开**：首次访问时在 30 秒内执行 `/register`，之后访问时执行 `/login`，并保持玩家名一致。
- **插件上传返回 HTTP 413**：将 JAR 文件大小控制在模板的 32 MiB 入口限制内。

应用问题可提交至[上游 Issues](https://github.com/yangchuansheng/eaglerXserver/issues)，平台问题可访问 [Sealos 社区](https://discord.gg/wdUn538zVP)。

## 许可证

本模板遵循 [Sealos 模板仓库](https://github.com/labring-actions/templates) 的许可条款。Eaglercraft、Paper 和内置插件分别遵循各自的上游许可证。
