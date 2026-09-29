# 在 Sealos 上部署 Corsfix

[Corsfix](https://corsfix.com) 是一款开源 CORS 代理，帮助浏览器应用访问 API，解决跨域请求问题。控制面板支持管理应用、允许访问的目标域名、API 密钥、加密凭据和请求统计。

本模板为控制面板和代理分别提供公开的 HTTPS 地址，并部署启用密码认证的 MongoDB、Redis 和持久化存储。

## 功能

- 代理浏览器 HTTP 请求并返回所需的 CORS 响应头。
- 注册应用域名，并限制应用可以访问的 API 域名。
- 在控制面板中管理 API 密钥、请求统计和加密的凭据变量。
- 支持响应缓存、自定义请求头和 JSONP。
- 在容器重启后保留应用数据和 Redis 状态。

## 包含的组件

| 组件 | 镜像 | 用途 |
| --- | --- | --- |
| 控制面板 | `ghcr.io/corsfix/corsfix-app:8899bb15e71c7238285ccefc4c95a0cd47daeaf0` | 使用 `3000` 端口的 Web 控制面板。 |
| 代理 | `ghcr.io/corsfix/corsfix-proxy:8899bb15e71c7238285ccefc4c95a0cd47daeaf0` | 使用 `80` 端口的 CORS 代理。 |
| MongoDB | `mongo:8.0.17` | 存储用户、应用、API 密钥、加密凭据和统计数据。 |
| Redis | `redis:7.4.11-alpine` | 提供缓存、限流和服务间协调。 |

数据库使用独立的 StatefulSet 和持久卷运行，以保留 Corsfix 自托管配置中已测试的数据库版本，无需 Sealos 托管数据库控制器。数据库端口仅在集群内部可访问。

当前控制面板镜像需要 **AMD64** 工作节点，模板会自动选择该架构。

## 部署与首次登录

1. 从 Sealos 应用商店部署模板。首次部署时，将 **Disable signup** 保持为 `false`。
2. 等待控制面板、代理、MongoDB 和 Redis 全部就绪。首次下载镜像和初始化数据库可能需要几分钟。
3. 打开 Corsfix 应用地址，在登录页面注册账户，然后登录。
4. 创建所需账户后，在 Sealos 中打开控制面板应用的环境变量设置，将 `DISABLE_SIGNUP` 改为 `true`，然后重新部署控制面板。
5. 在 Corsfix 中添加应用域名和允许访问的 API 域名，在前端请求中使用生成的代理地址。

关闭注册前，其他人也可以注册。如果在创建账户之前关闭了注册，请暂时将控制面板的 `DISABLE_SIGNUP` 环境变量改回 `false`，然后重新部署。

控制面板地址为 `https://<app_host>.<Sealos 域名>`，代理地址为 `https://<proxy_host>.<Sealos 域名>`。两个主机名均自动生成。在 Sealos 中打开名称以 `-proxy` 结尾的应用，即可找到代理的公开地址。访问该地址的 `/up` 路径应返回 `Corsfix: OK.`。

## 配置

| 输入项 | 默认值 | 说明 |
| --- | --- | --- |
| Disable signup | `false` | 控制账户注册。创建所需账户后请关闭注册。 |
| RPM | `180` | 每个客户端 IP 的每分钟请求限制。支持 `60`、`120`、`180` 和 `600`。本地开发来源使用单独的 `60` RPM 限制。 |
| Allowed origins | 空 | 可选的来源主机名列表，使用逗号分隔，例如 `app.example.com,www.example.com`。这些来源无需在控制面板中注册应用。不要填写协议或路径。 |
| Allowed targets | 空 | 限制上述来源可访问的目标主机名，使用逗号分隔。为空时，上述来源可访问任意公开目标。在控制面板注册的应用使用各自的目标设置。 |

通过控制面板管理应用时，两个允许列表都可以留空。

模板会自动创建 MongoDB 和 Redis 密码、认证密钥以及共享加密密钥。`KEK_VERSION_1` 解码后恰好为 32 字节，由控制面板和代理共同使用。备份或恢复应用时，请保留生成的 Kubernetes Secret；缺少原始密钥将无法解密已保存的凭据。

HTTPS 由 Sealos Ingress 终止。控制面板的 `AUTH_URL` 使用公开的 HTTPS 控制面板地址；`PROXY_DOMAIN` 和代理的 `APP_DOMAIN` 仅包含主机名，不含 URL 协议。如果使用自定义域名，需要同时更新这些变量、对应的 Ingress 主机名和证书。

## 资源与存储

| 组件 | CPU 请求 / 上限 | 内存请求 / 上限 | 持久化存储 |
| --- | --- | --- | --- |
| 控制面板 | `100m / 1000m` | `128Mi / 512Mi` | 无 |
| 代理 | `50m / 500m` | `64Mi / 256Mi` | 无 |
| MongoDB | `100m / 500m` | `128Mi / 512Mi` | 数据 `1Gi` + 配置 `1Gi` |
| Redis | `20m / 200m` | `32Mi / 128Mi` | 数据 `1Gi` |

默认共使用 3 GiB 持久化存储。请根据流量和数据保留需求增加资源与存储。MongoDB 的 WiredTiger 缓存上限为 `0.25` GiB，适用于此初始资源配置。Redis 启用了 AOF 持久化。

删除部署或更换数据库卷之前，请备份 MongoDB 数据以及生成的应用 Secret。重启工作负载不会删除持久卷；删除存储则会删除数据。

## 相关链接

- [Corsfix 官网](https://corsfix.com)
- [自托管文档](https://corsfix.com/docs/open-source/self-hosting)
- [Corsfix 文档](https://corsfix.com/docs)
- [源代码](https://github.com/corsfix/corsfix)
