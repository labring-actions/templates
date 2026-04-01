# Skardi

**SQL across anything** — query, join, and aggregate over local files, databases, S3, and vector stores, or turn any SQL into a parameterized HTTP API with zero application code. Written in Rust, powered by Apache DataFusion.

## Quick Start

Once deployed, open the dashboard URL to see the registered pipelines. A sample `product-search` pipeline is pre-loaded and ready to call:

```bash
curl -X POST https://<your-app-host>/product-search/execute \
  -H "Content-Type: application/json" \
  -d '{"brand": null, "max_price": 100.0, "category": null, "limit": 5}'
```

## Customizing Your Deployment

Skardi is configured via two YAML files mounted from the `<app-name>-config` ConfigMap:

| File | Purpose |
|------|---------|
| `ctx.yaml` | Defines data sources (CSV, Parquet, PostgreSQL, MySQL, SQLite, MongoDB, Redis, S3, Lance, Iceberg) |
| `pipeline.yaml` | Defines SQL queries served as REST endpoints |

Edit the ConfigMap through the Sealos dashboard or with `kubectl` to add your own data sources and pipelines, then restart the pod to apply changes.

### Example: Adding a PostgreSQL Data Source

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

### Example: Defining a Pipeline

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

Execute it:

```bash
curl -X POST https://<your-app-host>/user-lookup/execute \
  -H "Content-Type: application/json" \
  -d '{"user_id": 42}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Pipeline dashboard UI |
| `/health` | GET | Health check |
| `/pipelines` | GET | List all pipelines |
| `/:name/execute` | POST | Execute a pipeline |

## Uploading Data Files

User data files are stored on a persistent 1 Gi volume mounted at `/data`. Upload CSV, Parquet, SQLite, or Lance files via the Sealos file manager or `kubectl cp`, then reference them by path in `ctx.yaml`.

## Supported Data Sources

CSV · Parquet · JSON · PostgreSQL · MySQL · SQLite · MongoDB · Redis · Apache Iceberg · Lance (vector + full-text search) · S3 / GCS / Azure Blob

## Links

- [GitHub](https://github.com/SkardiLabs/skardi)
- [Documentation](https://github.com/SkardiLabs/skardi#readme)
