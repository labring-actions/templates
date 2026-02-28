# 在 Sealos 上部署并托管 OpenCart

OpenCart 是一个开源电商平台，用于搭建和管理在线商店。该模板会在 Sealos Cloud 上部署 OpenCart，并自动配置托管 MySQL、持久化存储和 HTTPS Ingress。

![OpenCart Logo](./logo.png)

## 关于在 Sealos 上托管 OpenCart

这个模板中的 OpenCart 以 Kubernetes 有状态工作负载（StatefulSet）方式运行，并预置了首次自动安装能力。容器启动后会自动应用管理员凭据、设置公网 HTTPS 地址、完成 MySQL 后端初始化，并移除安装器路径，默认配置更安全。

部署过程还会通过 KubeBlocks 自动创建托管 MySQL 集群，因此数据库凭据来自 Kubernetes Secret，而不是硬编码在镜像里。Sealos 同时会配置公网 HTTPS 访问、Ingress 路由，以及用于商品图片和 OpenCart 运行数据的持久化卷。

部署完成后的运维操作在 Canvas 中进行。你可以通过 AI 对话描述变更需求，也可以直接点开资源卡片调整计算、存储和网络配置。

## 常见使用场景

- **在线零售商城**: 快速上线商品目录、购物车和结算流程。
- **数字商品商店**: 销售模板、插件、媒体资源等可下载内容。
- **区域化电商站点**: 按地区定制语言、税率和配送规则。
- **B2B 商品目录门户**: 为企业客户提供账号化访问和分级价格体系。
- **传统主机迁移**: 将 OpenCart 从共享主机迁移到 Kubernetes 底座。

## OpenCart 托管依赖

该 Sealos 模板已包含完整依赖: OpenCart 运行时、托管 MySQL、持久化卷、服务发现和 HTTPS Ingress。

### 部署依赖

- [OpenCart 官网](https://www.opencart.com/) - 产品概览与生态入口
- [OpenCart 文档](https://docs.opencart.com/) - 安装、管理与扩展说明
- [OpenCart GitHub 仓库](https://github.com/opencart/opencart) - 源码与版本发布
- [MySQL 文档](https://dev.mysql.com/doc/) - 数据库配置与运维参考
- [Sealos 文档](https://sealos.run/docs) - 平台使用与运维指南

## 实现细节

### 架构组件

该模板会部署以下资源:

- **OpenCart StatefulSet (`ghcr.io/yangchuansheng/opencart:4.1.0.3`)**: 在集群内提供店铺前台和管理后台服务。
- **托管 MySQL 集群 (`ac-mysql-8.0.30-1`)**: 由 KubeBlocks 提供关系型数据存储。
- **持久化卷 (`/var/www/html/image`, 0.1Gi)**: 保存商品图片和上传媒体文件。
- **持久化卷 (`/var/www/storage`, 0.1Gi)**: 保存应用存储数据、缓存和运行时文件。
- **Service + Ingress**: 集群内暴露服务，并对外提供 HTTPS 访问入口。

### 配置项

模板对外暴露以下部署参数:

- `OPENCART_USERNAME`: OpenCart 初始管理员用户名（默认 `admin`）
- `OPENCART_PASSWORD`: OpenCart 初始管理员密码（必填）
- `OPENCART_ADMIN_EMAIL`: OpenCart 初始管理员邮箱（默认 `admin@example.com`）

运行时行为:

- 启用自动安装（`OPENCART_AUTO_INSTALL=true`）。
- 启用安装器清理（`OPENCART_REMOVE_INSTALLER=true`）。
- 后台路径设置为 `admincp`（`/admincp`）。
- 数据库参数从 `${app_name}-mysql-conn-credential` Secret 键注入。
- 默认数据库名和表前缀分别为 `opencart` 与 `oc_`。

### 许可证信息

OpenCart 由官方项目按 GNU GPL 条款发布。完整许可证信息请以上游仓库和官网说明为准。

## 为什么选择在 Sealos 上部署 OpenCart？

Sealos 是一个构建在 Kubernetes 之上的 AI 辅助云操作系统，可简化生产级应用的部署与日常运维。将 OpenCart 部署到 Sealos 后，你可以获得:

- **一键部署**: 无需手写 Kubernetes 编排，即可同时启动 OpenCart 和托管 MySQL。
- **稳定底座，降低复杂度**: 享受 Kubernetes 能力，同时不必承担高门槛集群管理成本。
- **内置持久化存储**: 商品图片和 OpenCart 运行数据可在重启后持续保留。
- **安全公网访问**: 自动配置 HTTPS 域名入口与证书管理。
- **灵活可配置**: 可通过 Canvas 的 AI 对话和资源卡片完成后续调优。
- **按量计费更高效**: 根据真实访问与业务负载弹性使用资源。
- **统一运维视图**: 在同一平台上管理应用与数据库资源。

将 OpenCart 部署到 Sealos，把精力放在业务增长，而不是基础设施维护上。

## 部署指南

1. 打开 [OpenCart 模板页](https://sealos.io/products/app-store/opencart) 并点击 **Deploy Now**。
2. 在弹窗中配置部署参数:
   - `OPENCART_USERNAME`
   - `OPENCART_PASSWORD`
   - `OPENCART_ADMIN_EMAIL`
3. 等待部署完成（通常 2-3 分钟）。部署结束后会自动跳转到 Canvas。后续如需变更，可在对话框描述需求让 AI 自动调整，或点击对应资源卡片手动修改。
4. 通过系统生成域名访问应用:
   - **店铺前台**: `https://<app-host>.<domain>/`
   - **管理后台**: `https://<app-host>.<domain>/admincp`

## 配置与运维

部署完成后，你可以通过以下方式管理 OpenCart:

- **AI 对话**: 请求资源调优、重启或环境变量更新等操作。
- **资源卡片**: 在 Canvas 中直接调整 StatefulSet、Service、Ingress 与 MySQL 配置。
- **OpenCart 管理后台**: 配置商品目录、税费、物流、支付模块和扩展。

建议的上线后动作:

1. 轮换管理员凭据并启用强密码策略。
2. 完成店铺资料、时区、币种和语言环境配置。
3. 在正式上线前接入 SMTP、支付和物流能力。
4. 审核扩展权限，仅安装可信插件。

## 扩缩容建议

扩缩容可按以下步骤进行:

1. 在 Canvas 打开当前部署。
2. 当流量或插件负载上升时，提升 OpenCart StatefulSet 的 CPU 与内存。
3. 当目录查询或结算性能下降时，调优 MySQL 组件资源。
4. 当图片与运行数据增长时，扩容对应持久化卷。

该模板默认以单实例 OpenCart 为基线。生产环境通常先做垂直扩容，再结合 MySQL 调优逐步提升吞吐能力。

## 故障排查

### 常见问题

**问题: 前台出现数据库连接错误**
- 原因: MySQL 集群仍在初始化，或数据库凭据尚未就绪。
- 解决: 等待 MySQL 就绪后，确认应用 Pod 已使用最新 Secret 重启。

**问题: 访问 `/admin` 无法进入后台**
- 原因: 该模板后台路径配置为 `/admincp`。
- 解决: 使用 `https://<app-host>.<domain>/admincp` 登录后台。

**问题: 首次访问显示安装未完成**
- 原因: OpenCart 容器内自动安装流程仍在执行。
- 解决: 查看 Pod 日志，待初始化完成后再重试登录。

**问题: 上传较大商品图片失败**
- 原因: 当前上传限制可能低于业务需求。
- 解决: 在 Canvas 中提高相关 Ingress 与运行时限制参数。

### 获取帮助

- [OpenCart 文档](https://docs.opencart.com/)
- [OpenCart GitHub Issues](https://github.com/opencart/opencart/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [OpenCart 扩展市场](https://www.opencart.com/index.php?route=marketplace/extension)
- [OpenCart 社区论坛](https://forum.opencart.com/)
- [Sealos 文档](https://sealos.run/docs)

## 许可证

该 Sealos 模板遵循本仓库许可证约定。OpenCart 本体由上游项目按 GNU GPL 条款发布。
