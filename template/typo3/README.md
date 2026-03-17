# Deploy and Host TYPO3 on Sealos

TYPO3 is an open-source enterprise content management system for building editorial websites, portals, and multi-site platforms. This template deploys TYPO3 with managed MySQL, persistent writable storage, automated CLI bootstrap, and HTTPS ingress on Sealos.

![TYPO3 Logo](./logo.png)

## About Hosting TYPO3

This template runs TYPO3 in classic mode with the upstream `martinhelmich/typo3` Apache image. Sealos provisions a managed MySQL cluster, creates the `typo3` database, mounts persistent volumes for `fileadmin`, `typo3conf`, and `typo3temp`, and publishes the application with a generated HTTPS domain.

Bootstrap is handled by an init container instead of the browser install wizard. On the first successful start, TYPO3 writes `settings.php`, applies the administrator credentials you provide, creates the initial site configuration, and injects `additional.php` so TYPO3 trusts Sealos ingress headers for HTTPS and host detection. The template also validates the administrator password against TYPO3 default password policy before setup begins, and it explicitly recreates the backend administrator if a partial initialization leaves `settings.php` in place without any backend users.

TYPO3 backend access uses the standard `/typo3/` path. The public root path `/` is the frontend site entry and depends on TYPO3 site and page configuration. If the backend is healthy but `/` returns `404`, sign in to TYPO3 and finish the frontend site setup or publish the homepage content.

Day-2 operations happen in Canvas. After deployment, you can resize resources, review logs, restart the workload, or ask the AI dialog to adjust storage, networking, or runtime settings.

## Common Use Cases

- **Corporate Websites**: Run brand, marketing, and editorial sites with structured publishing workflows.
- **Content Portals**: Build documentation hubs, magazines, and knowledge bases with TYPO3 content modeling.
- **Multi-Site Operations**: Manage multiple sites from one TYPO3 installation with shared governance.
- **Agency Delivery**: Hand over a maintainable CMS stack backed by Kubernetes storage and managed database services.
- **Migration from Traditional Hosting**: Move TYPO3 from VMs or shared hosting to a managed Kubernetes platform.

## Dependencies for TYPO3 Hosting

This Sealos template includes the full TYPO3 runtime stack: Apache/PHP, managed MySQL, persistent storage, internal service discovery, and HTTPS ingress.

### Deployment Dependencies

- [TYPO3 Official Website](https://typo3.org) - Product overview and ecosystem
- [TYPO3 Installation Guide](https://docs.typo3.org/installation) - Official installation and operations guidance
- [TYPO3 Docker Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/Docker/Index.html) - Official Docker deployment references
- [TYPO3 Reverse Proxy Guide](https://docs.typo3.org/permalink/t3coreapi:reverse-proxy-setup) - Reverse proxy and HTTPS detection settings
- [TYPO3 GitHub Repository](https://github.com/TYPO3/typo3) - Upstream source code
- [Sealos Documentation](https://sealos.io/docs) - Platform usage and operations

## Implementation Details

### Architecture Components

This template deploys the following resources:

- **TYPO3 StatefulSet**: Runs the main TYPO3 application on Apache with persistent writable directories.
- **Managed MySQL Cluster (`ac-mysql-8.0.30-1`)**: Provisioned by KubeBlocks for TYPO3 relational data.
- **MySQL Init Job**: Creates the `typo3` database before TYPO3 setup starts.
- **TYPO3 Setup Init Container**: Validates the admin password, waits for MySQL readiness, runs `typo3 setup`, and ensures a backend administrator exists.
- **ConfigMap (`additional.php`)**: Applies trusted host and reverse-proxy settings for Sealos ingress.
- **Persistent Volumes**:
  - `/var/www/html/fileadmin` (1Gi) for uploads and user-managed assets
  - `/var/www/html/typo3conf` (0.1Gi) for generated configuration and site settings
  - `/var/www/html/typo3temp` (0.1Gi) for cache and runtime temporary files
- **Service + Ingress**: Exposes TYPO3 internally and publishes a public HTTPS endpoint.

### Configuration

The template exposes these deployment inputs:

- `TYPO3_SETUP_ADMIN_EMAIL`: Initial TYPO3 administrator email
- `TYPO3_SETUP_ADMIN_USERNAME`: Initial TYPO3 administrator username
- `TYPO3_SETUP_ADMIN_PASSWORD`: Initial TYPO3 administrator password. It must be at least 8 characters and include upper case, lower case, digit, and special character.
- `TYPO3_PROJECT_NAME`: Initial TYPO3 site name

Runtime behaviors:

- The template generates `TYPO3_SETUP_CREATE_SITE=https://<app-host>.<domain>/` automatically for the initial site setup.
- TYPO3 runs with `TYPO3_CONTEXT=Production`.
- Reverse-proxy and trusted-host handling are injected through `typo3conf/system/additional.php`.
- MySQL connection host, port, username, and password are injected from `${app_name}-mysql-conn-credential`.
- Health probes use `/typo3/` with the public host header so trusted host validation stays compatible with Kubernetes probes.
- Administrator inputs are bootstrap-only. After the first successful initialization, change user credentials inside TYPO3 rather than by editing template inputs.
- If `settings.php` exists but no backend user exists, the init flow repairs the installation by creating the administrator explicitly.
- Frontend availability on `/` depends on TYPO3 site and page configuration; backend access remains `https://<app-host>.<domain>/typo3/`.

### License Information

TYPO3 is licensed under GPL-2.0. Review the upstream repository and TYPO3 project documentation for complete licensing terms.

## Why Deploy TYPO3 on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that simplifies production deployment and day-2 operations. By deploying TYPO3 on Sealos, you get:

- **One-Click Deployment**: Launch TYPO3, MySQL, ingress, and storage without hand-writing Kubernetes manifests.
- **Managed Database Integration**: Run TYPO3 on a KubeBlocks-managed MySQL cluster with secret-based credential injection.
- **Persistent Storage Included**: Keep uploads, configuration, and runtime data across restarts and upgrades.
- **Public HTTPS Access by Default**: Get an external domain and TLS termination without manual networking setup.
- **AI + Canvas Operations**: Use the AI dialog or resource cards to restart, resize, or adjust the deployment after launch.
- **Pay-as-You-Go Efficiency**: Scale compute and storage with the resources you actually use.
- **Kubernetes Reliability Without Platform Overhead**: Keep the benefits of Kubernetes while avoiding manual cluster plumbing.

Deploy TYPO3 on Sealos and focus on content delivery instead of infrastructure assembly.

## Deployment Guide

1. Open the [TYPO3 template](https://sealos.io/products/app-store/typo3) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - `TYPO3_SETUP_ADMIN_EMAIL`
   - `TYPO3_SETUP_ADMIN_USERNAME`
   - `TYPO3_SETUP_ADMIN_PASSWORD`
   - `TYPO3_PROJECT_NAME`
   Use an administrator password with at least 8 characters and at least one upper case letter, lower case letter, digit, and special character.
3. Wait 2-3 minutes for deployment to complete. Sealos provisions MySQL, creates the `typo3` database, runs the TYPO3 CLI bootstrap, and then redirects you to Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards.
4. Access your application with the generated domain:
   - **TYPO3 Backend**: `https://<app-host>.<domain>/typo3/`
   - **TYPO3 Frontend**: `https://<app-host>.<domain>/` after you complete TYPO3 site and homepage configuration

## Configuration

After deployment, you can manage TYPO3 through:

- **AI Dialog**: Ask Sealos AI to restart the workload, resize storage, or adjust resources.
- **Resource Cards**: Modify StatefulSet, Service, Ingress, ConfigMap, or MySQL settings directly in Canvas.
- **TYPO3 Backend**: Install extensions, configure sites, manage users, and publish content from `https://<app-host>.<domain>/typo3/`.

Recommended post-deployment actions:

1. Sign in to the TYPO3 backend using the administrator credentials from deployment.
2. Verify site configuration and publish or import the frontend homepage if the root path is not ready yet.
3. Rotate the initial administrator password if needed.
4. Review locales, mail settings, and extension requirements.
5. Configure backups for MySQL and media stored in `fileadmin`.

## Scaling

To scale your TYPO3 deployment:

1. Open the deployment in Canvas.
2. Increase CPU and memory for the TYPO3 StatefulSet when backend traffic, extensions, or cache generation need more headroom.
3. Tune MySQL component resources when editorial activity or frontend queries become slower.
4. Expand persistent volumes for `fileadmin`, `typo3conf`, or `typo3temp` as storage needs grow.

This template is optimized for a single TYPO3 application instance by default. Production scaling usually starts with vertical scaling and database tuning.

## Troubleshooting

### Common Issues

**Issue: The setup init container keeps restarting**
- Cause: MySQL is still initializing, or the TYPO3 bootstrap step failed.
- Solution: Check MySQL pod health first, then inspect the init-container logs on the TYPO3 StatefulSet pod.

**Issue: Deployment fails because of the administrator password**
- Cause: `TYPO3_SETUP_ADMIN_PASSWORD` does not satisfy TYPO3 default password policy.
- Solution: Redeploy with a password that is at least 8 characters long and includes upper case, lower case, digit, and special character.

**Issue: The backend cannot be accessed with credentials entered during deployment**
- Cause: Administrator inputs are applied only during the first successful bootstrap. Updating template variables later does not rotate existing TYPO3 users.
- Solution: Use the original bootstrap credentials, rotate the password inside TYPO3, or redeploy with fresh storage if you need a clean installation.

**Issue: The backend works, but the root path `/` returns `404`**
- Cause: TYPO3 backend bootstrap completed, but the frontend site or homepage is not configured yet.
- Solution: Sign in at `/typo3/`, review site management and root page configuration, and publish frontend content.

**Issue: TYPO3 redirects to HTTP or shows backend login issues**
- Cause: Reverse-proxy headers are not trusted, or the generated host does not match the trusted host pattern.
- Solution: Confirm the pod is using the mounted `additional.php` and that the ingress host matches the generated Sealos hostname.

**Issue: Uploads fail or storage fills quickly**
- Cause: The default volume size is too small for the current media workload.
- Solution: Expand the relevant volume in Canvas, especially `fileadmin`.

### Getting Help

- [TYPO3 Documentation](https://docs.typo3.org/)
- [TYPO3 Docker Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/Docker/Index.html)
- [TYPO3 GitHub Issues](https://github.com/TYPO3/typo3/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [TYPO3 Getting Started](https://docs.typo3.org/m/typo3/tutorial-getting-started/main/en-us/)
- [TYPO3 Extension Repository](https://extensions.typo3.org/)
- [TYPO3 Security Guidelines](https://docs.typo3.org/permalink/t3coreapi:security-administrators)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template follows repository licensing terms. TYPO3 itself is licensed under GPL-2.0 by the upstream project.
