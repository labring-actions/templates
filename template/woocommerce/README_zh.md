# 在 Sealos 上部署与托管 WooCommerce

WooCommerce 是基于 WordPress 构建的开源电商平台，可用于搭建和管理在线商店。该模板会在 Sealos Cloud 上部署 WooCommerce，并同时提供 WordPress、托管 MySQL、持久化存储与 HTTPS Ingress。

![WooCommerce Logo](./logo.png)

## 关于在 Sealos 托管 WooCommerce

这个模板中的 WooCommerce 运行在 WordPress StatefulSet 之上。启动阶段会由 init 容器调用 WP-CLI 自动完成 WordPress 引导、`wp-config.php` 生成、WooCommerce 插件安装与激活，首次登录即可进入可用状态。

部署过程中会通过 KubeBlocks 自动创建托管 MySQL 集群，并通过一个初始化 Job 在 WordPress 启动前创建应用数据库（`mydb`）。同时 Sealos 会提供公网 HTTPS 访问、域名路由，以及挂载到 `/var/www/html` 的持久化存储。

部署完成后，后续运维可在 Canvas 中进行：你可以通过 AI 对话描述变更，也可以直接在资源卡片中调整副本数与资源配置。

## 常见使用场景

- **DTC 品牌商城**：快速上线包含商品目录、购物车和结账流程的品牌店铺。
- **数字商品销售**：售卖软件、设计素材、课程资料等可下载商品。
- **区域化零售站点**：结合本地化主题和支付插件，部署面向不同区域的电商站点。
- **内容与电商一体化网站**：将 WordPress 内容发布能力与 WooCommerce 销售能力整合在同一平台。
- **小团队轻量运营**：先从单节点方案起步，再按订单增长逐步扩容。

## WooCommerce 托管依赖

该 Sealos 模板已包含完整依赖：WordPress 运行时、WooCommerce 插件自动激活、托管 MySQL、持久化卷、服务暴露与 HTTPS Ingress。

### 部署依赖文档

- [WooCommerce Documentation](https://woocommerce.com/documentation/) - 官方安装与店铺管理文档
- [WooCommerce GitHub Repository](https://github.com/woocommerce/woocommerce) - 源码与版本发布记录
- [WordPress Documentation](https://wordpress.org/documentation/) - WordPress 核心文档
- [WP-CLI Documentation](https://developer.wordpress.org/cli/commands/) - 初始化阶段所用命令参考
- [MySQL Documentation](https://dev.mysql.com/doc/) - 数据库参考文档

## 实现细节

### 架构组件

该模板会部署以下资源：

- **WordPress StatefulSet（`wordpress:6.9.1-php8.3-apache`）**：提供 Web 界面与 WooCommerce 商城前台。
- **WP-CLI Init 容器（`wordpress:cli-2.9.0-php8.3`）**：自动完成首次安装、管理员初始化、HTTPS 处理与 WooCommerce 激活。
- **MySQL 集群（`ac-mysql-8.0.30-1`）**：由 KubeBlocks 托管，提供持久化关系型存储。
- **MySQL 初始化 Job（`mysql:8.0.30`）**：等待数据库就绪后创建 `mydb` Schema。
- **持久化卷（`1Gi`）**：挂载到 `/var/www/html`，保存 WordPress 内容与插件数据。
- **Service + Ingress**：对内暴露 HTTP 服务，对外通过 HTTPS 域名访问。

### 配置项

模板暴露以下部署输入参数：

- `WP_ADMIN_USER`：WordPress 管理员用户名（默认：`admin`）
- `WP_ADMIN_PASSWORD`：WordPress 管理员密码（必填）
- `WP_ADMIN_EMAIL`：WordPress 管理员邮箱（默认：`admin@example.com`）
- `WP_SITE_TITLE`：站点标题（默认：`WooCommerce Store`）

运行时行为：

- 站点 URL 会自动设置为 `https://<app-host>.<sealos-domain>`。
- 启动时会自动更新 `home` 与 `siteurl`。
- WooCommerce 插件会以幂等方式安装并激活。
- 默认数据表前缀为 `wp_`。

### 许可证信息

WooCommerce 采用 [GNU General Public License v3.0](https://github.com/woocommerce/woocommerce/blob/trunk/LICENSE.md) 授权。WordPress 采用 GPLv2 或更高版本授权。

## 为什么在 Sealos 部署 WooCommerce？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，可显著简化应用部署与运维流程。将 WooCommerce 部署在 Sealos，你将获得：

- **一键部署**：无需手写 Kubernetes 清单，即可拉起 WordPress + WooCommerce + MySQL 整体栈。
- **托管数据库接入**：MySQL 自动创建并通过集群凭据完成连通。
- **内置持久化存储**：上传文件、主题和插件资源可稳定持久保存。
- **安全公网访问**：自动获得 HTTPS 访问入口与域名证书配置。
- **便捷自定义**：可在 Canvas 对话框与资源卡片中快速调整配置与资源。
- **按需付费扩展**：按实际流量与订单负载弹性调整计算与存储。
- **Kubernetes 级稳定性**：享受云原生能力，同时降低集群运维门槛。

把精力聚焦在店铺运营，而不是基础设施搭建。

## 部署指南

1. 打开 [WooCommerce 模板](https://sealos.io/products/app-store/woocommerce)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - `WP_ADMIN_USER`
   - `WP_ADMIN_PASSWORD`
   - `WP_ADMIN_EMAIL`
   - `WP_SITE_TITLE`（可选）
3. 等待部署完成（通常 2-3 分钟）。部署完成后会自动跳转到 Canvas。后续若需变更，可在对话框中描述需求让 AI 自动执行，或点击资源卡片手动调整。
4. 打开系统生成的访问地址：
   - **商城前台**：`https://<app-host>.<domain>/`
   - **WordPress 管理后台**：`https://<app-host>.<domain>/wp-admin`

## 配置说明

部署完成后，你可以通过以下方式管理 WooCommerce：

- **AI 对话**：发起资源调整、环境变量修改、重启等变更请求。
- **资源卡片**：在 Canvas 中直接编辑 StatefulSet / Service / Ingress 参数。
- **WordPress 管理后台**：配置商品、主题、支付网关、税率规则和物流设置。

建议在部署后优先完成以下操作：

1. 修改管理员凭据，并启用强密码策略。
2. 在 WooCommerce 设置中配置币种、税率与配送区域。
3. 仅安装必要插件，降低运维复杂度与安全风险。
4. 建立定期备份与数据导出流程。

## 扩缩容

如需扩缩容，可按以下步骤操作：

1. 在 Canvas 中打开当前应用。
2. 流量增长时，优先提升 WordPress StatefulSet 的 CPU/内存。
3. 若结账或后台操作变慢，检查并提高 MySQL 组件资源。
4. 当媒体与商品数据增长超过基线容量时，扩展持久化存储。

## 故障排查

### 常见问题

**问题：出现 WordPress 或 WooCommerce 安装向导页面**
- 原因：初始化流程尚未完成，或 init 容器执行失败。
- 解决：查看 init 容器日志中的 WP-CLI 报错，并确认数据库初始化 Job 已成功完成。

**问题：无法登录 `/wp-admin`**
- 原因：管理员凭据与部署时输入参数不一致。
- 解决：核对部署时填写的 `WP_ADMIN_USER` 与 `WP_ADMIN_PASSWORD`。

**问题：启动阶段出现数据库连接错误**
- 原因：MySQL 集群仍在启动，或连接 Secret 尚未就绪。
- 解决：等待 MySQL 集群 Ready，并确认 MySQL 初始化 Job 执行成功。

**问题：HTTPS 下出现 mixed content 或重定向异常**
- 原因：站点 URL 与 Ingress Host 不一致，或转发协议处理被中断。
- 解决：检查 Ingress Host 配置，并确认站点 URL 指向系统生成的 HTTPS 域名。

### 获取帮助

- [WooCommerce Documentation](https://woocommerce.com/documentation/)
- [WooCommerce GitHub Issues](https://github.com/woocommerce/woocommerce/issues)
- [WordPress Support](https://wordpress.org/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [WooCommerce Extensions Marketplace](https://woocommerce.com/products/)
- [WooCommerce Developer Docs](https://developer.woocommerce.com/docs/)
- [WordPress Plugin Handbook](https://developer.wordpress.org/plugins/)
- [Sealos Documentation](https://sealos.run/docs)

## 许可证

本 Sealos 模板遵循仓库许可证条款。WooCommerce 项目本身采用 GPLv3 授权，WordPress 采用 GPLv2 或更高版本授权。
