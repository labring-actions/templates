# Deploy and Host Headscale on Sealos

Headscale is an open source, self-hosted implementation of the Tailscale control server. This template deploys Headscale 0.29.2 with the Headplane 0.7.0 web UI, persistent storage, TLS-enabled public endpoints, and an optional KubeBlocks PostgreSQL database.

![Headscale website](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/headscale/website-screenshot.webp)

## About Headscale

Headscale coordinates a private Tailscale-compatible network. It manages users, machines, routes, DNS, ACL policies, and device enrollment while compatible clients establish their data paths.

The template runs Headscale and Headplane together in one StatefulSet so Headplane can safely reload Headscale configuration through its Kubernetes integration. SQLite is the default database and matches the upstream recommendation for new deployments. The `use_postgresql` option provisions a dedicated PostgreSQL 16.4.0 cluster when your operating model requires an external database.

## Common Use Cases

- Run a private control plane for Tailscale-compatible clients.
- Connect homelab, edge, and team devices across networks.
- Manage users, routes, DNS, ACLs, and pre-auth keys from Headplane.
- Keep control-plane state on persistent Sealos storage.
- Use a managed PostgreSQL database for database-specific operational requirements.

## Dependencies

The template includes the complete server-side runtime: Headscale, Headplane, persistent volumes, Service and Ingress resources, scoped Kubernetes RBAC, and the conditional PostgreSQL resources.

- [Headscale 0.29.2](https://github.com/juanfont/headscale/releases/tag/v0.29.2) provides the control server and APIs.
- [Headplane 0.7.0](https://github.com/tale/headplane/releases/tag/v0.7.0) provides the administration UI.
- KubeBlocks provides PostgreSQL 16.4.0 when `use_postgresql` is enabled.
- A compatible [Tailscale client](https://tailscale.com/download) is required on each device joining the network.

## Architecture

| Component | Version | Purpose | Minimum tested limit |
| --- | --- | --- | --- |
| Headscale | `0.29.2-debug` | Control server, REST API, gRPC API, and metrics | `100m` CPU / `128Mi` memory |
| Headplane | `0.7.0` | Web administration UI | `100m` CPU / `256Mi` memory |
| SQLite | Embedded | Default Headscale database on persistent storage | Included with Headscale |
| PostgreSQL | `16.4.0` | Optional KubeBlocks-managed database | `500m` CPU / `512Mi` memory |
| PostgreSQL init | `postgres:16-alpine` | Creates and verifies the `headscale` database | `100m` CPU / `128Mi` memory |

The application uses three `512Mi` persistent volumes:

| Path | Contents |
| --- | --- |
| `/var/lib/headscale` | SQLite database, keys, and Headscale runtime state |
| `/etc/headscale` | Validated, non-sensitive Headscale configuration |
| `/var/lib/headplane` | Headplane state |

The main public domain serves the Headscale HTTP API and Headplane at `/admin/`. A dedicated public domain exposes the Headscale gRPC endpoint. Metrics remain available only inside the cluster on port `9090`.

## Why Deploy Headscale on Sealos?

- Deploy the complete Headscale and Headplane stack from one App Store template.
- Receive HTTPS application and gRPC domains with managed TLS certificates.
- Keep configuration, keys, and database state on persistent volumes.
- Select embedded SQLite or a KubeBlocks-managed PostgreSQL database during deployment.
- Inspect resources, logs, events, and container terminals from the Sealos Canvas.
- Start with the tested minimum resources and adjust capacity as the tailnet grows.

## Deploy on Sealos

1. Open the [Headscale template](https://sealos.io/products/app-store/headscale) and click **Deploy Now**.
2. Keep `use_postgresql` disabled for the default SQLite deployment. Enable it to provision the dedicated PostgreSQL cluster.
3. Wait for all resources to become ready. SQLite usually starts in a few minutes. A new PostgreSQL cluster may take several minutes during its first initialization.
4. Open the application URL. The root path redirects to the Headplane sign-in page at `/admin/`.

## Sign In to Headplane

Headplane authenticates with a Headscale API key. Generate one from the Headscale container in the Sealos terminal:

```bash
headscale apikeys create
```

The command displays the key once. Store it securely and paste it into the **API Key** field on the Headplane sign-in page. Headscale gives a new key a 90-day lifetime by default. Set an explicit lifetime when needed:

```bash
headscale apikeys create --expiration 365d
```

After signing in:

1. Open **Users**, select **Add user**, and create the first Headscale user.
2. Open **Settings > Auth Keys**, select **Create pre-auth key**, choose the user, and set the desired lifetime and key options.

## Connect a Device

Install a compatible Tailscale client, then use the main Sealos application URL and the pre-auth key created in Headplane:

```bash
tailscale up \
  --login-server=https://your-headscale-domain.example.com \
  --authkey=<pre-auth-key>
```

The device appears under **Machines** in Headplane after enrollment.

## Remote Headscale CLI

The template exposes gRPC on a dedicated TLS domain. Use a `headscale` CLI binary matching server version `0.29.2`, then configure the endpoint and API key:

```bash
export HEADSCALE_CLI_ADDRESS=your-headscale-grpc-domain.example.com:443
export HEADSCALE_CLI_API_KEY=<api-key>
headscale users list
```

The Headplane UI covers the common administration workflow, so remote gRPC access is optional.

## Database Options

### SQLite

SQLite is enabled by default and stores its database at `/var/lib/headscale/db.sqlite`. Write-ahead logging is enabled, and the persistent volume keeps state across Pod replacement.

### PostgreSQL

Enable `use_postgresql` during deployment to create a KubeBlocks PostgreSQL cluster. The template creates the `headscale` database and waits for it to accept authenticated queries. Headscale receives the host, port, username, and password directly from the KubeBlocks Secret through its official `HEADSCALE_DATABASE_POSTGRES_*` environment variables.

The Kubernetes Secret remains the credential source, while `/etc/headscale/config.yaml` contains static, non-sensitive database settings. PostgreSQL adds a database Pod and a `1Gi` data volume. The initialization Job allows up to six minutes for a cold database start.

## Configuration

- Use Headplane to manage users, machines, routes, DNS, ACL policies, and pre-auth keys.
- Headscale reads `/etc/headscale/config.yaml` from persistent storage. The init container validates mode, placeholders, and the complete Headscale configuration before replacing an incomplete file with an atomic same-directory move.
- Headplane reads `/etc/headplane/config.yaml` from the template ConfigMap.
- Headplane receives its generated cookie secret through `HEADPLANE_SERVER__COOKIE_SECRET`, keeping the value out of the ConfigMap.
- PostgreSQL credentials are injected directly into the Headscale container from the KubeBlocks connection Secret and stay out of persistent volumes.
- `shareProcessNamespace` and scoped Pod-read RBAC let Headplane signal Headscale after supported configuration changes.
- The Pod runs as UID/GID `1000` with `RuntimeDefault` seccomp and all Linux capabilities dropped.

## Troubleshooting

### Headplane rejects the API key

Create a fresh API key in the Headscale container and paste the complete value into the sign-in form. API keys are displayed once and expire according to their configured lifetime.

### A client does not enroll

Confirm that `--login-server` uses the main HTTPS application URL and that the pre-auth key belongs to an existing user. Check the **Machines** and **Auth Keys** pages in Headplane.

### PostgreSQL deployment is still initializing

Open the Sealos Canvas and inspect the PostgreSQL Cluster, the `*-pg-init` Job, and the Headscale StatefulSet. The application starts after the database accepts an authenticated query and the `headscale` database exists.

### Health checks

Use these endpoints to verify the two application containers:

```text
https://your-headscale-domain.example.com/health
https://your-headscale-domain.example.com/admin/healthz
```

## Resources

- [Headscale documentation](https://headscale.net/stable/)
- [Headscale API documentation](https://headscale.net/stable/ref/api/)
- [Headscale GitHub repository](https://github.com/juanfont/headscale)
- [Headplane documentation](https://headplane.net/)
- [Headplane GitHub repository](https://github.com/tale/headplane)
- [Tailscale documentation](https://tailscale.com/kb/)
- [Sealos documentation](https://sealos.io/docs/)

## License

Headscale is available under the BSD-3-Clause license. Headplane is available under the MIT license. This template follows the repository license for Sealos templates.
