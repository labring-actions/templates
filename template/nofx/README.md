# Deploy and Host NOFX on Sealos

NOFX is an open-source AI trading terminal for market research, strategy generation, execution, and monitoring. This template deploys the NOFX backend, frontend, and KubeBlocks PostgreSQL on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/nofx/website-screenshot.webp)

## About Hosting NOFX

NOFX provides a browser workspace for AI-assisted trading workflows across crypto, US stocks, forex, and commodities. The Sealos template deploys separate frontend and backend workloads, routes `/api` traffic to the backend, and stores application state in an external PostgreSQL database.

The upstream Docker Compose file uses local storage by default, while the application also documents PostgreSQL support. This template selects KubeBlocks PostgreSQL for a production-oriented deployment.

## Common Use Cases

- **AI trading workspace**: Research markets, build strategies, and monitor traders.
- **Exchange configuration**: Store exchange accounts and trading settings.
- **Strategy testing**: Manage AI models, market symbols, and strategy logic.
- **Competition dashboards**: View trader performance and public competition data.

## Dependencies for NOFX Hosting

The Sealos template includes the NOFX frontend, NOFX backend, KubeBlocks PostgreSQL, HTTPS ingress, generated JWT/encryption values, and health probes.

### Deployment Dependencies

- [VergeX Official Website](https://vergex.trade) - Product homepage
- [NOFX GitHub Repository](https://github.com/NoFxAiOS/nofx) - Source code and deployment docs
- [NOFX API Docs](https://github.com/NoFxAiOS/nofx/tree/main/docs/api) - API documentation
- [NOFX Docker Compose](https://github.com/NoFxAiOS/nofx/blob/main/docker-compose.prod.yml) - Upstream container topology

### Implementation Details

**Architecture Components:**

- **Frontend**: Static web interface served by `ghcr.io/nofxaios/nofx/nofx-frontend`
- **Backend**: Go API server served by `ghcr.io/nofxaios/nofx/nofx-backend`
- **PostgreSQL**: KubeBlocks PostgreSQL `postgresql-16.4.0`
- **Ingress**: Root path routes to the frontend, `/api` routes to the backend

**Configuration:**

The template sets `DB_TYPE=postgres`, injects KubeBlocks database credentials, generates a JWT secret, configures data encryption, and disables anonymous telemetry by default. The backend health check uses `/api/health`; the frontend health check uses `/health`.

**License Information:**

NOFX is licensed under the GNU Affero General Public License v3.0.

## Why Deploy NOFX on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying NOFX on Sealos, you get:

- **One-Click Deployment**: Deploy frontend, backend, database, ingress, and SSL in one flow.
- **Managed PostgreSQL**: Use KubeBlocks PostgreSQL instead of local SQLite files.
- **Instant Public Access**: Open the generated HTTPS URL after deployment.
- **Secure Defaults**: Use generated secrets for JWT and data encryption.
- **Easy Operations**: Adjust resources and environment variables from the Sealos Canvas.

Deploy NOFX on Sealos and run the trading terminal with managed infrastructure.

## Deployment Guide

1. Open the [NOFX template](https://sealos.io/products/app-store/nofx) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete. This typically takes 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access NOFX via the provided URL.
5. Register the first user from the web interface. NOFX will show a Google Authenticator QR code and OTP secret during first-time registration.
6. Scan the QR code with an authenticator app, enter the current 6-digit OTP, and complete registration.
7. For later logins, enter the email and password first, then enter the current Google Authenticator code.

## Configuration

NOFX exposes first-time registration through the web interface and the backend authentication API. After the first user is initialized, the system closes additional public registration for the single-user deployment model. Registration and later logins require Google Authenticator/TOTP verification.

This template keeps application file handling inside the NOFX workloads and selects PostgreSQL over SQLite for the Sealos template.

## Scaling

To scale NOFX resources:

1. Open the Canvas for your deployment.
2. Click the frontend, backend, or PostgreSQL resource card.
3. Adjust CPU, memory, replicas, or storage.
4. Apply the changes in the dialog.

## Troubleshooting

**Registration or login fails**

- Cause: The backend may still be waiting for PostgreSQL or the JWT/encryption configuration.
- Solution: Wait for the backend readiness probe to pass, then retry registration.

**OTP verification fails**

- Cause: The authenticator app code may be expired or the device clock may be out of sync.
- Solution: Wait for the next 30-second OTP window, confirm the device time, and retry with the latest code.

**Frontend loads but API calls fail**

- Cause: `/api` routing or backend startup may need inspection.
- Solution: Check the backend workload logs and confirm `/api/health` is ready.

## Additional Resources

- [NOFX README](https://github.com/NoFxAiOS/nofx)
- [NOFX API Reference](https://github.com/NoFxAiOS/nofx/tree/main/docs/api)
- [NOFX Security Notes](https://github.com/NoFxAiOS/nofx/blob/main/SECURITY.md)

## License

This Sealos template is provided under the repository license. NOFX itself is licensed under AGPL-3.0.
