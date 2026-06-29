# 在 Sealos 上部署和托管 Syncthing

Syncthing 是持续运行的点对点文件同步系统，提供浏览器管理界面。此模板会在 Sealos Cloud 上部署带持久化 `/var/syncthing` 存储和公网 HTTPS 访问的 Syncthing。

![Syncthing 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/syncthing/website-screenshot.webp)

## 关于托管 Syncthing

Syncthing 会在设备之间直接同步文件，并把设备身份、配置和同步数据保存在本地数据目录中。Sealos 模板使用 StatefulSet 运行 Syncthing，让 `/var/syncthing` 在重启后继续保留。

Web GUI 通过 Sealos HTTPS Ingress 暴露在 `8384` 端口。模板也在内部 Service 中定义了同步端口，部署后可以在 Syncthing GUI 中添加远程设备。

## 常见使用场景

- **私有文件同步**：在可信设备之间同步文件夹，无需中心化 SaaS 账号。
- **自托管备份流程**：在 Sealos 工作空间中保存重要文件夹副本。
- **跨设备共享**：通过 Syncthing 设备 ID 配对桌面、服务器和边缘设备。
- **常驻同步节点**：为个人或团队同步运行稳定在线节点。

## Syncthing 托管依赖

此模板包含 Syncthing 容器、StatefulSet、持久化卷、GUI 和同步流量 Service 端口、HTTPS Ingress 和 App 资源。

### 部署依赖

- [Syncthing 官网](https://syncthing.net/) - 产品介绍
- [Syncthing 文档](https://docs.syncthing.net/) - 用户和管理文档
- [Syncthing Docker README](https://github.com/syncthing/syncthing/blob/main/README-Docker.md) - 官方 Docker 指南
- [Syncthing GitHub 仓库](https://github.com/syncthing/syncthing) - 源码和问题反馈

### 实现细节

**架构组件：**

- **Syncthing StatefulSet**：运行 `syncthing/syncthing:2.1.1`。
- **持久化卷**：保存 `/var/syncthing`，包括配置、身份和同步数据。
- **Service**：在 `8384` 暴露 GUI 流量，并在 `22000` 暴露同步流量。
- **Ingress 和 App 入口**：通过 Sealos 生成的 HTTPS URL 暴露 GUI。

**配置：**

- `device_name` 设置可见设备名称。
- `STGUIADDRESS=0.0.0.0:8384` 让 Web GUI 可通过 Sealos Ingress 访问。
- `STNODEFAULTFOLDER=true` 表示启动时不自动创建默认同步文件夹。

**许可证信息：**

Syncthing 使用 MPL-2.0 License。此 Sealos 模板提供在 Sealos Cloud 上运行 Syncthing 的部署配置。

## 为什么在 Sealos 上部署 Syncthing？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署和运维流程。在 Sealos 上部署 Syncthing，可以获得一键部署、自动 HTTPS、持久化存储、资源控制和基于 Canvas 的更新能力，用于运行常驻同步节点。

## 部署指南

1. 打开 [Syncthing 模板](https://sealos.io/products/app-store/syncthing)，点击 **Deploy Now**。
2. 如需自定义可见设备名，配置 `device_name`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可以在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 打开生成的公网 URL。
5. 在 Syncthing GUI 中按提示设置 GUI 用户名和密码。
6. 在 Syncthing Web 界面中添加远程设备和文件夹。

## 配置

部署后可以通过以下方式配置 Syncthing：

- **Syncthing GUI**：添加设备、文件夹、凭据和同步偏好。
- **AI 对话**：更新环境变量或资源设置。
- **资源卡片**：在 Canvas 中调整 CPU、内存和持久化存储。
- **持久化卷**：保留 `/var/syncthing` 以保持设备 ID。

## 扩缩容

Syncthing 通常作为单个稳定节点运行，因为设备身份保存在持久化存储中。同步更大文件夹或更多设备时，可以增加 CPU、内存或存储容量。

## 故障排查

### GUI 要求设置凭据

- 原因：Syncthing 建议为可公网访问的 GUI 设置保护。
- 解决方法：在 Syncthing Web 界面中设置 GUI 用户名和密码。

### 远程设备无法连接

- 原因：公网点对点连接可能需要显式设备地址或 relay 配置。
- 解决方法：如果自动发现效果有限，请在 Syncthing GUI 中手动添加远程设备地址。

### 设备身份变化

- 原因：持久化卷被删除或替换。
- 解决方法：更新工作负载时保留 `/var/syncthing` 卷。

## 更多资源

- [Syncthing 入门指南](https://docs.syncthing.net/intro/getting-started.html)
- [Syncthing Docker README](https://github.com/syncthing/syncthing/blob/main/README-Docker.md)
- [Syncthing Forum](https://forum.syncthing.net/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为部署配置提供给 Sealos 用户使用。Syncthing 本身基于 [MPL-2.0 License](https://github.com/syncthing/syncthing/blob/main/LICENSE) 授权。
