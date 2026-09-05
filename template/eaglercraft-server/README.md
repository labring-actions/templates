# Deploy and Host EaglerCraft Server on Sealos

EaglerCraft Server bundles a browser game client, secure WebSocket gateway, Paper server, and web administration console. This template deploys version **2.2.4** on Sealos with a persistent world and a bilingual English/Simplified Chinese admin panel.

![EaglerCraft Server admin console](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/eaglercraft-server/website-screenshot.webp)

## About Hosting EaglerCraft Server

Players open the browser client and join a Paper world through a secure WebSocket connection. Choose `1.12` for Paper 1.12.2 or `1.8` for Paper 1.8.8 before the first deployment. Use a separate instance and volume for each Minecraft version.

One StatefulSet runs the game gateway, Paper, and administration bridge. Sealos provisions a 1 GiB persistent volume, a public HTTPS address, and routing for gameplay and the admin panel. World files, server configuration, player accounts, and version-specific plugin repositories survive Pod replacement.

## Common Use Cases

- **Small community worlds**: Share a persistent multiplayer world through a browser link.
- **Classroom and club sessions**: Give a group a common world with browser access.
- **Server administration**: Manage weather, time, players, and plugins from the web console.
- **Plugin testing**: Try trusted Paper plugins in a separate instance.

## Dependencies for EaglerCraft Server Hosting

The image includes both browser clients, Paper runtimes, the WebSocket gateway, the admin bridge, and bundled plugins. The deployment uses local persistent storage, including the LoginSecurity plugin's SQLite account data.

### Deployment Dependencies

- [Upstream runtime documentation](https://github.com/yangchuansheng/eaglerXserver/tree/v2.2.4)
- [Version 2.2.4 release](https://github.com/yangchuansheng/eaglerXserver/releases/tag/v2.2.4)
- [Published container image](https://github.com/yangchuansheng/eaglerXserver/pkgs/container/eaglerx1.8server)

### Implementation Details

**Architecture Components:**

- **StatefulSet**: One replica using `ghcr.io/yangchuansheng/eaglerx1.8server:2.2.4`, pinned to its published SHA-256 digest.
- **Game route**: HTTPS `/` and secure WebSocket connections reach port `5200`.
- **Admin route**: `/admin`, `/api`, `/admin.css`, `/admin.js`, `/admin-i18n.js`, and `/dynmap` reach port `5201` on the same host.
- **Internal services**: Paper `25565` and RCON `25575` stay inside the Pod.
- **Persistent volume**: `/eaglerx-data` contains the full runtime, worlds, and configuration. `PERSISTENT_DATA_ROOT=/eaglerx-data/runtime/server-data` holds the version-specific plugin repositories.
- **Runtime initialization**: An init container seeds fresh volumes and refreshes image-owned scripts and browser assets on existing volumes, preserving Paper configuration, worlds, and plugin data.

The main container has a `200m` CPU limit and `1024Mi` memory limit; the init container uses `100m` CPU and `128Mi` memory. Validation at `100m` CPU triggered Paper 1.8's watchdog during chunk saving, and `512Mi` memory caused a startup OOM. Readiness waits for the game, HTTP, Paper, and RCON listeners plus the selected world's `level.dat` file. The startup probe verifies an RCON command response and saves newly generated worlds immediately, avoiding the five-minute wait for automatic saving.

`PUBLIC_GAME_URL` uses the generated HTTPS address. The admin Overview displays the corresponding `wss://` address and an **Open and join game** link. The ingress accepts plugin uploads up to **32 MiB**.

## Why Deploy EaglerCraft Server on Sealos?

[Sealos](https://sealos.io) runs applications on Kubernetes with one-click deployment, managed HTTPS access, and persistent storage. Pay-as-you-go resource controls let a small server start with the tested footprint. After deployment, use the Canvas AI dialog or resource cards to adjust CPU, memory, and storage.

## Deployment Guide

1. Open the [EaglerCraft Server template](https://sealos.io/products/app-store/eaglercraft-server) and click **Deploy Now**.
2. Choose `minecraft_version` (`1.12` by default) and set `rcon_password` to a strong, non-empty, single-line password. Save this value for administrator login.
3. Provisioning typically takes **2-3 minutes**. Allow additional time for initial world generation and plugin loading at the default CPU limit. The public URL may return **HTTP 502/503** during startup. Wait for the StatefulSet to become Ready, then open its application URL from the Canvas.
4. Open `/admin` on that HTTPS host, enter the deployment RCON password, and click **Confirm**. Use the header's **Language** selector to choose English or 简体中文.
5. On **Overview**, use **Open and join game**, or copy the WebSocket address into the browser client's Multiplayer server list. Complete the player registration or login described below.

## Administrator Login and Player Registration

### Administrator access

The admin login form uses the `rcon_password` set during deployment. Successful login creates an administration token stored in the current browser tab's `sessionStorage`, with an 8-hour lifetime. Closing the tab clears that tab's session; **Log out** also clears the stored login.

After connecting, try the **sunny** weather button and **noon** time button under **Operation control**. The world-state card and command console show the results. The panel also offers player management, world saving, and plugin controls.

### Player access

Choose a player name with 3-16 characters. Connect through the generated address:

```text
wss://[your-app-url-host]
```

Once you enter the world, press `T` to open chat and register within the 30-second login window. Use a player password with 6-32 characters:

```text
/register <password>
```

On later visits, use the same player name and password:

```text
/login <password>
```

Player passwords belong to LoginSecurity accounts. Keep the administrator RCON password for server management.

## Configuration and Upgrades

Use the Canvas AI dialog or the StatefulSet resource card to adjust resources. Keep **one replica** for this shared world and increase CPU or memory as player activity grows.

The `/eaglerx-data` volume must remain attached across upgrades. Each Pod start refreshes bundled scripts and browser assets; world directories, Paper configuration, and plugin repositories retain their existing content. Keep custom server configuration under the persisted Paper directories. Store a backup of the volume before changing the Minecraft runtime version.

The admin plugin panel supports uploading trusted JAR files up to 32 MiB through this template. Uploads and enable/disable changes take effect after a controlled Paper restart using **Restart the server**.

For Minecraft 1.8, initialization disables Dynmap's player health and armor display to accommodate the older Paper API. Map tiles and player positions remain available.

## Troubleshooting

- **The public URL returns HTTP 502/503 during startup**: Check the StatefulSet's Ready status in the Canvas. Startup automatically saves the new world once Paper and RCON are available, then enables public routing. Increase CPU in the Canvas when faster world generation and plugin loading matter.
- **Admin login fails**: Enter the saved `rcon_password`. Five failed attempts from the same source trigger a 10-minute lockout; clients sharing a reverse proxy may share that window.
- **The player is disconnected shortly after joining**: Complete `/register` on the first visit or `/login` on later visits within 30 seconds, using the same player name.
- **A plugin upload returns HTTP 413**: Keep the JAR within the template's 32 MiB ingress limit.

For application support, use [upstream issues](https://github.com/yangchuansheng/eaglerXserver/issues). For platform help, use the [Sealos community](https://discord.gg/wdUn538zVP).

## License

This template follows the [Sealos template repository](https://github.com/labring-actions/templates) licensing terms. Eaglercraft, Paper, and the bundled plugins retain their respective upstream licenses.
