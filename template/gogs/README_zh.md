# 在 Sealos 上部署和托管 Gogs

Gogs 是轻量级自托管 Git 服务，支持仓库、Issue、合并请求、Webhook 和简洁的 Web 界面。

![Gogs 文档](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gogs/website-screenshot.webp)

## 关于 Gogs 托管

本模板以单副本 StatefulSet 运行 Gogs，使用 SQLite 存储，并将 1 GiB 持久卷挂载到 `/data`。安装流程已锁定，服务会直接使用内置生产配置和自动生成的密钥启动。

打开公网地址并注册第一个账号。Gogs 会将这个账号设为站点管理员，可继续管理用户、仓库和站点设置。仓库数据与 SQLite 数据库会在 Pod 重启后保留。

## 常见使用场景

- 为小团队或个人项目托管私有 Git 仓库。
- 通过 Issue、合并请求和行内评论进行代码评审。
- 使用仓库 Webhook 触发轻量 CI 流程。
- 在私有网络内部镜像代码仓库。
- 为实验室和演示环境提供独立的 Git 平台。

## Gogs 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 用于仓库和 SQLite 数据库的 1 GiB 持久卷。
- 用于访问 Web 界面的现代浏览器。
- 使用 HTTPS 远程地址的 Git 客户端；本模板已关闭 SSH 访问。

## 为什么在 Sealos 上部署 Gogs？

- 一键部署即可获得公网 HTTPS Git 服务。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 持久化存储保留仓库、用户、Issue 和附件。
- 按量计费的资源卡让小规模 Git 服务保持低成本。
- 通过 Canvas 查看 StatefulSet、Service、Ingress 和 PVC。
- 在 Sealos 桌面中通过 AI 对话获取部署指导。

## 部署指南

1. 打开 [Gogs 模板](https://sealos.io/products/app-store/gogs)，点击 **Deploy Now**。
2. 保留自动生成的应用名称或自定义名称，确认 1 GiB 存储规格后提交部署。
3. 等待 2-3 分钟让 StatefulSet 就绪，然后从 App 卡片打开公网地址。
4. 注册第一个账号，Gogs 会将该账号设为站点管理员。
5. 创建一个仓库，再打开 Canvas 查看 StatefulSet、Service、Ingress 和持久卷。

## 许可证

Gogs 使用 [MIT License](https://github.com/gogs/gogs/blob/main/LICENSE) 许可证。
