# Deploy and Host Ory Hydra on Sealos

Ory Hydra is an OAuth 2.0 and OpenID Connect provider. This template deploys Hydra with a KubeBlocks PostgreSQL database and exposes the public OAuth/OIDC endpoints on Sealos Cloud.

![Ory Hydra Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/hydra/website-screenshot.webp)

## About Hosting Ory Hydra

Hydra provides standards-compliant OAuth 2.0 and OpenID Connect endpoints for applications that need delegated authorization, token issuance, and discovery metadata. The template runs the official Hydra container, performs SQL migrations at startup, and stores runtime state in PostgreSQL.

Hydra delegates user login and consent screens to your own identity UI. Configure `login_url` and `consent_url` during deployment so OAuth flows can redirect users to those pages.

## Common Use Cases

- **OAuth provider**: Issue access tokens and refresh tokens for APIs.
- **OpenID Connect discovery**: Publish issuer metadata and JWKS endpoints.
- **Central authorization layer**: Connect multiple services to a shared OAuth/OIDC provider.
- **Developer identity lab**: Test OAuth clients against a self-hosted Hydra instance.

## Dependencies for Ory Hydra Hosting

The Sealos template includes Hydra and KubeBlocks PostgreSQL.

### Deployment Dependencies

- [Ory Hydra Documentation](https://www.ory.sh/docs/hydra) - Official documentation
- [Hydra GitHub Repository](https://github.com/ory/hydra) - Source code and releases
- [OAuth 2.0 and OIDC Concepts](https://www.ory.sh/docs/hydra/concepts) - Core concepts

### Implementation Details

**Architecture Components:**

- **Hydra**: Public OAuth/OIDC service using the official `oryd/hydra:v2.3.0` image
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4 cluster for Hydra state
- **Migration init container**: Runs `hydra migrate sql up -e --yes` before Hydra starts
- **Ingress**: Publishes the public port with automatic HTTPS

**Configuration:**

The public issuer URL is generated from the Sealos app host. Hydra requires external login and consent URLs, so deploy this template with URLs from your identity UI or consent application.

**License Information:**

Ory Hydra is licensed under Apache License 2.0.

## Why Deploy Ory Hydra on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and lifecycle management. By deploying Ory Hydra on Sealos, you get:

- **One-Click Deployment**: Launch Hydra and PostgreSQL from the App Store template.
- **Managed Database**: KubeBlocks provisions and manages PostgreSQL for Hydra state.
- **Instant Public Access**: Sealos creates a public HTTPS endpoint for OAuth/OIDC metadata and APIs.
- **Easy Customization**: Configure login and consent URLs in the deployment form.
- **Kubernetes Operations**: Manage resources, logs, and scaling from the Sealos dashboard.

## Deployment Guide

1. Open the [Ory Hydra template](https://sealos.io/products/app-store/hydra) and click **Deploy Now**.
2. Configure `login_url` and `consent_url` with your external identity UI endpoints.
3. Wait for deployment to complete. Hydra runs database migrations before the service becomes ready.
4. Access the public endpoint at the provided URL:
   - **OIDC Discovery**: `https://[your-app-url]/.well-known/openid-configuration`
   - **JWKS**: `https://[your-app-url]/.well-known/jwks.json`
   - **Health**: `https://[your-app-url]/health/ready`

## Configuration

After deployment, configure OAuth clients through Hydra's admin API from inside your network or by adding an internal admin workflow. The public Sealos URL is intended for OAuth/OIDC client traffic.

## Scaling

To scale Hydra, open the Canvas for your deployment, click the Deployment resource card, adjust replicas or resources, and apply the change. Keep PostgreSQL sized for your token and consent traffic.

## Troubleshooting

### Login or Consent Redirect Fails

- Cause: `login_url` or `consent_url` points to a placeholder or unreachable identity UI.
- Solution: Update the deployment inputs to use the public URLs of your login and consent application.

### Discovery Metadata Has the Wrong Issuer

- Cause: The issuer must match the Sealos public URL.
- Solution: Verify the App URL and redeploy with the generated host settings preserved.

## Additional Resources

- [Hydra CLI Reference](https://www.ory.sh/docs/hydra/cli)
- [OAuth2 Flows](https://www.ory.sh/docs/hydra/oauth2)
- [Ory Community](https://www.ory.sh/docs/ecosystem/community)

## License

This Sealos template is provided under the repository license. Ory Hydra itself is licensed under Apache License 2.0.
