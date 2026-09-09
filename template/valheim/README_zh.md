# 在 Sealos 上部署和托管 Valheim Docker

[Valheim Docker](https://github.com/mbround18/valheim-docker) 通过 Odin 管理 Valheim 专用服务器，并内置 Huginn 状态面板。本模板部署一个原版游戏服务器，分别持久化保存游戏程序和世界存档。

![Valheim Docker 官网](./website-screenshot.webp)

## 关于托管 Valheim Docker

Odin 使用 SteamCMD 安装专用服务器，负责启动 Valheim 和安全关闭进程。Huginn 提供公开的只读状态面板、玩家信息、健康检查和交互式 API 文档。

游戏程序与配置保存在 2 GiB 持久卷中。世界存档独立保存在 1 GiB 持久卷中，挂载路径为 `/home/steam/.config/unity3d/IronGate/Valheim`。Sealos 通过 HTTPS 提供状态面板，通过 UDP NodePort 提供游戏入口。

## 常见使用场景

- 为朋友托管长期保留的多人合作世界。
- 将已有原版世界迁移到持续在线的服务器。
- 通过浏览器查看服务器健康状态和在线人数。

## Valheim Docker 托管依赖

模板包含服务器镜像、SteamCMD、Odin、Huginn、持久卷、Service 和 HTTPS Ingress。玩家需要拥有正版 Valheim 客户端，且客户端版本应与服务器版本兼容。

- [项目文档](https://mbround18.github.io/valheim-docker/)
- [Valheim 专用服务器指南](https://www.valheimgame.com/support/a-guide-to-dedicated-servers/)
- [Huginn API 文档](https://github.com/mbround18/valheim-docker/blob/v3.7.0/src/huginn/README.md)

### 实现细节

| 组件 | 配置 |
| --- | --- |
| 服务器 | `mbround18/valheim:3.7.0`，单副本 StatefulSet |
| CPU / 内存上限 | 100m / 2 GiB |
| 游戏程序 | 2 GiB PVC，挂载到 `/home/steam/valheim` |
| 世界存档 | 1 GiB PVC，挂载到 `/home/steam/.config/unity3d/IronGate/Valheim` |
| 状态面板 | Huginn 监听 `3000` 端口，通过 HTTPS 访问 |
| 游戏网络 | UDP `2456`（游戏）、`2457`（查询）和 `2458` |
| 运行配置 | 原版游戏、公开服务器列表、Steam 后端、UTC 时区 |

容器使用 UID `111` 和 GID `1000` 运行。启动检查和就绪检查使用 Huginn 的 `/readiness`；存活检查同时确认 Valheim 进程和 Huginn 可用。镜像标签固定 Docker 管理工具的版本；SteamCMD 在首次启动时安装当前稳定版 Valheim 服务器，后续重启复用已安装版本。需要升级时，临时将 `UPDATE_ON_STARTUP` 设为 `1`，升级完成后恢复为 `0`。

资源上限的测试覆盖空世界、公网服务器查询、面板/API 访问和存档持久化。持续多人游戏前应提高资源配置。2 GiB 程序卷可容纳本次测试的原版游戏版本。进行大型更新或添加模组前，应先扩容该卷。每个世界保持单副本；活跃玩家增多或世界变大时，增加 CPU 和内存。模板默认关闭定时自动更新和定时备份，请另行保留重要存档的副本。

## 为什么在 Sealos 上部署 Valheim Docker？

Sealos 基于 Kubernetes，提供一键部署、持久化存储和 HTTPS 状态页。按量付费的资源配置适合从小型服务器起步，后续可通过 Canvas 资源卡片或 AI 对话调整容量。

## 部署指南

1. 打开 [Valheim Docker 模板页面](https://sealos.io/products/app-store/valheim)，点击 **Deploy Now（立即部署）**。
2. 填写 `server_name`、`world_name` 和 `server_password`。密码至少包含 5 个字符，并与服务器名称保持不同。密码使用字母、数字和连字符；世界名称还支持下划线，服务器名称还支持空格。
3. Sealos 通常需要 2-3 分钟创建资源。服务器首次启动还需下载约 1.64 GiB 文件并生成世界，在最低 CPU 档位下可能需要数十分钟。启动检查为首次初始化预留了最长 60 分钟。进入 Canvas，等待服务器状态变为 Ready。
4. 打开应用的 HTTPS 地址即可查看 Huginn。状态面板直接提供公开的只读信息；进入游戏时使用部署时设置的密码。
5. 打开 Service 资源卡片，复制公网 UDP 主机地址以及内部端口 `2456` 对应的 NodePort。在 Valheim 中选择 **Start Game（开始游戏）**，选好角色后进入 **Join Game（加入游戏）**，通过 **Add Server（添加服务器）** 输入 `<public-host>:<game-node-port>`，并按提示输入 `server_password`。
6. 使用 Steam 服务器浏览器时，填写内部端口 `2457` 对应的独立查询端口。复制地址时区分游戏端口和查询端口，实际分配值以 Canvas 为准。

### 状态面板与游戏登录

Huginn 提供 `/status`、`/players`、`/mods`、`/metrics` 和 `/docs`。面板采用公开只读访问方式，直接打开即可使用。游戏密码保存在 StatefulSet 的 `PASSWORD` 环境变量中，可通过对应资源卡片查看或修改。

内置面板的 Steam 连接按钮按端口直接映射的环境生成地址。本模板使用 NodePort，请以 Canvas 显示的公网 UDP 地址连接游戏。

## 配置与备份

部署后，通过 Canvas 的 AI 对话或资源卡片修改配置。副本数保持为一；为单个世界增加容量时，调整 CPU 和内存即可。

导入已有世界时，先停止服务器，将配套的 `.db` 和 `.fwl` 文件复制到存档卷的 `worlds_local` 目录，将 `world_name` 设置为文件的共同名称，再重启服务器。备份时保留完整的存档目录。删除持久卷会同时删除其中保存的世界或游戏文件。

## 故障排查

**状态面板显示离线：** 查看服务器日志中的 SteamCMD 进度，并等待 `Game server connected` 消息。Huginn 会在世界初始化结束前启动。持续出现 OOM 终止时，应提高内存档位。

**客户端连接失败：** 核对公网 UDP 主机、分配的游戏端口、密码及客户端和服务器版本。HTTPS 面板地址用于网页访问；游戏客户端使用 Service 提供的 UDP 地址。

**更新提示磁盘空间不足：** 扩容游戏程序 PVC，再重启服务器。世界存档使用独立的持久卷。

## 许可证

Valheim Docker、Odin 和 Huginn 采用 [BSD 3-Clause 许可证](https://github.com/mbround18/valheim-docker/blob/v3.7.0/LICENSE)，版权归 © 2021 mbround18 所有。Valheim 及其游戏资产适用各自权利人的条款。
