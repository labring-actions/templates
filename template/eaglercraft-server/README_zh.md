# 在 Sealos 上部署和托管 EaglerCraft Server

EaglerCraft Server 集成网页版 Minecraft、WebSocket 网关、Paper 服务端和中英文管理面板。本模板部署 **2.2.7**，持久化保存世界存档和玩家账号。

![EaglerCraft Server 管理面板](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

截图来自实际测试的 Sealos 部署，展示英文管理面板和一名在线玩家。

## 关于托管 EaglerCraft Server

选择 `1.12` 可运行 Paper 1.12.2，选择 `1.8` 可运行 Paper 1.8.8。每次部署通过单副本 StatefulSet 运行一个游戏版本，并提供 1 GiB 持久卷，保存世界、配置、玩家账号和各版本的插件数据。同时运行两个版本时，请分别创建实例和存储卷。

玩家通过公开的 HTTPS 游戏页面和安全 WebSocket 地址连接服务器。应用卡片打开 `/admin`，服主可在其中管理天气、时间、玩家、世界和插件。

## 常见使用场景

- **好友共享世界**：通过浏览器链接邀请好友加入。
- **社团与课堂活动**：为集体活动提供持久化游戏世界。
- **服务器管理**：在网页面板中调整游戏设置和玩家权限。
- **插件试用**：在独立实例中测试可信的 Paper 插件。

## EaglerCraft Server 托管依赖

镜像已包含游戏客户端、Paper、Bungee 网关、Python 管理服务和插件。LoginSecurity 使用持久卷上的 SQLite 保存玩家账号。所选版本的部署文档采用本地文件系统保存数据。

### 部署依赖

- Sealos 账号和支持 WebGL 的浏览器。
- 一个高强度、非空、单行的管理密码。
- 接受 [Minecraft EULA](https://www.minecraft.net/en-us/eula)；上游启动脚本会在启动时写入 `eula=true`。
- [2.2.7 版本源码及部署文档](https://github.com/yangchuansheng/eaglerXserver/tree/v2.2.7)。
- [2.2.7 版本发布说明](https://github.com/yangchuansheng/eaglerXserver/releases/tag/v2.2.7)。

### 架构组件

- **StatefulSet**：单副本运行 `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.7`，镜像固定到已核验的 SHA-256 摘要。
- **初始化与探针**：ConfigMap 中的脚本初始化空卷、刷新镜像内的脚本和浏览器资源，并验证首次世界保存。已有世界、配置和插件仓库的数据持续保留。
- **持久化存储**：`/eaglerx-data/runtime` 保存运行目录；`server-data/plugins-1.8` 和 `server-data/plugins-1.12` 分别保存两个版本的插件仓库。
- **游戏路由**：HTTPS `/` 和 WSS 连接转发到 `5200` 端口。
- **管理路由**：同一 HTTPS 域名下的 `/admin`、`/api`、管理页面资源和 `/dynmap` 转发到 `5201`。Paper 的 `25565` 和 RCON 的 `25575` 仅供内部访问。

主容器的 CPU 上限为 `200m`，内存上限为 `1024Mi`；初始化容器使用 `100m` CPU 和 `128Mi` 内存。该配置覆盖已测试的个人使用负载，世界复杂度和玩家活动增加后应相应扩容。持久卷初始容量为 1 GiB，请随着区块、地图和备份增长关注剩余空间。

## 为什么在 Sealos 上部署 EaglerCraft Server？

[Sealos](https://sealos.io) 基于 Kubernetes，提供一键部署、托管 HTTPS、持久化存储和按量付费资源。部署完成后，可通过 Canvas 的 AI 对话框或资源卡片调整服务器的 CPU、内存和存储。

## 部署指南

1. 打开 [EaglerCraft Server 模板](https://sealos.io/products/app-store/eaglercraft-server)，点击 **Deploy Now**。
2. 选择 `minecraft_version`，设置 `rcon_password`，并保存该管理密码。
3. 部署通常需要 **2-3 分钟**，首次生成世界可能耗时更长。部署完成后，在 Canvas 中打开应用卡片，进入 `/admin`。
4. 输入 `rcon_password`，点击 **Confirm**。服务器启动期间即可登录管理面板；看到 **Paper is ready** 后再操作游戏控制项。
5. 在 **Overview** 中点击 **Join game**，按照下文完成玩家设置和注册。管理面板的 **Language** 选项可切换 English 和简体中文。

## 管理员登录与玩家注册

### 管理员登录

管理登录框使用部署时设置的 `rcon_password`。登录后签发的令牌有效期为 8 小时，保存在当前标签页的 `sessionStorage` 中。点击 **Log out** 可清除本地登录状态。

看到 **Paper is ready** 后，在 **Runtime controls** 中点击 **Rain** 和 **Noon**。世界状态卡片会更新天气与时间，**Command terminal** 会显示指令响应。**World tools** 提供世界保存操作；**System settings** 提供配置、插件管理和 Paper 受控重启。

### 玩家设置与登录

1. 打开游戏页面，出现声音提示时按任意键。
2. 首次使用浏览器客户端时，进入 **Edit Profile**，设置一个固定的 3-16 位玩家名，点击 **Done**，完成客户端信息提示。以后使用相同名字；直接快速加入时，客户端可能先分配一个随机名字。
3. 选择 **Multiplayer**。2.2.7 会自动列出当前部署，选中后点击 **Join Server**；设置好玩家资料后，也可使用管理面板的 **Join game** 链接。
4. 世界画面出现后，按 `T` 打开聊天，在 30 秒内完成注册。密码长度为 6-32 位：

   ```text
   /register <player-password>
   ```

5. 后续连接时，使用相同玩家名，按 `T` 输入：

   ```text
   /login <player-password>
   ```

注册成功后会自动登录。可用 `/sethome base` 设置家，再用 `/homes` 查看列表。玩家密码由 LoginSecurity 管理，服主使用 RCON 密码登录管理面板。

Overview 页面会显示安全连接地址：

```text
wss://[your-app-url-host]/
```

## 配置与升级

通过 Canvas 的 AI 对话框或 StatefulSet 资源卡片调整资源。共享世界保持单副本运行；切换游戏版本或升级前请保存备份。

升级时保留 `/eaglerx-data` 持久卷。每次 Pod 启动都会刷新镜像内的脚本和网页客户端，同时保留已有世界、Paper 配置和插件状态。自定义前端改动需要与新镜像资源合并。启动探针会执行首次世界保存，并检查 Paper 的 RCON 响应，随后将实例标记为就绪。

本模板的 Ingress 将可信插件上传限制为 **32 MiB**。上传、启用或停用插件后，在 **System settings** 中执行 Paper 受控重启。重启可能需要几分钟，完成后确认 **Paper is ready**。

Minecraft 1.8 的初始化脚本会关闭 Dynmap 的玩家血量和护甲显示，以兼容较旧的 Paper API；地图瓦片和玩家位置功能继续可用。

## 故障排查

- **管理面板已打开，游戏控制项仍在加载**：等待 **Paper is ready**。Service 会在启动期间开放管理页面和游戏页面。可通过 Canvas 资源日志检查启动过程；Paper 的详细日志位于 `/eaglerx-data/runtime/server/logs/latest.log`。
- **管理员登录失败**：使用部署时保存的密码。同一来源连续失败五次会触发 10 分钟锁定，代理后的多个客户端可能共享这一窗口。
- **游戏提示 Login timed out**：重新连接，在 30 秒内提交 `/register` 或 `/login`。保持玩家名固定，便于服务器找到原账号。
- **修改等待重启生效**：在面板中执行 Paper 受控重启，以应用配置和插件变更。
- **插件上传返回 HTTP 413**：将 JAR 大小控制在 32 MiB 以内。

应用问题可提交至[上游 Issues](https://github.com/yangchuansheng/eaglerXserver/issues)，平台问题可咨询 [Sealos 社区](https://discord.gg/wdUn538zVP)。

## 许可证

本模板遵循 [Sealos 模板仓库](https://github.com/labring-actions/templates)的许可条款。Eaglercraft、Paper、Minecraft 素材和各内置插件分别遵循其上游许可与使用条款。
