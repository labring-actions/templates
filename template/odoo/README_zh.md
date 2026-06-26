# 在 Sealos 上部署并托管 Odoo

Odoo 是开源企业应用套件，覆盖 CRM、销售、库存、会计、网站和运营管理。本模板会在 Sealos Cloud 上部署 Odoo 18.0，并自动配置 PostgreSQL、持久化 filestore、自定义 addon 存储和 HTTPS Ingress。

![Odoo 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odoo/website-screenshot.webp)

## 关于在 Sealos 上托管 Odoo

Odoo 是基于 PostgreSQL 的 Web 应用。全新部署首次打开时会进入数据库管理器，你需要先创建第一个业务数据库，并在创建数据库时设置该数据库的管理员账号。

这个 Sealos 模板会创建 KubeBlocks PostgreSQL 集群、专用 `odoo` 数据库角色、持久化 `/var/lib/odoo` filestore、持久化 `/mnt/extra-addons` 存储、Service、HTTPS Ingress 和 App 启动入口。模板还会在启动时处理空的默认 `odoo` 数据库，确保首次数据库管理页面可以正常打开。

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

**架构组成：**

- **Odoo Web**：在 `8069` 端口提供浏览器界面。
- **PostgreSQL**：通过 KubeBlocks 托管集群保存 Odoo 业务数据库。
- **数据库初始化 Job**：创建带 `CREATEDB` 权限的专用 `odoo` PostgreSQL role。
- **启动检查**：等待 PostgreSQL 就绪，并只在默认 `odoo` 数据库为空且未初始化时删除它。
- **Filestore 存储**：在 `/var/lib/odoo` 持久化附件和运行时数据。
- **Extra Addons 存储**：在 `/mnt/extra-addons` 持久化自定义模块。

**资源配置：**

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Odoo | 20m | 200m | 51Mi | 512Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

**配置说明：**

模板通过 ConfigMap 写入 `odoo.conf`，为 Sealos Ingress 启用 proxy mode，并自动生成 Odoo master password。PostgreSQL 管理凭据来自 KubeBlocks 托管 Secret，Odoo 使用专用 `odoo` role 连接数据库。Odoo 使用 `512Mi` 内存，因为首次创建数据库会执行迁移和模块加载。

**许可证信息：**

Odoo Community Edition 使用 [LGPL-3.0](https://github.com/odoo/odoo/blob/18.0/LICENSE)。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么在 Sealos 上部署 Odoo？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，统一了应用部署、运维和生命周期管理。部署 Odoo 后，你可以获得：

- **一键部署**：从一个模板页面启动 Odoo、PostgreSQL、存储和 HTTPS。
- **托管 PostgreSQL**：使用 KubeBlocks PostgreSQL 保存 Odoo 业务数据库。
- **内置持久化存储**：附件、运行时数据和自定义 addon 在重启后保留。
- **即时公网访问**：自动生成 HTTPS 访问地址，无需手动配置 Ingress 或证书。
- **简单运维**：通过 Sealos Canvas 调整资源、查看日志和更新设置。
- **按量使用资源**：从紧凑资源开始，随着业务增长再扩容。

## 部署指南

1. 打开 [Odoo 模板页面](https://sealos.io/products/app-store/odoo)，点击 **Deploy Now**。
2. 检查弹窗中的生成参数并部署。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。
4. 打开生成的 Odoo URL。全新部署不会先出现普通注册页，而是进入数据库管理器。
5. 创建第一个 Odoo 数据库：
   - **Master Password**：使用 Odoo ConfigMap 中 `odoo.conf` 里的 `admin_passwd` 生成值。
   - **Database Name**：输入业务数据库名称，例如 `company`。
   - **Email**：输入管理员登录邮箱。
   - **Password**：输入管理员登录密码。
   - **Language / Country**：选择语言和国家。
6. 点击 **Create database**，等待 Odoo 初始化基础模块。
7. 使用创建数据库时填写的管理员邮箱和密码登录。
8. 打开 **Apps**，安装 CRM、Sales、Inventory 或 Accounting 等需要的模块。

## 注册和登录

Odoo 的第一个管理员不是通过公开注册页创建的，而是在首次创建数据库时创建的。

第一个数据库创建完成后，可以通过 `/web/login` 或生成的应用 URL 登录。登录凭据是数据库创建表单中填写的管理员邮箱和密码。生成的 `admin_passwd` 只是数据库管理器的 master password，不是管理员登录密码。

## 配置

通过 Odoo 设置管理应用、用户、公司、邮件、模块和业务流程。运维类变更可以在 Sealos Canvas 中完成：在 AI 对话框描述要修改的内容，或点击资源卡片调整 CPU、内存、`/var/lib/odoo`、`/mnt/extra-addons` 或 PostgreSQL 存储。

## 扩缩容

本模板按单实例 Odoo 优化。安装应用、报表、导入或计划任务需要更多余量时，可以提高 CPU 和内存。随着业务数据增长，可以扩展 PostgreSQL 和 filestore 存储。

## 故障排查

**问题：Odoo 显示数据库管理器**
- 原因：还没有创建第一个业务数据库。
- 处理方法：使用 `odoo.conf` 中生成的 master password 创建数据库。

**问题：创建数据库后登录失败**
- 原因：master password 和管理员密码不是同一个密码。
- 处理方法：使用数据库创建表单中填写的管理员邮箱和密码登录。

**问题：Odoo 拒绝使用 postgres 用户启动**
- 原因：官方 Odoo 镜像不允许应用容器使用 `postgres` 数据库角色启动。
- 处理方法：本模板会自动创建并使用专用 `odoo` role。

## 更多资源

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [Odoo Docker Image](https://hub.docker.com/_/odoo)
- [Odoo GitHub Issues](https://github.com/odoo/odoo/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Odoo Community Edition 本身使用 LGPL-3.0。
