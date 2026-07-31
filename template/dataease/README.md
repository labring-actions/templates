# Deploy and Host DataEase on Sealos

DataEase is an open-source business intelligence and data visualization platform for building datasets, dashboards, and large-screen data displays. This Sealos template deploys DataEase Community Edition 2.10.26 with a dedicated MySQL database, persistent application storage, and a managed HTTPS endpoint.

## About Hosting DataEase

DataEase provides a browser-based workspace for connecting data sources, preparing datasets, and building interactive visualizations. The template keeps the application configuration, uploaded assets, maps, plugins, fonts, exports, and MySQL metadata on persistent volumes.

The deployment initializes a local administrator account. Administrators can create and manage additional users from DataEase system settings.

## Common Use Cases

- **Operational Dashboards**: Track sales, finance, support, and service metrics.
- **Self-Service Analytics**: Let teams explore governed datasets through a visual interface.
- **Embedded Visualization**: Publish dashboards and data screens for internal applications.
- **Data Source Consolidation**: Connect MySQL, PostgreSQL, SQL Server, APIs, files, and other supported sources.

## Dependencies for DataEase Hosting

The template includes the runtime dependencies required for a standalone DataEase deployment:

- **DataEase 2.10.26**: Runs the web application and analytics service.
- **KubeBlocks MySQL 8.0.30**: Stores users, permissions, datasets, dashboards, and application metadata.
- **Persistent Volumes**: Store configuration, logs, uploads, maps, exports, plugins, fonts, and localization data.
- **Sealos Ingress**: Publishes the application through a managed HTTPS endpoint.

### Deployment Dependencies

- [DataEase Documentation](https://dataease.io/docs/v2/)
- [DataEase Installation Guide](https://dataease.io/docs/v2/installation/online_installation/)
- [DataEase GitHub Repository](https://github.com/dataease/dataease)

## Implementation Details

### Architecture

The template creates:

- One DataEase StatefulSet and Service.
- One KubeBlocks MySQL cluster.
- One database initialization Job.
- One KubeBlocks Configuration resource for DataEase-compatible MySQL parameters.
- One Ingress and one Sealos App link.

The MySQL configuration sets `max_connections=2000`, `max_connect_errors=6000`, and `group_concat_max_len=1024000`, matching the requirements of the official DataEase deployment configuration.

### Persistent Data

The DataEase StatefulSet uses:

- `1Gi` for `/opt/apps/config`.
- `1Gi` for `/opt/dataease2.0`.

The MySQL cluster uses a separate `1Gi` data volume. Back up the MySQL cluster and both DataEase volumes together to preserve a complete deployment.

### Resource Baseline

The default application limit is `500m` CPU and `1024Mi` memory. This tier completed a clean cold start, authenticated successfully, and loaded the bundled sales dashboard with zero restarts. The observed dashboard working set was approximately `768Mi`.

The MySQL component uses the Sealos database service baseline of `500m` CPU and `512Mi` memory.

## Why Deploy DataEase on Sealos?

- **One-Click Deployment**: Create DataEase, MySQL, persistent storage, and HTTPS networking from one template.
- **Persistent Analytics Workspace**: Keep dashboards, datasets, accounts, and uploaded assets across restarts.
- **Managed Database Lifecycle**: Operate MySQL through a KubeBlocks resource card in Sealos Canvas.
- **Integrated Operations**: Inspect logs, resources, storage, and networking from the same Canvas.
- **Adjustable Resources**: Scale CPU, memory, and storage as dashboard usage grows.

## Deployment Guide

1. Open the [DataEase template](https://sealos.io/products/app-store/dataease).
2. Click **Deploy Now**.
3. Wait for DataEase and MySQL to become ready. A fresh deployment usually takes 2-3 minutes.
4. Open the generated HTTPS application URL.

## Login and First Use

Use the upstream default administrator credentials:

```text
Username: admin
Password: DataEase@123456
```

After signing in:

1. Open the administrator menu in the upper-right corner.
2. Select **Change Password**.
3. Set a private administrator password.
4. Open **Data Preparation > Data Sources** to connect a data source, or open **Dashboards** to explore the bundled example.

User accounts are managed by an administrator from **System Settings**.

## Configuration

After deployment, use Sealos Canvas to manage:

- **DataEase StatefulSet**: CPU, memory, probes, image version, and application storage.
- **MySQL Cluster**: Database resources, storage, status, and backups.
- **Ingress**: Public hostname, TLS, upload size, and request timeouts.
- **Application Configuration**: The persistent `application.yml` file generated during the first startup.

## Scaling

For larger teams or complex dashboards:

1. Increase DataEase memory before increasing concurrent dashboard traffic.
2. Increase CPU when query rendering or dashboard loading becomes CPU-bound.
3. Expand the DataEase and MySQL volumes before storage usage reaches capacity.
4. Review MySQL metrics and connection usage after adding many data sources.

## Backup and Restore

A complete backup includes:

1. The KubeBlocks MySQL data volume.
2. The DataEase configuration volume.
3. The DataEase application data volume.

Restore the database and both application volumes from the same backup point, then restart the DataEase StatefulSet.

## Troubleshooting

### The login page returns a 401 response

Use the current template configuration with an empty servlet context path. A literal `/` context path is interpreted incorrectly by the DataEase 2.10.26 request whitelist.

### Data sources report too many database connections

Open the MySQL Configuration resource and confirm:

```text
max_connections=2000
max_connect_errors=6000
group_concat_max_len=1024000
```

The template applies these settings declaratively and retains them across MySQL Pod replacements.

### DataEase remains in the startup phase

Confirm that the MySQL cluster is `Running` and the database initialization Job is `Complete`. The DataEase Pod waits for the `dataease` database before starting.

### The default password does not work

The initial password applies to a fresh database. Use the password previously configured by the administrator when restoring an existing MySQL volume.

## Additional Resources

- [DataEase User Manual](https://dataease.io/docs/v2/user_manual/)
- [DataEase Releases](https://github.com/dataease/dataease/releases)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

DataEase Community Edition is distributed under the GNU Affero General Public License v3.0. This Sealos template follows the license of the Sealos templates repository.
