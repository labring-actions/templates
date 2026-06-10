# Deploy and Host Grafana on Sealos

Grafana is an open-source analytics and visualization platform. This template deploys Grafana on Sealos Cloud with persistent storage and an optional managed PostgreSQL database.

![Grafana Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/grafana/website-screenshot.webp)

## About Hosting Grafana

Grafana runs as a single StatefulSet with persistent storage for dashboards, plugins, users, and local configuration. By default, Grafana uses its embedded SQLite database on the persistent volume for a compact self-hosted setup.

When `use_postgresql` is enabled, the template provisions a managed PostgreSQL 16.4 database and configures Grafana to store application data there. Sealos also provides the public HTTPS URL, service routing, and resource controls.

## Common Use Cases

- **Metrics dashboards**: Build dashboards from Prometheus, Graphite, PostgreSQL, and other data sources.
- **Operations monitoring**: Track infrastructure health, application metrics, and alert trends.
- **Log and trace exploration**: Connect Loki, Tempo, and related observability backends.
- **Team reporting**: Share panels and dashboards with operators and product teams.

## Dependencies for Grafana Hosting

The Sealos template includes the Grafana container, persistent storage, public HTTPS ingress, and optional PostgreSQL.

### Deployment Dependencies

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/) - Official documentation
- [Grafana Docker Image](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/) - Docker deployment reference
- [Grafana GitHub Repository](https://github.com/grafana/grafana) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Grafana StatefulSet**: Runs the Grafana web application on port `3000`.
- **Persistent volume**: Stores `/var/lib/grafana` data.
- **Optional PostgreSQL**: Stores Grafana metadata when `use_postgresql` is set to `true`.
- **Ingress and App**: Publish the HTTPS web interface from Sealos.

**Configuration:**

- Admin username is `admin`.
- Admin password is generated automatically as `admin_password`.
- User self-signup is disabled by default.
- SQLite is the default storage mode; PostgreSQL is available through the deployment option.

**License Information:**

Grafana is licensed under AGPL-3.0. This Sealos template is provided under the repository license.

## Why Deploy Grafana on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Grafana on Sealos, you get:

- **One-Click Deployment**: Deploy Grafana with a single click.
- **Persistent Storage Included**: Keep dashboards and configuration across restarts.
- **Optional Managed Database**: Use PostgreSQL for a more durable metadata store.
- **Instant Public Access**: Receive an HTTPS URL automatically.
- **Easy Customization**: Adjust resources, environment variables, and storage from the Canvas.

## Deployment Guide

1. Open the [Grafana template](https://sealos.io/products/app-store/grafana) and click **Deploy Now**.
2. Choose whether to enable `use_postgresql`.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the Grafana URL and log in with:
   - **Username**: `admin`
   - **Password**: the generated `admin_password` value shown in your deployment parameters.
5. Change the admin password when Grafana prompts you on first login.

## Configuration

After deployment, configure Grafana through:

- **Grafana UI**: Add data sources, dashboards, folders, and users.
- **AI Dialog**: Describe resource or environment changes and let Sealos apply them.
- **Resource Cards**: Click the StatefulSet, Service, Ingress, or PostgreSQL cards to update deployment settings.

## Scaling

Grafana is deployed as a single replica because the default local storage and SQLite mode are single-writer. For larger deployments, enable PostgreSQL, keep shared plugin and data requirements in mind, and then adjust CPU and memory from the StatefulSet card.

## Troubleshooting

### Cannot log in

- Cause: The generated admin password was copied incorrectly.
- Solution: Check the `admin_password` deployment value and log in as `admin`.

### Dashboards disappear after restart

- Cause: The persistent volume was removed or replaced.
- Solution: Keep the Grafana StatefulSet volume and PVC when customizing the deployment.

## Additional Resources

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana Data Sources](https://grafana.com/docs/grafana/latest/datasources/)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)

## License

This Sealos template is provided under the repository license. Grafana itself is licensed under AGPL-3.0.
