# Deploy and Host Minecraft on Sealos

This template runs a persistent Minecraft Java Edition server on Sealos with the official `itzg/minecraft-server:2026.8.0-java25` image. It supports Paper, Fabric, and Forge, publishes the game protocol through a TCP NodePort, and stores all server data under `/data`.

![Minecraft Server on Docker Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/minecraft/website-screenshot.webp)

## About Hosting Minecraft

One StatefulSet replica owns one world. A persistent volume keeps world data, server properties, plugins, mods, and logs across pod replacement. `mc-health` drives startup, readiness, and liveness checks through the Minecraft status protocol.

The container image is pinned to release `2026.8.0-java25`. The default `VERSION=LATEST` resolves the newest compatible game server at each cold start; choose a concrete `VERSION` when plugins, mods, or reproducible upgrades require one.

## What Gets Deployed

| Component | Purpose | Default profile |
| --- | --- | --- |
| Minecraft StatefulSet | One Java Edition server | 200m CPU / 2 GiB |
| Persistent volume | `/data` world and runtime files | 1 GiB |
| NodePort Service | Public Minecraft Java TCP protocol | Container port 25565 |

The JVM heap is `1024M`. The 2 GiB container limit provides native-memory and startup headroom. Resource requests are 20m CPU and 204 MiB memory.

## Deployment Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `TYPE` | `PAPER` | Selects `PAPER`, `FABRIC`, or `FORGE`. |
| `VERSION` | `LATEST` | Selects a concrete Minecraft release or resolves the newest compatible release. |

Deploying this template sets `EULA=TRUE`. Proceed only after reviewing and accepting the [Minecraft EULA](https://www.minecraft.net/eula).

## Access and Administration

Players connect from Minecraft Java Edition with their regular Minecraft or Microsoft account. The server address uses the Sealos region host plus the generated NodePort, such as `usw-1.sealos.io:46520`.

The image enables RCON for local administration and provides `rcon-cli` inside the container. The template keeps RCON port 25575 inside the pod network. Use the Sealos terminal to run commands such as `rcon-cli list`, `rcon-cli say ...`, and `rcon-cli save-all`.

## Deployment Guide

1. Open the [Minecraft template](https://sealos.io/products/app-store/minecraft) and select **Deploy Now**.
2. Choose `PAPER`, `FABRIC`, or `FORGE`.
3. Keep `VERSION=LATEST` for a moving release target, or enter a concrete game version for reproducible servers.
4. Start the deployment and allow several minutes for downloads, patching, and initial world generation.
5. Open the Service card in Sealos and copy the NodePort mapped from container port 25565.
6. Add `<region-host>:<mapped-port>` as a Minecraft Java Edition server.

## Configuration

- **Server files**: Edit persistent files under `/data`, including `server.properties`, plugins, mods, and whitelist files.
- **RCON**: Run administrative commands from the container with the bundled `rcon-cli`.
- **Sealos Canvas**: Inspect logs, resource metrics, StatefulSet health, Service mapping, and volume capacity.
- **Whitelist and operators**: Configure the Minecraft whitelist and operator list according to your community policy.

## Scaling

A Minecraft world scales vertically because one process owns its live state. Increase CPU for simulation distance, entities, plugins, or additional players. Raise both the container memory limit and `MEMORY` when intentionally expanding the JVM heap.

The validated startup floor is 200m CPU with a 2 GiB memory limit. A 100m CPU and 1 GiB candidate produced repeated exit code 137 and remained unready; the selected profile completed Paper startup, world generation, protocol checks, and RCON commands.

## Validated Runtime

A fresh Paper deployment resolved Paper `26.2`, generated all three dimensions, reached readiness with zero restarts, and answered the Minecraft status protocol from both localhost and the public NodePort.

Runtime administration completed `list`, a broadcast message, and `save-all` through RCON. The bound persistent volume contained `server.properties`, `world/level.dat`, and saved world data after those operations.

## Troubleshooting

### The server is still starting

Inspect the pod logs for download, patch, and world-generation progress. First startup can take several minutes, and the startup probe allows up to five minutes after its initial delay.

### The client cannot connect

Confirm that the pod is Ready, copy the TCP NodePort from the Service card, and use the Sealos region host with that mapped port.

### Paper, Fabric, or Forge fails

Check the compatibility between `TYPE`, `VERSION`, Java 25, plugins, and mods. Pin a concrete `VERSION` for a fixed modpack or plugin set.

### The world needs more capacity

Expand the persistent volume before world data or backups approach 1 GiB. Run `save-all` before maintenance that affects the pod or volume.

## Resources

- [Minecraft Server on Docker Documentation](https://docker-minecraft-server.readthedocs.io/en/latest/)
- [2026.8.0 Release](https://github.com/itzg/docker-minecraft-server/releases/tag/2026.8.0)
- [Official Docker Compose](https://github.com/itzg/docker-minecraft-server/blob/2026.8.0/docker-compose.yml)
- [Paper Documentation](https://docs.papermc.io/)
- [Minecraft EULA](https://www.minecraft.net/eula)
- [Sealos Documentation](https://sealos.io/docs)

## License

This template follows the Sealos templates repository license. Minecraft, Paper, Fabric, Forge, and `itzg/docker-minecraft-server` follow their respective upstream licenses and terms.
