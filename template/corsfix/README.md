# Deploy and Host Corsfix on Sealos

[Corsfix](https://corsfix.com) is an open-source CORS proxy that lets browser applications fetch data from APIs without CORS errors. Its dashboard manages applications, allowed target domains, API keys, encrypted secrets, and request analytics.

This template deploys the Corsfix dashboard and proxy with separate public HTTPS addresses, password-protected MongoDB and Redis, and persistent database storage.

## Features

- Proxy HTTP requests from browser applications with the appropriate CORS response headers.
- Register application domains and control which API domains they can access.
- Manage API keys, request analytics, and encrypted secret variables from the dashboard.
- Use response caching, custom request headers, and JSONP where needed.
- Keep application data and Redis state across container restarts.

## Included Components

| Component | Image | Purpose |
| --- | --- | --- |
| Dashboard | `ghcr.io/corsfix/corsfix-app:8899bb15e71c7238285ccefc4c95a0cd47daeaf0` | Web dashboard on port `3000`. |
| Proxy | `ghcr.io/corsfix/corsfix-proxy:8899bb15e71c7238285ccefc4c95a0cd47daeaf0` | CORS proxy on port `80`. |
| MongoDB | `mongo:8.0.17` | Users, applications, API keys, encrypted secrets, and metrics. |
| Redis | `redis:7.4.11-alpine` | Cache, rate limiting, and coordination between services. |

The databases run as dedicated StatefulSets with persistent volumes. This keeps the database versions aligned with Corsfix's tested self-hosting configuration without requiring the Sealos managed-database operator. Database ports are available only inside the cluster.

The pinned dashboard image requires an **AMD64** worker node. The template selects this architecture automatically.

## Deployment and First Login

1. Deploy the template from the Sealos App Store. Leave **Disable signup** set to `false` for the first deployment.
2. Wait for the dashboard, proxy, MongoDB, and Redis to become ready. Initial image downloads and database initialization can take several minutes.
3. Open the Corsfix App URL. Register an account on the authentication page, then sign in.
4. Open the dashboard application's environment settings in Sealos. Set `DISABLE_SIGNUP` to `true` and redeploy the dashboard after creating the accounts you need.
5. In Corsfix, add your application's domain and the API domains it can access. Use the generated proxy address in your frontend requests.

Registration remains open until you disable it. If signup was disabled before creating an account, temporarily set the dashboard's `DISABLE_SIGNUP` environment variable back to `false` and redeploy it.

The dashboard is available at `https://<app_host>.<Sealos domain>` and the proxy at `https://<proxy_host>.<Sealos domain>`. Both hostnames are generated automatically. Find the proxy's public address in the Sealos application ending in `-proxy`; opening `/up` on that address should return `Corsfix: OK.`

## Configuration

| Input | Default | Description |
| --- | --- | --- |
| Disable signup | `false` | Controls account registration. Disable it after creating your accounts. |
| RPM | `180` | Rate limit per client IP. Supported options are `60`, `120`, `180`, and `600`. Local development origins have a separate `60` RPM limit. |
| Allowed origins | Empty | Optional comma-separated hostnames allowed without registering applications in the dashboard, such as `app.example.com,www.example.com`. Omit URL schemes and paths. |
| Allowed targets | Empty | Optional comma-separated target hostnames for those environment-allowed origins. Empty permits any public target for those origins. Applications registered in the dashboard use their own target settings. |

For normal dashboard-based use, leave both allowlist inputs empty.

The template automatically creates MongoDB and Redis passwords, an authentication secret, and one shared encryption key. `KEK_VERSION_1` decodes to exactly 32 bytes and is shared by the dashboard and proxy. Preserve the generated Kubernetes Secret when backing up or restoring the application: the stored encrypted secrets cannot be decrypted without their original key.

HTTPS terminates at the Sealos Ingress. The dashboard's `AUTH_URL` is the public HTTPS dashboard address, while `PROXY_DOMAIN` and the proxy's `APP_DOMAIN` contain hostnames without a URL scheme. If you configure custom domains, update these values and the corresponding Ingress hosts and certificates together.

## Resources and Storage

| Component | CPU request / limit | Memory request / limit | Persistent storage |
| --- | --- | --- | --- |
| Dashboard | `100m / 1000m` | `128Mi / 512Mi` | None |
| Proxy | `50m / 500m` | `64Mi / 256Mi` | None |
| MongoDB | `100m / 500m` | `128Mi / 512Mi` | `1Gi` data + `1Gi` configuration |
| Redis | `20m / 200m` | `32Mi / 128Mi` | `1Gi` data |

The default allocation uses 3 GiB of persistent storage. Increase resources and storage as your traffic and retained data grow. MongoDB's WiredTiger cache is capped at `0.25` GiB for this initial resource profile. Redis uses append-only persistence.

Back up the MongoDB data and generated application Secret before deleting the deployment or changing database volumes. Restarting a workload preserves its persistent volumes; deleting the storage removes its data.

## Useful Links

- [Corsfix website](https://corsfix.com)
- [Self-hosting documentation](https://corsfix.com/docs/open-source/self-hosting)
- [Corsfix documentation](https://corsfix.com/docs)
- [Source code](https://github.com/corsfix/corsfix)
