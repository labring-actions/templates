# 在 Sealos 上部署和托管 Minecraft

Minecraft 是一款沙盒多人游戏，玩家可以一起建造、探索并长期运行共享世界。这个模板基于 `itzg/docker-minecraft-server` 在 Sealos Cloud 上部署 Minecraft Java 版服务器，并支持 Paper、Fabric 或 Forge 运行时。

![Minecraft 模板截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/minecraft/website-screenshot.webp)

## 关于 Minecraft 托管

这个模板以 StatefulSet 方式运行单节点 Minecraft 服务器。Sealos 会为游戏端口创建 NodePort Service，并为 `/data` 提供持久化存储，因此世界数据、服务器配置、日志、插件和运行时文件会在重启后保留。

默认配置使用 Paper，并将 `VERSION` 设置为 `LATEST`，部署时会解析为当前兼容的最新 Minecraft 服务端版本。模板固定使用 `itzg/minecraft-server:2026.5.3-java25` 镜像，为当前 Minecraft 版本提供 Java 25 运行环境，并为小型多人服务器设置了更稳妥的默认内存配置。

## 常见使用场景

- **好友生存服**：为小团队托管私有 Java 版世界。
- **Paper 插件服**：使用 Paper 启动，并在部署后通过持久化的 `/data/plugins` 目录添加插件。
- **Fabric 或 Forge 模组服**：选择 Fabric 或 Forge，并设置与模组包匹配的 Minecraft 版本。
- **课堂或社区服务器**：用 Sealos 管理存储和重启，让长期世界保持在线。

## Minecraft 托管依赖

Sealos 模板包含 Minecraft 服务端容器、持久化存储，以及用于客户端连接的 TCP NodePort Service。该应用不需要数据库，也没有 Web 应用登录流程。

### 部署依赖

- [Minecraft Server on Docker 文档](https://docker-minecraft-server.readthedocs.io/) - `itzg/minecraft-server` 运行时配置
- [itzg/docker-minecraft-server GitHub](https://github.com/itzg/docker-minecraft-server) - 镜像源码和配置参考
- [PaperMC 文档](https://docs.papermc.io/) - Paper 服务端文档
- [Sealos 应用商店](https://sealos.io/products/app-store/minecraft) - Minecraft 模板页面

### 实现细节

**架构组件：**

这个模板会部署以下资源：

- **Minecraft StatefulSet**：运行 `itzg/minecraft-server:2026.5.3-java25`，并根据参数选择服务端类型和版本。
- **持久化卷**：保存 `/data`，包括世界数据、服务端配置、插件、模组和日志。
- **NodePort Service**：暴露 TCP `25565` 端口，供 Minecraft Java 版客户端连接。

**配置：**

- `TYPE` 用于选择服务端运行时：`PAPER`、`FABRIC` 或 `FORGE`。
- `VERSION` 用于控制 Minecraft 服务端版本。默认 `LATEST` 会解析为所选运行时兼容的最新版本。
- `MEMORY` 设置为 `1024M`，容器内存限制为 `2G`，为启动、Paper patch 和 JVM 额外开销保留空间。
- `USE_AIKAR_FLAGS` 已启用，用于 JVM 参数优化。

**许可证信息：**

这个 Sealos 模板遵循仓库许可证。Minecraft 归 Mojang Studios 和 Microsoft 所有；`itzg/docker-minecraft-server` 由其上游项目维护，并遵循其自身许可证。

## 为什么在 Sealos 上部署 Minecraft？

Sealos 是基于 Kubernetes 的 AI 云操作系统，可以简化应用部署和管理。在 Sealos 上部署 Minecraft 可以获得：

- **一键部署**：从模板页面启动 Minecraft 服务器，不需要手写 Kubernetes YAML。
- **世界持久化**：世界数据保存在持久化存储中，容器重启后仍会保留。
- **运行时可选**：通过模板参数选择 Paper、Fabric 或 Forge。
- **公网 TCP 访问**：通过 Sealos 显示的 NodePort 从 Minecraft Java 版客户端连接。
- **资源可调整**：玩家数量或插件负载增加时，可以在 Sealos Canvas 中调整 CPU、内存和存储。

## 部署指南

1. 打开 [Minecraft 模板](https://sealos.io/products/app-store/minecraft)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **TYPE**：建议默认选择 `PAPER`；如果需要模组服务器，可以选择 `FABRIC` 或 `FORGE`。
   - **VERSION**：保留 `LATEST` 可使用当前兼容的最新服务端版本；如果插件或模组要求固定版本，请填写对应 Minecraft 版本。
3. 如果 Sealos 要求登录，请注册或登录 Sealos Cloud 账号。登录后会回到模板部署流程。
4. 等待部署完成。首次启动 Paper 世界通常需要几分钟，因为服务端会下载运行时文件并生成初始世界。
5. 在 Canvas 中打开 Minecraft 的 Service 资源，找到 `25565` 对应的公网端口，例如 `25565:33789/TCP`。
6. 在 Minecraft Java 版客户端中使用区域域名和映射端口连接：
   - **服务器地址**：`usw-1.sealos.io:<映射端口>`
   - 示例：`usw-1.sealos.io:33789`

## 访问与登录

Minecraft 不是 Web 应用，也不会创建模板专属的网页账号。玩家需要用自己的 Minecraft Java 版客户端和正常的 Minecraft/Microsoft 账号进入游戏。

模板默认不启用白名单。如果需要私有白名单，可以在 Sealos 中打开运行中的服务器文件或控制台，并根据服务器策略配置 Minecraft `server.properties`、`whitelist.json` 或 RCON。

## 配置

部署后，可以通过 Sealos 管理服务器：

- **AI 对话框**：描述要修改的资源或配置，让 AI 协助应用变更。
- **资源卡片**：打开 StatefulSet、Service 或存储卡片，查看并调整设置。
- **服务器文件**：通过持久化的 `/data` 目录管理插件、模组、日志和世界数据。
- **Minecraft 控制台/RCON**：启用后可通过服务器日志或兼容 RCON 的工具执行管理员命令。

## 扩容

Minecraft 服务器通常采用纵向扩容，而不是增加副本，因为单个世界进程持有游戏状态。若要支持更多玩家或更重的插件负载：

1. 打开该部署的 Canvas。
2. 点击 Minecraft StatefulSet 资源卡片。
3. 增加 CPU 和内存限制；如需提高 JVM 堆内存，再同步调整 `MEMORY`。
4. 当世界、插件或备份接近当前容量时，提前扩展持久化存储。

## 故障排查

### 服务已部署但客户端无法连接

- 确认 Pod 已经是 `Running` 且 Ready。
- 打开 Service 资源，复制 `25565` 映射出来的 NodePort。
- 使用 Sealos 区域域名和映射端口连接，不要使用内部 ClusterIP。

### Paper、Fabric 或 Forge 启动失败

- 检查所选 `VERSION` 是否被当前 `TYPE` 支持。
- 如果是 Fabric 或 Forge 模组包，确认模组与 Minecraft 版本一致。
- 在 Sealos 中查看服务端日志，定位 Java 版本、模组加载或 EULA 相关错误。

### 服务器需要更多容量

- 提高 StatefulSet 的内存和 CPU 限制。
- 保持 JVM 堆内存低于容器内存限制，为启动过程和原生开销留出余量。
- 在世界或备份占满磁盘前扩展持久化卷。

### 获取帮助

- [Minecraft Server on Docker 文档](https://docker-minecraft-server.readthedocs.io/)
- [itzg/docker-minecraft-server Issues](https://github.com/itzg/docker-minecraft-server/issues)
- [Sealos 文档](https://sealos.io/docs/)

## 更多资源

- [PaperMC 下载](https://papermc.io/downloads)
- [Fabric 文档](https://docs.fabricmc.net/)
- [Forge 文档](https://docs.minecraftforge.net/)
- [Minecraft EULA](https://www.minecraft.net/eula)

## 许可证

这个 Sealos 模板遵循仓库许可证。Minecraft、Paper、Fabric、Forge 和 `itzg/docker-minecraft-server` 分别遵循各自上游项目的许可证和使用条款。
