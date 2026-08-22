# Deploy and Host Speedtest Tracker on Sealos

Speedtest Tracker is a self-hosted internet performance monitoring application. This template deploys Speedtest Tracker with PostgreSQL storage, persistent configuration, HTTPS ingress, and an initial administrator account on Sealos Cloud.

![Speedtest Tracker Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/speedtest-tracker/website-screenshot.webp)

## About Hosting Speedtest Tracker

Speedtest Tracker runs scheduled Ookla speed tests and stores latency, download, and upload history for long-term network visibility. The web UI provides charts, thresholds, and user management through the built-in Filament admin panel.

This Sealos template provisions Speedtest Tracker with a KubeBlocks PostgreSQL database and a persistent `/config` volume. Sealos manages the public HTTPS endpoint, storage, database lifecycle, and application resource controls from the Canvas.

## Common Use Cases

- **Home Network Monitoring**: Track ISP performance, outages, and latency trends over time.
- **Office Connectivity Checks**: Keep a lightweight dashboard for branch or workspace internet health.
- **SLA Evidence**: Preserve historical speed test data for provider discussions and incident reports.
- **Infrastructure Baselines**: Compare connection quality before and after network changes.

## Dependencies for Speedtest Tracker Hosting

The Sealos template includes Speedtest Tracker, PostgreSQL, persistent application storage, and HTTPS ingress.

### Deployment Dependencies

- [Official Documentation](https://docs.speedtest-tracker.dev/) - Installation, environment variables, and user guidance
- [GitHub Repository](https://github.com/alexjustesen/speedtest-tracker) - Source code and releases
- [LinuxServer Image](https://docs.linuxserver.io/images/docker-speedtest-tracker/) - Container image documentation

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Speedtest Tracker**: Laravel-based web application served by the LinuxServer container on port 80
- **PostgreSQL**: KubeBlocks-managed database for test results, users, and application state
- **Persistent Storage**: A 1 Gi volume mounted at `/config`
- **Ingress**: Sealos HTTPS endpoint for the browser UI

**Configuration:**

- `APP_URL` and `ASSET_URL` are set to the generated Sealos HTTPS domain.
- PostgreSQL credentials are injected from the KubeBlocks connection secret.
- The initial admin email and password are configured during deployment.
- The default login path is the root application URL, which redirects to the login screen when required.

**License Information:**

Speedtest Tracker is licensed under the MIT License. This Sealos template is provided under the repository license.

## Why Deploy Speedtest Tracker on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, database provisioning, storage, networking, and ongoing operations. By deploying Speedtest Tracker on Sealos, you get:

- **One-Click Deployment**: Open the template page, configure credentials, and deploy without writing Kubernetes YAML.
- **Managed PostgreSQL**: KubeBlocks provisions and operates the database for the application.
- **Persistent Storage Included**: The `/config` volume survives restarts and upgrades.
- **Instant Public Access**: Sealos creates an HTTPS URL automatically.
- **AI Ops and Canvas**: Adjust resources, environment variables, and storage from the Canvas or AI dialog.
- **Pay-as-You-Go Resources**: Start small and tune CPU, memory, and storage as monitoring needs grow.

## Deployment Guide

1. Open the [Speedtest Tracker template](https://sealos.io/products/app-store/speedtest-tracker) and click **Deploy Now**.
2. Configure the administrator email and password in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Speedtest Tracker through the provided URL and log in with the administrator email and password you configured.

## Configuration

After deployment, you can configure Speedtest Tracker through:

- **Web UI**: Change profile details, add users, configure thresholds, and review results.
- **AI Dialog**: Describe changes such as schedule updates or resource tuning.
- **Resource Cards**: Modify CPU, memory, storage, and environment variables from the Canvas.

## Scaling

Speedtest Tracker is intended to run as a single web instance backed by PostgreSQL. Increase CPU and memory from the Deployment or StatefulSet resource card when scheduled tests, dashboards, or user load grow.

## Troubleshooting

### Login Does Not Work

- Cause: The initial administrator values apply during the first application bootstrap.
- Solution: Use the email and password configured during first deployment. For later account changes, update the user profile or user management page inside Speedtest Tracker.

### Scheduled Tests Do Not Appear

- Cause: No speed test schedule has been configured, or the selected server cannot be reached.
- Solution: Configure `SPEEDTEST_SCHEDULE` and optional server settings from the Canvas environment variables.

## Additional Resources

- [Environment Variables](https://docs.speedtest-tracker.dev/getting-started/environment-variables)
- [Authentication Guide](https://docs.speedtest-tracker.dev/security/authentication)
- [Speedtest Tracker Releases](https://github.com/alexjustesen/speedtest-tracker/releases)

## License

This Sealos template is provided under the repository license. Speedtest Tracker is licensed under the MIT License.
