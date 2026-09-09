# 在 Sealos 上部署和托管 tModLoader

tModLoader 为 Terraria 提供社区模组支持；本模板在 Sealos Cloud 上部署专用服务器，提供联机密码、世界持久化和 Steam 创意工坊模组支持。

![tModLoader 官方模组游戏画面](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tmodloader/website-screenshot.webp)

素材来源：[游戏内标题 Logo](https://github.com/tModLoader/tModLoader/blob/v2026.07.3.0/patches/tModLoader/Terraria/ModLoader/Logo.png) 和 [Steam 官方截图](https://store.steampowered.com/app/1281930/tModLoader/)。画面用于展示官方模组玩法；本次部署实测范围为下文列出的服务器测试。

## 关于 tModLoader 托管

玩家通过 tModLoader 游戏客户端进入共享的 Terraria 世界。服务器使用适配 **Terraria 1.4.4.9** 的稳定版 **tModLoader v2026.7.3.0**，镜像为 `jacobsmile/tmodloader1.4:v2026.07.3.0`。客户端版本和启用的模组需要与服务器一致。

Sealos 会创建一个服务器实例、公网 TCP 端口、启动配置，以及保存世界和模组的持久卷。服务器每 10 分钟自动存档，关闭时通过原生 `exit` 命令保存世界。玩家在游戏的加入服务器流程中输入密码；管理员通过 Sealos 资源终端和环境变量管理服务器。

## 常见使用场景

- **好友合作世界**：与好友共享持久化世界，使用自动生成的密码控制加入权限。
- **创意工坊模组联机**：下载并启用一组兼容的 Steam 创意工坊模组。
- **模组开发验证**：使用专用服务器测试多人联机兼容性和世界持久化。

## tModLoader 托管依赖

模板使用上游 Docker 镜像，其中包含 tModLoader、SteamCMD 和控制台工具。容器启动时，上游脚本会下载 .NET 运行时。玩家需要安装 Terraria 和版本匹配的 tModLoader 客户端。

### 部署依赖

- [tModLoader 官网](https://www.tmodloader.net/) — 安装方式和项目信息
- [Docker 镜像文档](https://github.com/JACOBSMILE/tmodloader1.4/blob/master/README.md) — 环境变量、模组和控制台命令
- [专用服务器指南](https://github.com/tModLoader/tModLoader/wiki/Starting-a-modded-server) — 多人联机服务器配置
- [模板固定的稳定版本](https://github.com/tModLoader/tModLoader/releases/tag/v2026.07.3.0) — 本模板使用的服务器版本

### 实现细节

**架构组件：**

| 组件 | 用途 |
| --- | --- |
| 单副本 StatefulSet | 运行专用游戏服务器，管理一个世界 |
| TCP NodePort Service (`<app-name>-nodeport`) | 将容器的 `7777` 端口映射到当前地域分配的公网端口 |
| 挂载到 `/data` 的 1Gi 持久卷 | 保存世界、已启用模组配置和下载的创意工坊内容 |
| ConfigMap | 初始化数据目录并生成服务器配置，同时避免输出联机密码 |

**配置：**

| 设置 | 默认值 | 说明 |
| --- | --- | --- |
| `workshop_mods` | 留空 | 以逗号分隔的数字模组 ID；下载并启用列出的模组 |
| `world_size` | `1` | `1` = 小型，`2` = 中型，`3` = 大型 |
| `difficulty` | `0` | `0` = 经典，`1` = 专家，`2` = 大师，`3` = 旅途 |
| 联机密码 | 每次部署自动生成 | 在服务器环境变量的 `TMOD_PASS` 中查看 |
| 世界名称和种子 | `Sealos` | 分别由 `TMOD_WORLDNAME` 和 `TMOD_WORLDSEED` 设置 |
| 玩家上限 | `8` | 连接数上限；增加活跃玩家时应提高资源配置 |
| 自动存档间隔 | 10 分钟 | 由 `TMOD_AUTOSAVE_INTERVAL` 设置 |

个人低负载配置为 **100m CPU、1024Mi 内存**，资源请求分别为 `10m` CPU 和 `102Mi` 内存。实测覆盖了全新小型世界生成、密码认证、世界数据交换、玩家列表和存档命令，以及超过 60 秒的稳定运行窗口。相邻的 `512Mi` 内存档位在生成全新小型世界时触发了 `System.OutOfMemoryException`。Recipe Browser v0.12.0.3 也在该档位通过了认证、世界数据和存档检查。大型世界、内容较多的模组和活跃多人联机场景需要增加资源。

世界文件保存在 `/data/tModLoader/Worlds`，启用的模组配置保存在 `/data/tModLoader/Mods`，创意工坊下载内容保存在 `/data/steamMods`。世界大小和难度只影响新生成的世界，已有世界会保留存档中的设置。

**许可证信息：** tModLoader 和 Docker 封装项目分别以 MIT 许可证发布其代码。Terraria 及其他打包组件适用各自的许可证和使用条款。

## 为什么在 Sealos 上部署 tModLoader？

Sealos 基于 Kubernetes，提供可视化的应用部署和管理环境。

- **一键部署**：通过一个模板创建服务器、公网 TCP 入口和持久化存储。
- **资源可调**：通过资源卡片调整 CPU、内存和存储，按量付费。
- **世界持久化**：常规容器重启后继续使用已有的世界和模组数据。
- **Canvas 与 AI 运维**：部署后查看资源状态和日志，或通过 AI 对话描述配置修改需求。

## 部署指南

1. 打开 [tModLoader 模板页面](https://sealos.io/products/app-store/tmodloader)，点击 **Deploy Now**。
2. 选择世界大小和难度。需要模组时，填入以逗号分隔的创意工坊 ID；留空即可创建全新、初始无模组的世界。
3. 等待部署完成，通常需要 2-3 分钟，随后会进入 Canvas。服务器首次启动还需下载运行时并生成世界，网络速度、世界大小和模组可能增加数分钟等待时间。请等待服务器资源变为 Ready，并在日志中看到 `Server started`。
4. 打开服务器资源卡片，在网络设置中复制公网 TCP 地址和映射端口，再到环境变量中查看自动生成的 `TMOD_PASS`。公网端口由 Sealos 分配，具体数值可能与容器的 `7777` 端口不同。
5. 启动匹配的 **tModLoader v2026.7.3.0** 客户端。选择 **多人游戏（Multiplayer）→ 通过 IP 加入（Join via IP）**，选择兼容的角色，再输入页面显示的主机名和公网端口。例如，美国西部部署使用的地域主机名可能是 `tcp.usw-1.sealos.app`；端口请以自己的部署为准。
6. 在游戏的密码提示中输入 `TMOD_PASS`。按客户端提示完成兼容模组的同步后，进入世界。将主机名、端口、版本、模组列表和密码提供给受邀玩家。

## 配置

部署后，可以通过 Canvas、AI 对话或服务器资源卡片修改环境变量和资源上限。

### 模组

模板将 `workshop_mods` 同时传给 `TMOD_AUTODOWNLOAD` 和 `TMOD_ENABLEDMODS`。请使用以逗号分隔的数字 ID，例如 [Recipe Browser](https://steamcommunity.com/sharedfiles/filedetails/?id=2619954303) 的 ID 为 `2619954303`。同时加入所需依赖，并选择与固定服务器版本兼容的模组版本。

当 `TMOD_ENABLEDMODS` 留空时，服务器读取已保存的 `/data/tModLoader/Mods/enabled.json`，新部署中的该文件初始为空。若要清空所有启用的模组，请先停止服务器并备份世界，将该文件改为 `[]`，同时保持 `TMOD_ENABLEDMODS` 为空。移除内容模组可能影响已有世界。

模组下载完成后，可以清空 `TMOD_AUTODOWNLOAD`，并保留 `TMOD_ENABLEDMODS` 中的 ID，让后续启动直接使用已保存的文件。需要更新模组时，再填回下载 ID。

### 控制台与备份

打开服务器容器终端，执行原生控制台命令：

```sh
inject "playing"
inject "save"
inject "say Welcome to the server!"
```

复制 `/data` 进行备份前，先保存世界并停止服务器，确保备份数据一致。删除持久卷前，请将备份保存在部署之外。模板为正常关闭预留了最多 120 秒。

## 扩容

每个世界保持一个副本。增加活跃玩家、使用大型世界或模组包时，在 Canvas 中打开 StatefulSet 资源卡片，按需提高 CPU、内存和存储。修改后观察服务器响应、内存占用和存档耗时；模板实测的基础配置适用于个人低负载场景。

## 故障排查

- **连接或密码错误**：检查公网 TCP 主机名和分配端口，确认资源已 Ready，并查看当前 `TMOD_PASS`。输入主机名时去掉 `https://` 前缀。
- **版本或模组不匹配**：保持客户端稳定版本、模组版本和依赖与服务器一致。升级前先备份世界，再统一升级服务器和客户端。
- **启动缓慢或内存不足**：查看日志中的运行时和创意工坊下载进度。大型世界或模组包需要增加内存；世界生成或游戏运行过慢时，提高 CPU 配置。
- **依赖区域规则的模组**：上游镜像缺少 ICU。本模板启用 .NET 固定区域性模式（invariant globalization），同时允许创建命名区域性；格式化和排序使用固定规则。需要特定语言或地区行为的模组，应使用包含 ICU 的运行时镜像。

需要帮助时，可前往 [tModLoader 问题反馈](https://github.com/tModLoader/tModLoader/issues)、[Docker 封装项目问题反馈](https://github.com/JACOBSMILE/tmodloader1.4/issues) 或 [Sealos 社区](https://discord.gg/wdUn538zVP)。

## 许可证

请查阅 [Docker 封装项目许可证](https://github.com/JACOBSMILE/tmodloader1.4/blob/master/LICENSE.md) 和 [tModLoader 许可证](https://github.com/tModLoader/tModLoader/blob/stable/LICENSE)。Terraria 适用其发行商的条款。
