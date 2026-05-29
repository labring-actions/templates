# Deploy and Host Dolibarr on Sealos

Dolibarr is an open-source ERP and CRM suite for managing customers, suppliers, invoices, orders, inventory, projects, and everyday business operations. This template deploys Dolibarr with a managed MySQL database and persistent application storage on Sealos Cloud.

## About Hosting Dolibarr

Dolibarr runs as a web-based business management system backed by a relational database. The Sealos template provisions the Dolibarr application, a Kubeblocks-managed MySQL cluster, persistent volumes for uploaded documents and custom modules, and public HTTPS access through Sealos Ingress.

The deployment is configured for first-boot automatic installation. During deployment, you provide the administrator username and password, company name, country code, and initial modules. Dolibarr then creates the database schema, initializes the company profile, enables practical business modules, and exposes the web UI through the generated Sealos domain.

## Common Use Cases

- **CRM and Contact Management**: Track customers, suppliers, contacts, opportunities, and account activity.
- **Invoicing and Billing**: Create invoices, manage payments, and follow customer billing workflows.
- **Inventory and Product Catalogs**: Maintain products, services, stock records, and related commercial documents.
- **Project Operations**: Organize projects, tasks, business records, and internal collaboration.
- **Small Business ERP**: Run core back-office processes from a single browser-based application.

## Dependencies for Dolibarr Hosting

The Sealos template includes all required runtime dependencies: Dolibarr PHP application runtime, MySQL database resources, database initialization job, persistent volumes, internal service discovery, and public ingress exposure.

### Deployment Dependencies

- [Dolibarr Official Website](https://www.dolibarr.org/) - Product overview and community information
- [Dolibarr Documentation](https://wiki.dolibarr.org/) - Official user and administrator documentation
- [Dolibarr Docker Repository](https://github.com/Dolibarr/dolibarr-docker) - Source Docker image and environment configuration
- [Sealos Documentation](https://sealos.io/docs) - Platform guides and operational docs

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Dolibarr StatefulSet**: Main application service running `dolibarr/dolibarr:23.0.3-php8.2` pinned by digest.
- **MySQL Cluster**: Kubeblocks-managed ApeCloud MySQL `ac-mysql-8.0.30-1` for persistent relational data.
- **MySQL Init Job**: Creates the `dolibarr` database before the application performs its automatic installer flow.
- **Service + Ingress**: Internal service on port `80` and public HTTPS ingress with Sealos domain routing.
- **Persistent Storage**: PVC-backed paths mounted at `/var/www/documents` and `/var/www/html/custom`.

**Configuration:**

- Database connection values are injected from the Kubeblocks generated MySQL secret.
- `DOLI_INSTALL_AUTO=1` enables first-boot installation and database schema creation.
- `DOLI_ADMIN_LOGIN` and `DOLI_ADMIN_PASSWORD` define the first administrator account.
- `DOLI_COMPANY_COUNTRYCODE` and `DOLI_ENABLE_MODULES` complete the initial company setup and enable practical modules.
- The application resource floor was validated with a live cold-start deployment at `100m` CPU and `128Mi` memory for the Dolibarr container. The managed MySQL cluster uses `500m` CPU and `512Mi` memory.

**License Information:**

Dolibarr is licensed under GNU General Public License v3.0 or later.

## Why Deploy Dolibarr on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to production operations. By deploying Dolibarr on Sealos, you get:

- **One-Click Deployment**: Launch Dolibarr and its database stack without manual Kubernetes setup.
- **Managed Database Experience**: Use Kubeblocks MySQL resources with standardized secret and service wiring.
- **Persistent Storage Included**: Keep uploaded documents and custom modules safe across pod restarts.
- **Instant Public Access**: Receive a public domain with TLS enabled by platform ingress.
- **Easy Customization**: Update resources and environment settings from Canvas dialogs.
- **Zero Kubernetes Expertise Required**: Get Kubernetes reliability without writing infrastructure YAML manually.
- **AI-Assisted Operations**: Use the Canvas AI dialog for post-deployment updates and routine adjustments.

Deploy Dolibarr on Sealos and focus on running business workflows instead of managing infrastructure.

## Deployment Guide

1. Open the [Dolibarr template](https://sealos.io/products/app-store/dolibarr) and click **Deploy Now**.
2. Configure the deployment parameters in the popup dialog:
   - `DOLI_ADMIN_LOGIN`: Administrator username created during first boot. The default is `admin`.
   - `DOLI_ADMIN_PASSWORD`: Administrator password created during first boot. Set a strong password before deployment.
   - `DOLI_COMPANY_NAME`: Company name used in the initial Dolibarr setup.
   - `DOLI_COMPANY_COUNTRYCODE`: Two-letter country code, such as `US`, `CN`, or `DE`.
   - `DOLI_ENABLE_MODULES`: Comma-separated modules enabled at first boot. The default enables company, invoicing, stock, and project features.
3. Wait for deployment to complete. Dolibarr performs database initialization during the first cold start, so the initial startup can take several minutes.
4. After deployment, open the generated Dolibarr URL from the app card.
5. Log in with the `DOLI_ADMIN_LOGIN` and `DOLI_ADMIN_PASSWORD` values you configured during deployment. Dolibarr does not require separate self-registration for the first administrator account.
6. After the first login, create additional users and rotate the administrator password according to your security policy.

## Configuration

After deployment, configure Dolibarr through:

- **AI Dialog in Canvas**: Describe desired changes and let AI apply updates.
- **Resource Cards**: Open StatefulSet, Service, Ingress, or database cards to adjust resources and environment variables.
- **Dolibarr Setup and Admin Menus**: Configure company profile, users, modules, permissions, email settings, and business workflows from the web interface.

## Scaling

To scale Dolibarr resources:

1. Open the deployment in Canvas.
2. Click the Dolibarr StatefulSet resource card.
3. Adjust CPU and memory limits/requests.
4. Apply updates and monitor rollout status.

For most Dolibarr installations, keep a single application replica and scale vertically first because uploaded documents and installed custom modules are stored on persistent volumes attached to the StatefulSet.

## Troubleshooting

### Common Issues

**Issue: First startup takes longer than expected**
- Cause: Dolibarr creates database tables and initializes modules during first boot.
- Solution: Wait for the StatefulSet pod to become ready and review application logs if startup exceeds the probe window.

**Issue: Login page returns after submitting credentials**
- Cause: The username or password does not match the deployment inputs.
- Solution: Use the `DOLI_ADMIN_LOGIN` and `DOLI_ADMIN_PASSWORD` values configured at deployment time.

**Issue: Dolibarr reports setup is not complete**
- Cause: Required company or module setup values were omitted or changed incorrectly.
- Solution: Verify `DOLI_COMPANY_NAME`, `DOLI_COMPANY_COUNTRYCODE`, and `DOLI_ENABLE_MODULES`, then complete any remaining setup steps in the Dolibarr admin interface.

**Issue: Database connection errors**
- Cause: The MySQL cluster is still initializing or generated secret values are not ready.
- Solution: Check the MySQL cluster and init job status in Canvas, then restart the Dolibarr pod after the database is healthy.

### Getting Help

- [Dolibarr Documentation](https://wiki.dolibarr.org/)
- [Dolibarr GitHub Issues](https://github.com/Dolibarr/dolibarr/issues)
- [Dolibarr Docker Issues](https://github.com/Dolibarr/dolibarr-docker/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Dolibarr User Documentation](https://wiki.dolibarr.org/index.php/User_documentation)
- [Dolibarr Administrator Documentation](https://wiki.dolibarr.org/index.php/Admin_documentation)
- [Dolibarr Docker Environment Variables](https://github.com/Dolibarr/dolibarr-docker)

## License

Dolibarr is licensed under GNU General Public License v3.0 or later.
This Sealos template is distributed under the license terms of the templates repository.
