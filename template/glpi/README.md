# Deploy and Host GLPI on Sealos

GLPI is an open source IT asset management and service desk platform for inventory, licensing, support requests, and ITIL workflows.

## What This Template Deploys

This template deploys a GLPI application with:

- GLPI `11.0.8` running as a single StatefulSet.
- A Kubeblocks-managed MySQL `8.0.30` cluster with persistent storage.
- An initialization Job that creates the configured GLPI database.
- Persistent storage for `/var/glpi`.
- A public Sealos Ingress with TLS and the generated application hostname.

Database connection values are injected from the Kubeblocks-generated connection Secret. The application and database use the same generated application name, so each deployment is isolated within its namespace.

## Deploy on Sealos

1. Open the GLPI template in the Sealos App Store and click **Deploy Now**.
2. Keep the generated application name and hostname, or provide your own values.
3. Wait for the database cluster and GLPI application to become ready.
4. Open the generated public URL from the application card.
5. Complete the GLPI setup wizard and change the default credentials immediately.

## Configuration

The template exposes these deployment values:

- `app_name`: Name used for the GLPI resources and database cluster.
- `app_host`: Public hostname prefix.
- `glpi_database`: MySQL database name created during initialization.

GLPI application data is stored on a persistent volume mounted at `/var/glpi`. The database uses its own persistent volume, so application and database data survive pod restarts.

## Troubleshooting

If the public URL is not ready, wait for the MySQL cluster, database initialization Job, and GLPI StatefulSet to become ready. For database connection errors, confirm that the generated `*-mysql-conn-credential` Secret exists and that the initialization Job has completed successfully.

## Resources

- [GLPI official website](https://glpi-project.org/)
- [GLPI documentation](https://glpi-project.org/documentation/)
- [GLPI GitHub repository](https://github.com/glpi-project/glpi)
- [Sealos documentation](https://sealos.io/docs)

## License

GLPI is distributed under the GNU General Public License (GPL). This Sealos template is distributed under the license terms of the templates repository.
