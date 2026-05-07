# Deploy and Host 1.12 EaglerCraft Server on Sealos

EaglerCraft is an AOT compiled voxel game inspired from Minecraft designed to run on Javascript. It uses TeaVM and LAX1DUDE's OpenGL emulator to run a Java virtual machine fully compatible with browsers. Eaglercraft can be played on ChromeOS, iOS, Android, and pretty much any device with a web browser; including your smart fridge. This template deploys a production-ready EaglerCraft 1.8 server with WebSocket support and persistent world storage on Sealos Cloud.

## About Hosting EaglerCraft Server

EaglerCraft Server runs as a stateful game server that provides dual WebSocket endpoints for browser-based Minecraft gameplay. The server maintains three persistent worlds (Overworld, Nether, and The End) with dedicated storage for each dimension, ensuring your players' progress and builds are safely preserved across restarts and updates.

The Sealos template automatically provisions separate persistent volumes for each Minecraft dimension, handles SSL certificate generation for secure WebSocket connections, and provides two access endpoints optimized for different connection scenarios.

## Common Use Cases

- **Educational Gaming**: Provide instant-access Minecraft servers for students without requiring client installations or account purchases
- **Browser-Based Gaming Communities**: Host public or private Minecraft servers accessible from any device with a web browser
- **Quick Multiplayer Sessions**: Set up temporary game servers for friends without complex port forwarding or hosting configuration
- **Cross-Platform Play**: Enable Minecraft gameplay on devices where traditional clients cannot be installed (Chromebooks, tablets, restricted networks)
- **Demo and Testing Environments**: Create disposable Minecraft servers for mod testing or plugin development

## Dependencies for EaglerCraft Server Hosting

The Sealos template includes all required dependencies: the EaglerCraft server runtime, WebSocket proxy, and persistent storage for world data.

### Deployment Dependencies

- [EaglerCraft GitHub Repository](https://github.com/lax1dude/eaglercraft) - Original EaglerCraft project and documentation
- [EaglerCraft Server Docker Image](https://github.com/yangchuansheng/eaglercraft-server) - Containerized server implementation used in this template
- [Minecraft Wiki](https://minecraft.fandom.com/wiki/Java_Edition_1.8) - Minecraft 1.8 gameplay reference

## Implementation Details

### Architecture Components

This template deploys a single stateful service with dual WebSocket endpoints:

- **EaglerCraft Server**: Minecraft 1.8 server with dual WebSocket proxies for browser connectivity
- **WebSocket Endpoint (Port 5200)**: Standard WebSocket connection for multiplayer mode - required for adding servers via the multiplayer menu
- **WebSocket Endpoint (Port 5201)**: Enhanced WebSocket connection with persistent connection support - recommended for extended play sessions as it prevents disconnections
- **Persistent Storage**: Three dedicated 1GB volumes for Overworld, Nether, and End dimensions

**Configuration:**

The server uses a StatefulSet deployment to ensure stable network identity and persistent storage association. Both endpoints use WebSocket protocol (wss://) for secure real-time game communication. Port 5200 is designed for multiplayer server registration, while port 5201 provides a more stable connection that won't drop during long gameplay sessions.

Each Minecraft dimension (Overworld, Nether, End) receives its own persistent volume to prevent data loss and enable efficient backups. The server is allocated 200m-2000m CPU and 409Mi-4096Mi memory to handle multiple concurrent players and world generation.

**Credits（Password）:**

- **EaglerCraft and EaglerCraftX**: lax1dude (Calder Young)
- **EaglerCraft Server**: ayunami2000

**License Information:**

EaglerCraft is provided as-is under its respective license. Please review the [original repository](https://github.com/lax1dude/eaglercraft) for licensing details. This template uses a community-maintained server image.

## Why Deploy EaglerCraft Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying EaglerCraft Server on Sealos, you get:

- **One-Click Deployment**: Deploy a complete Minecraft server with persistent world storage in seconds. No server configuration, no port forwarding, no complex networking - just click and play.
- **Auto-Scaling Built-In**: Your server automatically scales resources based on player count and world complexity. Handle more players without manual intervention.
- **Easy Customization**: Adjust CPU, memory, and storage limits through intuitive forms. Scale your server resources as your player base grows.
- **Zero Kubernetes Expertise Required**: Get all the benefits of Kubernetes - high availability, automatic restarts, and persistent storage - without becoming a Kubernetes expert.
- **Persistent Storage Included**: Built-in persistent storage ensures your Minecraft worlds survive restarts, updates, and scaling events. Your players' builds are always safe.
- **Instant Public Access**: Each deployment gets automatic public URLs with SSL certificates. Share your server with players instantly - they just need the URL to connect from their browsers.
- **Automated Backups**: Automatic backups and disaster recovery ensure your world data is always protected.

Deploy EaglerCraft Server on Sealos and focus on building amazing worlds instead of managing game servers.

## Deployment Guide

1. Visit [EaglerCraft Template Page](https://sealos.io/products/app-store/eaglercraft-server)
2. Click the "Deploy Now" button
3. Wait for deployment to complete (typically 2-3 minutes)
4. Access your server via two available endpoints (shown in App Launchpad):
   - **Port 5200 URL** (wss://): `wss://[your-app-url]` - Use this for adding servers via multiplayer menu
   - **Port 5201 URL** (wss://): `wss://[your-app-url-http]` - Use this for stable, long-duration gameplay (no disconnections)

## Configuration

After deployment, you can customize your server through App Launchpad:

- **Resource Scaling**: Adjust CPU and Memory based on player count
- **Storage Expansion**: Increase storage for any world dimension if your players build extensively
- **Endpoint Selection**: Both endpoints work for gameplay, but port 5201 is recommended for extended sessions

### Connecting to Your Server

**For Multiplayer Mode (Adding Server to List):**

1. Open EaglerCraft client in your web browser
2. Go to "Multiplayer" menu
3. Click "Add Server" or "Direct Connect"
4. **Important**: Use the **Port 5200 URL** (`wss://[your-app-url]`)
5. Save and connect

**For Direct Play (Stable Connection):**

1. Open EaglerCraft client in your web browser using the **Port 5201 URL** (`https://[your-app-url-http]`)
2. This endpoint prevents disconnections during long play sessions

**Note**: Both endpoints provide full gameplay functionality. Port 5200 is required for multiplayer server registration, while port 5201 offers superior connection stability.

## Troubleshooting

### Common Issues

**Issue 1: Cannot Add Server in Multiplayer Menu**
- Cause: Using the wrong endpoint URL (port 5201 instead of port 5200)
- Solution: Make sure you use the **Port 5200 URL** (`wss://[your-app-url]`) when adding servers via the multiplayer menu. Port 5201 won't work for server registration.

**Issue 2: Frequent Disconnections During Gameplay**
- Cause: Using port 5200 for extended play sessions
- Solution: Switch to the **Port 5201 URL** (`https://[your-app-url-http]`) for stable, uninterrupted gameplay. This endpoint is optimized to prevent disconnections.

**Issue 3: Server Performance Degradation**
- Cause: Insufficient resources for player count or world complexity
- Solution: Scale up CPU and memory through App Launchpad. Monitor resource usage in the Sealos dashboard.

**Issue 4: World Data Not Persisting**
- Cause: Persistent volume claim not properly mounted
- Solution: Verify in App Launchpad that all three volume mounts are properly configured. Check deployment logs for mount errors.

### Getting Help

- [EaglerCraft Original Repository](https://github.com/lax1dude/eaglercraft)
- [Server Docker Image Issues](https://github.com/yangchuansheng/eaglercraft-server/issues)
- [Sealos Discord Community](https://discord.gg/wdUn538zVP)

## Additional Resources

- [EaglerCraft Client Access](https://eaglercraft.com/) - Play EaglerCraft in your browser
- [Minecraft 1.8 Gameplay Guide](https://minecraft.fandom.com/wiki/Java_Edition_1.8)

## License

This Sealos template is provided under MIT License. EaglerCraft itself is provided under its respective license - please review the [original repository](https://github.com/lax1dude/eaglercraft) for details.
