# Deploy and Host WAHA on Sealos

WAHA is a WhatsApp HTTP API with a dashboard, Swagger UI, persistent sessions, and webhook support. This template deploys WAHA with KubeBlocks PostgreSQL for session storage and optional Sealos Object Storage for WhatsApp media files on Sealos Cloud.

![WAHA Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/waha/website-screenshot.webp)

## About Hosting WAHA

WAHA exposes WhatsApp automation through HTTP APIs and a browser-based dashboard. You can create sessions, scan WhatsApp QR codes, send messages, receive webhooks, and inspect the API through Swagger UI.

This template uses the pinned `devlikeapro/waha:chrome-2026.5.1` image because the default WEBJS engine depends on a bundled browser runtime. PostgreSQL stores WhatsApp session data so sessions survive restarts. Media files are stored on a local persistent volume by default, and Sealos S3-compatible Object Storage can be enabled during deployment.

## Common Use Cases

- **WhatsApp API gateway**: Provide HTTP endpoints for sending and receiving WhatsApp messages.
- **Webhook automation**: Connect WhatsApp events to CRM, helpdesk, and workflow systems.
- **Session management**: Manage multiple WhatsApp sessions from the dashboard.
- **API testing**: Use Swagger UI to inspect and test WAHA endpoints.

## Dependencies for WAHA Hosting

The Sealos template includes WAHA, KubeBlocks PostgreSQL 16.4.0, persistent volumes for local runtime files and media, optional Sealos Object Storage, public HTTPS ingress, and an App launcher entry.

### Deployment Dependencies

- [WAHA Documentation](https://waha.devlike.pro/docs/overview/introduction/) - Official documentation
- [Install Guide](https://waha.devlike.pro/docs/how-to/install/) - Docker deployment reference
- [Storage Guide](https://waha.devlike.pro/docs/how-to/storages/) - Session and media storage options
- [GitHub Repository](https://github.com/devlikeapro/waha) - Source code and releases

### Implementation Details

**Architecture Components:**

- **WAHA**: Main API, dashboard, and Swagger UI service.
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4.0 for WhatsApp session storage.
- **Persistent Volumes**: Local runtime and media directories.
- **Object Storage**: Optional Sealos S3-compatible storage for media files.

**Configuration:**

- Dashboard login uses the configured username and generated password.
- Swagger login uses the configured username and generated password.
- API authentication uses a generated `WAHA_API_KEY`.
- Session storage uses `WHATSAPP_SESSIONS_POSTGRESQL_URL` and the KubeBlocks PostgreSQL connection secret.
- The template sets `WAHA_BASE_URL` and `WAHA_PUBLIC_URL` to the Sealos HTTPS URL.

**License Information:**

WAHA is distributed from the upstream project. Review the upstream repository and documentation for edition-specific licensing and feature availability.

## Why Deploy WAHA on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying WAHA on Sealos, you get:

- **One-Click Deployment**: Deploy WAHA, PostgreSQL, storage, HTTPS ingress, and the App launcher together.
- **Persistent Storage Included**: Keep WhatsApp sessions and media across restarts.
- **Easy Customization**: Change resource limits, environment variables, and storage settings from Canvas.
- **Zero Kubernetes Expertise Required**: Operate a Kubernetes-backed deployment through a simple UI.
- **Instant Public Access**: Access WAHA through an HTTPS URL after deployment.

Deploy WAHA on Sealos and focus on WhatsApp workflows instead of infrastructure.

## Deployment Guide

1. Open the [WAHA template](https://sealos.io/products/app-store/waha) and click **Deploy Now**.
2. Configure the dashboard username, Swagger username, and optional object storage setting.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Open the WAHA App URL from Canvas. The App launcher opens the dashboard at `/dashboard/`.
5. Log in to the dashboard with the configured dashboard username and the generated `dashboard_password` value from the template defaults.
6. Open the root WAHA URL `/` to use Swagger UI, or open `/-json` for the OpenAPI document. Use the configured Swagger username and generated `swagger_password` value when prompted.
7. Use the generated `api_key` value as the `WAHA_API_KEY` for API requests that require authentication, for example the `X-Api-Key` header.

## Configuration

After deployment, you can configure WAHA through:

- **AI Dialog**: Describe environment variable, resource, or storage changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, PostgreSQL, Object Storage, Service, or Ingress cards to modify settings.
- **Dashboard**: Create and manage WhatsApp sessions from the web UI.
- **Swagger UI**: Test API endpoints from the root WAHA URL `/`.
- **OpenAPI JSON**: Fetch `/-json` from the same host for the OpenAPI schema.

## Scaling

The template runs one WAHA replica because browser-backed WhatsApp sessions are stateful. For multiple workers sharing the same database, configure unique `WAHA_WORKER_ID` values and review WAHA's storage namespace guidance before scaling.

## Troubleshooting

### Dashboard Login Fails

- Cause: Username or generated password mismatch.
- Solution: Check the deployed environment variables for `WAHA_DASHBOARD_USERNAME` and `WAHA_DASHBOARD_PASSWORD`.

### QR Code or Session State Disappears

- Cause: Session storage is unavailable or the PostgreSQL connection is failing.
- Solution: Inspect the WAHA logs and the PostgreSQL resource status in Canvas.

### Media Uploads Need Durable External URLs

- Cause: Local media storage keeps files in the app volume.
- Solution: Enable object storage during deployment or update `WAHA_MEDIA_STORAGE=S3` with the Sealos S3 variables.

## Additional Resources

- [WAHA Configuration](https://waha.devlike.pro/docs/how-to/config/)
- [WAHA Dashboard](https://waha.devlike.pro/docs/how-to/dashboard/)
- [WAHA Swagger](https://waha.devlike.pro/docs/how-to/swagger/)
- [Sealos Documentation](https://sealos.io/docs)

## License

WAHA licensing depends on the upstream edition and image you use. Review the [upstream repository](https://github.com/devlikeapro/waha) and [WAHA documentation](https://waha.devlike.pro/) before production use.
