# 在 Sealos 上部署和托管 PrestaShop

PrestaShop 是一个开源电商平台，可用于构建可定制的在线商店、商品目录、购物车、结账流程和商家后台。该模板会在 Sealos Cloud 上部署 PrestaShop 9.1.3，并自动配置由 KubeBlocks 管理的 MySQL 数据库、持久化应用存储和公开 HTTPS 入口。

![PrestaShop 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/prestashop/website-screenshot.webp)

## 关于 PrestaShop 托管

PrestaShop 是一个基于 PHP 和 Apache 的 Web 应用，后端依赖 MySQL。Sealos 模板会创建 PrestaShop 容器、MySQL 8 数据库、用于创建 `prestashop` 数据库的初始化任务、挂载到 `/var/www/html` 的持久化存储、内部 Service、HTTPS Ingress，以及 Sealos 应用入口。

模板会自动完成首次安装。部署过程中，它会创建你配置的管理员账号，安装商店，移除安装目录，并将后台管理入口暴露在 `/admin-dev/`。模板还内置了一个轻量的反向代理配置文件，让 PrestaShop 能在 Sealos Ingress 后面正确识别 HTTPS 访问。

应用文件保存在持久化卷中；商店数据、商品、订单、客户和配置保存在 MySQL 中。这样即使 Pod 重启，商店文件和业务数据也能保留，适合评估、演示和轻量级店铺场景。

## 常见使用场景

- **在线商店**：快速启动包含商品页、购物车、结账和客户账号的中小型电商站点。
- **商品目录和运营演示**：测试 PrestaShop 主题、目录结构、价格和促销流程。
- **商家后台培训**：通过后台仪表盘练习商品、订单、客户和店铺配置管理。
- **扩展测试**：在独立的 Sealos 工作空间中评估 PrestaShop 模块、支付集成和主题。
- **电商原型验证**：在投入更大生产配置前，验证电商项目想法和基础流程。

## PrestaShop 托管依赖

该 Sealos 模板包含所需运行组件：`prestashop/prestashop:9.1.3-apache` 容器镜像、KubeBlocks MySQL `ac-mysql-8.0.30-1` 集群、数据库初始化任务、持久化存储、Kubernetes Service、Ingress 和 Sealos 应用入口。

### 部署依赖

- [PrestaShop 项目官网](https://www.prestashop-project.org/) - 产品概览和社区项目信息
- [PrestaShop 文档](https://docs.prestashop-project.org/) - 用户和管理员文档
- [PrestaShop 开发者文档](https://devdocs.prestashop-project.org/) - 面向开发者和集成方的技术文档
- [PrestaShop GitHub 仓库](https://github.com/PrestaShop/PrestaShop) - 源码和版本信息
- [PrestaShop Docker 镜像](https://hub.docker.com/r/prestashop/prestashop) - 本模板使用的官方容器镜像

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **PrestaShop Web 服务**：运行 `prestashop/prestashop:9.1.3-apache`，监听 `80` 端口，提供前台商店、后台管理和 PHP 应用运行环境。
- **MySQL 数据库**：由 KubeBlocks 管理的 MySQL `ac-mysql-8.0.30-1`，存储店铺配置、商品、客户、购物车、订单、模块和员工账号。
- **MySQL 初始化任务**：等待 MySQL 就绪后创建使用 `utf8mb4` 字符集的 `prestashop` 数据库。
- **应用持久化存储**：将 `1Gi` 持久化卷挂载到 `/var/www/html`，保留已安装的应用文件和上传资源。
- **反向代理 ConfigMap**：注入 `defines_custom.inc.php`，让 PrestaShop 信任来自 Sealos HTTPS Ingress 的 `X-Forwarded-Proto` 和 `X-Forwarded-Host`。
- **Ingress 和应用入口**：通过生成的 HTTPS 域名暴露商店，并创建 Sealos 控制台入口。

**配置：**

模板会自动配置：

- `PS_INSTALL_AUTO=1`，容器启动时自动完成首次安装。
- `PS_INSTALL_DB=0`，数据库由 MySQL 初始化任务提前创建。
- `PS_DOMAIN=${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`，让前台和后台链接使用 Sealos 生成域名。
- `PS_ENABLE_SSL=1`，并配合 HTTPS 感知的反向代理配置。
- `PS_FOLDER_ADMIN=admin-dev`，后台入口为 `/admin-dev/`。
- `ADMIN_MAIL` 和 `ADMIN_PASSWD` 来自部署输入，用于创建第一个管理员账号。
- MySQL 连接信息来自 KubeBlocks 连接 Secret。

**资源配置：**

PrestaShop 容器使用经过测试的紧凑资源配置：`200m` CPU 和 `512Mi` 内存。`256Mi` 内存不足以完成首次安装，会导致 OOM 重启，因此不要把 Web 容器内存降到 `512Mi` 以下。

**许可证信息：**

PrestaShop 使用 Open Software License 3.0 许可证。该 Sealos 模板只是 PrestaShop 的部署配置，不改变上游应用许可证。

## 为什么在 Sealos 上部署 PrestaShop？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一管理应用部署、存储、网络和运维。在 Sealos 上部署 PrestaShop，你可以获得：

- **一键部署**：通过一个模板同时部署 PrestaShop、MySQL、存储、网络和控制台入口。
- **无需 Kubernetes 经验**：不用手写清单，也能使用 Kubernetes 的可靠性。
- **内置持久化数据**：应用文件和数据库数据可跨重启保留。
- **即时公开访问**：每次部署都会获得可访问前台和后台的 HTTPS 地址。
- **易于调整配置**：可通过 Sealos Canvas 和 AI 对话调整环境变量、CPU、内存和存储。
- **按量使用资源**：从紧凑资源配置开始，根据店铺规模再逐步扩容。

在 Sealos 上部署 PrestaShop，把精力放在店铺配置上，而不是基础设施维护上。

## 部署指南

1. 打开 [PrestaShop 模板](https://sealos.io/products/app-store/prestashop)，点击 **Deploy Now**。
2. 配置必填管理员参数：
   - `ADMIN_MAIL`：用于登录后台的管理员邮箱。
   - `ADMIN_PASSWD`：用于登录后台的管理员密码。
3. 等待部署完成。首次安装通常需要数分钟，因为 PrestaShop 会初始化 MySQL、安装商店并准备后台。
4. 从 Sealos 应用入口打开生成的 PrestaShop 地址。
5. 通过 `https://<your-app-host>.<SEALOS_CLOUD_DOMAIN>/` 访问前台商店。
6. 通过 `https://<your-app-host>.<SEALOS_CLOUD_DOMAIN>/admin-dev/` 访问后台管理。
7. 使用部署时配置的 `ADMIN_MAIL` 和 `ADMIN_PASSWD` 登录。如果保留默认值，请使用：
   - 邮箱：`admin@example.com`
   - 密码：`PrestaShopDemo2026!`
8. 首次登录后，建议在后台员工设置中修改管理员邮箱和密码，再用于真实数据。

客户账号从前台登录页创建。打开前台商店，进入登录入口，使用注册表单创建客户账号，即可测试下单流程。

## 配置

部署完成后，你可以通过以下方式配置 PrestaShop：

- **后台管理**：打开 `/admin-dev/`，管理商品、分类、订单、客户、模块、主题、支付、配送、税费和店铺偏好。
- **Sealos AI 对话**：描述你想调整的环境变量或资源配置，让 AI 协助应用变更。
- **资源卡片**：在 Canvas 中点击 StatefulSet、MySQL、Ingress 或存储卡片，查看并调整配置。
- **PrestaShop 模块**：在后台安装和配置支付、配送、分析、SEO 和前台主题模块。

如果后续添加自定义域名，请同步更新 PrestaShop 的商店 URL 设置，并保持 HTTPS 开启，确保前台和后台链接继续使用正确域名。

## 扩容

在 Sealos 上扩容 PrestaShop：

1. 打开 PrestaShop 部署对应的 Canvas。
2. 点击 PrestaShop StatefulSet 资源卡片。
3. 当商品目录、后台操作、模块负载或访问流量增加时，提高 CPU 或内存。
4. 应用变更并等待 Pod 重新就绪。

模板默认使用已通过安装和后台冒烟测试的最小资源配置。用于生产店铺前，建议提高应用内存，按业务规模调整 MySQL 资源，配置 SMTP，并确认备份和支付服务要求。

## 故障排查

### 首次启动需要数分钟

PrestaShop 会在第一次容器启动时自动安装。请等待 StatefulSet Pod 就绪后，再打开前台商店和 `/admin-dev/` 后台地址。

### 后台登录页无法打开

请在生成的 HTTPS 域名下使用 `/admin-dev/` 路径。如果部署后更换过公开域名，请更新 PrestaShop 的商店 URL 设置，或使用目标域名重新部署。

### 安装时容器重启

不要将 PrestaShop Web 容器内存降到 `512Mi` 以下。首次安装比稳定空闲状态需要更多内存。

### 客户注册或邮件通知无法发送邮件

发送订单、账号或密码重置邮件前，需要在 PrestaShop 后台配置 SMTP。模板本身不包含 SMTP 服务。

### 获取帮助

- [PrestaShop 文档](https://docs.prestashop-project.org/)
- [PrestaShop 开发者文档](https://devdocs.prestashop-project.org/)
- [PrestaShop GitHub Issues](https://github.com/PrestaShop/PrestaShop/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [PrestaShop 项目官网](https://www.prestashop-project.org/)
- [PrestaShop Docker 镜像](https://hub.docker.com/r/prestashop/prestashop)
- [PrestaShop Releases](https://github.com/PrestaShop/PrestaShop/releases)
- [PrestaShop 模块市场](https://addons.prestashop.com/)

## 许可证

该 Sealos 模板遵循本仓库的模板许可证。PrestaShop 本身使用 Open Software License 3.0 许可证。
