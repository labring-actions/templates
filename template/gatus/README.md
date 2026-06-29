# Deploy and Host Gatus on Sealos

Gatus is a developer-oriented uptime monitor with configurable checks, alerting, and status dashboards. This template deploys Gatus with KubeBlocks PostgreSQL storage on Sealos.

![Gatus Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gatus/website-screenshot.webp)

## About Hosting Gatus

Gatus runs as a single dashboard service on port `8080`. The template mounts a ConfigMap at `/config/config.yaml`, uses the official PostgreSQL storage mode, and stores monitoring state in a KubeBlocks PostgreSQL database.

The default configuration includes internal health checking for Gatus itself and an external Sealos availability check. You can edit the ConfigMap from the Sealos Canvas to add services, alert providers, endpoint groups, or security settings.

## Common Use Cases

- **Service Uptime Monitoring**: Check HTTP, TCP, ICMP, DNS, and other endpoint types.
- **Status Dashboard**: Publish current availability and incident visibility for services.
- **Pre-User Impact Alerts**: Detect failures before customers report them.
- **Synthetic Checks**: Run lightweight acceptance checks against APIs and web services.

## Dependencies for Gatus Hosting

The Sealos template includes all required dependencies: Gatus, KubeBlocks PostgreSQL `postgresql-16.4.0`, an initialization Job for the `gatus` database, a ConfigMap, Service, Ingress, and App entry.

### Deployment Dependencies

- [Official Documentation](https://github.com/TwiN/gatus#configuration) - Configuration reference
- [PostgreSQL Storage Example](https://github.com/TwiN/gatus/tree/master/.examples/docker-compose-postgres-storage) - Official compose example
- [Sealos](https://sealos.io) - Kubernetes-based application hosting

### Implementation Details

**Architecture Components:**

- **Gatus Web Service**: Runs `twinproduction/gatus:v5.36.0` on port `8080`.
- **PostgreSQL**: KubeBlocks-managed `postgresql-16.4.0` stores endpoint results.
- **ConfigMap**: Provides `/config/config.yaml` with PostgreSQL storage and starter checks.
- **Service and Ingress**: Expose the dashboard through HTTPS.

**Configuration:**

The ConfigMap uses environment variables in the official Gatus configuration format to connect to PostgreSQL. Database credentials are injected from the KubeBlocks connection secret.

**License Information:**

This Sealos template is provided under the repository license. Gatus is licensed under the Apache License 2.0.

## Why Deploy Gatus on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, public access, and operations. By deploying Gatus on Sealos, you get:

- **One-Click Deployment**: Launch a PostgreSQL-backed monitoring dashboard from the App Store.
- **Persistent Monitoring State**: KubeBlocks PostgreSQL stores check history.
- **Instant Public Access**: Sealos creates an HTTPS dashboard URL automatically.
- **Easy Customization**: Update the ConfigMap and resource settings from the Canvas.

## Deployment Guide

1. Open the [Gatus template](https://sealos.io/products/app-store/gatus) and click **Deploy Now**.
2. Review the generated app name and host, then start deployment.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access the Gatus dashboard through the provided App URL. The default template opens the dashboard directly.

## Configuration

Edit `/config/config.yaml` through the ConfigMap resource card to add endpoints, alerting providers, dashboard settings, or Basic Auth. Gatus automatically reloads valid configuration updates.

## Additional Resources

- [Gatus README](https://github.com/TwiN/gatus)
- [Configuration Reference](https://github.com/TwiN/gatus#configuration)
- [Security Configuration](https://github.com/TwiN/gatus#security)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the repository license. Gatus is licensed under the Apache License 2.0.
