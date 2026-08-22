# Deploy and Host MockServer on Sealos

MockServer is an open-source HTTP(S) mock server, proxy, recorder, and request inspection tool. This template deploys MockServer as a single non-root container with an HTTPS ingress on Sealos Cloud.

![MockServer Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mockserver/website-screenshot.webp)

## About Hosting MockServer

MockServer lets teams create API expectations, validate requests, proxy traffic, record interactions, and inspect logs from one service. It listens on port 1080 and serves HTTP, HTTPS, proxy, dashboard, and API traffic through the same endpoint.

This Sealos template deploys the official MockServer Docker image with Kubernetes probes and a public HTTPS URL. No database is required for the default in-memory mode.

## Common Use Cases

- **API Mocking**: Create predictable responses for frontend, integration, and contract tests.
- **Traffic Recording**: Capture real API interactions and replay them during development.
- **Proxy Debugging**: Forward requests while inspecting payloads and headers.
- **MCP Testing**: Expose MockServer's MCP endpoint for agent-based testing workflows.

## Dependencies for MockServer Hosting

The Sealos template includes the official MockServer container image, service, ingress, and health probes.

### Deployment Dependencies

- [Official Website](https://www.mock-server.com/) - Product documentation and guides
- [Running MockServer](https://www.mock-server.com/mock_server/running_mock_server.html) - Docker, Helm, and CLI usage
- [GitHub Repository](https://github.com/mock-server/mockserver-monorepo) - Source code and release process

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **MockServer**: Official non-root Java 17 distroless container on port 1080
- **Service**: Internal Kubernetes service for HTTP traffic
- **Ingress**: Sealos HTTPS endpoint for dashboard and API access

**Configuration:**

- The container uses `SERVER_PORT=1080` and `MOCKSERVER_SERVER_PORT=1080`.
- The App URL opens `/mockserver/dashboard`.
- Health probes use MockServer's documented readiness and liveness endpoints.
- MockServer has no built-in login for the default deployment.

**License Information:**

MockServer is licensed under the Apache License 2.0. This Sealos template is provided under the repository license.

## Why Deploy MockServer on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that handles deployment, networking, resource management, and operations from one workspace. By deploying MockServer on Sealos, you get:

- **One-Click Deployment**: Launch a ready-to-use mock API service from the App Store.
- **Instant HTTPS Endpoint**: Share a secure MockServer URL with clients, tests, and teammates.
- **Kubernetes-Based Reliability**: Readiness and liveness probes keep the service observable.
- **Easy Customization**: Adjust resource limits, environment variables, and startup flags from Canvas.
- **AI Ops Workflow**: Describe changes in the AI dialog and let Sealos apply them to resources.
- **Pay-as-You-Go Runtime**: Run MockServer only for the environments that need it.

## Deployment Guide

1. Open the [MockServer template](https://sealos.io/products/app-store/mockserver) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your deployment through the provided URL:
   - **Dashboard**: Open `/mockserver/dashboard`
   - **Status API**: Send `PUT /mockserver/status`
   - **MCP Endpoint**: Use `/mockserver/mcp` when MCP is enabled in your workflow

## Configuration

After deployment, you can configure MockServer through:

- **REST API**: Create, retrieve, verify, and clear expectations.
- **Dashboard**: Inspect requests, logs, and active expectations.
- **AI Dialog**: Add environment variables or command-line options.
- **Resource Cards**: Tune CPU and memory from the Canvas.

## Scaling

The default template runs one in-memory MockServer instance. Keep one replica for deterministic expectation state, or add an external persistence or clustered setup before scaling horizontally.

## Troubleshooting

### Status API Fails

- Cause: MockServer may still be starting, or the request method may be wrong.
- Solution: Use `PUT /mockserver/status` and wait until the deployment is Ready in Canvas.

### Expectations Disappear After Restart

- Cause: The default deployment stores expectations in memory.
- Solution: Configure initialization or persistence files through a custom resource update when durable expectations are required.

## Additional Resources

- [MockServer Dashboard](https://www.mock-server.com/mock_server/mockserver_ui.html)
- [Configuration Properties](https://www.mock-server.com/mock_server/configuration_properties.html)
- [Docker Documentation](https://www.mock-server.com/where/docker.html)

## License

This Sealos template is provided under the repository license. MockServer is licensed under the Apache License 2.0.
