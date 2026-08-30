# Deploy and Host EaglerCraft Server on Sealos

EaglerCraft Server packages the EaglercraftX browser client, WebSocket game gateway, Paper server, and RCON-backed admin panel in one image. This template deploys EaglercraftX Server 2.2.3 on Sealos Cloud with persistent world and plugin data.

![EaglerCraft Server Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## About Hosting EaglerCraft Server

EaglerCraft Server lets players open a Minecraft-style client in a browser and connect to a self-hosted Paper world over secure WebSocket access. Image 2.2.3 contains EaglercraftX 1.8 and 1.12 clients plus Paper 1.8.8 and 1.12.2 runtimes; the `minecraft_version` parameter selects the runtime at startup.

The Sealos template runs one StatefulSet with a persistent volume. The volume is mounted at `/eaglerx-data`, the image runtime is initialized under `/eaglerx-data/runtime`, and `PERSISTENT_DATA_ROOT` keeps world data and version-specific plugin repositories across restarts.

## Common Use Cases

- **Browser-Based Minecraft Sessions**: Run a multiplayer world for browsers, ChromeOS devices, tablets, and school computers.
- **Classroom or Club Servers**: Give a group a shared Minecraft-style world without distributing desktop clients.
- **Private Community Worlds**: Keep a small community server online with persistent storage and automatic HTTPS.
- **Plugin and Configuration Testing**: Test Paper 1.8.8 or 1.12.2 changes in an isolated deployment.

## Dependencies for EaglerCraft Server Hosting

The Sealos template includes the EaglercraftX server image, browser game endpoint, admin API, Paper runtime, and persistent storage.

### Deployment Dependencies

- [EaglerXserver source and documentation](https://github.com/yangchuansheng/eaglerXserver) - Official source and runtime guide
- [Published GHCR image](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server) - `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.3`
- [Sealos Discord](https://discord.gg/wdUn538zVP) - Community support

## Implementation Details

### Architecture Components

The template deploys one stateful service with two public routes and one persistent volume:

- **EaglerCraft Server**: Browser client, WebSocket gateway, Paper runtime, and admin bridge in one container
- **Game endpoint**: Port `5200`, exposed at the HTTPS root for the browser client and Multiplayer server entry
- **Admin endpoint**: Port `5201`, exposed through `/admin`, `/admin.css`, `/admin.js`, `/api`, and `/dynmap`
- **Internal Paper and RCON**: Ports `25565` and `25575` remain inside the container and are reached by the admin bridge
- **Persistent storage**: A 1 GiB volume mounted at `/eaglerx-data` stores `/eaglerx-data/runtime/server-data` and plugin repositories

**Configuration:**

The `minecraft_version` input accepts `1.8` or `1.12` and sets `MINECRAFT_VERSION`. The default `1.12` option starts Paper 1.12.2; `1.8` starts Paper 1.8.8. The `rcon_password` input sets `RCON_PASSWORD` and protects `/api/login` and the `/admin` panel. The tested starting footprint is 100m CPU, 1 GiB memory, and 1 GiB storage; increase resources from the Canvas as the world and player count grow.

Sealos terminates TLS at the Ingress layer and routes one public HTTPS host to the game and admin ports. The game route keeps WebSocket support and long proxy timeouts, while the admin route sends API, panel assets, and Dynmap traffic to port `5201`.

**License Information:**

This Sealos template is provided under the MIT License. Review the EaglercraftX project and bundled server components for their applicable licenses before redistribution.

## Why Deploy EaglerCraft Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operation, scaling, and management. By deploying EaglerCraft Server on Sealos, you get:

- **One-Click Deployment**: Start a browser-playable server from the App Store template.
- **Persistent World Data**: Keep Paper worlds and plugin repositories on managed storage.
- **Instant HTTPS Access**: Receive a public HTTPS URL for gameplay and administration.
- **Resource Controls**: Adjust CPU, memory, and storage from the Canvas as usage grows.
- **AI-Assisted Operations**: Use the Canvas AI dialog or resource cards to apply changes.
- **Pay-As-You-Go Efficiency**: Begin with a compact footprint and scale with demand.

Deploy EaglerCraft Server on Sealos and run a persistent browser-playable world with managed infrastructure.

## Deployment Guide

1. Open the [EaglerCraft Server template](https://sealos.io/products/app-store/eaglercraft-server) and click **Deploy Now**.
2. Review the generated app name and host, choose `1.12` or `1.8`, and enter an RCON password in the popup dialog. The password is used for admin login and RCON-backed operations.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your server through the generated HTTPS URL:
   - **Game client**: Open `https://[your-app-url-host]` to load the browser client.
   - **Multiplayer server entry**: In the EaglercraftX Multiplayer dialog, enter `wss://[your-app-url-host]`.
   - **Admin panel**: Open `https://[your-app-url-host]/admin` and sign in with the RCON password from deployment.

## Configuration

After deployment, configure EaglerCraft Server through:

- **Browser client**: Open the root URL and use the in-browser game client.
- **Admin panel**: Open `/admin`, enter the deployment RCON password, and use the server controls.
- **Canvas AI dialog**: Describe CPU, memory, storage, or environment changes for AI-assisted updates.
- **Resource cards**: Open the StatefulSet, Service, Ingress, or storage cards to inspect and edit resources.

### Admin Login and Player Registration

The admin panel uses the `rcon_password` entered during deployment. Open `/admin`, enter that password, and the browser stores a short-lived session token for the management API.

Players connect through the secure WebSocket endpoint below. When the world appears, press `T` or `/` to open chat and register within the 30-second login window:

```text
/register <password>
```

On later visits, log in with the same password:

```text
/login <password>
```

Use this address in Multiplayer:

```text
wss://[your-app-url-host]
```

The bundled 1.12 client also normalizes a bare hostname to `wss://`; the explicit secure WebSocket address is the documented connection format.

## Scaling

To scale your server:

1. Open the Canvas for your deployment.
2. Open the StatefulSet resource card.
3. Increase CPU and memory for more players or heavier world generation.
4. Expand the storage resource when worlds, plugins, or assets grow.

## Troubleshooting

### Common Issues

**The admin panel asks for a password**

- **Cause**: The panel is protected by `RCON_PASSWORD`.
- **Solution**: Use the `rcon_password` value from the deployment parameters.

**The browser client cannot connect**

- **Cause**: Multiplayer connects through the secure WebSocket endpoint on the generated host.
- **Solution**: Enter `wss://[your-app-url-host]`. After entering the world, complete `/register <password>` or `/login <password>` within the displayed login window.

**The first server action is still starting**

- **Cause**: Paper and the selected EaglercraftX runtime initialize during the first launch.
- **Solution**: Wait for the deployment to finish its 2-3 minute startup window, then retry the admin action.

**World data is missing after a restart**

- **Cause**: The world data path must remain on the persistent volume.
- **Solution**: Keep the template volume mounted at `/eaglerx-data` so the runtime data under `/eaglerx-data/runtime/server-data` remains available.

### Getting Help

- [EaglerXserver issues](https://github.com/yangchuansheng/eaglerXserver/issues)
- [EaglerXserver documentation](https://github.com/yangchuansheng/eaglerXserver)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [EaglerXserver source and runtime documentation](https://github.com/yangchuansheng/eaglerXserver)
- [Sealos EaglerCraft Server blog](https://sealos.io/blog/eaglercraft-server/)
- [Published container image](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server)

## License

This Sealos template is provided under the MIT License. EaglerCraft Server and its bundled upstream components retain their own applicable licenses.
