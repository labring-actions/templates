# 在 Sealos 上部署和托管 Hasura

Hasura 可以把 PostgreSQL 数据转换成 GraphQL API，并通过浏览器 Console 管理数据库模式、元数据、权限和查询。该模板会在 Sealos Cloud 上部署 Hasura GraphQL Engine 2.49.5、同版本 Data Connector Agent 和托管 PostgreSQL 16.4。

![Sealos 上的 Hasura Console](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/hasura/website-screenshot.webp)

## 关于托管 Hasura

Hasura 会根据已追踪的数据库对象生成 GraphQL Schema，并将配置保存为元数据。团队可以通过 Console 或 Metadata API 管理数据表、关系、权限、Action、Event 和 Remote Schema。

该 Sealos 模板为 GraphQL Engine 创建公网 HTTPS 入口，并让 PostgreSQL 与 Data Connector Agent 保持在集群私网。全新部署会自动把托管 PostgreSQL 注册为 `default` 数据源。

## 常见使用场景

- **应用后端**：为 PostgreSQL 数据表提供类型安全的 GraphQL API。
- **内部数据 API**：为数据看板和内部工具提供统一的数据访问层。
- **API 原型开发**：通过 Hasura Console 快速创建并查询 Schema。
- **事件驱动工作流**：把数据库变更连接到 Webhook 和异步处理流程。
- **组合式数据访问**：通过 Hasura Data Connector 接入受支持的外部系统。

## Hasura 托管依赖

该模板包含全新部署所需的全部运行组件。

### 部署依赖链接

- [Hasura Documentation](https://hasura.io/docs/latest/) - 产品、API 与运维文档
- [GraphQL Engine Repository](https://github.com/hasura/graphql-engine) - 源代码与版本发布
- [Data Connector Documentation](https://hasura.io/docs/latest/databases/data-connectors/) - 连接器概念与支持的数据后端
- [Metadata API Reference](https://hasura.io/docs/latest/api-reference/metadata-api/index/) - 元数据自动化接口参考

### 实现细节

**架构组件：**

- **GraphQL Engine 2.49.5**：单副本，在 `8080` 端口提供 Console 与 GraphQL API。
- **Data Connector Agent 2.49.5**：单个私网副本，在 `8081` 端口提供连接器端点。
- **托管 PostgreSQL 16.4**：单个 KubeBlocks 副本，配备 1 GiB 持久卷。
- **HTTPS Ingress**：由 Sealos 管理的公网域名与 TLS 证书。

GraphQL Engine 会等待 PostgreSQL TCP 端点可用后再启动。两个应用工作负载都配置了启动、就绪与存活探针。PostgreSQL 凭据来自 KubeBlocks 托管的连接 Secret，Kubernetes 环境变量展开会生成元数据数据库和应用数据库连接地址。

经过线上低负载验证的资源限制为：GraphQL Engine `100m/256Mi`、Data Connector Agent `100m/256Mi`、PostgreSQL `500m/512Mi`。`HASURA_GRAPHQL_DATABASE_URL` 会自动注册数据源，`HASURA_GRAPHQL_METADATA_DATABASE_URL` 会把 Hasura 元数据保存在同一个托管集群中。

Hasura GraphQL Engine 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 Hasura？

- **一键创建完整服务栈**：通过一个模板创建 Hasura、PostgreSQL、网络、存储和健康检查。
- **自动连接数据源**：打开 Console 即可看到可用的托管 PostgreSQL。
- **强制管理员认证**：部署时设置 Console 与 API 共用的管理员密钥。
- **持久化元数据**：Pod 重启后继续保留 Hasura 元数据和应用数据表。
- **自动 HTTPS**：由 Sealos 提供公网域名和 TLS 证书。
- **Kubernetes 运维能力**：通过 Sealos Canvas 查看日志、健康状态、资源与存储。

## 部署指南

1. 打开 [Hasura 模板](https://sealos.io/products/app-store/hasura)，点击 **Deploy Now**。
2. 为 `admin_secret` 输入强度足够且唯一的值，并保存到密码管理器。
3. 点击 **Deploy**，等待 PostgreSQL、GraphQL Engine 与 Data Connector Agent 进入 Ready 状态。
4. 打开 Sealos 中显示的 Hasura 应用入口。

PostgreSQL 首次初始化通常需要几分钟。GraphQL Engine 的启动门禁会在这段时间持续等待数据库。

## 登录 Hasura Console

1. 打开系统生成的应用地址，根路径会跳转到 `/console`。
2. 输入部署弹窗中使用的同一个 `admin_secret`。
3. 在可信设备上需要持久登录时，勾选 **Remember on the browser**。
4. 打开 **Data**，确认页面中已经出现 `default` PostgreSQL 数据源。

Hasura 使用共享管理员密钥完成 Console 与管理 API 认证。持有该值的用户拥有完整管理员权限。

调用 API 时，请通过 `x-hasura-admin-secret` 请求头发送该密钥：

```bash
curl "https://<your-domain>/v1/graphql" \
  -H "content-type: application/json" \
  -H "x-hasura-admin-secret: <your-admin-secret>" \
  --data '{"query":"query { __typename }"}'
```

## 创建并查询数据表

1. 打开 **Data**，展开 `default`，选择 `public` Schema。
2. 点击 **Create Table**，定义字段与主键，然后创建数据表。
3. 打开 **Insert Row** 并新增一条记录。
4. 打开 **API**，在 GraphiQL 中查询已追踪的数据表。

也可以通过 **SQL** 页面创建数据库对象。需要立即加入 GraphQL Schema 时，请启用 **Track this**。

## 配置

| 名称 | 必填 | 说明 |
|------|------|------|
| `admin_secret` | 是 | 用于 Hasura Console 登录和管理 API 请求的共享密钥。 |

重要访问路径：

| 路径 | 用途 |
|------|------|
| `/console` | Hasura Console 登录与管理 |
| `/v1/graphql` | GraphQL API |
| `/v1/metadata` | Metadata API |
| `/healthz` | Kubernetes 探针使用的公开健康检查端点 |

初始部署启用了开发模式。生产环境完成初始化后，建议设置 `HASURA_GRAPHQL_DEV_MODE=false`，并根据认证模型配置 CORS、JWT、Webhook 或角色权限。

## 持久化与扩缩容

PostgreSQL 会把 Hasura 元数据和应用数据表保存到持久卷中。执行数据库迁移或大版本升级前，请先备份该持久卷。

初始拓扑包含一个 GraphQL Engine 副本、一个 Data Connector Agent 副本和一个 PostgreSQL 副本。查询量增长后，可以在 Sealos Canvas 中增加 CPU 与内存。多副本或高可用架构需要结合 Hasura 与 PostgreSQL 运维文档设计对应的数据库、元数据和工作负载方案。

## 故障排查

### Console 提示管理员密钥错误

请使用部署时输入的原始 `admin_secret`。密码管理器自动填充和复制内容中的空格可能改变提交值。

### GraphQL Engine 长时间停留在初始化状态

请在 Sealos Canvas 中检查 PostgreSQL Cluster 状态和 `wait-for-postgresql` 初始化容器。托管数据库开始接受 TCP 连接后，GraphQL Engine 会继续启动。

### API 请求返回 401

请添加 `x-hasura-admin-secret` 请求头，并确认其值与部署输入一致。

### 自定义配置后 `default` 数据源消失

编辑 Deployment 环境变量时，请保留 `HASURA_GRAPHQL_DATABASE_URL`、`HASURA_GRAPHQL_METADATA_DATABASE_URL` 与 `PG_DATABASE_URL`。这些值由 KubeBlocks 连接 Secret 生成。

### Data Connector Agent 无法就绪

请在 Sealos Canvas 中检查启动探针与日志。经过验证的初始内存限制为 `256Mi`；`128Mi` 会在启动阶段触发内存溢出。

### 获取帮助

- [Hasura GitHub Issues](https://github.com/hasura/graphql-engine/issues)
- [Hasura Documentation](https://hasura.io/docs/latest/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

该 Sealos 模板遵循 templates 仓库的许可条款。Hasura GraphQL Engine 使用 [Apache License 2.0](https://github.com/hasura/graphql-engine/blob/v2.49.5/LICENSE)。
