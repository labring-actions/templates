# Deploy and Host WordPress on Sealos

WordPress is an open-source content management system for publishing websites, blogs, news, and other web content. This template deploys WordPress `7.0.0` with KubeBlocks MySQL, persistent site storage, an HTTPS Ingress, and a Sealos App entry.

![WordPress Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/wordpress/website-screenshot.webp)

## About Hosting WordPress

The template runs the official WordPress image behind a managed Kubernetes Service. WordPress files, themes, plugins, and uploads are stored on a 1 GiB persistent volume mounted at `/var/www/html`, so application content survives pod restarts.

KubeBlocks MySQL `ac-mysql-8.0.30-1` stores the WordPress database. An idempotent initialization Job creates the `mydb` database after MySQL becomes reachable. Sealos configures the generated HTTPS hostname and exposes it through the Sealos App entry.

## Common Use Cases

- **Content sites**: Publish blogs, news, documentation, and company websites.
- **Marketing pages**: Combine themes and plugins for campaign pages and lead capture.
- **Editorial teams**: Give writers and editors a shared publishing workflow.
- **Small communities**: Run a self-hosted site with persistent media and user data.

## Architecture and Dependencies

- **WordPress web service**: WordPress `7.0.0` listens on port `80`.
- **MySQL**: A single KubeBlocks MySQL component provides the `mydb` database and a 1 GiB data volume.
- **Database initialization Job**: Creates `mydb` with the managed MySQL connection Secret and exits after successful initialization.
- **Persistent site storage**: The `/var/www/html` volume stores core files, themes, plugins, and media uploads.
- **Service, Ingress, and App entry**: Sealos publishes the HTTPS URL and adds a direct launch entry.

## Why Deploy WordPress on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes. The template packages WordPress, MySQL, storage, HTTPS routing, and an App entry so a content site can start with one deployment.

- **One-click setup**: Provision the application and database together.
- **Persistent content**: Keep themes, plugins, and uploads on managed storage.
- **Simple operations**: Use Canvas resource cards and the AI dialog for updates.
- **Pay-as-you-go resources**: Scale the site as traffic and media storage grow.

## Configuration

This template has no additional deployment inputs. Sealos generates the application name and host, and KubeBlocks generates the database connection credentials.

## Deployment Guide

1. Open the [WordPress template](https://sealos.io/products/app-store/wordpress) and click **Deploy Now**.
2. Keep the default parameters unless you need a custom application name or host.
3. Wait for MySQL, the initialization Job, and WordPress to become Ready. Typical Sealos deployments take 2-3 minutes; database provisioning can extend a first cold start. After deployment, Canvas provides the AI dialog and resource cards for further changes.
4. Open the generated URL from the Sealos App entry.
5. Complete the WordPress first-run form, choose the site language, create the administrator account, and sign in.

### First-time setup, login, and user registration

- A new deployment opens `/wp-admin/install.php`. Choose the site language, enter a site title, create the first administrator username and password, then submit the form.
- Sign in later at `/wp-login.php` with that administrator account. The dashboard is available at `/wp-admin/`.
- WordPress creates the first administrator during installation. Public account registration is controlled by **Settings > General > Membership** after login; enable **Anyone can register** only when the site should accept self-service accounts, then choose the default role.
- Test the flow with a private browser window after enabling registration. Keep the administrator password in a password manager.

## Storage and Operations

Use the Canvas resource cards to increase WordPress CPU or memory and to expand the `/var/www/html` volume as media and plugins grow. Sealos is built on Kubernetes and follows a pay-as-you-go resource model. Back up both the WordPress volume and the MySQL data before a migration or major plugin upgrade; use the Canvas AI dialog for configuration requests.

WordPress receives the MySQL host, port, username, password, and database name from the managed connection Secret. The Ingress allows 32 MiB request bodies and keeps long uploads within a 300-second proxy timeout.

## Troubleshooting

### The setup page reports a database error

Check that the MySQL Cluster is Ready and that the `wordpress-mysql-init` Job completed. Re-run the Job only after confirming the connection Secret points to the current MySQL Service.

### Media uploads fail

Inspect the `/var/www/html` volume capacity and the Ingress request limit. Increase storage for large media libraries and keep individual uploads below the configured 32 MiB request limit.

### The site uses an old host name

Open the Ingress and App resources in Canvas and confirm the generated `app_host` value. Update WordPress Address and Site Address from the WordPress settings after changing a custom domain.

### Getting Help

- [WordPress Documentation](https://wordpress.org/documentation/)
- [WordPress Support Forums](https://wordpress.org/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Official Links

- [WordPress website](https://wordpress.org/)
- [WordPress source repository](https://github.com/WordPress/WordPress)

## Additional Resources

- [WordPress Developer Resources](https://developer.wordpress.org/)
- [WordPress Plugin Directory](https://wordpress.org/plugins/)

## License

This Sealos template is provided under the templates repository license. WordPress is distributed under the GNU General Public License version 2 or later.
