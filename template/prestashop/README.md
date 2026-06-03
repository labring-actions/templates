# Deploy and Host PrestaShop on Sealos

PrestaShop is an open-source e-commerce platform for building customizable online stores, product catalogs, carts, checkout flows, and merchant back offices. This template deploys PrestaShop 9.1.3 with a KubeBlocks-managed MySQL database, persistent application storage, and a public HTTPS endpoint on Sealos Cloud.

![PrestaShop Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/prestashop/website-screenshot.webp)

## About Hosting PrestaShop

PrestaShop runs as a PHP and Apache web application backed by MySQL. The Sealos template provisions the PrestaShop container, a MySQL 8 database, an initialization job for the `prestashop` database, persistent storage for `/var/www/html`, an internal Service, an HTTPS Ingress, and a Sealos App entry.

The template performs the first installation automatically. During deployment, it creates the configured administrator account, installs the shop, removes the install folder, and exposes the back office at `/admin-dev/`. It also includes a small reverse-proxy configuration file so PrestaShop detects the Sealos HTTPS route correctly behind Ingress.

Application files are stored on a persistent volume, while store data, products, orders, customers, and configuration are stored in MySQL. This keeps the shop available across pod restarts and makes the deployment suitable for evaluation, demos, and light storefront workloads.

## Common Use Cases

- **Online storefronts**: Launch a small or medium e-commerce site with product pages, carts, checkout, and customer accounts.
- **Catalog and merchandising demos**: Test PrestaShop themes, catalog organization, pricing, and promotion workflows.
- **Merchant back-office training**: Use the admin dashboard to practice product management, orders, customers, and shop settings.
- **Extension testing**: Evaluate PrestaShop modules, payment integrations, and themes in an isolated Sealos workspace.
- **Prototype commerce projects**: Validate an e-commerce idea before moving to a larger production configuration.

## Dependencies for PrestaShop Hosting

The Sealos template includes the required runtime components: the `prestashop/prestashop:9.1.3-apache` container image, a KubeBlocks MySQL `ac-mysql-8.0.30-1` cluster, a database initialization job, persistent storage, a Kubernetes Service, an Ingress, and a Sealos App entry.

### Deployment Dependencies

- [PrestaShop Project](https://www.prestashop-project.org/) - Product overview and community project information
- [PrestaShop Documentation](https://docs.prestashop-project.org/) - User and administrator documentation
- [PrestaShop Developer Documentation](https://devdocs.prestashop-project.org/) - Technical documentation for developers and integrators
- [PrestaShop GitHub Repository](https://github.com/PrestaShop/PrestaShop) - Source code and release information
- [PrestaShop Docker Image](https://hub.docker.com/r/prestashop/prestashop) - Official container image used by this template

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **PrestaShop Web Service**: Runs `prestashop/prestashop:9.1.3-apache` on port `80` and serves the storefront, back office, and PHP application runtime.
- **MySQL Database**: KubeBlocks-managed MySQL `ac-mysql-8.0.30-1` stores shop configuration, products, customers, carts, orders, modules, and employee accounts.
- **MySQL Init Job**: Waits for MySQL and creates the `prestashop` database with `utf8mb4` settings before the PrestaShop installer connects.
- **Persistent Application Storage**: A `1Gi` volume mounted at `/var/www/html` preserves the installed application files and uploaded assets.
- **Reverse-Proxy ConfigMap**: Injects `defines_custom.inc.php` so PrestaShop trusts `X-Forwarded-Proto` and `X-Forwarded-Host` from the Sealos HTTPS Ingress.
- **Ingress and App Entry**: Exposes the shop through a generated HTTPS domain and creates a Sealos dashboard link.

**Configuration:**

The template automatically configures:

- `PS_INSTALL_AUTO=1` to run the first installation during container startup.
- `PS_INSTALL_DB=0` because the MySQL init job creates the database before installation.
- `PS_DOMAIN=${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}` so generated storefront and back-office URLs use the Sealos domain.
- `PS_ENABLE_SSL=1` with an HTTPS-aware reverse-proxy configuration.
- `PS_FOLDER_ADMIN=admin-dev`, making the back office available at `/admin-dev/`.
- `ADMIN_MAIL` and `ADMIN_PASSWD` from deployment inputs for the first administrator account.
- MySQL connection details from the KubeBlocks connection Secret.

**Resource Profile:**

The deployed PrestaShop container uses a compact tested profile of `200m` CPU and `512Mi` memory. A `256Mi` memory limit was not sufficient for the initial install and caused an OOM restart, so avoid reducing the web container below `512Mi`.

**License Information:**

PrestaShop is licensed under the Open Software License 3.0. This Sealos template is provided as deployment configuration for PrestaShop and does not change the upstream application license.

## Why Deploy PrestaShop on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and operations. By deploying PrestaShop on Sealos, you get:

- **One-Click Deployment**: Deploy PrestaShop, MySQL, storage, networking, and the dashboard entry from one template.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed reliability without writing manifests manually.
- **Persistent Data Included**: Keep application files and database data across restarts.
- **Instant Public Access**: Each deployment receives an HTTPS URL for the storefront and admin back office.
- **Easy Customization**: Adjust environment variables, CPU, memory, and storage through the Sealos Canvas and AI dialog.
- **Pay-As-You-Go Resources**: Start from a compact resource profile and scale only when your store needs more capacity.

Deploy PrestaShop on Sealos and focus on store setup instead of managing infrastructure.

## Deployment Guide

1. Open the [PrestaShop template](https://sealos.io/products/app-store/prestashop) and click **Deploy Now**.
2. Configure the required administrator parameters:
   - `ADMIN_MAIL`: the administrator email used to sign in to the back office.
   - `ADMIN_PASSWD`: the administrator password used to sign in to the back office.
3. Wait for deployment to complete. The first install usually takes several minutes because PrestaShop initializes MySQL, installs the shop, and prepares the back office.
4. Open the generated PrestaShop URL from the Sealos App entry.
5. Use the storefront at `https://<your-app-host>.<SEALOS_CLOUD_DOMAIN>/`.
6. Use the back office at `https://<your-app-host>.<SEALOS_CLOUD_DOMAIN>/admin-dev/`.
7. Sign in with the `ADMIN_MAIL` and `ADMIN_PASSWD` values configured during deployment. If you kept the defaults, use:
   - Email: `admin@example.com`
   - Password: `PrestaShopDemo2026!`
8. After the first login, change the administrator email and password from the back-office employee settings before using the store for real data.

Customer accounts are created from the storefront sign-in page. Open the storefront, choose the sign-in option, and use the registration form to create a customer account for checkout testing.

## Configuration

After deployment, you can configure PrestaShop through:

- **Back Office**: Open `/admin-dev/` to manage products, categories, orders, customers, modules, themes, payment settings, shipping, taxes, and shop preferences.
- **Sealos AI Dialog**: Describe environment or resource changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, MySQL, Ingress, or storage cards in Canvas to inspect and adjust settings.
- **PrestaShop Modules**: Install and configure payment, shipping, analytics, SEO, and storefront modules from the back office.

If you add a custom domain later, update the shop URL settings in PrestaShop and keep HTTPS enabled so storefront and admin links continue to use the correct host.

## Scaling

To scale PrestaShop on Sealos:

1. Open the Canvas for your PrestaShop deployment.
2. Click the PrestaShop StatefulSet resource card.
3. Increase CPU or memory when product catalogs, back-office operations, module workloads, or traffic require more capacity.
4. Apply the change and wait for the pod to become ready.

The template starts with the smallest resource profile that completed install and back-office smoke testing. For production stores, increase the application memory, tune MySQL resources, configure SMTP, and review backup and payment-provider requirements before launch.

## Troubleshooting

### The first startup takes several minutes

PrestaShop performs an automated install during the first container startup. Wait until the StatefulSet pod is ready, then open the storefront and `/admin-dev/` back office URL.

### The back office login page does not load

Use the `/admin-dev/` path on the generated HTTPS domain. If you changed the public domain after deployment, update PrestaShop shop URL settings or redeploy with the desired host.

### The container restarts during installation

Do not reduce the PrestaShop web container below `512Mi` memory. The initial installer needs more memory than a steady idle storefront.

### Customer registration or email notifications do not send mail

Configure SMTP settings in the PrestaShop back office before sending order, account, or password-reset emails. The template does not include an SMTP server.

### Getting Help

- [PrestaShop Documentation](https://docs.prestashop-project.org/)
- [PrestaShop Developer Documentation](https://devdocs.prestashop-project.org/)
- [PrestaShop GitHub Issues](https://github.com/PrestaShop/PrestaShop/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [PrestaShop Project](https://www.prestashop-project.org/)
- [PrestaShop Docker Image](https://hub.docker.com/r/prestashop/prestashop)
- [PrestaShop Releases](https://github.com/PrestaShop/PrestaShop/releases)
- [PrestaShop Modules Marketplace](https://addons.prestashop.com/)

## License

This Sealos template is provided under the repository's template license. PrestaShop itself is licensed under the Open Software License 3.0.
