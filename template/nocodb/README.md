# Deploy and Host NocoDB on Sealos

NocoDB turns databases into collaborative smart spreadsheets and no-code applications. This template deploys NocoDB with persistent storage plus optional Sealos-managed PostgreSQL and S3-compatible object storage.

![NocoDB Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/nocodb/website-screenshot.webp)

## About Hosting NocoDB

NocoDB provides a spreadsheet-style interface for building tables, views, forms, automations, and lightweight internal tools on top of relational data. It is commonly used as an open-source Airtable alternative for teams that want database-backed collaboration without writing a custom admin interface.

This Sealos template runs the NocoDB web service from the pinned `nocodb/nocodb:2026.06.2` image with the official `1024Mi` minimum memory. The default configuration keeps the SQLite metadata database and attachments on the persistent `/usr/app/data` volume. Independent deployment options can provision a PostgreSQL `postgresql-16.4.0` cluster for metadata and a private Sealos Object Storage bucket for attachments.

## Common Use Cases

- **Internal data tools**: Build spreadsheet-like interfaces for operations, support, and admin workflows.
- **No-code apps**: Create forms, views, and collaborative interfaces on top of structured data.
- **Database frontends**: Manage PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, and other connected databases through a visual UI.
- **Team collaboration**: Share database-backed workspaces with role-based access.

## Dependencies for NocoDB Hosting

The Sealos template includes the NocoDB runtime, persistent application storage, HTTPS ingress, and optional managed data services.

### Deployment Dependencies

- [NocoDB Documentation](https://docs.nocodb.com/) - Official product documentation
- [NocoDB GitHub Repository](https://github.com/nocodb/nocodb) - Source code and release notes
- [NocoDB Docker Image](https://hub.docker.com/r/nocodb/nocodb) - Official container image

### Implementation Details

**Architecture Components:**

- **NocoDB**: Web application and API service running on port `8080`
- **Metadata database**: SQLite on the application volume by default, with optional Kubeblocks-managed PostgreSQL `postgresql-16.4.0`
- **Attachment storage**: Local storage on the application volume by default, with optional private Sealos Object Storage
- **Persistent storage**: `1Gi` volume mounted at `/usr/app/data` for SQLite and local attachments
- **Ingress**: Sealos-managed HTTPS public endpoint

**Configuration:**

- `use_postgresql` controls the independent PostgreSQL branch. NocoDB uses SQLite on `/usr/app/data` when the option is disabled.
- `enable_s3_storage` controls the independent Sealos Object Storage branch. NocoDB uses local attachment storage when the option is disabled.
- `NC_DB` is assembled from the Kubeblocks PostgreSQL connection secret when PostgreSQL is enabled.
- `NC_SITE_URL` is set to the generated Sealos HTTPS URL.
- NocoDB receives S3 endpoint and bucket credentials directly from the Sealos-managed bucket secret.
- `NC_ADMIN_EMAIL` and `NC_ADMIN_PASSWORD` initialize the first admin account.

**License Information:**

NocoDB is available under the GNU Affero General Public License v3.0. Review the upstream repository for current licensing details.

## Why Deploy NocoDB on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is ideal for running modern web applications and database-backed tools. By deploying NocoDB on Sealos, you get:

- **One-Click Deployment**: Deploy NocoDB and the selected data services from one template.
- **Flexible Metadata Storage**: Start with SQLite or enable a Kubeblocks PostgreSQL cluster.
- **Managed Object Storage**: Move attachments to a private Sealos S3-compatible bucket with one option.
- **Persistent Storage Included**: Keep NocoDB local data across restarts and rescheduling.
- **Instant Public Access**: Open NocoDB through a generated HTTPS URL after deployment.
- **Easy Customization**: Adjust resources and environment variables through Sealos resource cards or the AI dialog.
- **Kubernetes Without the Complexity**: Run on Kubernetes while managing the app through the Sealos dashboard.

## Deployment Guide

1. Open the [NocoDB template](https://sealos.io/products/app-store/nocodb) and click **Deploy Now**.
2. Configure the deployment parameters:
   - `NC_ADMIN_EMAIL`: initial admin email address.
   - `NC_ADMIN_PASSWORD`: required initial admin password with at least 8 characters, an uppercase letter, a number, and a special character.
   - `use_postgresql`: enable the Sealos-managed PostgreSQL metadata database. The default SQLite database persists on the application volume.
   - `enable_s3_storage`: enable Sealos Object Storage for attachments. The default local attachment storage persists on the application volume.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated NocoDB URL from the App card. The App opens the `/signin` page.
5. Sign in at `/signin` with the configured `NC_ADMIN_EMAIL` and `NC_ADMIN_PASSWORD` values.

## Configuration

After deployment, you can configure NocoDB through:

- **NocoDB UI**: Create workspaces, bases, tables, views, forms, and integrations.
- **AI Dialog**: Describe changes you want Sealos to apply to resources.
- **Resource Cards**: Click the StatefulSet, optional PostgreSQL cluster, optional Object Storage bucket, service, or ingress cards to modify settings.

## Scaling

To adjust resources:

1. Open the Canvas for your deployment.
2. Click the NocoDB StatefulSet resource card.
3. Adjust CPU or memory resources as needed.
4. Apply the changes in the dialog.

The template uses a conservative single-replica deployment with persistent storage. Review NocoDB upstream guidance before changing replica count.

## Troubleshooting

### Cannot sign in

Confirm that you are using the exact `NC_ADMIN_EMAIL` and `NC_ADMIN_PASSWORD` entered during deployment. The template initializes this account on first start.

### Application is still starting

NocoDB may take a few minutes during the first cold start. The PostgreSQL option adds database provisioning and metadata initialization time. Wait for the NocoDB StatefulSet to show `Ready` in the Sealos Canvas.

### Getting Help

- [NocoDB Documentation](https://docs.nocodb.com/)
- [NocoDB GitHub Issues](https://github.com/nocodb/nocodb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [NocoDB Website](https://nocodb.com/)
- [NocoDB API Documentation](https://docs.nocodb.com/api-reference/introduction/)
- [NocoDB Docker Hub](https://hub.docker.com/r/nocodb/nocodb)

## License

NocoDB is licensed under AGPL-3.0. See the upstream project for details.
