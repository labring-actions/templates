# 在 Sealos 上部署和托管 LibreDB Studio

## 概述

LibreDB Studio 是一个开源、自托管的 SQL IDE。它提供基于 Web 的客户端，让您在同一界面中浏览、查询和管理 SQL 数据库。

此 Sealos 模板将 **LibreDB Studio** 部署为 `libredb-studio` 应用。它使用仓库维护的 Sealos 清单，将部署、网络和存储配置都保留在模板内。

## 在 Sealos 上部署

在 Sealos 应用商店中打开此模板，检查配置值，然后点击 **部署**。Sealos 会渲染模板变量、创建所需的 Kubernetes 资源，并为应用管理公共访问地址。

## 访问

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。具体主机名由 `defaults.app_host` 和您的 Sealos Cloud 域名生成。使用部署时设置的管理员邮箱和密码登录。

## 配置

部署期间可用的用户输入项如下：

| 名称 | 描述 | 必填 | 默认值 |
|------|-------------|----------|---------|
| `admin_email` | 首次登录的管理员邮箱 | `true` | `` |
| `admin_password` | 管理员密码（至少 8 个字符） | `true` | `` (部署时设置) |
| `jwt_secret` | 用于签名会话令牌的密钥（至少 32 个字符） | `false` | `${{ random(48) }}` |
| `volume_size` | 数据库的持久化存储大小（GiB） | `false` | `1` |

数据存储在 `/app/data/libredb-storage.db` 的内嵌 SQLite 数据库中，并保存在持久卷上，因此在重启和重新部署后仍然保留。

admin_password 和 jwt_secret 都作为 Sealos 管理的输入项存储，因此请使用自动生成的默认值，或在部署时设置，而不要将其硬编码。

## 官方链接

- 官方网站: https://libredb.org
- 源代码仓库: https://github.com/libredb/libredb-studio
