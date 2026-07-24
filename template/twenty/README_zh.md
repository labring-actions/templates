# 在 Sealos 上部署和托管 Twenty

Twenty 是一款开源客户关系管理（CRM）系统，可用于管理公司、联系人、商机、任务、笔记、仪表盘与工作流。此模板会在 Sealos 上部署 Twenty 2.22.0，包括独立服务端、后台 worker、PostgreSQL、Redis、自动 HTTPS，以及可选的文件存储方案。

![Twenty 应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/twenty/website-screenshot.webp)

## 关于 Twenty 托管

Twenty 将可定制的 CRM 界面、工作流自动化与可扩展数据模型整合在一起。团队可以在同一个工作区中管理客户资料、跟踪商机、分配任务并构建业务流程。

Sealos 部署保留 Twenty 官方的多服务架构。服务端负责 Web 界面与 API，worker 处理后台队列，PostgreSQL 保存应用和工作区数据，Redis 负责队列与缓存。

本地文件存储使用一个由服务端和 worker 在同一节点共享的 1 GiB 持久卷。启用 S3 后，模板会创建私有 Sealos 对象存储桶，并移除本地文件卷及其节点调度约束。

## 常见使用场景

- **销售 CRM**：跟踪公司、联系人、商机、负责人和业务活动。
- **客户运营**：集中管理任务、笔记、时间线和共享客户背景信息。
- **自定义数据模型**：按内部流程调整对象、字段、视图和关联关系。
- **工作流自动化**：通过后台 worker 执行事件驱动与定时工作流。

## Twenty 托管依赖

此模板会创建全部必需服务，并自动生成应用加密密钥。

### 部署依赖

- [Twenty 文档](https://docs.twenty.com/) - 产品与自托管文档
- [Twenty 源码](https://github.com/twentyhq/twenty) - 上游代码仓库
- [Sealos 应用商店](https://sealos.io/products/app-store/twenty) - 模板部署页面

### 实现细节

**架构组件：**

- **Twenty server 2.22.0**：StatefulSet，通过 3000 端口提供 Web 界面和 API。
- **Twenty worker 2.22.0**：Deployment，负责处理队列、工作流、Webhook 与定时任务。
- **PostgreSQL 16.4**：KubeBlocks 托管数据库，配备 1 GiB 数据卷。
- **Redis 7.2.7**：KubeBlocks 托管的 Redis 与 sentinel 组件，用于队列和缓存。
- **文件存储**：默认使用 1 GiB 共享本地卷，也可以选择私有 S3 兼容存储桶。
- **Ingress**：提供自动生成的公网域名并终止 TLS。

服务端会在启动前等待 PostgreSQL 连续完成三次查询，并通过带认证的 Redis PING 检查。这套机制可以避免托管服务创建过程中的竞态影响首次数据库迁移。worker 会在服务端健康检查通过后启动。

**部署选项：**

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `USE_S3_STORAGE` | `false` | 使用私有 Sealos 对象存储保存文件；默认使用共享本地卷。 |

经验证的资源上限为：服务端 1 CPU、2 GiB 内存，worker 500m CPU、1 GiB 内存。这组资源可以承载首次迁移和活跃队列处理。

**许可证信息：**

Twenty 主要采用 AGPL-3.0 许可证。带有上游企业许可证声明的文件遵循 Twenty 商业条款。

## 为什么在 Sealos 上部署 Twenty？

- **完整服务组合**：一次部署即可创建服务端、worker、PostgreSQL、Redis、存储与网络资源。
- **托管数据库**：通过 KubeBlocks 运行带持久卷的 PostgreSQL 与 Redis。
- **可选文件存储**：紧凑部署可使用共享本地卷，对象文件可使用私有 S3 存储。
- **CRM 数据持久化**：工作区记录、配置与队列状态会在 Pod 重启后继续保留。
- **托管公网访问**：自动获得已配置 Ingress 与 TLS 的 HTTPS 地址。

## 部署指南

1. 打开 [Twenty 模板](https://sealos.io/products/app-store/twenty)，点击 **Deploy Now**。
2. 需要将上传文件保存到 Sealos 对象存储时，请启用 S3 存储，然后确认部署。
3. 等待 PostgreSQL、Redis、服务端和 worker 进入就绪状态。Twenty 首次部署会执行数据库迁移，通常需要几分钟。
4. 打开应用卡片中显示的访问地址。

## 注册与登录

首次访问时，选择 **Continue with email**，填写电子邮件地址和密码，然后选择 **Sign up**。接着创建第一个工作区、完善个人资料，并完成或跳过可选的引导步骤。首位注册用户会成为工作区所有者和管理员。

后续访问继续使用 **Continue with email** 流程，输入已注册的电子邮件地址和密码即可登录。

## 配置

你可以在 Twenty 工作区设置中配置对象、字段、视图、角色、工作流与集成。模板会生成稳定的加密密钥，用于保护配置值。

需要调整基础设施时，请打开部署 Canvas，通过 AI 对话或资源卡片修改配置。更新现有部署时，请保持自动生成的加密密钥稳定。

## 扩缩容

模板默认运行一个服务端和一个 worker。本地文件存储会将两个 Pod 调度到同一节点，以便共享 `ReadWriteOnce` 卷。S3 存储会解除本地卷约束，为后续扩展 worker 提供更合适的基础。

## 故障排查

### 首次启动需要几分钟

Twenty 会在提供服务前执行数据库设置、迁移和工作区升级命令。请检查服务端日志中的迁移进度，并等待 `/healthz` 端点进入就绪状态。

### worker 正在等待启动

worker 会等待服务端健康检查通过。请依次检查 PostgreSQL、Redis 和服务端的就绪状态。

### 获取帮助

- [Twenty 文档](https://docs.twenty.com/)
- [Twenty GitHub Issues](https://github.com/twentyhq/twenty/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Twenty 的许可证详情见[上游许可证文件](https://github.com/twentyhq/twenty/blob/main/LICENSE)。
