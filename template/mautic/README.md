# Deploy and Host Mautic on Sealos

[Mautic](https://www.mautic.org/) is an open source marketing automation platform for email campaigns, landing pages, lead scoring, segmentation, and customer journeys.

This Sealos template deploys Mautic 7 with the official Apache image, a managed MySQL 8.4.2 database, persistent application storage, cron jobs, and queue workers.

## Features

- Mautic 7.1.2 using `mautic/mautic:7.1.2-apache`
- Managed MySQL 8.4.2 database provisioned through KubeBlocks
- Dedicated web, cron, and worker workloads
- Persistent volumes for configuration, logs, uploaded files, and images
- Public HTTPS ingress managed by Sealos

## Deploy on Sealos

1. Open the [Mautic template on Sealos](https://sealos.io/products/app-store/mautic).
2. Click **Deploy Now**.
3. Keep the default generated app name and domain, or customize them if needed.
4. Choose the `TIMEZONE` value for PHP and scheduled tasks.
5. Click **Deploy** and wait until the application status is running.

## First-run setup and login

Mautic does not ship with a default administrator account. On the first visit, open the generated public URL and complete the installer:

1. On **Environment Check**, click **Next Step**.
2. On **Database Setup**, keep the prefilled MySQL values from the template and click **Next Step**.
3. On **Administrative User**, create your administrator username, password, and email address.
4. After the installer finishes, sign in at `/s/login` with the administrator account you created.

If the installer or later settings page asks for a site URL, use the public Sealos HTTPS URL shown for your app.

## Resource profile

The template was tuned with live Sealos deployment tests:

| Component | CPU limit | Memory limit | Notes |
| --- | ---: | ---: | --- |
| Mautic web | `200m` | `256Mi` | Serves the UI and installer |
| Mautic cron | `100m` | `256Mi` | Runs scheduled Mautic jobs |
| Mautic worker | `100m` | `512Mi` | Runs Messenger queue consumers |
| MySQL | `1000m` | `1024Mi` | Minimum stable KubeBlocks MySQL 8.4.2 profile |

The worker needs more memory than the web container after installation because Messenger consumers are started in parallel.

## Configuration

| Name | Description | Required | Default |
| --- | --- | --- | --- |
| `TIMEZONE` | PHP timezone used by Mautic and scheduled tasks. | No | `UTC` |

Email sending is configured inside Mautic after installation. Add your SMTP provider in **Settings → Configuration → Email** before running production campaigns.

## Data persistence

The template persists:

- `/var/www/html/config`
- `/var/www/html/var/logs`
- `/var/www/html/docroot/media/files`
- `/var/www/html/docroot/media/images`
- MySQL data volume

Deleting the Sealos app removes the application and database resources according to the template termination policy.

## Official links

- Website: https://www.mautic.org/
- Documentation: https://docs.mautic.org/
- Source code: https://github.com/mautic/mautic
- Docker image: https://hub.docker.com/r/mautic/mautic
