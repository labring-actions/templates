# Deploy and Host Nakama Server on Sealos

Nakama is an open-source game server for real-time multiplayer, social features, and live ops. This template deploys a production-ready Nakama server with PostgreSQL database on Sealos Cloud.

## About Hosting Nakama

Nakama is a distributed game server designed for modern multiplayer games and social applications. It provides real-time communication, user authentication, leaderboard management, achievement systems, and match-making capabilities out of the box. The Sealos template automatically provisions PostgreSQL for persistent data storage and configures Nakama with secure encryption keys for session management and runtime execution.

The deployment includes automatic SSL certificate provisioning, domain management, and integrated monitoring through the Sealos dashboard. All security credentials (session encryption keys, runtime keys, console signing keys) are automatically generated during deployment.

## Common Use Cases

- **Real-time Multiplayer Games**: Build synchronous multiplayer games with WebSocket-based real-time communication
- **Social Features**: Implement chat, friend lists, groups, and social interactions
- **Leaderboards and Rankings**: Create global or grouped leaderboards for competitive games
- **User Authentication**: Handle player accounts, device authentication, and social login integration
- **Live Game Operations**: Manage game configurations, tournaments, and events through the admin console

## Dependencies for Nakama Hosting

The Sealos template includes all required dependencies: Nakama server runtime and PostgreSQL database.

### Deployment Dependencies

- [Official Nakama Documentation](https://heroiclabs.com/docs/nakama/) - Comprehensive documentation and guides
- [Nakama GitHub Repository](https://github.com/heroiclabs/nakama) - Source code and community contributions
- [Nakama Console Guide](https://heroiclabs.com/docs/nakama/getting-started/install/console/) - Admin console documentation
- [Nakama Discord](https://discord.gg/8DkBAUCm4Y) - Community support and discussions

### Implementation Details

**Architecture Components:**

This template deploys two main services:

- **Nakama Server**: The core game server handling real-time connections, authentication, and game logic
- **PostgreSQL Database**: PostgreSQL 16.4.0 for persistent storage of user data, game state, and configurations

**Configuration:**

Nakama runs as a StatefulSet with three init containers that ensure proper initialization:

1. **init-modules-dir**: Creates the necessary directory structure for Lua/Go runtime modules
2. **wait-for-postgres**: Waits for PostgreSQL to be ready and verifies the database exists
3. **migrate**: Runs database migrations to set up the required schema

The server is configured with multiple ports:
- **7350**: HTTP API for REST requests
- **7349**: gRPC server for high-performance client connections
- **7348**: Admin console gRPC interface
- **7351**: Metrics endpoint for monitoring

**Optional gRPC Exposure:**

By default, gRPC ports (7348/7349) are only accessible within the cluster. You can enable public gRPC access by setting `enable_grpc` to `true` during deployment, which will create public Ingress routes for both gRPC and console gRPC endpoints.

**Security:**

All sensitive credentials are automatically generated:
- Session encryption keys for secure user sessions
- Runtime HTTP key for server-side code execution
- Console signing key and MFA encryption key for admin authentication
- Server key for socket connections

You can override the default admin console username and set your own password during deployment.

**License Information:**

Nakama is licensed under Apache-2.0. See the [Nakama GitHub repository](https://github.com/heroiclabs/nakama) for details.

## Why Deploy Nakama on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern multiplayer games and real-time applications. By deploying Nakama on Sealos, you get:

- **One-Click Deployment**: Deploy complex game server infrastructure with a single click. No YAML configuration, no database setup - just point, click, and deploy.
- **Auto-Scaling Built-In**: Your game server automatically scales based on player demand. Handle traffic spikes from game launches or events without manual intervention.
- **Easy Customization**: Configure environment variables, resource limits, and credentials with intuitive forms. Customize your Nakama setup without touching configuration files.
- **Zero Kubernetes Expertise Required**: Get all the benefits of Kubernetes - high availability, service discovery, and container orchestration - without becoming a Kubernetes expert.
- **Persistent Storage Included**: Built-in PostgreSQL with persistent storage ensures your player data, game state, and configurations are safe across deployments.
- **Instant Public Access**: Each deployment gets automatic public URLs with SSL certificates for HTTP and optional gRPC endpoints. Connect your game clients immediately.
- **Automated Backups**: Automatic database backups ensure your game data and player progress are always safe.

Deploy Nakama on Sealos and focus on building great games instead of managing infrastructure.

## Deployment Guide

1. Visit [Nakama Template Page](https://sealos.io/products/app-store/nakama)
2. Click the "Deploy Now" button
3. Configure the parameters in the popup dialog:
   - **Console Username**: Admin username for Nakama Console (default: admin)
   - **Console Password**: Set a secure password for initial console login
   - **Enable gRPC**: Check this to expose gRPC ports publicly (optional)
4. Wait for deployment to complete (typically 2-3 minutes)
5. Access your Nakama server via the provided URLs:
   - **Nakama Console**: Use your configured username and password
   - **HTTP API**: For REST client connections
   - **gRPC**: If enabled, for high-performance client connections

## Configuration

After deployment, you can manage Nakama through:

- **Nakama Console**: Access at the console URL provided in your deployment dashboard
- **Environment Variables**: Modify server settings in the App Launchpad by editing the deployment
- **Runtime Modules**: Upload custom Lua or Go modules to extend Nakama functionality

### Accessing the Console

1. Navigate to your deployed application in Sealos
2. Click on the provided URL to access the Nakama Console
3. Log in with your configured username and password
4. Use the console to manage users, view leaderboards, and configure game settings

### gRPC Configuration

If you enabled gRPC during deployment, you'll receive separate URLs for:
- **Nakama gRPC**: For client connections (port 7349)
- **Console gRPC**: For admin console communication (port 7348)

Use these URLs in your game client configuration to connect to Nakama via gRPC for optimal performance.

## Scaling

To scale your Nakama deployment:

1. Open App Launchpad in Sealos
2. Select your Nakama deployment
3. Adjust CPU/Memory resources based on your player count
4. For horizontal scaling, you can run multiple Nakama instances behind a load balancer (advanced configuration)

**Resource Guidelines:**
- **Small games** (< 100 concurrent players): 100m CPU, 256Mi memory
- **Medium games** (100-1000 concurrent players): 500m CPU, 512Mi memory
- **Large games** (> 1000 concurrent players): 1000m CPU, 1Gi memory or more

## Troubleshooting

### Common Issues

**Issue: Database connection failed**
- Cause: PostgreSQL is still initializing
- Solution: Wait 2-3 minutes for the database to fully start. The init container will automatically wait for the database to be ready.

**Issue: Cannot access Nakama Console**
- Cause: Console URL not correctly configured or password incorrect
- Solution: Verify your console username and password in the deployment configuration. Use the credentials you set during deployment.

**Issue: gRPC connection fails**
- Cause: gRPC ports not enabled or firewall blocking connections
- Solution: Ensure you enabled "Expose gRPC ports" during deployment if you need public gRPC access. Check your game client configuration for the correct endpoint URL.

**Issue: High memory usage**
- Cause: Large number of concurrent players or runtime modules consuming resources
- Solution: Increase memory limits in the App Launchpad or optimize your runtime modules

### Getting Help

- [Nakama Documentation](https://heroiclabs.com/docs/nakama/)
- [Nakama GitHub Issues](https://github.com/heroiclabs/nakama/issues)
- [Sealos Documentation](https://sealos.io/docs/)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [Nakama Developer Guide](https://heroiclabs.com/docs/nakama/getting-started/) - Quick start and development guides
- [Nakama Client SDKs](https://heroiclabs.com/docs/nakama/client-libraries/) - Official SDKs for Unity, Godot, JavaScript, and more
- [Nakama Runtime Code](https://heroiclabs.com/docs/nakama/getting-started/runtime/) - Custom server-side logic with Lua and Go
- [Nakama Tutorials](https://heroiclabs.com/docs/nakama/category-tutorials/) - Step-by-step tutorials for common features

## License

This Sealos template is provided under Apache-2.0. Nakama itself is licensed under Apache-2.0.
