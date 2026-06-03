# 在 Sealos 上部署和托管 Ever Gauzy

Ever Gauzy 是一款开源业务管理平台，覆盖 ERP、CRM、HRM、ATS、项目管理和时间追踪等场景。这个模板会在 Sealos 上部署官方 Ever Gauzy 演示版 Web 应用、API 服务、PostgreSQL 数据库，以及用于公开资源的持久化存储。

## 关于 Ever Gauzy 托管

Ever Gauzy 采用多服务架构。Web 应用负责浏览器界面，API 服务负责身份验证和业务数据处理，PostgreSQL 用来存储组织、用户、任务、工时、项目、发票等工作区数据。

此 Sealos 模板会通过 KubeBlocks 创建 PostgreSQL 16.4 数据库，初始化 `gauzy` 数据库，为 Web UI 和 API 分别创建公网访问地址，并为 API 公开资源挂载持久化存储。API 首次启动时会执行演示模式的数据库迁移和数据初始化，因此登录页完全可用前通常需要等待几分钟。

## 常见使用场景

- **业务运营工作台**：集中管理团队、组织、客户、项目、任务和发票。
- **HR 与员工管理**：管理员工、团队、可用时间、角色、权限和内部流程。
- **工时追踪与项目交付**：通过工时表、仪表盘、任务视图和项目模块支持交付团队协作。
- **招聘与 ATS 流程**：体验候选人管理、应聘记录和面试排期等功能。
- **开源 ERP 评估**：在定制生产环境前，先验证 Gauzy 的模块化 ERP、CRM 和 HRM 能力。

## Ever Gauzy 托管依赖

此 Sealos 模板已经包含演示部署所需的运行依赖：

- **Ever Gauzy Webapp**：使用官方演示 Web 镜像提供浏览器界面。
- **Ever Gauzy API**：使用官方演示 API 镜像提供后端接口。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4 数据库，并初始化 `gauzy` 数据库。
- **API 公开资源存储**：为 API 公开文件和初始化集成图标提供 1 GiB 持久化卷。

### 部署依赖

- [官方网站](https://gauzy.co/) - 产品信息与下载入口
- [源码仓库](https://github.com/ever-co/ever-gauzy) - 应用源码和上游文档
- [GitHub Packages](https://github.com/ever-co/ever-gauzy/pkgs/container/gauzy-api-demo) - 官方演示容器镜像

## 实现细节

**架构组件：**

此模板会部署四个主要组件：

- **Web UI**：在 4200 端口提供 Gauzy 浏览器界面，并连接到公网 API 地址。
- **API 服务**：在 3000 端口提供 REST 和应用接口，负责执行数据库迁移和演示数据初始化。
- **PostgreSQL**：存储 Gauzy 的工作区、租户、用户、任务、工时追踪和配置数据。
- **公开资源持久化卷**：持久化 API 启动时复制的公开资源，包括初始化集成图标和上传文件。

**配置说明：**

此模板以演示模式运行 Ever Gauzy。模板会自动生成 JWT 与会话密钥，关闭 Redis 后台队列以减少单实例部署资源，并为 Web UI 和 API 分别暴露公网域名，因为官方生产 Web 容器不会在内部代理 API 请求。

已验证的最小资源配置如下：

- **API StatefulSet**：CPU 500m、内存 768 MiB，`--max-old-space-size=512`
- **Web Deployment**：CPU 200m、内存 512 MiB
- **PostgreSQL Cluster**：CPU 200m、内存 256 MiB，遵循 Sealos KubeBlocks 数据库基线

**许可证信息：**

Ever Gauzy 使用 AGPL-3.0 许可证。此 Sealos 模板仅用于便捷部署，不改变上游应用许可证。

## 为什么在 Sealos 上部署 Ever Gauzy？

Sealos 是基于 Kubernetes 的 AI 云操作系统，可以帮助你部署和管理多服务应用，而不必手写 Kubernetes 编排文件或维护集群基础设施。

在 Sealos 上部署 Ever Gauzy 后，你可以获得：

- **一键部署**：通过一个模板同时启动 Web UI、API、数据库、存储、服务和 Ingress。
- **托管公网访问**：Sealos 会为 Web UI 和 API 自动分配 HTTPS 公网地址。
- **持久化存储**：数据库数据和 API 公开资源可以在 Pod 重启后保留。
- **Canvas 运维**：部署完成后，可以通过 Sealos Canvas、AI 对话和资源卡片调整资源或检查服务。
- **按量使用资源**：先使用已验证的最小资源配置，业务增长后再按需扩容。

## 部署指南

1. 打开 [Ever Gauzy 模板](https://sealos.io/products/app-store/ever-gauzy)，点击 **Deploy Now**。
2. 保留自动生成的默认配置，或按需调整应用名称和域名前缀。
3. 等待部署完成。首次启动通常需要 6-10 分钟，因为 API 会执行数据库迁移和演示数据初始化。
4. 通过部署后生成的地址访问应用：
   - **Web UI**：打开 Ever Gauzy 应用卡片中的 Web 地址。
   - **API Endpoint**：使用 API 地址进行健康检查或接口访问。
5. 在登录页使用以下任一演示账号：
   - **Super Admin**：`admin@ever.co` / `admin`
   - **Employee**：`employee@ever.co` / `12345678`
6. 在演示模式下，登录页可能会自动填入 Super Admin 账号，或显示演示账号按钮。若页面已填好演示账号，可以直接点击 **Log In**。

## 配置说明

部署完成后，你可以通过以下方式管理 Ever Gauzy：

- **AI 对话**：描述你想调整的资源或配置，让 Sealos 自动应用变更。
- **资源卡片**：在 Canvas 中打开 Web、API、PostgreSQL、Service、Ingress 或 App 资源卡片，查看或修改配置。
- **Gauzy 界面**：登录后使用侧边栏进入仪表盘、任务、员工、项目、工时、客户、发票等模块。

此模板主要面向演示和评估场景。若用于生产环境，请先评估 SMTP、OAuth、Redis Worker、备份、访问控制以及组织内部安全要求，再处理真实业务数据。

## 扩容

如需扩容：

1. 打开 Ever Gauzy 部署对应的 Canvas。
2. 点击 API StatefulSet 或 Web Deployment 资源卡片。
3. 如果启动、导入或活跃使用变慢，可以提高 CPU 和内存资源。
4. 在对话框中应用变更，并等待新的 Pod 就绪。

## 故障排查

### 首次启动需要几分钟

API 首次启动会执行数据库迁移和演示数据初始化。请等待 API Pod 就绪后再登录。如果登录页已经打开但 API 还没准备好，几分钟后刷新浏览器即可。

### 登录成功后页面加载较慢

演示数据包含 ERP、HRM、ATS、项目管理和工时追踪等多个模块。如果在较高负载下仪表盘或大型模块响应变慢，可以通过 Sealos 资源卡片增加 API 内存。

### API 健康检查在启动阶段失败

请在 Canvas 或资源卡片中查看 API Pod 日志。API 依赖 PostgreSQL 就绪，同时依赖初始化 Job 创建 `gauzy` 数据库。

## 更多资源

- [Ever Gauzy 官方网站](https://gauzy.co/)
- [Ever Gauzy 源码仓库](https://github.com/ever-co/ever-gauzy)
- [Ever Gauzy API 演示镜像](https://github.com/ever-co/ever-gauzy/pkgs/container/gauzy-api-demo)
- [Ever Gauzy Webapp 演示镜像](https://github.com/ever-co/ever-gauzy/pkgs/container/gauzy-webapp-demo)

## 许可证

Ever Gauzy 使用 AGPL-3.0 许可证。此 Sealos 模板用于便捷部署，并遵循模板仓库规范。
