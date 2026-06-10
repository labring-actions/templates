# Deploy and Host cobalt on Sealos

cobalt is a privacy-focused media processing API for saving media from supported social and video services. This template deploys the cobalt API container with HTTPS ingress and configurable authentication controls on Sealos Cloud.

![cobalt Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cobalt/website-screenshot.webp)

## About Hosting cobalt

cobalt runs as a lightweight API service. It accepts media processing requests, applies rate limits, and returns structured responses for supported services. The official container requires `API_URL`, which this template sets to the Sealos public HTTPS URL.

The Sealos template deploys cobalt as a Kubernetes Deployment on port `9000`. It does not require a database for the default single-instance mode. Redis is only required by upstream cobalt when `API_INSTANCE_COUNT` is greater than `1`, so this template keeps the default single-instance mode and avoids unnecessary database resources.

Sealos handles public HTTPS access, service discovery, resource configuration, and app entry management.

## Common Use Cases

- **Media Processing API**: Provide a self-hosted API for supported media extraction workflows.
- **Private Utility Backend**: Run a controlled cobalt instance for internal tools.
- **Rate-Limited Public Endpoint**: Use built-in rate limit environment variables for public deployments.
- **Bot Protection**: Configure Cloudflare Turnstile session authentication when exposing the instance broadly.

## Dependencies for cobalt Hosting

The Sealos template includes the required runtime dependencies:

- cobalt image `ghcr.io/imputnet/cobalt:7.13.3`
- HTTPS Ingress and Sealos App entry

### Deployment Dependencies

- [cobalt GitHub Repository](https://github.com/imputnet/cobalt) - Source code and releases
- [cobalt Run an Instance Guide](https://github.com/imputnet/cobalt/blob/main/docs/run-an-instance.md) - Runtime deployment reference
- [cobalt API Environment Variables](https://github.com/imputnet/cobalt/blob/main/docs/api-env-variables.md) - Configuration reference

## Implementation Details

**Architecture Components:**

- **cobalt Deployment**: Runs `ghcr.io/imputnet/cobalt:7.13.3` on port `9000`.
- **Service and Ingress**: Expose cobalt through a public HTTPS URL.
- **Sealos App Resource**: Adds cobalt to the Sealos application interface.

**Configuration:**

The template sets:

- `API_URL` to the Sealos public URL with a trailing slash
- `API_PORT=9000`
- conservative rate limit defaults matching upstream documentation
- optional `TURNSTILE_SITEKEY` and `TURNSTILE_SECRET`
- optional `API_AUTH_REQUIRED`
- optional comma-separated `DISABLED_SERVICES`

cobalt has no login or registration flow. API access is open by default. Enable `api_auth_required` and provide Turnstile settings when you want API requests to require a configured Turnstile session.

**Resource Defaults:**

- App CPU limit: `200m`
- App memory limit: `256Mi`
- App CPU request: `20m`
- App memory request: `25Mi`

**Health Checks:**

The template uses TCP startup, readiness, and liveness probes on the cobalt API port.

**License Information:**

cobalt is licensed under GNU AGPL v3.0.

## Why Deploy cobalt on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and operations. By deploying cobalt on Sealos, you get:

- **One-Click Deployment**: Deploy cobalt with HTTPS access from one template.
- **No Database Overhead**: The default single-instance deployment runs without PostgreSQL, Redis, or object storage.
- **Instant Public Access**: Sealos provisions a public HTTPS endpoint automatically.
- **Easy Customization**: Adjust rate limits, disabled services, and auth settings from the Sealos Canvas.
- **AI-Assisted Operations**: Use the Sealos AI dialog or resource cards for post-deployment changes.

## Deployment Guide

1. Open the [cobalt template](https://sealos.io/products/app-store/cobalt) and click **Deploy Now**.
2. Configure deployment parameters:
   - **api_auth_required**: Enable when requests should require a configured Turnstile session.
   - **disabled_services**: Optional comma-separated service list to disable.
   - **turnstile_sitekey** and **turnstile_secret**: Optional Cloudflare Turnstile settings.
3. Wait for deployment to complete. This typically takes 1-2 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access cobalt through the provided URL:
   - **API Base URL**: Use the public HTTPS URL from Sealos.
   - **Server Info**: Open `/` to see cobalt metadata.

## Configuration

After deployment, configure cobalt through:

- **Environment Variables**: Adjust rate limits, disabled services, Turnstile, API auth, proxy, and YouTube session settings from the Deployment resource card.
- **AI Dialog**: Describe configuration changes in Sealos and let AI apply updates.
- **Ingress Settings**: Adjust upload and timeout settings if your media workflows require longer requests.

## Troubleshooting

### The container exits immediately

- **Cause**: `API_URL` is missing or malformed.
- **Solution**: Keep the template-generated `API_URL` value, including the `https://` scheme and trailing slash.

### Public requests should require Turnstile sessions

- **Cause**: cobalt is open by default.
- **Solution**: Enable `api_auth_required` and configure `turnstile_sitekey` plus `turnstile_secret`.

### Some services fail to process

- **Cause**: cobalt may need service-specific cookies, proxy settings, or YouTube session settings for certain providers.
- **Solution**: Add the relevant upstream environment variables from the cobalt documentation in the Deployment resource card.

## Additional Resources

- [cobalt Documentation](https://github.com/imputnet/cobalt/tree/main/docs)
- [cobalt API Reference](https://github.com/imputnet/cobalt/blob/main/docs/api.md)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template provides deployment configuration for running cobalt on Sealos. cobalt itself is distributed under GNU AGPL v3.0.
