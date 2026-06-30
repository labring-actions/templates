# Deploy and Host EaglerCraft Server on Sealos

EaglerCraft Server packages the EaglercraftX browser client, WebSocket game access, Paper server runtime, and an RCON-backed admin panel. This template deploys Paper 1.12.2 by default and can also launch a Paper 1.8.8 server with persistent world data on Sealos Cloud.

![EaglerCraft Server Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## About Hosting EaglerCraft Server

EaglerCraft Server lets players open a Minecraft-style game client directly in the browser and connect to a self-hosted Paper server over secure WebSocket access. The published image contains both 1.8 and 1.12 runtime trees; this template exposes a `minecraft_version` choice that sets `MINECRAFT_VERSION`, with `1.12` selected by default.

The Sealos template deploys EaglerCraft Server as a single StatefulSet with one persistent volume mounted at `/eaglerX-1.8-server/server-data`. That mount preserves generated world data while keeping the image's runtime scripts and version directories intact.

## Common Use Cases

- **Browser-Based Minecraft Sessions**: Run a multiplayer game server that players can join from ChromeOS, tablets, school devices, and other browser-only environments.
- **Classroom or Club Servers**: Provide a shared Minecraft-style world without distributing desktop clients.
- **Private Community Worlds**: Keep a persistent Paper server online for a small group with managed storage and automatic HTTPS.
- **Plugin and Configuration Testing**: Test Paper 1.12.2 or 1.8.8 server changes in an isolated, disposable deployment.

## Dependencies for EaglerCraft Server Hosting

The Sealos template includes the EaglercraftX server image, WebSocket game endpoint, RCON-enabled admin panel, and persistent storage for world data.

### Deployment Dependencies

- [EaglerCraft Server Docker Image](https://github.com/yangchuansheng/eaglercraft-server) - Container image and runtime documentation used by this template
- [Published GHCR Image](https://github.com/yangchuansheng/eaglercraft-server/pkgs/container/eaglerx1.8server) - `ghcr.io/yangchuansheng/eaglerx1.8server:1.12.1`
- [Upstream Server Source](https://gitee.com/mirrorvim/eaglerX-1.8-server) - Source project used to build the image

## Implementation Details

### Architecture Components

This template deploys one stateful service:

- **EaglerCraft Server**: Browser client, WebSocket gateway, Paper runtime, and admin bridge in one container
- **Game Endpoint**: Port `5200`, exposed at the deployment root URL for browser gameplay and multiplayer access
- **Admin Panel**: Port `5201`, exposed at `/admin` for RCON-backed server administration
- **Persistent Storage**: One 1 GiB volume mounted at `/eaglerX-1.8-server/server-data` for generated world data

**Configuration:**

The `minecraft_version` input sets `MINECRAFT_VERSION`; choose `1.12` for Paper 1.12.2 or `1.8` for Paper 1.8.8. The `rcon_password` input sets `RCON_PASSWORD`. Use that password when the `/admin` panel prompts for access.

Sealos terminates TLS at the Ingress layer and routes the same public host to two backend ports: `/` reaches the browser game client and WebSocket multiplayer endpoint on port `5200`, while `/admin` reaches the management panel on port `5201`.

**License Information:**

This template is provided under the MIT License. Review the upstream EaglercraftX and bundled server components for their own licenses before redistribution.

## Why Deploy EaglerCraft Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operation, scaling, and management. By deploying EaglerCraft Server on Sealos, you get:

- **One-Click Deployment**: Start a browser-playable server from the App Store template without writing Kubernetes YAML.
- **Persistent World Data**: Store generated Paper world data on a persistent volume.
- **Instant HTTPS Access**: Get a public HTTPS URL for both gameplay and administration.
- **Resource Controls**: Adjust CPU, memory, and storage from the Canvas when your player count or world size grows.
- **AI-Assisted Operations**: Use the Canvas AI dialog or resource cards to change settings after deployment.
- **Pay-As-You-Go Efficiency**: Start with a compact footprint and scale only when the server needs more resources.

Deploy EaglerCraft Server on Sealos and run a persistent browser-playable world with managed infrastructure.

## Deployment Guide

1. Open the [EaglerCraft Server template](https://sealos.io/products/app-store/eaglercraft-server) and click **Deploy Now**.
2. Review the generated app name and host, choose the Minecraft version, and enter an RCON password in the popup dialog. The default Minecraft version is `1.12`; choose `1.8` when you want the Paper 1.8.8 runtime.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your server via the provided URL:
   - **Game Client**: Open `https://[your-app-url]` to load the browser client and play.
   - **Admin Panel**: Open `https://[your-app-url]/admin` and log in with the RCON password you entered during deployment.

## Configuration

After deployment, configure EaglerCraft Server through:

- **Browser Client**: Open the root URL and use the in-browser game client.
- **Admin Panel**: Open `/admin` and enter the RCON password from the deployment form to use the RCON-backed management surface.
- **Canvas AI Dialog**: Describe CPU, memory, storage, or environment changes and let AI apply them.
- **Resource Cards**: Click the StatefulSet, Service, Ingress, or storage cards to inspect and modify settings.

### Connecting Players

Use the deployment root URL for browser gameplay. When the client shows `press any key to continue`, press any key, set your player name and skin, then click **Multiplayer** -> **Direct Connect** -> **Connect to Server**.

Enter the public Sealos domain that was created for the deployment. In EaglercraftX direct connection fields, the secure WebSocket form of the same host is:

```text
wss://[your-app-url-host]
```

After joining the server, movement is blocked until the player account is registered. Open chat and run:

```text
/register <password>
```

The admin panel uses the same public host with `/admin`:

```text
https://[your-app-url]/admin
```

## Scaling

To scale your server:

1. Open the Canvas for your deployment.
2. Click the StatefulSet resource card.
3. Increase CPU and memory for more players or heavier world generation.
4. Click the storage resource card to expand the persistent volume when worlds, plugins, or assets grow.

## Troubleshooting

### Common Issues

**The admin panel asks for a password**

- Cause: The admin panel is protected by `RCON_PASSWORD`.
- Solution: Use the `rcon_password` value from the deployment parameters.

**Players cannot connect from the browser client**

- Cause: The client needs the public WebSocket endpoint for the deployed host.
- Solution: Use the root app URL for the bundled client or enter the host as `wss://[your-app-url-host]` in an EaglercraftX multiplayer flow.

**World data disappears after restart**

- Cause: World data must live under the configured `SERVER_DATA_DIR`.
- Solution: Keep the provided persistent volume mounted at `/eaglerX-1.8-server/server-data`.

### Getting Help

- [EaglerCraft Server Issues](https://github.com/yangchuansheng/eaglercraft-server/issues)
- [Upstream Server Source](https://gitee.com/mirrorvim/eaglerX-1.8-server)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [EaglerCraft Server Documentation](https://github.com/yangchuansheng/eaglercraft-server)
- [EaglerCraft Server Blog](https://sealos.io/blog/eaglercraft-server/)
- [Published Container Image](https://github.com/yangchuansheng/eaglercraft-server/pkgs/container/eaglerx1.8server)

## License

This Sealos template is provided under the MIT License. EaglerCraft Server is licensed under MIT, and bundled upstream components retain their own licenses.
