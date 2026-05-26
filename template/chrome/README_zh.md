# 在 Sealos 上部署和托管 Chrome

Chrome 是 Google 推出的网页浏览器，适合快速、安全、可定制地访问互联网。这个模板会在 Sealos Cloud 上部署 LinuxServer.io Chrome 容器，提供 Selkies 网页桌面界面、持久化浏览器存储和 HTTPS 访问入口。

## 关于 Chrome 托管

Chrome 会作为一个单实例浏览器桌面服务运行，你可以直接通过网页界面访问。该部署使用 `linuxserver/chrome` 镜像，自动启动 Chrome，并通过 Sealos 管理的 HTTPS 域名暴露 Selkies 桌面服务的 `3000` 端口。

模板会为 `/config` 自动配置持久化存储，因此浏览器配置、下载文件、设置和扩展可以在容器重启后保留。同时，模板还配置了 HTTP Basic Auth、启动/就绪/存活探针，以及受控的虚拟显示分辨率，让资源消耗更可预测。

这个模板适合个人云端浏览、网页测试、演示和轻量级远程浏览器场景。由于浏览器桌面具备较强的容器内操作能力，请妥善保管生成的密码，不要把公开访问地址分享给不可信用户。

## 常见使用场景

- **云端浏览器工作区**：在本地设备受限或性能不足时，通过浏览器运行远程 Chrome。
- **网页应用测试**：使用干净的远程浏览器配置测试网站，并保留必要设置。
- **远程排障**：从服务端浏览器打开页面、复现问题并观察行为。
- **演示环境**：为演示、培训或临时访问提供一个可控的浏览器会话。
- **持久化浏览器配置**：通过持久化存储保留 Cookie、扩展、书签和会话数据。

## Chrome 托管依赖

Sealos 模板包含托管 Chrome 所需的运行组件：

- `lscr.io/linuxserver/chrome:148.0.7778.178-1-ls95`
- 运行 Chrome/Selkies 容器的 StatefulSet
- 挂载到 `/config` 的持久化存储
- 用于浏览器访问的 Service 和 HTTPS Ingress
- 基于 ConfigMap 的启动脚本，用于以稳定参数启动 Chrome

### 部署依赖

- [Google Chrome](https://www.google.com/chrome/) - Chrome 官方网站
- [LinuxServer.io Chrome 文档](https://docs.linuxserver.io/images/docker-chrome/) - 容器配置与运行参数
- [linuxserver/docker-chrome GitHub 仓库](https://github.com/linuxserver/docker-chrome) - 上游镜像源码仓库
- [Sealos 应用商店](https://sealos.run/products/app-store/chrome) - Chrome 模板页面
- [Sealos Discord](https://discord.gg/wdUn538zVP) - 社区支持

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Chrome StatefulSet**：运行 LinuxServer.io Chrome 容器，并提供网页可访问的 Selkies 桌面。
- **Launcher ConfigMap**：安装 autostart 脚本，用配置的启动 URL 或 CLI 参数启动 Chrome。
- **持久化存储**：通过 1 GiB PVC 挂载 `/config`，保存浏览器配置和用户文件。
- **Service**：在集群内暴露容器的 HTTP 桌面界面，端口为 `3000`。
- **Ingress**：通过 Sealos 管理的 Ingress 和证书提供公网 HTTPS 地址。
- **App Link**：在 Sealos 应用视图中添加已部署的 Chrome 入口。

**配置：**

模板会从部署表单读取 `CHROME_CLI`，你可以填写启动 URL 或 Chrome CLI 参数。HTTP Basic Auth 由 `CUSTOM_USER` 和自动生成的密码启用；浏览器配置保存在 `/config`；Selkies 的公开分享和协作开关默认关闭。

为了在云端稳定运行，模板设置了 `PIXELFLUX_WAYLAND=false`、`MAX_RES=4096x2160`、`SELKIES_ENCODER=jpeg,x264enc`，并加入 `--disable-dev-shm-usage` 等 Chrome 启动参数。容器限制为 `200m` CPU 和 `1024Mi` 内存，requests 按 Sealos 资源阶梯规则从 limits 推导。

**许可证信息：**

上游 `linuxserver/docker-chrome` 仓库使用 GPL-3.0 许可证发布。Google Chrome 本身适用 Google 的相关条款；如果要在生产环境或共享环境中使用，请先确认适用的 Chrome 使用条款。

## 为什么在 Sealos 上部署 Chrome？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维、存储、网络和管理流程。在 Sealos 上部署 Chrome 可以获得：

- **一键部署**：无需编写 Kubernetes YAML，也不用手动维护服务器，即可启动远程 Chrome 桌面。
- **内置持久化存储**：通过持久卷保留浏览器数据和设置。
- **即时公网访问**：自动获得 HTTPS 访问地址，证书由 Sealos 管理。
- **易于定制**：可以在 Canvas、AI 对话框或资源卡中更新启动 URL、凭据、资源和存储。
- **Kubernetes 底座**：基于标准工作负载、服务、Ingress 和存储能力运行浏览器。
- **资源成本可控**：按需使用资源，并可根据负载调整 CPU、内存和存储。

当你需要快速获得远程浏览器，并希望专注于浏览或测试而不是维护基础设施时，可以选择在 Sealos 上部署 Chrome。

## 部署指南

1. 打开 [Chrome 模板](https://sealos.run/products/app-store/chrome)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **Chrome startup URL or CLI flags**：通过 `CHROME_CLI` 设置初始页面或额外 Chrome 参数。
   - **Custom user**：设置 HTTP Basic Auth 用户名，默认值为 `abc`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需修改配置，可以在 AI 对话框中描述需求让 AI 应用变更，也可以点击对应资源卡调整设置。
4. 通过生成的访问地址打开应用：
   - **Chrome Web Desktop**：使用配置的用户名和生成的密码登录，然后在网页界面中使用 Chrome。

## 配置

部署后，你可以通过以下方式配置 Chrome：

- **AI 对话框**：描述想要的变更，例如更新启动 URL、提升资源或调整环境变量。
- **资源卡**：打开 StatefulSet、Ingress 或存储资源卡，修改运行设置。
- **环境变量**：调整 `CHROME_CLI`、`CUSTOM_USER`、`PASSWORD`、`MAX_RES` 和 Selkies 相关设置。
- **持久化配置**：浏览器状态保存在 `/config`；如果需要保留大量下载文件或扩展，请适当增加存储容量。

## 扩缩容

Chrome 会作为单用户 StatefulSet 运行，副本数固定为 1。对这个模板来说，通常更适合做垂直扩容：

1. 打开该部署对应的 Canvas。
2. 点击 Chrome StatefulSet 资源卡。
3. 根据负载调整 CPU、内存或存储。
4. 在对话框中应用变更，并等待工作负载重启。

如果要打开复杂页面、播放视频、保留大量标签页或安装较多扩展，建议先增加内存，而不是增加副本数。

## 故障排查

### 常见问题

**Chrome 能打开，但网页加载失败或崩溃**
- 原因：浏览器类负载对内存比较敏感，复杂页面或多标签页尤其明显。
- 解决：提高 StatefulSet 内存限制，关闭不用的标签页，或降低虚拟显示分辨率。

**网页桌面黑屏或看不到 Chrome**
- 原因：桌面栈兼容性或启动时序可能导致浏览器窗口不可见。
- 解决：确认工作负载已就绪，保持 `PIXELFLUX_WAYLAND=false`，并确认 launcher ConfigMap 正确挂载。

**存储空间耗尽**
- 原因：下载文件、浏览器缓存、用户配置或崩溃报告可能占满 `/config` PVC。
- 解决：从浏览器配置目录中删除不需要的文件，或通过存储资源卡扩大 PVC。

**界面响应慢**
- 原因：远程浏览器渲染会受 CPU、内存、页面复杂度、网络延迟和显示分辨率影响。
- 解决：增加 CPU/内存，关闭高负载标签页，或在不需要 4K 输出时降低 `MAX_RES`。

### 获取帮助

- [LinuxServer.io Chrome 文档](https://docs.linuxserver.io/images/docker-chrome/)
- [linuxserver/docker-chrome Issues](https://github.com/linuxserver/docker-chrome/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Chrome 帮助](https://support.google.com/chrome/)
- [LinuxServer.io 文档](https://docs.linuxserver.io/)
- [Sealos](https://sealos.run/)

## 许可证

该 Sealos 模板作为 Sealos templates 仓库的一部分提供。上游 `linuxserver/docker-chrome` 项目使用 GPL-3.0 许可证，Google Chrome 适用 Google 的 Chrome 相关条款。
