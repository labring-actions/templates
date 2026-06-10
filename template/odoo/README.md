# Deploy and Host Odoo on Sealos

Odoo is an open-source business application suite for CRM, sales, inventory, accounting, websites, and operations. This template deploys Odoo 18.0 with PostgreSQL, persistent filestore storage, custom addon storage, and HTTPS ingress on Sealos Cloud.

![Odoo Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odoo/website-screenshot.webp)

## About Hosting Odoo

Odoo runs as a web application backed by PostgreSQL. On first launch, Odoo opens the database manager so you can create the first business database, set the master password, configure the administrator account, and select apps to install.

This Sealos template provisions a KubeBlocks PostgreSQL cluster, an initialization job that creates a dedicated `odoo` database role, persistent `/var/lib/odoo` filestore storage, persistent `/mnt/extra-addons` storage, HTTPS ingress, and an App launcher entry.

## Common Use Cases

- **CRM and Sales Operations**: Manage leads, opportunities, quotations, orders, and customer communication.
- **Inventory and Purchase Workflows**: Track products, vendors, stock movements, and replenishment.
- **Accounting and Invoicing**: Run invoicing and finance workflows with Odoo apps.
- **Website and Ecommerce**: Build a business website or store from Odoo modules.
- **Custom Business Apps**: Add custom modules through `/mnt/extra-addons`.

## Dependencies for Odoo Hosting

The Sealos template includes Odoo, PostgreSQL, a database role initialization job, persistent Odoo data storage, persistent addon storage, a Service, an Ingress, and an App launcher entry.

### Deployment Dependencies

- [Odoo Documentation](https://www.odoo.com/documentation/) - Official product documentation
- [Odoo Docker Image Documentation](https://hub.docker.com/_/odoo) - Official container environment and volume guide
- [Odoo GitHub Repository](https://github.com/odoo/odoo) - Source code and releases

## Implementation Details

### Architecture Components

- **Odoo Web**: Runs on port `8069`
- **PostgreSQL**: Stores Odoo business databases
- **Database Init Job**: Creates a dedicated `odoo` PostgreSQL role with `CREATEDB`
- **Filestore Storage**: Persists attachments and Odoo runtime data at `/var/lib/odoo`
- **Extra Addons Storage**: Persists custom modules at `/mnt/extra-addons`

### Resource Allocation

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Odoo | 20m | 200m | 51Mi | 512Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### Configuration

The template writes `odoo.conf` through a ConfigMap, enables proxy mode for Sealos ingress, and generates the Odoo master password automatically. PostgreSQL admin credentials are injected from KubeBlocks-managed secrets only into the init job, while the Odoo container uses the dedicated `odoo` role created by the job. Odoo uses `512Mi` memory because the first database creation workflow performs migrations and module loading.

### License Information

Odoo Community Edition is licensed under [LGPL-3.0](https://github.com/odoo/odoo/blob/18.0/LICENSE). This template follows the licensing policy of the Sealos templates repository.

## Why Deploy Odoo on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies deployment and operations. By deploying Odoo on Sealos, you get:

- **One-Click Deployment**: Launch Odoo with PostgreSQL, storage, and HTTPS from one template page.
- **Managed PostgreSQL**: Store Odoo business databases in a KubeBlocks-managed PostgreSQL cluster.
- **Persistent Filestore**: Keep attachments and runtime data across restarts.
- **Addon Storage**: Reserve a persistent path for custom Odoo modules.
- **Simple Operations**: Resize resources or inspect logs from the Sealos Canvas.

## Deployment Guide

1. Open the [Odoo template](https://sealos.io/products/app-store/odoo) and click **Deploy Now**.
2. Review the generated parameters in the popup dialog and deploy.
3. Wait for PostgreSQL, the role init job, and Odoo to become ready.
4. Open the generated URL and create the first Odoo database:
   - Use the generated master password from the template defaults
   - Enter a database name
   - Enter the administrator email and password
   - Select the language and country
   - Create the database
5. Log in with the administrator account, install at least one app such as CRM or Sales, and create a test record.

## Configuration

Use Odoo settings for apps, users, companies, email, modules, and business workflows. Use Sealos Canvas to resize CPU, memory, `/var/lib/odoo`, `/mnt/extra-addons`, or PostgreSQL storage.

## Scaling

This template is optimized for a single Odoo instance. Increase CPU and memory when app installation, reporting, imports, or scheduled jobs require more headroom. Increase PostgreSQL and filestore storage as business data grows.

## Troubleshooting

**Issue: Odoo shows the database manager**
- Cause: The first business database has not been created yet.
- Solution: Create a database using the generated master password.

**Issue: Odoo refuses to start with the postgres user**
- Cause: The official Odoo image rejects the `postgres` database role for application startup.
- Solution: This template creates and uses a dedicated `odoo` role automatically.

## Additional Resources

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [Odoo Docker Image](https://hub.docker.com/_/odoo)
- [Odoo GitHub Issues](https://github.com/odoo/odoo/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing policy of the templates repository. Odoo Community Edition itself is licensed under LGPL-3.0.
