# Skardi

**跨多源 SQL 查询引擎** — 对文件、数据库、S3 和向量存储执行联邦 SQL 查询，或将任意 SQL 零代码转为参数化 HTTP API。基于 Rust 与 Apache DataFusion 构建。

## 快速开始

首次启动实例时，会预置一个 `product-search-demo` Pipeline。可用它来验证实例是否正常运行：

```bash
# 列出所有已注册的 Pipeline
curl https://<your-app-host>/pipelines

# 执行示例 Pipeline — 按价格、品牌、分类等条件过滤商品
curl -X POST https://<your-app-host>/product-search-demo/execute \
  -H "Content-Type: application/json" \
  -d '{
    "brand": null,
    "max_price": 50.0,
    "min_price": null,
    "color": null,
    "category": null,
    "availability": null,
    "limit": 10
  }'
```

所有参数均为可选，传 `null` 表示不过滤该字段。

## 自定义配置

Skardi 通过挂载自 ConfigMap 的两个 YAML 文件进行配置：

| ConfigMap | 文件 | 用途 |
|-----------|------|------|
| `<app-name>-ctx` | `ctx.yaml` | 定义数据源（CSV、Parquet、PostgreSQL、MySQL、SQLite、MongoDB、Redis、S3、Lance、Iceberg） |
| `<app-name>-pipeline` | `pipeline.yaml` | 定义以 REST 端点形式提供的 SQL 查询 |

通过 Sealos 控制台或 `kubectl` 编辑对应 ConfigMap，重启 Pod 后生效。

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
| `/health` | GET | 健康检查 |
| `/pipelines` | GET | 列出所有 Pipeline |
| `/:name/execute` | POST | 执行指定 Pipeline |

## 支持的数据源

CSV · Parquet · JSON · PostgreSQL · MySQL · SQLite · MongoDB · Redis · Apache Iceberg · Lance（向量搜索 + 全文检索）· S3 / GCS / Azure Blob

## 相关链接

- [GitHub](https://github.com/SkardiLabs/skardi)
- [文档](https://github.com/SkardiLabs/skardi#readme)
