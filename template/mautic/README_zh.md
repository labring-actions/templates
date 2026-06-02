# 在 Sealos 上部署 Mautic

[Mautic](https://www.mautic.org/) 是一款开源营销自动化平台，可用于邮件营销、落地页、线索评分、客户分群和客户旅程编排。

此 Sealos 模板会部署 Mautic 7 官方 Apache 镜像、托管 MySQL 8.4.2 数据库、持久化应用存储、定时任务和队列 Worker。

## 功能特性

- 使用 `mautic/mautic:7.1.2-apache` 部署 Mautic 7.1.2
- 通过 KubeBlocks 创建托管 MySQL 8.4.2 数据库
- Web、Cron、Worker 工作负载分工运行
- 持久化配置、日志、上传文件和图片
- 由 Sealos 自动管理公网 HTTPS 入口

## 在 Sealos 上部署

1. 打开 [Sealos 上的 Mautic 模板](https://sealos.io/products/app-store/mautic)。
2. 点击 **Deploy Now**。
3. 保留默认生成的应用名和域名，或按需自定义。
4. 选择 `TIMEZONE`，用于 PHP 和定时任务。
5. 点击 **Deploy**，等待应用状态变为运行中。

## 首次设置与登录

Mautic 没有默认管理员账号。首次打开生成的公网地址时，需要完成安装向导：

1. 在 **Environment Check** 页面点击 **Next Step**。
2. 在 **Database Setup** 页面保留模板自动填入的 MySQL 配置，点击 **Next Step**。
3. 在 **Administrative User** 页面创建管理员用户名、密码和邮箱。
4. 安装完成后，使用刚创建的管理员账号在 `/s/login` 登录。

如果安装向导或后续设置页面要求填写站点地址，请使用 Sealos 为应用生成的公网 HTTPS 地址。

## 资源配置

该模板已通过 Sealos 线上部署测试调试资源下限：

| 组件 | CPU 上限 | 内存上限 | 说明 |
| --- | ---: | ---: | --- |
| Mautic Web | `200m` | `256Mi` | 提供界面和安装向导 |
| Mautic Cron | `100m` | `256Mi` | 运行 Mautic 定时任务 |
| Mautic Worker | `100m` | `512Mi` | 运行 Messenger 队列消费者 |
| MySQL | `1000m` | `1024Mi` | MySQL 8.4.2 在 KubeBlocks 下的稳定下限 |

安装完成后，Worker 会启动多个队列消费者，因此它需要比 Web 容器更高的内存。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
| --- | --- | --- | --- |
| `TIMEZONE` | Mautic 和定时任务使用的 PHP 时区。 | 否 | `UTC` |

邮件发送需要在安装后进入 Mautic 后台配置。生产使用前，请在 **Settings → Configuration → Email** 中添加 SMTP 服务商。

## 数据持久化

模板会持久化以下数据：

- `/var/www/html/config`
- `/var/www/html/var/logs`
- `/var/www/html/docroot/media/files`
- `/var/www/html/docroot/media/images`
- MySQL 数据卷

删除 Sealos 应用时，应用和数据库资源会按模板的终止策略一并删除。

## 官方链接

- 官网：https://www.mautic.org/
- 文档：https://docs.mautic.org/
- 源码：https://github.com/mautic/mautic
- Docker 镜像：https://hub.docker.com/r/mautic/mautic
