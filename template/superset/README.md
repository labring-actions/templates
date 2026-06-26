# Deploy and Host Apache Superset on Sealos

Apache Superset is a modern data exploration and visualization platform. This template deploys Superset with managed PostgreSQL, managed Redis, persistent application storage, and a public HTTPS URL on Sealos Cloud.

![Apache Superset Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/superset/website-screenshot.webp)

## About Hosting Apache Superset

Superset runs as a web application backed by PostgreSQL for metadata and Redis for caching, rate-limit storage, and async-capable runtime paths. The template includes a database creation Job and a Superset initialization Job that runs migrations, creates the administrator account, and initializes permissions.

Sealos provisions PostgreSQL 16.4 and Redis 7.2.7 as managed KubeBlocks clusters. The web application is exposed through an HTTPS Ingress and is represented by a Sealos App shortcut.

## Common Use Cases

- **Business dashboards**: Build and share charts, dashboards, and KPI views.
- **SQL exploration**: Query connected databases through SQL Lab.
- **Embedded analytics**: Use Superset as an internal analytics layer for teams.
- **Operational reporting**: Monitor product, sales, infrastructure, or finance data.

## Dependencies for Apache Superset Hosting

The Sealos template includes Superset, PostgreSQL, Redis, a configuration ConfigMap, initialization Jobs, persistent storage, and HTTPS ingress.

### Deployment Dependencies

- [Apache Superset Documentation](https://superset.apache.org/docs/intro) - Official documentation
- [Superset Docker Guide](https://superset.apache.org/docs/installation/docker-compose) - Docker deployment reference
- [Superset GitHub Repository](https://github.com/apache/superset) - Source code and releases

### Implementation Details

**Architecture Components:**

- **PostgreSQL 16.4**: Stores Superset metadata in the `superset` database.
- **Redis 7.2.7**: Stores cache and rate-limit state.
- **PostgreSQL init Job**: Creates the `superset` database idempotently.
- **Superset init Job**: Runs `superset db upgrade`, creates the `admin` user, and runs `superset init`.
- **Superset StatefulSet**: Runs the web application on port `8088`.
- **Persistent volume**: Stores `/app/superset_home`.

**Configuration:**

- Admin username is `admin`.
- Admin password is configured through the `admin_password` deployment input.
- Admin email is `admin@superset.local`.
- `SUPERSET_SECRET_KEY` is generated automatically.

**License Information:**

Apache Superset is licensed under Apache-2.0. This Sealos template is provided under the repository license.

## Why Deploy Apache Superset on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Superset on Sealos, you get:

- **One-Click Deployment**: Deploy Superset with PostgreSQL and Redis together.
- **Managed Dependencies**: Databases and cache are provisioned automatically.
- **Initialized Admin Account**: Log in immediately after the init Job completes.
- **Persistent Storage Included**: Keep Superset state across restarts.
- **Instant Public Access**: Use a public HTTPS URL without manual ingress work.

## Deployment Guide

1. Open the [Apache Superset template](https://sealos.io/products/app-store/superset) and click **Deploy Now**.
2. Set `admin_password`, or keep the generated default, and deploy.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the Superset URL and log in with:
   - **Username**: `admin`
   - **Password**: the `admin_password` value from your deployment form.
5. Add your first database connection from **Settings > Database Connections**.

## Configuration

After deployment, configure Superset through:

- **Superset UI**: Add database connections, datasets, charts, dashboards, and roles.
- **AI Dialog**: Describe deployment changes and let Sealos apply them.
- **Resource Cards**: Adjust Superset, PostgreSQL, Redis, Service, and Ingress settings.

## Scaling

The template deploys a single Superset web replica for a compact self-hosted setup. For higher throughput, increase CPU and memory first, then split worker and beat processes into dedicated workloads if your workload requires async reports or long-running tasks.

## Troubleshooting

### Cannot log in

- Cause: The initialization Job has not completed or the deployment-form password was copied incorrectly.
- Solution: Wait for the `superset-init` Job to complete, then log in as `admin` with the `admin_password` value from your deployment form.

### Database connection test fails

- Cause: Superset cannot reach the target database or the driver is missing from the base image.
- Solution: Verify the target database network address and install additional drivers through a custom image when needed.

## Additional Resources

- [Superset Documentation](https://superset.apache.org/docs/intro)
- [Creating Your First Dashboard](https://superset.apache.org/docs/creating-charts-dashboards/creating-your-first-dashboard)
- [Connecting to Databases](https://superset.apache.org/docs/configuration/databases)

## License

This Sealos template is provided under the repository license. Apache Superset itself is licensed under Apache-2.0.
