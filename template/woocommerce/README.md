# Deploy and Host WooCommerce on Sealos

WooCommerce is an open-source ecommerce platform built on WordPress for creating and managing online stores. This template deploys WooCommerce with WordPress, managed MySQL, persistent storage, and HTTPS ingress on Sealos Cloud.

![WooCommerce Logo](./logo.png)

## About Hosting WooCommerce

WooCommerce in this template runs on top of a WordPress StatefulSet. During startup, an init container uses WP-CLI to bootstrap WordPress, generate `wp-config.php`, install the WooCommerce plugin, and activate it automatically so the store stack is ready on first login.

The deployment includes a managed MySQL cluster provisioned by KubeBlocks, plus a bootstrap job that creates the application database (`mydb`) before WordPress initialization. Sealos also provisions public HTTPS access, domain routing, and persistent storage for site content under `/var/www/html`.

Post-deployment operations are managed in Canvas: you can use the AI dialog for guided changes or edit resource cards directly for replica and resource tuning.

## Common Use Cases

- **Direct-to-Consumer Storefronts**: Launch a branded online store with catalog, cart, and checkout workflows.
- **Digital Product Sales**: Sell downloadable assets such as software, design files, or course materials.
- **Regional Retail Sites**: Run localized ecommerce deployments with custom themes and payment plugins.
- **Content + Commerce Sites**: Combine WordPress publishing with WooCommerce product sales in one stack.
- **Small Team Operations**: Start with a single-node setup and scale resources as order volume grows.

## Dependencies for WooCommerce Hosting

This Sealos template includes all required dependencies: WordPress runtime, WooCommerce plugin activation, managed MySQL database, persistent volume, service exposure, and HTTPS ingress.

### Deployment Dependencies

- [WooCommerce Documentation](https://woocommerce.com/documentation/) - Official setup and store management docs
- [WooCommerce GitHub Repository](https://github.com/woocommerce/woocommerce) - Source code and release history
- [WordPress Documentation](https://wordpress.org/documentation/) - Core CMS documentation
- [WP-CLI Documentation](https://developer.wordpress.org/cli/commands/) - Command reference used during initialization
- [MySQL Documentation](https://dev.mysql.com/doc/) - Database reference

## Implementation Details

### Architecture Components

This template deploys the following resources:

- **WordPress StatefulSet (`wordpress:6.9.1-php8.3-apache`)**: Serves the web UI and WooCommerce storefront.
- **WP-CLI Init Container (`wordpress:cli-2.9.0-php8.3`)**: Automates first-time install, admin bootstrap, HTTPS handling, and WooCommerce activation.
- **MySQL Cluster (`ac-mysql-8.0.30-1`)**: Managed by KubeBlocks for persistent relational storage.
- **MySQL Init Job (`mysql:8.0.30`)**: Waits for database readiness and creates the `mydb` schema.
- **Persistent Volume (`1Gi`)**: Mounted at `/var/www/html` for WordPress content and plugins.
- **Service + Ingress**: Exposes HTTP internally and HTTPS publicly on your generated domain.

### Configuration

The template exposes these deployment inputs:

- `WP_ADMIN_USER`: WordPress admin username (default: `admin`)
- `WP_ADMIN_PASSWORD`: WordPress admin password (required)
- `WP_ADMIN_EMAIL`: WordPress admin email (default: `admin@example.com`)
- `WP_SITE_TITLE`: Site title (default: `WooCommerce Store`)

Runtime behaviors:

- Site URL is set to `https://<app-host>.<sealos-domain>`.
- `home` and `siteurl` options are updated automatically at startup.
- WooCommerce plugin is installed and activated idempotently.
- Default table prefix is `wp_`.

### License Information

WooCommerce is licensed under the [GNU General Public License v3.0](https://github.com/woocommerce/woocommerce/blob/trunk/LICENSE.md). WordPress is licensed under GPLv2 or later.

## Why Deploy WooCommerce on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies application deployment and operations. By deploying WooCommerce on Sealos, you get:

- **One-Click Deployment**: Launch WordPress + WooCommerce + MySQL without manually writing Kubernetes manifests.
- **Managed Database Provisioning**: MySQL is provisioned and wired through cluster-managed credentials.
- **Persistent Storage Included**: Store uploads, themes, and plugin assets on durable volumes.
- **Secure Public Access**: Get a public HTTPS endpoint with automatic domain and certificate handling.
- **Easy Customization**: Update inputs and runtime resources through Canvas dialogs and resource cards.
- **Pay-as-You-Go Efficiency**: Scale compute and storage with actual storefront traffic and order load.
- **Kubernetes Reliability**: Run on a Kubernetes-native platform without needing deep cluster expertise.

Deploy WooCommerce on Sealos and focus on your store operations instead of infrastructure setup.

## Deployment Guide

1. Open the [WooCommerce template](https://sealos.io/products/app-store/woocommerce) and click **Deploy Now**.
2. Configure deployment parameters in the popup dialog:
   - `WP_ADMIN_USER`
   - `WP_ADMIN_PASSWORD`
   - `WP_ADMIN_EMAIL`
   - `WP_SITE_TITLE` (optional)
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click resource cards to modify settings.
4. Open the generated application URL:
   - **Storefront**: `https://<app-host>.<domain>/`
   - **WordPress Admin**: `https://<app-host>.<domain>/wp-admin`

## Configuration

After deployment, you can manage WooCommerce through:

- **AI Dialog**: Request changes such as resource adjustments, env updates, or component restarts.
- **Resource Cards**: Edit StatefulSet/Service/Ingress parameters from Canvas.
- **WordPress Admin**: Configure products, themes, payment gateways, tax rules, and shipping methods.

Recommended post-deployment actions:

1. Change admin credentials and enforce a strong password policy.
2. Set store currency, tax, and shipping zones in WooCommerce settings.
3. Install only required plugins to reduce operational and security risk.
4. Configure regular backup/export routines for store data.

## Scaling

To scale your deployment:

1. Open your app in Canvas.
2. Increase CPU/Memory for the WordPress StatefulSet when traffic grows.
3. Review MySQL component resources if checkout or admin operations slow down.
4. Expand persistent storage if media uploads and product data exceed baseline capacity.

## Troubleshooting

### Common Issues

**Issue: WordPress or WooCommerce setup page appears unexpectedly**
- Cause: Initialization may not have finished, or init container failed.
- Solution: Check init container logs for WP-CLI errors and confirm database job completed successfully.

**Issue: Cannot log in to `/wp-admin`**
- Cause: Provided admin credentials do not match deployment inputs.
- Solution: Verify `WP_ADMIN_USER` and `WP_ADMIN_PASSWORD` values used during deployment.

**Issue: Database connection errors on startup**
- Cause: MySQL cluster is still provisioning or connection secret is not ready.
- Solution: Wait for MySQL cluster readiness and confirm the MySQL init job succeeded.

**Issue: Mixed-content or redirect problems behind HTTPS**
- Cause: Site URL may not match ingress host or forwarded protocol handling was interrupted.
- Solution: Verify ingress host and ensure site URL points to the generated HTTPS domain.

### Getting Help

- [WooCommerce Documentation](https://woocommerce.com/documentation/)
- [WooCommerce GitHub Issues](https://github.com/woocommerce/woocommerce/issues)
- [WordPress Support](https://wordpress.org/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [WooCommerce Extensions Marketplace](https://woocommerce.com/products/)
- [WooCommerce Developer Docs](https://developer.woocommerce.com/docs/)
- [WordPress Plugin Handbook](https://developer.wordpress.org/plugins/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template follows repository licensing terms. WooCommerce itself is licensed under GPLv3, and WordPress is licensed under GPLv2 or later.
