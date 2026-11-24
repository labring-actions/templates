# 在 Sealos 上部署和托管 Huginn

Huginn 是自托管自动化平台，可监控事件、处理数据，并通过可视化界面触发 Agent 工作流。

![Huginn 项目](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/huginn/website-screenshot.webp)

## 关于 Huginn 托管

本模板以单副本 StatefulSet 运行 Huginn 官方镜像，内置 MariaDB 数据库并挂载 1 GiB 持久卷。部署时会创建名为 `admin` 的管理员账号，密码由模板输入提供。

Pod 就绪后访问 `/users/sign_in` 登录。**Agents** 页面是主要工作区，可创建 Agent、通过事件连接 Agent，并安排周期任务。数据库内容和 Agent 定义会在 Pod 重启后保留。

## 常见使用场景

- 监控网站、RSS 和 API 的变更。
- 将筛选后的事件转发到邮件、聊天或 Webhook 端点。
- 构建定时数据采集与转换流水线。
- 将多个 Agent 组合为事件驱动自动化流程。
- 为内部告警和个人监控任务搭建原型。

## Huginn 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 用于内置数据库和应用数据的 1 GiB 持久卷。
- 通过模板 input 提供的管理员密码。
- Agent 调用外部网站和 API 所需的出站网络访问。

## 为什么在 Sealos 上部署 Huginn？

- 一键部署即可通过公网 HTTPS 使用 Web 界面。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 持久化存储保留用户、Agent、事件和凭据。
- 按量计费的资源卡适配个人与团队自动化负载。
- 通过 Canvas 查看 StatefulSet、Service、Ingress 和 PVC。
- 在 Sealos 桌面中通过 AI 对话了解部署情况。

## 部署指南

1. 打开 [Huginn 模板](https://sealos.io/products/app-store/huginn)，点击 **Deploy Now**。
2. 输入初始管理员密码，保留自动生成的应用名称，并确认资源规格。
3. 等待 2-3 分钟让数据库迁移完成，然后从 App 卡片打开公网地址。
4. 使用 `admin` 和第 2 步的密码登录，进入 **Agents** 页面。
5. 创建一个测试 Agent，再打开 Canvas 查看 StatefulSet、Service、Ingress 和持久卷。

## 许可证

Huginn 使用 [MIT License](https://github.com/huginn/huginn/blob/master/LICENSE) 许可证。
