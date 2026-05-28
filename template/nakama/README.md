# Deploy and Host Nakama Server on Sealos

Nakama is an open-source game server for realtime multiplayer, player accounts, social systems, and live operations. This template deploys Nakama v3.39.0 with a managed PostgreSQL database on Sealos Cloud.

![Nakama Console Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/nakama/website-screenshot.webp)

## About Hosting Nakama

Nakama runs as a single game-server node with built-in HTTP API, realtime socket support, gRPC endpoints, and an embedded admin console. It stores users, sessions, leaderboards, groups, storage objects, chat messages, and other game data in PostgreSQL.

The Sealos template provisions PostgreSQL 16.4.0, creates the `nakama` database, runs Nakama schema migrations, and starts the server after the database is ready. It also generates session, runtime, console, and socket keys for each deployment.

Nakama Console is exposed as the primary web entry. The HTTP API is exposed on a separate URL for REST and WebSocket clients, while public gRPC ingress can be enabled when your client stack needs direct gRPC access.

## Common Use Cases

- **Realtime Multiplayer Games**: Handle realtime sessions, matchmaking, authoritative matches, and game server logic.
- **Player Identity and Accounts**: Use device, email, social, or custom authentication flows for players.
- **Social Game Systems**: Add friends, groups, chat, parties, notifications, and user metadata.
- **Leaderboards and Tournaments**: Build competitive rankings, seasonal challenges, and event-based scoring.
- **Live Operations Dashboards**: Inspect players, storage, matches, runtime modules, and service metrics through Nakama Console.

## Dependencies for Nakama Hosting

The Sealos template includes all required runtime dependencies: Nakama Server and PostgreSQL. No separate console image is required because Nakama Console is embedded in the Nakama binary.

### Deployment Dependencies

- [Official Nakama Documentation](https://heroiclabs.com/docs/nakama/) - Product documentation and development guides
- [Nakama GitHub Repository](https://github.com/heroiclabs/nakama) - Source code and release notes
- [Nakama Docker Installation Guide](https://heroiclabs.com/docs/nakama/getting-started/install/docker/) - Official container deployment reference
- [Nakama Client Libraries](https://heroiclabs.com/docs/nakama/client-libraries/) - SDKs for Unity, Unreal, Godot, JavaScript, and more

### Implementation Details

**Architecture Components:**

This template deploys these services:

- **Nakama Server**: StatefulSet running `heroiclabs/nakama:3.39.0` with persistent `/data` storage for runtime modules.
- **PostgreSQL Database**: KubeBlocks PostgreSQL 16.4.0 cluster for persistent Nakama data.
- **PostgreSQL Init Job**: Creates the `nakama` database idempotently before the server starts.
- **Nakama Console Ingress**: Primary web entry that routes to Nakama Console on port `7351`.
- **Nakama HTTP API Ingress**: Secondary endpoint for `/v2` REST API and `/ws` realtime WebSocket traffic on port `7350`.
- **Optional gRPC Ingresses**: Public routes for Nakama gRPC (`7349`) and console gRPC (`7348`) when `enable_grpc` is enabled.

**Configuration:**

Nakama starts only after PostgreSQL is reachable and the target database exists. A migration init container runs `nakama migrate up` before the main server starts, then health probes use `nakama healthcheck` for startup, readiness, and liveness checks.

The primary resource profile is tuned to the smallest validated Sealos tier for this template: `100m` CPU and `128Mi` memory for the Nakama container. PostgreSQL uses the standard database profile: `500m` CPU and `512Mi` memory.

**Login and Access:**

Nakama Console requires the console credentials configured during deployment:

- **Username**: value of `console_username` (default `admin`)
- **Password**: value of `console_password`

Player accounts are not created from the console login screen. Game clients create or authenticate player accounts through Nakama APIs such as device authentication at `/v2/account/authenticate/device?create=true`, using the configured socket/server key as Basic Auth username.

**License Information:**

Nakama is licensed under Apache-2.0. This Sealos template is also provided under Apache-2.0.

## Why Deploy Nakama on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to operations. By deploying Nakama on Sealos, you get:

- **One-Click Deployment**: Deploy Nakama and PostgreSQL from the App Store without writing Kubernetes YAML.
- **Managed Public URLs**: Get HTTPS URLs for the console and API automatically.
- **Persistent Data**: Store player, leaderboard, group, and storage data in managed PostgreSQL.
- **Easy Customization**: Adjust credentials, resource limits, and optional gRPC exposure from the deployment form or Canvas.
- **Kubernetes Foundation**: Run on a Kubernetes-based platform without managing cluster primitives directly.
- **Pay-As-You-Go Resources**: Start from a small validated footprint and scale resources as player traffic grows.

## Deployment Guide

1. Open the [Nakama Server template](https://sealos.io/products/app-store/nakama) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **Console Username**: Admin username for Nakama Console. The default is `admin`.
   - **Console Password**: Password for the console user. Set a strong value and save it securely.
   - **Enable gRPC**: Optional. Enable only if your clients need public gRPC endpoints.
3. Wait for deployment to complete. It typically takes 2-3 minutes because PostgreSQL must initialize before Nakama starts.
4. Open the primary application URL to access **Nakama Console**.
5. Log in with the configured Console Username and Console Password.
6. Use the API URL for game clients:
   - **HTTP API**: `https://<api-url>/v2/...`
   - **WebSocket**: `wss://<api-url>/ws`
   - **gRPC**: Use the generated gRPC URLs only when `enable_grpc` is enabled.

## Configuration

After deployment, manage Nakama through:

- **Nakama Console**: Inspect users, groups, storage, matches, leaderboards, notifications, API Explorer, and runtime modules.
- **Canvas AI Dialog**: Describe configuration changes and let Sealos apply updates.
- **Resource Cards**: Adjust StatefulSet resources, Ingress routes, and PostgreSQL settings from the Canvas.
- **Runtime Modules**: Mount or upload Lua, JavaScript, or Go runtime modules under `/data/modules` as needed.

### Console Login

The console does not provide public self-registration. Use the console credentials configured during deployment. If you lose the password, update `console_password` in the Nakama StatefulSet arguments or redeploy with a new password.

### Client Authentication

Nakama supports player registration through API flows such as device authentication, email authentication, and social provider authentication. For a basic device-auth smoke test, game clients call:

```bash
curl -X POST "https://<api-url>/v2/account/authenticate/device?create=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(printf '<server-key>:' | base64)" \
  -d '{"id":"unique-device-id","vars":{}}'
```

Replace `<server-key>` with the generated server key for your deployment. The template generates this value automatically as `server_key`; view it from the rendered deployment arguments or the Nakama StatefulSet `NAKAMA_SOCKET_SERVER_KEY` environment variable if you need to run manual API tests.

## Scaling

Start with the default validated resource profile for development and small tests. To scale your Nakama deployment:

1. Open the Canvas for your deployment.
2. Click the Nakama StatefulSet resource card.
3. Increase CPU and memory to the next Sealos resource tier if player traffic, runtime modules, or match logic require more capacity.
4. Click the PostgreSQL resource card if database load becomes the bottleneck.
5. Apply the changes and verify readiness in Nakama Console.

For production multiplayer games, benchmark with representative concurrent users, match logic, runtime modules, and API traffic before choosing final resource limits.

## Troubleshooting

### Common Issues

**Nakama Console login fails**
- Cause: Incorrect console username or password.
- Solution: Use the credentials configured during deployment. The default username is `admin`, but the password is whatever you entered in the deployment form.

**API returns `Server key invalid`**
- Cause: The client is using the wrong Basic Auth username.
- Solution: Use the deployment's server key as the Basic Auth username and an empty password.

**Database initialization takes longer than expected**
- Cause: PostgreSQL is still starting or creating the `nakama` database.
- Solution: Wait a few minutes. The init containers are designed to wait for database readiness and run migrations automatically.

**gRPC client cannot connect**
- Cause: Public gRPC ingress was not enabled or the client is using the HTTP API URL.
- Solution: Redeploy or update the template with `enable_grpc` enabled, then use the generated gRPC endpoint.

### Getting Help

- [Nakama Documentation](https://heroiclabs.com/docs/nakama/)
- [Nakama GitHub Issues](https://github.com/heroiclabs/nakama/issues)
- [Heroic Labs Forum](https://forum.heroiclabs.com/)
- [Sealos Documentation](https://sealos.io/docs/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Nakama Getting Started](https://heroiclabs.com/docs/nakama/getting-started/)
- [Nakama Runtime Code](https://heroiclabs.com/docs/nakama/server-framework/runtime-code/)
- [Nakama API Reference](https://heroiclabs.com/docs/nakama/api/)
- [Nakama Console Guide](https://heroiclabs.com/docs/nakama/getting-started/install/console/)

## License

This Sealos template is provided under Apache-2.0. Nakama itself is licensed under Apache-2.0.
