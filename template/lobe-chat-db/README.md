# Deploy and Host Lobe Chat Database Version on Sealos

Lobe Chat Database Version is an open-source LLM chat interface with server-side persistence. This template deploys Lobe Chat with PostgreSQL and Sealos-managed S3-compatible object storage on Sealos Cloud.

![Lobe Chat Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/lobe-chat-db/website-screenshot.webp)

## About Hosting Lobe Chat Database Version

Lobe Chat provides a polished web interface for working with OpenAI-compatible models, multimodal conversations, assistant workflows, and shared team state. The database version stores application data in PostgreSQL instead of relying only on browser-local IndexedDB, which makes it suitable for authenticated multi-device usage.

This Sealos template provisions the Lobe Chat database image, a Kubeblocks-managed PostgreSQL `postgresql-16.4.0` cluster, an idempotent PostgreSQL initialization job for the `lobechat` database, a private ObjectStorageBucket, a Service, an Ingress, and a Sealos App entry. Logto remains an external identity dependency because Lobe Chat needs its OAuth client ID, client secret, and issuer URL during deployment.

## Common Use Cases

- **Personal AI Workspace**: Run a private chat interface with persistent history and OpenAI-compatible model access.
- **Team AI Portal**: Give team members a shared authenticated entry point backed by PostgreSQL.
- **Multimodal Assistant UI**: Store images and generated assets through S3-compatible object storage.
- **Prototype LLM Products**: Test prompts, agents, and workflows before integrating them into larger applications.

## Dependencies for Lobe Chat Database Version Hosting

The Sealos template includes the runtime container, PostgreSQL, object storage, Kubernetes Service, Ingress, and App entry. You need a Logto application before deploying Lobe Chat because the template requires Logto OAuth credentials.

### Deployment Dependencies

- [Lobe Chat Documentation](https://lobehub.com/docs) - Official product and self-hosting documentation
- [Lobe Chat GitHub Repository](https://github.com/lobehub/lobe-chat) - Source code and release notes
- [Logto Documentation](https://docs.logto.io/) - Identity provider setup and application configuration
- [Sealos App Store](https://sealos.io/products/app-store/lobe-chat-db) - One-click deployment entry

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Lobe Chat**: The web application container serving the chat UI and API on port `3210`.
- **PostgreSQL**: Kubeblocks-managed PostgreSQL `postgresql-16.4.0` for accounts, conversations, settings, and application metadata.
- **PostgreSQL Init Job**: Creates the `lobechat` database after PostgreSQL is ready and exits cleanly when the database already exists.
- **Object Storage**: Sealos-managed private ObjectStorageBucket injected through S3-compatible environment variables.
- **Ingress and App Entry**: Public HTTPS route and Sealos dashboard entry for the Lobe Chat UI.
- **Logto**: A separately deployed identity provider used for registration and login.

**Configuration:**

The template composes `DATABASE_URL` from Kubeblocks secret fields and injects S3 credentials from Sealos object-storage secrets. The managed Sealos ObjectStorageBucket is the supported storage path for this template. External S3-compatible services can be evaluated after deployment for advanced operations, using the official Lobe Chat S3 documentation as a migration reference.

**License Information:**

Lobe Chat is released under the Apache-2.0 license. This Sealos template is provided as deployment configuration for the Sealos template repository.

## Why Deploy Lobe Chat Database Version on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and lifecycle management. By deploying Lobe Chat Database Version on Sealos, you get:

- **One-Click Deployment**: Deploy Lobe Chat from the App Store without writing Kubernetes manifests.
- **Managed Database and Storage**: PostgreSQL and S3-compatible object storage are provisioned with the template.
- **Instant Public Access**: The Ingress gives your deployment an HTTPS URL automatically.
- **Canvas Operations**: After deployment, use Canvas, the AI dialog, and resource cards to adjust resources or environment variables.
- **Resource Efficiency**: Pay-as-you-go resources keep the database version practical for small teams and prototypes.

## Before Deploying

Prepare Logto first:

1. Open the [Logto template](https://sealos.io/products/app-store/logto) and click **Deploy Now**.
2. Wait for Logto to finish deploying, then open the Logto console URL.
3. Register the first Logto administrator account.
4. In Logto, create a new application using the **Next.js (App Router)** application type.
5. Copy the Logto client ID and client secret, then use the Logto OpenID Connect issuer as `AUTH_LOGTO_ISSUER`. The issuer usually uses the `/oidc` suffix, for example `https://<your-logto-domain>/oidc`.

## Deployment Guide

1. Open the [Lobe Chat Database Version template](https://sealos.io/products/app-store/lobe-chat-db) and click **Deploy Now**.
2. Configure the required Logto parameters:
   - `AUTH_LOGTO_ID`: Logto application client ID
   - `AUTH_LOGTO_SECRET`: Logto application client secret
   - `AUTH_LOGTO_ISSUER`: Logto OpenID Connect issuer, usually `https://<your-logto-domain>/oidc`
3. Optionally configure OpenAI-compatible model access:
   - `OPENAI_API_KEY`
   - `OPENAI_PROXY_URL`
   - `OPENAI_MODEL_LIST`
   - `ACCESS_CODE`
4. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
5. Copy the Lobe Chat public URL from Canvas.

## Logto Callback Configuration

After Lobe Chat has a public URL, return to the Logto application settings and add these URLs:

- Redirect URI: `https://<your-lobe-chat-domain>/api/auth/callback/logto`
- Post sign-out redirect URI: `https://<your-lobe-chat-domain>`

Save the Logto changes, open the Lobe Chat public URL, click the account avatar, choose **Log in / Sign up**, and register or sign in through Logto.

## Scaling

To scale the deployment:

1. Open the Canvas for your Lobe Chat deployment.
2. Click the Lobe Chat Deployment or PostgreSQL resource card.
3. Adjust CPU, memory, storage, or replica settings.
4. Apply the change in the dialog and wait for the resource to become ready.

## Troubleshooting

### Logto Login Fails

- Cause: Redirect URI or post sign-out redirect URI is missing or uses a different domain.
- Solution: Reopen the Logto application settings and save the exact callback URLs shown above.

### Model Requests Fail

- Cause: `OPENAI_API_KEY`, `OPENAI_PROXY_URL`, or `OPENAI_MODEL_LIST` does not match your model provider.
- Solution: Update the values through Canvas, then restart the Lobe Chat Deployment.

### Uploads Fail

- Cause: Object storage configuration was changed after deployment.
- Solution: Keep the Sealos-managed ObjectStorageBucket and its injected S3 environment variables together.

## Additional Resources

- [Lobe Chat Self-Hosting Guide](https://lobehub.com/docs/self-hosting/start)
- [Lobe Chat Environment Variables](https://lobehub.com/docs/self-hosting/environment-variables)
- [Logto Applications](https://docs.logto.io/docs/recipes/integrate-logto/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. Lobe Chat is licensed under Apache-2.0.
