# 在 Sealos 上部署和托管 drawDB

drawDB 是一个基于浏览器的数据库实体关系图编辑器和 SQL 生成器。此模板会在 Sealos Cloud 上部署 drawDB 静态 Web 应用，并自动提供 HTTPS 访问地址。

![drawDB 编辑器截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/drawdb/website-screenshot.webp)

## 关于托管 drawDB

drawDB 以单个 Web 服务运行，由 NGINX 提供静态页面。用户打开编辑器后选择数据库方言，即可绘制 ER 图、导入 SQL、导出图表并生成 SQL。

此模板部署 drawDB 核心编辑器。图表数据保存在浏览器侧存储中，用户可以通过导出和导入文件进行迁移。

drawDB 还提供可选的分享后端 [drawdb-server](https://github.com/drawdb-io/drawdb-server)。该后端需要额外配置邮件服务和 GitHub Token，所以此模板保留默认的轻量编辑器流程。

## 常见使用场景

- **数据库架构设计**：为新数据库项目创建 ER 图。
- **SQL 审阅**：导入 SQL 脚本并可视化检查表关系。
- **迁移规划**：生成 SQL，并在实施前比较架构变化。
- **团队文档**：将图表导出为文件或图片，用于架构记录。
- **数据库学习**：探索 MySQL、PostgreSQL、SQLite、MariaDB、MSSQL、Oracle SQL 和通用模型。

## drawDB 托管依赖

Sealos 模板包含 drawDB Web 容器、Kubernetes Deployment、Service、Ingress、App 链接，以及一个用于直接打开编辑器路由的 NGINX 配置。

### 部署依赖

- [官方网站](https://drawdb.app/) - drawDB 托管产品站点
- [GitHub 仓库](https://github.com/drawdb-io/drawdb) - 源代码和 Docker 说明
- [官方文档](https://drawdb-io.github.io/docs) - drawDB 使用文档
- [可选分享后端](https://github.com/drawdb-io/drawdb-server) - 用于分享功能的独立服务

## 实现细节

**架构组件：**

此模板部署一个服务：

- **drawDB Web App**：由 NGINX 在 80 端口提供服务的静态 React 应用。

**配置：**

- App 链接打开 `/editor`，用户会直接进入编辑器。
- NGINX 配置会把 `/` 重定向到 `/editor`。
- 部署使用官方 `ghcr.io/drawdb-io/drawdb:v1.5.0` 容器镜像。
- 资源请求和限制遵循 docker-to-sealos 轻量 Web 服务基线。
- 默认编辑器流程无需数据库、持久卷或对象存储。

**许可证信息：**

drawDB 使用 [AGPL-3.0 许可证](https://github.com/drawdb-io/drawdb/blob/main/LICENSE)。此 Sealos 模板遵循相同的应用分发条款。

## 为什么在 Sealos 上部署 drawDB？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从部署到运维的生命周期。在 Sealos 上部署 drawDB 可以获得：

- **一键部署**：从应用商店模板页面部署 drawDB，无需编写 Kubernetes YAML。
- **自动 HTTPS**：每个部署都会获得带托管 TLS 的公网地址。
- **简洁运维**：通过 Canvas、AI 对话框和资源卡片完成后续调整。
- **按量计费**：以轻量基线资源运行静态编辑器。
- **Kubernetes 基础**：保留 Kubernetes 的可移植性和弹性，同时使用更简单的界面。

## 部署指南

1. 打开 [drawDB 模板](https://sealos.io/products/app-store/drawdb)，点击 **Deploy Now**。
2. 在弹窗中配置应用名称和公网域名。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续调整可以在 AI 对话框中描述需求，也可以点击相关资源卡片修改配置。
4. 通过 App 链接访问 drawDB。应用会打开 `/editor` 路由。
5. 选择 MySQL 或 PostgreSQL 等数据库方言，然后开始添加表和关系。

## 配置

默认部署可直接使用。若要启用分享功能，请单独部署 [drawdb-server](https://github.com/drawdb-io/drawdb-server)，配置邮件和 GitHub Token，并在自定义前端构建中通过 `VITE_BACKEND_URL` 指向该后端。

## 扩展

drawDB 是静态编辑器，通常一个副本即可稳定运行。调整资源的步骤：

1. 打开部署对应的 Canvas。
2. 点击 drawDB Deployment 资源卡片。
3. 调整 CPU、内存或副本数。
4. 在对话框中应用修改。

## 故障排查

### 编辑器打开后是空白图表

在启动弹窗中选择数据库方言，然后从编辑器工具栏添加表。

### 分享选项需要服务端配置

使用可选的 [drawdb-server](https://github.com/drawdb-io/drawdb-server) 项目，并将自定义前端构建连接到该后端。

### 获取帮助

- [官方文档](https://drawdb-io.github.io/docs)
- [GitHub Issues](https://github.com/drawdb-io/drawdb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [drawDB 官网](https://drawdb.app/)
- [drawDB GitHub 仓库](https://github.com/drawdb-io/drawdb)
- [drawDB Server](https://github.com/drawdb-io/drawdb-server)

## 许可证

此 Sealos 模板用于在 Sealos 上部署 drawDB。drawDB 本身使用 [AGPL-3.0 许可证](https://github.com/drawdb-io/drawdb/blob/main/LICENSE)。
