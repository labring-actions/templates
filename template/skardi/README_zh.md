# Skardi

**跨多源 SQL 查询引擎** — 对文件、数据库、S3 和向量存储执行联邦 SQL 查询，或将任意 SQL 零代码转为参数化 HTTP API。基于 Rust 与 Apache DataFusion 构建。

## 快速开始

部署完成后，打开 Dashboard URL 查看已注册的 Pipeline。预置了一个 `product-search` 示例 Pipeline，可立即调用：

```bash
curl -X POST https://<your-app-host>/product-search/execute \
  -H "Content-Type: application/json" \
  -d '{"brand": null, "max_price": 100.0, "category": null, "limit": 5}'
```

## 自定义配置

Skardi 通过挂载自 `<app-name>-config` ConfigMap 的两个 YAML 文件进行配置：

| 文件 | 用途 |
|------|------|
| `ctx.yaml` | 定义数据源（CSV、Parquet、PostgreSQL、MySQL、SQLite、MongoDB、Redis、S3、Lance、Iceberg） |
| `pipeline.yaml` | 定义以 REST 端点形式提供的 SQL 查询 |

通过 Sealos 控制台或 `kubectl` 编辑 ConfigMap，添加自己的数据源和 Pipeline，重启 Pod 后生效。

### 示例：添加 PostgreSQL 数据源

```yaml
# ctx.yaml
data_sources:
  - name: "users"
    type: "postgres"
    connection_string: "postgresql://localhost:5432/mydb?sslmode=disable"
    options:
      table: "users"
      user_env: "PG_USER"
      pass_env: "PG_PASSWORD"
```

### 示例：定义 Pipeline

```yaml
# pipeline.yaml
metadata:
  name: user-lookup
  version: 1.0.0

query: |
  SELECT id, name, email
  FROM users
  WHERE id = {user_id}
```

调用示例：

```bash
curl -X POST https://<your-app-host>/user-lookup/execute \
  -H "Content-Type: application/json" \
  -d '{"user_id": 42}'
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | Pipeline 管理 Dashboard |
| `/health` | GET | 健康检查 |
| `/pipelines` | GET | 列出所有 Pipeline |
| `/:name/execute` | POST | 执行指定 Pipeline |

## 上传数据文件

用户数据文件存储在挂载于 `/data`的 1Gi持久化存储上, 通过 Sealos 文件管理器或 `kubectl cp` 上传 CSV、Parquet、SQLite 或 Lance 文件，然后在 `ctx.yaml` 中按路径引用。

## 支持的数据源

CSV · Parquet · JSON · PostgreSQL · MySQL · SQLite · MongoDB · Redis · Apache Iceberg · Lance（向量搜索 + 全文检索）· S3 / GCS / Azure Blob

## 相关链接

- [GitHub](https://github.com/SkardiLabs/skardi)
- [文档](https://github.com/SkardiLabs/skardi#readme)
