# Deploy and Host EaglerCraft Server on Sealos

EaglerCraft Server bundles browser-based Minecraft, a WebSocket gateway, Paper, and an English/Simplified Chinese administration console. This template deploys **2.2.7** with persistent worlds and player accounts.

![EaglerCraft Server administration console](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

The screenshot shows the English console of a tested Sealos deployment with a connected player.

## About Hosting EaglerCraft Server

Choose `1.12` for Paper 1.12.2 or `1.8` for Paper 1.8.8. Each deployment runs one game version in a single StatefulSet, with a 1 GiB persistent volume for worlds, configuration, player accounts, and version-specific plugins. Create separate instances and volumes to run both versions.

Players connect through the public HTTPS game page and secure WebSocket endpoint. The application card opens `/admin`, where the server owner can manage weather, time, players, worlds, and plugins.

## Common Use Cases

- **Small shared worlds**: Invite friends with a browser link.
- **Clubs and classrooms**: Host a persistent world for group sessions.
- **Server administration**: Manage game settings and player access from the console.
- **Plugin trials**: Test trusted Paper plugins in a separate instance.

## Dependencies for EaglerCraft Server Hosting

The image includes the game clients, Paper, Bungee gateway, Python administration bridge, and plugins. LoginSecurity stores player accounts in SQLite on the persistent volume. The selected release documents local filesystem storage for this deployment.

### Deployment Dependencies

- A Sealos account and a browser with WebGL support.
- A strong, non-empty, single-line administration password.
- Acceptance of the [Minecraft EULA](https://www.minecraft.net/en-us/eula); the upstream entrypoint writes `eula=true` during startup.
- [Version 2.2.7 source and deployment documentation](https://github.com/yangchuansheng/eaglerXserver/tree/v2.2.7).
- [Version 2.2.7 release](https://github.com/yangchuansheng/eaglerXserver/releases/tag/v2.2.7).

### Architecture Components

- **StatefulSet**: One replica using `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.7`, pinned to its verified SHA-256 digest.
- **Initialization and probes**: ConfigMap scripts initialize fresh storage, refresh image-owned scripts and browser assets, and verify the first world save. Existing worlds, configuration, and plugin repositories retain their data.
- **Persistent storage**: `/eaglerx-data/runtime` holds the runtime; `server-data/plugins-1.8` and `server-data/plugins-1.12` hold the version-specific plugin repositories.
- **Game route**: HTTPS `/` and WSS connections reach port `5200`.
- **Management route**: `/admin`, `/api`, admin assets, and `/dynmap` reach port `5201` on the same HTTPS host. Paper `25565` and RCON `25575` remain internal.

The main container uses a `200m` CPU limit and `1024Mi` memory limit. Initialization uses `100m` CPU and `128Mi` memory. These settings cover the tested personal workload; increase resources as world complexity and player activity grow. The volume starts at 1 GiB; monitor free space as chunks, maps, and backups accumulate.

## Why Deploy EaglerCraft Server on Sealos?

[Sealos](https://sealos.io) provides one-click deployment on Kubernetes, managed HTTPS, persistent storage, and pay-as-you-go resources. After deployment, use the Canvas AI dialog or resource cards to adjust the server's CPU, memory, and storage.

## Deployment Guide

1. Open the [EaglerCraft Server template](https://sealos.io/products/app-store/eaglercraft-server) and click **Deploy Now**.
2. Choose `minecraft_version` and set `rcon_password`. Save this password for administration.
3. Deployment typically takes **2-3 minutes**; initial world generation can take longer. After deployment, open the application card in the Canvas to reach `/admin`.
4. Enter your `rcon_password` and click **Confirm**. The console accepts login during startup; wait for **Paper is ready** before using game controls.
5. On **Overview**, click **Join game**. Follow the player setup and registration steps below. The **Language** selector switches the console between English and 简体中文.

## Administrator Login and Player Registration

### Administrator login

The administration dialog uses the deployment's `rcon_password`. Login issues a token valid for 8 hours, stored in the current tab's `sessionStorage`. **Log out** clears that session.

After **Paper is ready**, click **Rain** and **Noon** under **Runtime controls**. The world card updates its weather and time, and **Command terminal** shows command responses. **World tools** provides world-save operations; **System settings** provides configuration, plugins, and controlled Paper restarts.

### Player setup and login

1. Open the game page. Press a key when prompted to enable sound.
2. For a fresh browser profile, choose **Edit Profile**, set a stable player name of 3-16 characters, and click **Done**. Complete any client information screen. Keep this same name for later visits; quick join can initially assign a random name.
3. Choose **Multiplayer**. Version 2.2.7 lists this deployment automatically. Select it and click **Join Server**, or use the console's **Join game** link after configuring your profile.
4. Once the world appears, press `T` and register within 30 seconds with a password of 6-32 characters:

   ```text
   /register <player-password>
   ```

5. On later connections, use the same player name, press `T`, and enter:

   ```text
   /login <player-password>
   ```

A successful registration signs the player in. Try `/sethome base` and `/homes` to save and list a home. Player passwords belong to LoginSecurity; the server owner uses the RCON password for administration.

The secure connection address is displayed on Overview:

```text
wss://[your-app-url-host]/
```

## Configuration and Upgrades

Use the Canvas AI dialog or StatefulSet resource card for resource changes. Keep one replica for this shared world. Store a backup before changing game versions or upgrading.

Keep the `/eaglerx-data` volume attached. Each Pod start refreshes bundled scripts and web clients while preserving existing worlds, Paper configuration, and plugin state. Custom frontend changes require merging with the new image assets. The startup probe performs the first world save and checks Paper's RCON response before declaring readiness.

Trusted plugin uploads are limited to **32 MiB** by this template's ingress. Upload, enable, or disable a plugin, then use the controlled Paper restart in **System settings** to apply changes. Allow several minutes for restart and check **Paper is ready** afterward.

For Minecraft 1.8, initialization disables Dynmap's player health/armor display to match the older Paper API; map tiles and player positions remain available.

## Troubleshooting

- **The console is available while game controls are loading**: Wait for **Paper is ready**. The Service publishes the console and game page during startup. Use the Canvas resource logs to inspect startup; Paper's detailed log is `/eaglerx-data/runtime/server/logs/latest.log`.
- **Administrator login fails**: Use the saved deployment password. Five failed attempts from the same source cause a 10-minute lockout; clients behind a proxy may share the window.
- **Login timed out in the game**: Rejoin and submit `/register` or `/login` within 30 seconds. Use a stable player name so the server can find your account.
- **Changes wait for a restart**: Configuration and plugin changes take effect after the console's controlled Paper restart.
- **Plugin upload returns HTTP 413**: Keep the JAR within 32 MiB.

See [upstream issues](https://github.com/yangchuansheng/eaglerXserver/issues) for application support and the [Sealos community](https://discord.gg/wdUn538zVP) for platform help.

## License

This template follows the [Sealos templates repository](https://github.com/labring-actions/templates) licensing terms. Eaglercraft, Paper, Minecraft assets, and bundled plugins retain their respective upstream licenses and terms.
