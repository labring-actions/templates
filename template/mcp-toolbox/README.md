# Deploy and Host MCP Toolbox for Databases on Sealos

MCP Toolbox for Databases is an open source Model Context Protocol server for database tools. This template deploys the official Toolbox server with KubeBlocks PostgreSQL on Sealos Cloud.

![MCP Toolbox Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mcp-toolbox/website-screenshot.webp)

## About Hosting MCP Toolbox for Databases

MCP Toolbox connects AI agents, IDEs, and applications to databases through Model Context Protocol tools. This template starts the official Toolbox container with the PostgreSQL prebuilt configuration and provisions a PostgreSQL database for immediate exploration.

The exposed endpoint is an MCP server endpoint for compatible clients. Connect Codex, Claude Code, Gemini CLI, or another MCP client to the generated Sealos URL.

## Common Use Cases

- **Agent database access**: Let AI agents inspect schemas and execute controlled SQL.
- **IDE database tooling**: Connect MCP-compatible IDEs to PostgreSQL tools.
- **Tooling prototype**: Validate MCP database workflows before connecting production databases.
- **Schema exploration**: Use prebuilt PostgreSQL tools such as table listing and database overview.

## Dependencies for MCP Toolbox Hosting

The Sealos template includes MCP Toolbox and KubeBlocks PostgreSQL.

### Deployment Dependencies

- [MCP Toolbox Documentation](https://mcp-toolbox.dev/) - Official documentation
- [Docker Deployment Guide](https://mcp-toolbox.dev/documentation/deploy-to/docker/) - Official Docker deployment
- [PostgreSQL Prebuilt Configuration](https://mcp-toolbox.dev/integrations/postgres/prebuilt-configs/postgresql/) - Available tools and environment variables
- [GitHub Repository](https://github.com/googleapis/mcp-toolbox) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Toolbox server**: Official `us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:1.5.0` image
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4 cluster with a `toolbox_db` database
- **Ingress**: Public HTTPS endpoint for MCP clients and SDKs

**Configuration:**

The template passes the PostgreSQL connection through official `POSTGRES_*` environment variables and starts Toolbox with `--prebuilt=postgres`, `--address=0.0.0.0`, and `--port=5000`.

**License Information:**

MCP Toolbox for Databases is licensed under Apache License 2.0.

## Why Deploy MCP Toolbox for Databases on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and lifecycle management. By deploying MCP Toolbox on Sealos, you get:

- **One-Click Deployment**: Launch Toolbox and PostgreSQL from the App Store template.
- **Managed Database**: KubeBlocks provisions PostgreSQL for immediate MCP testing.
- **Instant Public Access**: Each deployment gets a generated HTTPS endpoint.
- **Easy Customization**: Adjust resources and environment variables from the Sealos dashboard.
- **Agent-Ready Runtime**: Connect MCP-compatible tools directly to the public endpoint.

## Deployment Guide

1. Open the [MCP Toolbox template](https://sealos.io/products/app-store/mcp-toolbox) and click **Deploy Now**.
2. Review the generated host and application name, then deploy.
3. Wait for deployment to complete. The PostgreSQL database is created before Toolbox starts.
4. Connect your MCP client or SDK to the generated public URL, for example `https://[your-app-url]`.

## Configuration

Use your MCP client configuration to point at the generated Sealos URL. For SDK usage, initialize the Toolbox client with the same URL.

## Scaling

To scale Toolbox, open the Canvas for your deployment, click the Deployment resource card, adjust CPU, memory, or replicas, and apply the change.

## Troubleshooting

### MCP Client Cannot Connect

- Cause: The client is using a local URL or the deployment is still starting.
- Solution: Use the generated Sealos HTTPS URL and wait until the Toolbox pod is ready.

### PostgreSQL Tool Calls Fail

- Cause: The database is empty or the query requires permissions beyond the default connection.
- Solution: Create tables or connect Toolbox to your target database through an updated source configuration.

## Additional Resources

- [Prebuilt Tools Reference](https://mcp-toolbox.dev/documentation/configuration/prebuilt-configs/)
- [PostgreSQL Source Reference](https://mcp-toolbox.dev/integrations/postgres/source/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## License

This Sealos template is provided under the repository license. MCP Toolbox for Databases itself is licensed under Apache License 2.0.
