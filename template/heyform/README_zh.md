# 在 Sealos 上部署和托管 HeyForm

HeyForm 是一个开源对话式表单构建器，可用于创建调查问卷、信息收集表单、测验、投票和反馈页面。这个模板会在 Sealos 上部署 HeyForm Community Edition，并自动配置托管 MongoDB、托管 Redis、持久化上传存储和 HTTPS 访问入口。

![HeyForm 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/heyform/website-screenshot.webp)

## 功能特性

- 创建对话式表单、问卷、测验、投票和反馈页面。
- 通过公开表单链接收集提交，并在 Web 控制台中管理数据。
- 使用 Sealos 托管 MongoDB 存储用户、团队、表单和提交记录。
- 使用 Sealos 托管 Redis 支撑缓存、会话和后台队列。
- 使用持久化卷保存上传文件。
- 可选配置 SMTP，用于邮箱验证、密码重置、邀请和通知邮件。

## 适用场景

- 客户反馈和满意度调查。
- 线索收集和营销问卷。
- 活动报名和信息登记。
- 内部申请、审批和入职表单。
- 测验、投票和轻量研究问卷。

## 模板组件

| 组件 | 说明 |
| --- | --- |
| HeyForm | 使用 `heyform/community-edition:v3.0.0-rc.7`，服务端口为 `9157`。 |
| MongoDB | 存储用户、团队、表单、项目、提交、模板和系统设置。 |
| Redis | 支撑队列、缓存和运行时协调。 |
| 持久化存储 | 挂载到 `/app/packages/server/uploads` 和 `/app/packages/server/static/upload`，用于保存上传资源。 |
| Ingress | 提供 Sealos 自动生成的 HTTPS 访问地址。 |

## 部署方式

1. 打开 Sealos 应用商店中的 [HeyForm 模板](https://sealos.io/products/app-store/heyform)，点击 **Deploy Now**。
2. 如需快速部署，可以保留默认配置；如需邮箱验证、密码重置、邀请或通知邮件，请先填写 SMTP 配置。
3. 点击 **Deploy Application**。
4. 部署完成后，在 Sealos 中打开应用 URL。

## 首次登录和注册

HeyForm 是 Web 应用，创建表单前需要先注册账号。

1. 打开部署后的 HeyForm 访问地址。
2. 点击 **Create an account**，或直接打开 `/sign-up`。
3. 输入姓名、邮箱和密码。
4. 密码至少 8 位，并包含大写字母、小写字母和数字。
5. 注册完成后，使用同一个邮箱和密码登录。

本模板默认启用注册。如果未配置 SMTP，账号仍可创建；但邮箱验证邮件、密码重置邮件、邀请邮件和通知邮件需要有效的 SMTP 配置才能发送。

## 配置项

| 配置项 | 说明 | 是否必填 |
| --- | --- | --- |
| SMTP From | 验证和通知邮件的发件人地址。 | 否 |
| SMTP Host | SMTP 服务器地址。 | 否 |
| SMTP Port | SMTP 服务器端口，默认 `587`。 | 否 |
| SMTP User | SMTP 用户名。 | 否 |
| SMTP Password | SMTP 密码。 | 否 |
| SMTP Secure | 是否使用 TLS 连接 SMTP。 | 否 |
| SMTP Server Name | 可选的 TLS 服务器名称。 | 否 |
| SMTP Ignore Cert | 是否忽略 SMTP 证书校验错误。 | 否 |

## 资源配置

该模板使用在 Sealos 上验证通过的 HeyForm Community Edition `v3.0.0-rc.7` 最小资源配置：

- HeyForm 应用：限制 `80m` CPU / `192Mi` 内存，请求 `20m` CPU / `25Mi` 内存。
- MongoDB：Sealos 托管 MongoDB，限制 `500m` CPU / `512Mi` 内存。
- Redis：Sealos 托管 Redis，限制 `500m` CPU / `512Mi` 内存。
- 上传存储：一个 `1Gi` 持久化卷，同时挂载到 HeyForm 的两个上传目录。

测试中，应用内存限制降到 `160Mi` 会在启动阶段触发 OOM，因此 `192Mi` 是当前模板验证通过的最小内存限制。

## 常用链接

- [HeyForm 官网](https://heyform.net/)
- [HeyForm 文档](https://docs.heyform.net/)
- [HeyForm GitHub 仓库](https://github.com/heyform/heyform)
- [HeyForm Docker 镜像](https://hub.docker.com/r/heyform/community-edition)
