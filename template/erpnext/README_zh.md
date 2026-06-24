# 在 Sealos 上部署和托管 ERPNext

ERPNext 是覆盖财务、库存、CRM、人力资源、制造、项目和运营的开源 ERP 平台。此模板会在 Sealos Cloud 上按官方 Frappe Docker 拓扑部署 ERPNext，并包含 MariaDB StatefulSet、Redis 缓存和队列服务、Worker、Scheduler、Websocket 和持久化站点文件。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/erpnext/website-screenshot.webp)

## 关于托管 ERPNext

ERPNext 基于 Frappe 框架运行，采用多服务运行时。Frontend Nginx 服务提供 Web UI，Backend 服务运行 Frappe 应用服务器，Websocket 服务处理实时更新，Worker 处理队列任务，Scheduler 执行周期任务。

此模板使用 MariaDB `11.4.7` 作为 ERPNext 外接数据库，因为 Frappe v16 在创建站点时需要 MariaDB 兼容的 DDL 语义。模板还会创建一个 Redis 7.2.7 KubeBlocks 集群，共同承载缓存和队列流量，并为 Frappe sites 与 logs 创建持久化卷。

## 常见使用场景

- **财务与会计**：管理发票、总账、付款、税务和报表。
- **库存与运营**：跟踪库存、仓库、采购和履约。
- **CRM 与销售**：管理线索、商机、报价和客户记录。
- **人力资源与项目**：协同员工、任务、工时和项目交付。

## ERPNext 托管依赖

此 Sealos 模板包含 ERPNext frontend、backend、websocket、队列 worker、scheduler、站点初始化 Jobs、MariaDB StatefulSet、一个 KubeBlocks Redis 集群、持久化站点存储、持久化日志、内部 Service 和 HTTPS Ingress。

### 部署依赖

- [ERPNext 文档](https://docs.erpnext.com/) - 官方 ERPNext 文档
- [Frappe Docker](https://github.com/frappe/frappe_docker) - 官方 Docker 部署拓扑
- [ERPNext GitHub](https://github.com/frappe/erpnext) - 源代码和发布版本

### 实现细节

**架构组件：**

- **Frontend**：使用 `frappe/erpnext:v16.21.1` 和 `nginx-entrypoint.sh`，监听 `8080` 端口。
- **Backend**：使用 `frappe/erpnext:v16.21.1`，作为 Frappe 应用服务器，监听 `8000` 端口。
- **Websocket**：运行 `frappe/socketio.js`，监听 `9000` 端口。
- **Queue Workers**：独立的 long 和 short 队列 worker。
- **Scheduler**：运行 ERPNext 周期性后台任务。
- **Configurator Job**：写入数据库、Redis 和 websocket 的全局站点配置。
- **Create Site Job**：创建默认 `frontend` 站点并安装 ERPNext。
- **MariaDB**：MariaDB `11.4.7` StatefulSet，作为 ERPNext/Frappe 站点数据的外接数据库。
- **Redis**：KubeBlocks Redis `7.2.7` 集群，共同承载缓存和队列流量。
- **文件存储**：站点和日志持久化卷挂载到 `/home/frappe/frappe-bench/sites` 和 `/home/frappe/frappe-bench/logs`。

**配置：**

部署表单会要求填写初始 ERPNext 管理员用户名和密码。模板会在创建站点时把配置的用户名写入内置 Administrator 账号，并启用用户名登录。

**许可证信息：**

ERPNext 使用 GNU General Public License v3.0。

## 为什么在 Sealos 上部署 ERPNext？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端 IDE 开发到生产部署与运维的完整应用生命周期。它非常适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 ERPNext，你可以获得：

- **一键部署**：一次部署完整 ERPNext 栈，包括数据库、缓存、队列、Worker 和 Ingress。
- **易于自定义**：通过 Sealos UI 调整资源和环境变量。
- **无需 Kubernetes 专业知识**：无需手动维护 Kubernetes 资源即可运行多服务 ERP 系统。
- **内置持久化存储**：重启后保留站点文件、上传文件和日志。
- **即时公网访问**：自动获得 HTTPS ERPNext 地址。

在 Sealos 上部署 ERPNext，把精力放在业务运营上。

## 部署指南

1. 打开 [ERPNext 模板](https://sealos.io/products/app-store/erpnext)，点击 **Deploy Now**。
2. 在弹窗中配置管理员用户名和密码。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 通过提供的 URL 访问应用：
   - **ERPNext Desk**：使用部署时配置的管理员用户名和密码登录。
5. 首次使用管理员账号登录后会进入 ERPNext 初始化向导。完成账号、组织、币种和科目表步骤后即可使用 Desk。

## 配置

ERPNext 会创建初始站点 `frontend`，与官方 Frappe Docker 示例一致。模板会把站点文件和日志保存在持久化卷中。

## 扩缩容

ERPNext 包含独立的 frontend、backend、websocket、worker、scheduler、MariaDB 和 Redis 组件。队列堆积时增加 worker 资源，Web 流量增加时提升 frontend 资源，应用延迟上升时提升 backend 资源。

## 故障排查

### 登录页面没有立即就绪

- 原因：站点创建 Job 需要先完成，frontend 才能提供 ERPNext Desk。
- 解决办法：在 Canvas 中检查 `create-site` Job、MariaDB StatefulSet、Redis Cluster 和 frontend 日志。

### 后台任务延迟

- 原因：队列 worker 或 Redis 资源饱和。
- 解决办法：增加 queue worker CPU 和内存，然后检查 Redis 集群。

## 更多资源

- [ERPNext 文档](https://docs.erpnext.com/)
- [Frappe Framework 文档](https://frappeframework.com/docs)
- [Frappe Docker](https://github.com/frappe/frappe_docker)

## 许可证

此 Sealos 模板使用 Apache License 2.0。ERPNext 本身使用 GNU General Public License v3.0。
