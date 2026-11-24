# Pgweb

## 应用概览

Pgweb 是一款轻量、跨平台的 PostgreSQL Web 客户端，支持浏览表数据、执行 SQL、查看查询计划、导出数据和管理多个数据库会话。

此 Sealos 模板部署 Pgweb `0.17.0`。模板不会创建 PostgreSQL 数据库；你可以连接已有的 Sealos PostgreSQL 实例，或 Pgweb 容器能够访问的其他 PostgreSQL 服务。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，保留自动生成的 HTTP 认证密码或自行修改，然后点击 **部署**。

## 访问方式

打开 Sealos 提供的公网地址。浏览器会先显示 HTTP Basic Auth 登录框：

- 用户名：`auth_username`，默认为 `admin`
- 密码：自动生成或自定义的 `auth_password`

登录后，在 Pgweb 页面填写目标 PostgreSQL 的连接信息。如果 PostgreSQL 位于同一个 Sealos 命名空间，请使用数据库的内部 Service 域名和 `5432` 端口，并根据数据库配置选择正确的 SSL 模式。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `auth_username` | 用于保护 Pgweb Web 界面的用户名 | 是 | `admin` |
| `auth_password` | 用于保护 Pgweb Web 界面的密码 | 是 | 随机生成的 24 位字符串 |

Pgweb 默认启用多会话模式，因此不同浏览器会话可以连接不同的 PostgreSQL 数据库。数据库凭据在 Pgweb 中填写，不会写入此模板。

## 安全建议

- Pgweb 能以你提供的数据库账号执行 SQL，请勿关闭 HTTP 认证。
- 建议使用仅具备必要权限的独立 PostgreSQL 账号。
- 不要公开分享访问地址和认证密码。

## 官方链接

- 官网：https://sosedoff.github.io/pgweb/
- 源码：https://github.com/sosedoff/pgweb
- 文档：https://github.com/sosedoff/pgweb/wiki
