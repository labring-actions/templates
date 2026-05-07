# Skardi

**SQL across anything** — query, join, and aggregate over local files, databases, S3, and vector stores, or turn any SQL into a parameterized HTTP API with zero application code. Written in Rust, powered by Apache DataFusion.

## Quick Start

A `product-search-demo` pipeline is pre-loaded when you first launch the instance. Use it to verify everything is working:

```bash
# List all registered pipelines
curl https://<your-app-host>/pipelines

# Run the demo pipeline — returns products filtered by price, brand, category, etc.
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

All parameters are optional — pass `null` to skip a filter.

## Customizing Your Deployment

Skardi is configured via two YAML files mounted from ConfigMaps:

| ConfigMap | File | Purpose |
|-----------|------|---------|
| `<app-name>-ctx` | `ctx.yaml` | Defines data sources (CSV, Parquet, PostgreSQL, MySQL, SQLite, MongoDB, Redis, S3, Lance, Iceberg) |
| `<app-name>-pipeline` | `pipeline.yaml` | Defines the SQL query served as a REST endpoint |

Edit the ConfigMaps through the Sealos dashboard or with `kubectl`, then restart the pod to apply changes.

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
| `/health` | GET | Health check |
| `/pipelines` | GET | List all pipelines |
| `/:name/execute` | POST | Execute a pipeline |

## Supported Data Sources

CSV · Parquet · JSON · PostgreSQL · MySQL · SQLite · MongoDB · Redis · Apache Iceberg · Lance (vector + full-text search) · S3 / GCS / Azure Blob

## Links

- [GitHub](https://github.com/SkardiLabs/skardi)
- [Documentation](https://github.com/SkardiLabs/skardi#readme)
