# 在 Sealos 上部署并托管 Odoo

Odoo 是开源企业应用套件，覆盖 CRM、销售、库存、会计、网站和运营管理。本模板会在 Sealos Cloud 上部署 Odoo 18.0，并自动配置 PostgreSQL、持久化 filestore、自定义 addon 存储和 HTTPS Ingress。

![Odoo 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odoo/website-screenshot.webp)

## 关于在 Sealos 上托管 Odoo

Odoo 是基于 PostgreSQL 的 Web 应用。首次打开时，Odoo 会进入数据库管理器，你可以创建第一个业务数据库，设置 master password，配置管理员账号，并选择要安装的应用。

这个 Sealos 模板会创建 KubeBlocks PostgreSQL 集群、用于创建专用 `odoo` 数据库角色的初始化 Job、持久化 `/var/lib/odoo` filestore、持久化 `/mnt/extra-addons` 存储、HTTPS Ingress 和 App 启动入口。

## 常见使用场景

- **CRM 和销售运营**：管理线索、商机、报价、订单和客户沟通。
- **库存和采购流程**：跟踪产品、供应商、库存流转和补货。
- **会计和开票**：通过 Odoo 应用运行发票和财务流程。
- **网站和电商**：使用 Odoo 模块构建业务网站或商店。
- **自定义业务应用**：通过 `/mnt/extra-addons` 添加自定义模块。

## Odoo 托管依赖

本模板包含 Odoo、PostgreSQL、数据库角色初始化 Job、Odoo 数据持久化存储、addon 持久化存储、Service、Ingress 和 App 启动入口。

### 部署依赖

- [Odoo Documentation](https://www.odoo.com/documentation/) - 官方文档
- [Odoo Docker Image Documentation](https://hub.docker.com/_/odoo) - 官方容器环境变量与卷说明
- [Odoo GitHub Repository](https://github.com/odoo/odoo) - 源码与发布记录

## 实现细节

### 架构组成

- **Odoo Web**：监听端口 `8069`
- **PostgreSQL**：保存 Odoo 业务数据库
- **数据库初始化 Job**：创建带 `CREATEDB` 权限的专用 `odoo` PostgreSQL role
- **Filestore 存储**：在 `/var/lib/odoo` 持久化附件和运行时数据
- **Extra Addons 存储**：在 `/mnt/extra-addons` 持久化自定义模块

### 资源配置

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Odoo | 20m | 200m | 51Mi | 512Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### 配置说明

模板通过 ConfigMap 写入 `odoo.conf`，为 Sealos Ingress 启用 proxy mode，并自动生成 Odoo master password。PostgreSQL 管理员凭据只注入到初始化 Job 中，Odoo 容器使用该 Job 创建的专用 `odoo` role。Odoo 使用 `512Mi` 内存，因为首次创建数据库会执行迁移和模块加载。

### 许可证信息

Odoo Community Edition 使用 [LGPL-3.0](https://github.com/odoo/odoo/blob/18.0/LICENSE)。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么在 Sealos 上部署 Odoo？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可以简化部署和运维。部署 Odoo 后，你可以获得：

- **一键部署**：从一个模板页面启动 Odoo、PostgreSQL、存储和 HTTPS。
- **托管 PostgreSQL**：使用 KubeBlocks PostgreSQL 保存 Odoo 业务数据库。
- **持久化 Filestore**：附件和运行时数据在重启后保留。
- **Addon 存储**：为自定义 Odoo 模块预留持久化路径。
- **简单运维**：通过 Sealos Canvas 扩容资源或查看日志。

## 部署指南

1. 打开 [Odoo 模板页面](https://sealos.io/products/app-store/odoo)，点击 **Deploy Now**。
2. 检查弹窗中的生成参数并部署。
3. 等待 PostgreSQL、角色初始化 Job 和 Odoo 就绪。
4. 打开生成的 URL，创建第一个 Odoo 数据库：
   - 使用模板默认值中生成的 master password
   - 输入数据库名称
   - 输入管理员邮箱和密码
   - 选择语言和国家
   - 创建数据库
5. 使用管理员账号登录，安装 CRM 或 Sales 等至少一个应用，并创建一条测试记录。

## 配置

通过 Odoo 设置管理应用、用户、公司、邮件、模块和业务流程。通过 Sealos Canvas 调整 CPU、内存、`/var/lib/odoo`、`/mnt/extra-addons` 或 PostgreSQL 存储。

## 扩缩容

本模板按单实例 Odoo 优化。安装应用、报表、导入或计划任务需要更多余量时，提高 CPU 和内存。随着业务数据增长，扩展 PostgreSQL 和 filestore 存储。

## 故障排查

**问题：Odoo 显示数据库管理器**
- 原因：还没有创建第一个业务数据库。
- 处理方法：使用生成的 master password 创建数据库。

**问题：Odoo 拒绝使用 postgres 用户启动**
- 原因：官方 Odoo 镜像拒绝应用容器使用 `postgres` 数据库角色启动。
- 处理方法：本模板会自动创建并使用专用 `odoo` role。

## 更多资源

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [Odoo Docker Image](https://hub.docker.com/_/odoo)
- [Odoo GitHub Issues](https://github.com/odoo/odoo/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Odoo Community Edition 本身使用 LGPL-3.0。
