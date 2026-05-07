# Deploy and Host Supabase on Sealos

Supabase is an open source backend platform that combines PostgreSQL, authentication, realtime subscriptions, storage, and edge functions. This template deploys a production-ready Supabase stack with managed PostgreSQL and API gateway routing on Sealos Cloud.

## About Hosting Supabase

Supabase in this template runs as a multi-service architecture behind Kong, with each core capability deployed as an isolated workload. Studio provides the web console, while Auth, REST, Realtime, Storage, and Edge Functions are exposed through a single public domain with path-based routing.

The deployment automatically provisions a PostgreSQL cluster through Kubeblocks, initializes required Supabase schemas and roles with a bootstrap job, and wires credentials through Kubernetes secrets. Storage and runtime components use persistent volumes so configuration, files, and function cache data survive restarts.

Sealos also handles ingress, TLS, public domain access, and lifecycle operations in Canvas, so you can focus on product development instead of cluster plumbing.

## Common Use Cases

- **SaaS Backends**: Build full backend services with PostgreSQL, auth, and APIs from one stack.
- **Mobile App Backends**: Provide authentication, data APIs, and file storage for iOS and Android apps.
- **Realtime Dashboards**: Stream database changes to web clients using realtime channels.
- **Internal Tools**: Ship admin tools with role-based access and SQL-backed APIs.
- **Edge API Logic**: Run custom TypeScript functions close to your data with Supabase Edge Functions.

## Dependencies for Supabase Hosting

The Sealos template includes all required dependencies: Supabase Studio, Kong gateway, GoTrue Auth, PostgREST, Realtime, Storage API, Imgproxy, Postgres Meta, Edge Runtime, Logflare analytics, Vector log pipeline, Supavisor connection pooling, and a managed PostgreSQL 16.4 cluster.

### Deployment Dependencies

- [Supabase Documentation](https://supabase.com/docs) - Official docs and product guides
- [Supabase Self-Hosting Guide](https://supabase.com/docs/guides/self-hosting) - Self-hosting concepts and architecture
- [Supabase GitHub Repository](https://github.com/supabase/supabase) - Source code and release information
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth) - Authentication setup and providers
- [Supabase Storage Docs](https://supabase.com/docs/guides/storage) - Bucket and object storage usage
- [Supabase Edge Functions Docs](https://supabase.com/docs/guides/functions) - Serverless function development

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Supabase Studio**: Web dashboard for project management and SQL tooling (port `3000`).
- **Kong Gateway**: Unified API entrypoint and route management for all Supabase APIs (ports `8000` and `8443`).
- **Auth (GoTrue)**: Authentication and user management APIs (`/auth/v1/*`).
- **REST (PostgREST)**: PostgreSQL-backed REST and GraphQL endpoints (`/rest/v1/*`, `/graphql/v1`).
- **Realtime**: WebSocket and realtime API endpoints (`/realtime/v1/*`).
- **Storage API**: Object and file operations (`/storage/v1/*`) with local persistent storage.
- **Imgproxy**: Image transformation backend used by Storage API.
- **Postgres Meta**: Metadata and admin API used by Studio (`/pg/*` via gateway).
- **Edge Functions Runtime**: Deno-based function runtime exposed at `/functions/v1/*`.
- **Analytics (Logflare) + Vector**: Internal telemetry pipeline used by Studio and platform logs.
- **Supavisor**: PostgreSQL connection pooling service (ports `5432` and `6543`).
- **PostgreSQL (Kubeblocks)**: Persistent database cluster plus an init job that prepares Supabase roles and schemas.

**Configuration:**

- Required input parameters:
  - `jwt_secret`: JWT signing secret used by Auth, REST, Studio, and Storage.
  - `anon_key`: Anonymous API key signed by `jwt_secret`.
  - `service_role_key`: Service role API key signed by `jwt_secret`.
- Public access defaults to `https://<app-name>.<your-sealos-domain>`.
- Studio dashboard traffic is protected by HTTP basic auth through Kong (`dashboard_username` and generated `dashboard_password`).
- SMTP, signup behavior, JWT expiry, storage backend settings, and pooler limits are configurable via environment variables in Canvas.
- Persistent volumes are created for PostgreSQL data, storage files, Studio snippets/functions, and Edge Runtime cache.

**License Information:**

Supabase is open source and distributed under component-specific licenses (many Supabase repositories use Apache-2.0). Review the upstream repositories for exact license terms of each component.

## Why Deploy Supabase on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies development, deployment, and operations. By deploying Supabase on Sealos, you get:

- **One-Click Deployment**: Launch a full Supabase stack without manually assembling multiple services.
- **Kubernetes Reliability**: Get Kubernetes orchestration, health checks, and service discovery by default.
- **Pay-as-You-Go Efficiency**: Start with small resources and scale only when traffic grows.
- **Built-In HTTPS Access**: Receive an automatic public domain with SSL certificates.
- **Persistent Storage Included**: Keep database and object data durable across restarts.
- **Easy Customization**: Update env vars, resources, and replicas through Canvas dialogs.
- **AI-Assisted Operations**: Describe desired changes in the AI dialog for faster day-2 operations.

Deploy Supabase on Sealos and focus on shipping features instead of managing infrastructure.

## Deployment Guide

1. Open the [Supabase template](https://sealos.io/products/app-store/supabase) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - Set a strong `jwt_secret` (at least 32 characters).
   - Provide matching `anon_key` and `service_role_key` signed with the same `jwt_secret`.
   - Keep defaults for other values unless you have specific networking or auth requirements.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or edit resource cards directly.
4. Access your application via the generated public URL:
   - **Studio Dashboard**: `https://<app-name>.<your-sealos-domain>/`
   - **REST API**: `https://<app-name>.<your-sealos-domain>/rest/v1/`
   - **Auth API**: `https://<app-name>.<your-sealos-domain>/auth/v1/`
   - **Realtime API**: `https://<app-name>.<your-sealos-domain>/realtime/v1/`
   - **Storage API**: `https://<app-name>.<your-sealos-domain>/storage/v1/`
   - **Edge Functions API**: `https://<app-name>.<your-sealos-domain>/functions/v1/`

## Configuration

After deployment, you can configure Supabase through:

- **AI Dialog**: Describe updates such as changing auth behavior or adjusting resources.
- **Resource Cards**: Modify environment variables, CPU/memory, and replica counts for each service.
- **Studio UI**: Manage tables, SQL, auth users, and storage buckets.

Recommended post-deployment checks:

- Replace placeholder SMTP values if you need production email flows.
- Confirm `GOTRUE_DISABLE_SIGNUP`, phone/email signup options, and redirect allow list fit your auth policy.
- Verify your client apps use `anon_key` and server-side jobs use `service_role_key`.
- Keep `functions_verify_jwt` aligned with your edge function security model.

## Scaling

To scale your Supabase deployment:

1. Open your deployment in Canvas.
2. Select the services you want to scale (for example `rest`, `realtime`, `auth`, or `storage`).
3. Increase CPU and memory resources, then raise replica count where stateless scaling is appropriate.
4. Apply the changes and monitor pod status and latency metrics.

## Troubleshooting

### Common Issues

**Issue: 401/403 when calling APIs**
- Cause: Invalid API key usage or missing `apikey`/`Authorization` headers.
- Solution: Use `anon_key` for client requests and `service_role_key` only on trusted server-side paths.

**Issue: Cannot sign in or receive verification emails**
- Cause: SMTP defaults are placeholders or signup policies are restrictive.
- Solution: Configure valid SMTP credentials and review Auth env settings in the `auth` deployment.

**Issue: Edge Functions return auth errors**
- Cause: JWT verification settings do not match your request tokens.
- Solution: Check `functions_verify_jwt` and pass a valid bearer token if verification is enabled.

**Issue: Storage uploads work but image transformations fail**
- Cause: Imgproxy is unavailable or storage/image env values were modified incorrectly.
- Solution: Verify `imgproxy` pod health and confirm `IMGPROXY_URL` points to the internal service.

**Issue: Early startup errors in Supabase services**
- Cause: PostgreSQL init job or dependent services are still starting.
- Solution: Wait until PostgreSQL cluster and init job complete, then recheck dependent pod logs.

### Getting Help

- [Supabase Docs](https://supabase.com/docs)
- [Supabase GitHub Issues](https://github.com/supabase/supabase/issues)
- [Supabase Discord](https://discord.supabase.com)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Supabase API Reference](https://supabase.com/docs/reference)
- [PostgREST Documentation](https://postgrest.org/en/stable/)
- [Kong Gateway Documentation](https://docs.konghq.com/gateway/latest/)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the template repository license. Supabase and related runtime components are distributed under their respective upstream open source licenses.
