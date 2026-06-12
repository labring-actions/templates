# 在 Sealos 上部署和托管 Matomo

Matomo 是一款开源网站分析平台，可用于跟踪访客行为、转化、营销活动和网站性能。此模板会在 Sealos Cloud 上部署 Matomo，包含官方 Apache/PHP 运行时、持久化应用存储，以及由 Sealos 管理的 MySQL 数据库。

## 关于 Matomo 托管

Matomo 以单个 Apache/PHP 应用容器运行，直接提供公网 HTTP 入口，并避免重启时出现 sidecar 配置漂移。Sealos 会通过 KubeBlocks 创建 MySQL 数据库，并为 `/var/www/html` 提供持久化存储，因此应用文件和生成的配置在重启后仍会保留。

首次访问时，Matomo 会打开安装向导。模板已经通过 Matomo 支持的环境变量预配置数据库主机、数据库用户名、密码、数据库名、表前缀和可信主机，因此可以直接在浏览器中继续向导并创建第一个超级用户账号。

## 常见使用场景

- **注重隐私的网站分析**：在保留数据控制权的同时跟踪网站流量。
- **营销活动和转化跟踪**：衡量推广活动、目标、漏斗和电商事件。
- **产品使用分析**：观察用户如何浏览产品文档、门户或 SaaS 控制台。
- **自托管报表**：为团队提供分析仪表盘，同时避免依赖第三方托管分析服务。

## Matomo 托管依赖

此 Sealos 模板包含所需运行服务：Matomo Apache/PHP 运行时、持久化存储和 MySQL 数据库。

### 部署依赖

- [Matomo 官方网站](https://matomo.org/) - 产品概览和文档
- [Matomo 安装指南](https://matomo.org/faq/on-premise/installing-matomo/) - 首次安装流程
- [Matomo Docker 镜像](https://hub.docker.com/_/matomo) - 官方容器镜像
- [Matomo GitHub 仓库](https://github.com/matomo-org/matomo) - 源码和版本发布

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Matomo 应用**：使用官方 Apache/PHP 镜像运行 Matomo 5.10.0，并在 80 端口提供 Web UI。
- **MySQL**：由 Sealos 管理的 KubeBlocks MySQL 集群，用于存储分析数据和应用设置。
- **持久化存储**：1 GiB 卷用于保存 `/var/www/html` 下的 Matomo 应用文件和生成配置。

**配置：**

- 公网入口通过 Sealos Ingress 暴露，并自动启用 HTTPS。
- 数据库连接值使用 Matomo 支持的 `MATOMO_DATABASE_*` 环境变量，并来自 Sealos 管理的 MySQL 凭据 Secret。
- 第一个 Matomo 管理员需要在安装向导中创建。
- 安装完成后请保持生成的公网 URL 稳定，因为 Matomo 会将其记录为可信主机。

**许可证信息：**

Matomo 使用 GPL-3.0 许可证。此 Sealos 模板使用仓库许可证发布。

## 为什么在 Sealos 上部署 Matomo？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、网络、存储和运维。在 Sealos 上部署 Matomo 可以获得：

- **一键部署**：通过现成模板部署 Matomo 和 MySQL，无需手写 Kubernetes YAML。
- **托管公网访问**：Sealos 会为 Matomo Web UI 创建 HTTPS 访问入口。
- **持久化数据**：应用文件和数据库数据都保存在持久化卷中。
- **便捷运维**：通过 Canvas、AI 对话和资源卡片调整资源或查看运行状态。
- **按量使用资源**：从较小资源配置开始，后续根据分析流量增长再扩容。

## 部署指南

1. 打开 [Matomo 模板](https://sealos.io/products/app-store/matomo)，点击 **Deploy Now**。
2. 在弹窗中保留默认参数，或调整生成的应用名称和访问域名前缀。
3. 等待部署完成，通常需要 2-3 分钟。部署后会进入 Canvas。后续如需修改，可在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 打开生成的 Matomo 访问 URL。
5. 完成 Matomo 安装向导：
   - 确认系统检查结果。
   - 数据库配置页使用模板预填的数据库设置。
   - 创建第一个超级用户账号。
   - 添加第一个网站，并将跟踪代码复制到需要统计的网站中。
   - 在最后的 Congratulations 页面点击 **Continue to Matomo**，进入登录页。
6. 使用安装向导中创建的超级用户账号和密码登录。

## 配置说明

部署后，可以通过以下方式配置 Matomo：

- **安装向导**：首次打开应用时创建第一个管理员和网站。
- **Matomo 管理后台**：安装完成后管理用户、网站、隐私设置、插件和跟踪代码。
- **AI 对话**：在 Sealos Canvas 中描述资源或配置变更需求。
- **资源卡片**：打开 StatefulSet、MySQL、Ingress 或存储卡片，查看并调整运行配置。

## 扩展

模板使用经过验证的 512 MiB 内存限制，可避免安装向导创建表、插件和管理员账号时因内存不足被 OOMKilled。随着访问量增长，可以按以下步骤扩展：

1. 打开当前部署的 Canvas。
2. 点击 Matomo StatefulSet 资源卡片。
3. 如果仪表盘或归档变慢，可按 Sealos 允许的资源选项增加 CPU 或内存。
4. 应用变更，并确认 Matomo 仪表盘仍可访问。

对于高流量场景，还应根据 Matomo 官方文档配置 cron 归档任务。

## 故障排查

### 安装向导无法连接数据库

- 原因：MySQL 可能仍在启动，或凭据尚未就绪。
- 解决：等待 MySQL Pod 和 Matomo Pod 都进入运行状态后刷新安装向导。

### 浏览器显示可信主机或 HTTPS 警告

- 原因：Matomo 会校验访问所使用的主机名。
- 解决：使用 Sealos 提供的公网 URL，安装完成后避免更改应用访问域名。

### 安装向导中途停止或 Pod 重启

- 原因：Matomo 在创建表、插件和管理员账号时可能超过 256 MiB 容器内存限制。
- 解决：安装期间保持模板的内存限制为 512 MiB 或更高。当前模板已经使用经过验证的 512 MiB 限制。

### 大型网站的分析报表较慢

- 原因：流量增大后，由浏览器触发的归档可能变慢。
- 解决：根据 Matomo 的 cron 归档指南配置定时归档，并按需提升应用资源。

### 获取帮助

- [Matomo 文档](https://matomo.org/help/)
- [Matomo 社区论坛](https://forum.matomo.org/)
- [Matomo GitHub Issues](https://github.com/matomo-org/matomo/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [跟踪代码指南](https://matomo.org/faq/new-to-piwik/how-to-install-the-javascript-tracking-code/)
- [隐私功能](https://matomo.org/privacy/)
- [开发者文档](https://developer.matomo.org/)

## 许可证

此 Sealos 模板使用仓库许可证发布。Matomo 本身使用 GPL-3.0 许可证。
