# 在 Sealos 上部署并托管 Notifuse

Notifuse 是一个开源邮件平台，支持新闻邮件、事务邮件、自动化流程，以及面向收件人的订阅管理。本模板会在 Sealos Cloud 上部署 Notifuse v28.4，并自动配置 PostgreSQL、持久化存储和 HTTPS Ingress。

## 关于在 Sealos 上托管 Notifuse

Notifuse 把邮件营销、事务投递、受众管理、自动化工作流和通知中心整合在同一个应用里。首次打开时，Notifuse 会引导你完成内置的 Setup Wizard（初始化向导），在浏览器中补齐 root 管理员邮箱、公开 API 地址和 SMTP 配置。

这个 Sealos 模板会准备好自托管所需的核心组件，包括 PostgreSQL 集群、用于创建 `notifuse_system` 数据库的初始化 Job、挂载到 `/app/data` 的持久化存储，以及一个公开可访问的 HTTPS 控制台地址。应用还会在集群内部暴露 `587` 端口，方便你后续扩展 SMTP relay 等场景。

## 常见使用场景

- **新闻邮件运营**：管理订阅列表、创建活动，并定期发送产品更新或内容邮件。
- **事务邮件发送**：统一处理密码重置、账户提醒、收据通知等系统邮件。
- **生命周期自动化**：基于联系人行为构建欢迎、培育、召回等自动化流程。
- **多工作区邮件管理**：按品牌、客户或业务线拆分工作区，分别管理邮件业务。
- **品牌化订阅管理**：借助 Notifuse 的通知中心和退订流程，让收件人自行管理订阅偏好。

## Notifuse 托管依赖

这个 Sealos 模板已经包含运行 Notifuse 所需的基础依赖：Notifuse 应用本体、PostgreSQL 数据库集群、数据库初始化 Job、应用持久化存储、用于 HTTP 和 SMTP relay 的内部 Service，以及用于浏览器访问的 HTTPS Ingress。

### 部署依赖

- [Notifuse Documentation](https://docs.notifuse.com/) - Notifuse 官方文档
- [Notifuse Installation Guide](https://docs.notifuse.com/installation) - 自托管与初始化向导说明
- [Notifuse GitHub Repository](https://github.com/notifuse/notifuse) - 源码仓库、发布记录与上游许可证
- [Notifuse SMTP Integration Guide](https://docs.notifuse.com/integrations/smtp) - SMTP 服务商接入说明

## 实现细节

### 架构组成

本模板会部署以下服务和资源：

- **Notifuse 应用**：提供 Web 控制台和 API，监听端口 `8080`
  - 镜像：`notifuse/notifuse:v28.4`
  - 持久化存储：`1Gi`，挂载到 `/app/data`
  - 健康检查：`/healthz` 启动、就绪和存活探针
- **PostgreSQL 集群**：为系统数据和工作区数据提供底层数据库
  - 版本：PostgreSQL `16.4.0`
  - 持久化存储：`1Gi`
  - 凭据来源：通过 Kubernetes Secret 注入
- **数据库初始化 Job**：在主应用启动前创建 `notifuse_system` 数据库
- **Service + Ingress**：通过 HTTPS 对外暴露 Web 界面，同时在集群内保留 `587` 端口用于 SMTP relay 流量

### 资源配置

| 组件 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Notifuse | 20m | 200m | 25Mi | 256Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### 配置说明

这个模板刻意保持运行时配置简洁，把大部分业务侧初始化交给 Notifuse 自带的 Setup Wizard。Sealos 会自动生成应用名、访问域名和 `SECRET_KEY`，模板则负责把数据库凭据注入到容器里，并在主容器启动前等待 PostgreSQL 就绪。

部署完成后，请在 Notifuse 控制台里完成初始化：

- 填写 root 管理员邮箱
- 确认 Sealos 为你生成的公开 API 地址
- 配置用于发信的 SMTP 服务商

Notifuse 会使用模板注入的数据库凭据来管理内部系统库和工作区数据。部署完成后请保持 `SECRET_KEY` 稳定，因为上游文档说明，一旦修改它，之前已经加密保存的集成凭据会失效。

### 许可证信息

Notifuse 采用 [GNU Affero General Public License v3.0](https://github.com/notifuse/notifuse/blob/main/LICENCE.md) 许可证发布。本模板遵循 Sealos templates 仓库的许可证策略。

## 为什么要在 Sealos 上部署 Notifuse？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，可以把应用从部署到运维的整套流程简化下来。把 Notifuse 部署到 Sealos 后，你可以获得：

- **一键部署**：从模板页直接拉起 Notifuse、PostgreSQL、存储和 HTTPS 入口。
- **托管式 Kubernetes 基础设施**：开箱即用获得服务发现、持久卷、滚动更新和 Ingress 管理，无需手写清单。
- **更简单的后续运维**：应用启动后，可以通过 Canvas、AI 对话框和资源卡片调整资源或更新配置。
- **默认持久化**：应用数据和 PostgreSQL 数据在重启与常规更新后都能保留下来。
- **按量使用更省心**：可以先用较小资源启动，随着发信规模增长再逐步扩容。
- **安全的公网访问**：Sealos 会自动为 Notifuse 控制台分配带 TLS 的公网地址。

如果你想保留自托管的灵活性，又不想自己拼装整套基础设施，这个模板会是一个更省事的起点。

## 部署指南

1. 打开 [Notifuse 模板页面](https://sealos.io/products/app-store/notifuse)，点击 **Deploy Now**。
2. 在弹出的参数窗口中检查默认配置。大多数情况下直接使用默认值即可；如果有需要，也可以在部署前调整应用名、访问域名或 secret key。
3. 等待部署完成，通常需要 2-3 分钟。部署结束后，Sealos 会跳转到 Canvas，后续你可以通过 AI 对话框或资源卡片继续调整配置。
4. 打开生成的应用地址，完成 Notifuse 的 Setup Wizard：
   - 填写 root 管理员邮箱
   - 确认公开 API 地址
   - 配置发信所需的 SMTP 服务商
5. 完成初始化后，就可以在 Notifuse 控制台中开始创建工作区、列表、模板、群发活动和自动化流程。

## 配置

部署完成后，你可以从两个层面管理这套服务：

- **Sealos 基础设施层**：通过 Canvas、AI 对话框或资源卡片调整 CPU、内存、存储、域名和 Ingress 相关设置。
- **Notifuse 应用层**：通过 Web 控制台配置 SMTP 集成、创建工作区、设置品牌化 endpoint URL、管理发信身份、联系人列表和自动化流程。

如果你希望邮件里的点击链接、退订页面等面向收件人的地址使用自定义域名，请在完成初始化后，进入各个工作区单独配置 custom endpoint URL。

## 扩缩容

这个模板默认按单实例 Notifuse 部署来设计，并依赖本地持久化存储。对大多数团队来说，第一步更适合做纵向扩容，而不是直接增加副本数。

扩容方式如下：

1. 打开已部署应用的 Canvas。
2. 点击 Notifuse 的 StatefulSet 资源卡片。
3. 根据活动发送量、自动化任务负载和 API 流量提高 CPU 或内存限制。
4. 随着模板、日志或联系人数据增长，按需扩展应用或 PostgreSQL 的存储容量。

如果你需要更复杂的多实例架构，建议把它作为单独的定制项目处理，而不是直接在这个模板上增加副本数。

## 故障排查

### 常见问题

**问题：界面可以打开，但初始化还没完成**
- 原因：Notifuse 首次启动时必须先完成 Setup Wizard。
- 处理方法：打开公网地址，按提示完成 root 邮箱、API 地址和 SMTP 配置。

**问题：部署后几分钟内应用仍不可用**
- 原因：PostgreSQL 和数据库初始化 Job 可能还在准备 `notifuse_system` 数据库，应用此时会等待健康检查通过。
- 处理方法：先等待部署稳定。如果仍未恢复，再到 Canvas 中检查 PostgreSQL 集群、初始化 Job 和 StatefulSet 的状态。

**问题：邮件发送失败**
- 原因：还没有配置 SMTP，或者 SMTP 提供商凭据填写错误。
- 处理方法：在 Notifuse 设置中补充或修正 SMTP 集成。首次配置时，最快的入口就是初始化向导。

**问题：点击追踪或退订页面使用了错误的域名**
- 原因：工作区级别的 endpoint branding 还没有配置。
- 处理方法：为对应工作区设置 custom endpoint URL，让面向收件人的链接使用你期望的域名。

### 获取帮助

- [Notifuse Documentation](https://docs.notifuse.com/)
- [Notifuse GitHub Issues](https://github.com/notifuse/notifuse/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Notifuse Workspaces](https://docs.notifuse.com/features/workspaces) - 工作区模型与自定义 endpoint URL
- [Notifuse Automations](https://docs.notifuse.com/features/automations) - 事件驱动的生命周期自动化
- [Notifuse Notification Center](https://docs.notifuse.com/features/notification-center) - 面向收件人的订阅管理中心
- [Notifuse Broadcast Campaigns](https://docs.notifuse.com/concepts/broadcast-campaigns) - 群发活动的目标管理与投递概念

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Notifuse 本身采用 [GNU Affero General Public License v3.0](https://github.com/notifuse/notifuse/blob/main/LICENCE.md) 许可证发布。
