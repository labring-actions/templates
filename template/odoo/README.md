# Deploy and Host Odoo on Sealos

Odoo is an open-source business application suite for CRM, sales, inventory, accounting, websites, and operations. This template deploys Odoo 18.0 with PostgreSQL, persistent filestore storage, custom addon storage, and HTTPS ingress on Sealos Cloud.

![Odoo Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odoo/website-screenshot.webp)

## About Hosting Odoo

Odoo runs as a web application backed by PostgreSQL. A fresh Odoo deployment starts at the database manager, where you create the first business database and define the administrator account for that database.

The Sealos template provisions a KubeBlocks PostgreSQL cluster, a dedicated `odoo` database role, persistent `/var/lib/odoo` filestore storage, persistent `/mnt/extra-addons` storage, a Service, an HTTPS Ingress, and an App launcher. It also guards startup against an empty default `odoo` database so the first-run database manager remains reachable.

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

**Architecture Components:**

- **Odoo Web**: Serves the browser UI on port `8069`.
- **PostgreSQL**: Stores Odoo business databases in a KubeBlocks-managed cluster.
- **Database Init Job**: Creates a dedicated `odoo` PostgreSQL role with `CREATEDB`.
- **Startup Gate**: Waits for PostgreSQL and removes only an empty, uninitialized default `odoo` database if one exists.
- **Filestore Storage**: Persists attachments and Odoo runtime data at `/var/lib/odoo`.
- **Extra Addons Storage**: Persists custom modules at `/mnt/extra-addons`.

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Odoo | 20m | 200m | 51Mi | 512Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

**Configuration:**

The template writes `odoo.conf` through a ConfigMap, enables proxy mode for Sealos ingress, and generates the Odoo master password automatically. PostgreSQL admin credentials come from KubeBlocks-managed secrets, while Odoo connects through the dedicated `odoo` role. Odoo uses `512Mi` memory because first database creation performs migrations and module loading.

**License Information:**

Odoo Community Edition is licensed under [LGPL-3.0](https://github.com/odoo/odoo/blob/18.0/LICENSE). This template follows the licensing policy of the Sealos templates repository.

## Why Deploy Odoo on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, operations, and application lifecycle management. By deploying Odoo on Sealos, you get:

- **One-Click Deployment**: Launch Odoo with PostgreSQL, storage, and HTTPS from one template page.
- **Managed PostgreSQL**: Store Odoo business databases in a KubeBlocks-managed PostgreSQL cluster.
- **Persistent Storage Included**: Keep attachments, runtime data, and custom addons across restarts.
- **Instant Public Access**: Use the generated HTTPS URL without manual ingress or certificate setup.
- **Simple Operations**: Resize resources, inspect logs, and update settings from the Sealos Canvas.
- **Pay-as-You-Go Efficiency**: Start with compact resources and scale when your business workload grows.

## Deployment Guide

1. Open the [Odoo template](https://sealos.io/products/app-store/odoo) and click **Deploy Now**.
2. Review the generated parameters in the popup dialog and deploy.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated Odoo URL. On a fresh deployment, Odoo shows the database manager instead of a normal sign-up page.
5. Create the first Odoo database:
   - **Master Password**: use the generated `admin_passwd` value from the Odoo ConfigMap (`odoo.conf`).
   - **Database Name**: enter a business database name such as `company`.
   - **Email**: enter the administrator login email.
   - **Password**: enter the administrator login password.
   - **Language / Country**: choose your preferred options.
6. Click **Create database** and wait for Odoo to initialize the base modules.
7. Log in with the administrator email and password you entered during database creation.
8. Open **Apps** and install the modules you need, such as CRM, Sales, Inventory, or Accounting.

## Registration and Login

Odoo does not use public self-registration for the first administrator. The first administrator is created when you create the first database from the database manager.

After the first database exists, use `/web/login` or the generated app URL to log in. The login credentials are the administrator email and password you entered on the database creation form. The generated `admin_passwd` is only the database manager master password; it is not the administrator login password.

## Configuration

Use Odoo settings for apps, users, companies, email, modules, and business workflows. Use the Sealos Canvas for operational changes: describe the desired change in the AI dialog, or click resource cards to adjust CPU, memory, `/var/lib/odoo`, `/mnt/extra-addons`, or PostgreSQL storage.

## Scaling

This template is optimized for a single Odoo instance. Increase CPU and memory when app installation, reporting, imports, or scheduled jobs require more headroom. Increase PostgreSQL and filestore storage as business data grows.

## Troubleshooting

**Issue: Odoo shows the database manager**
- Cause: The first business database has not been created yet.
- Solution: Create a database using the generated master password from `odoo.conf`.

**Issue: Login fails after creating a database**
- Cause: The master password and administrator password are different.
- Solution: Log in with the administrator email and password from the database creation form.

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
