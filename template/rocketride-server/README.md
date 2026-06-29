# Deploy and Host RocketRide Server on Sealos

RocketRide Server is the runtime engine for open source AI development workflows and portable pipeline execution. This template deploys the official RocketRide engine container with an HTTPS endpoint on Sealos Cloud.

![RocketRide Server Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketride-server/website-screenshot.webp)

## About Hosting RocketRide Server

RocketRide turns AI and data pipelines into portable runtime processes that can be designed in an IDE and executed on your own infrastructure. The server exposes the engine over HTTP so clients, SDKs, and development tooling can connect to a shared runtime.

This Sealos template deploys the official `ghcr.io/rocketride-org/rocketride-engine` image with a managed KubeBlocks PostgreSQL database and pgvector extension. Sealos provides the HTTPS ingress, resource management, and lifecycle controls from the Canvas.

## Common Use Cases

- **AI Pipeline Runtime**: Run RocketRide pipelines on a managed cloud endpoint.
- **IDE-Backed Development**: Connect local IDE workflows to a hosted runtime.
- **SDK Integration**: Use Python or TypeScript clients against a stable server URL.
- **Internal AI Services**: Host a backend runtime for team experiments and prototypes.

## Dependencies for RocketRide Server Hosting

The Sealos template includes the official RocketRide engine image, KubeBlocks PostgreSQL with pgvector, service, ingress, and health probes.

### Deployment Dependencies

- [RocketRide Website](https://rocketride.org/) - Product overview and ecosystem links
- [RocketRide Documentation](https://docs.rocketride.org/) - Quickstart, protocol, and SDK guidance
- [GitHub Repository](https://github.com/rocketride-org/rocketride-server) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **RocketRide Engine**: Official runtime container listening on port 5565
- **PostgreSQL**: KubeBlocks PostgreSQL database with pgvector enabled for the engine runtime
- **Service**: Kubernetes service for internal HTTP routing
- **Ingress**: Sealos HTTPS endpoint for external access

**Configuration:**

- The official image entrypoint starts `./engine ./ai/eaas.py --host=0.0.0.0`.
- `POSTGRES_URL` is generated from the KubeBlocks PostgreSQL connection secret.
- The database init Job creates the `rocketride` database and enables the `vector` extension.
- `ROCKETRIDE_APIKEY` is generated during deployment and used by RocketRide clients.
- Health probes use the image's public `/version` endpoint.
- The App URL points to `/version` so first access confirms the runtime is available.
- RocketRide Server has no built-in web login in this runtime template.

**License Information:**

RocketRide Server is licensed under the MIT License. This Sealos template is provided under the repository license.

## Why Deploy RocketRide Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes for deploying, operating, and scaling applications. By deploying RocketRide Server on Sealos, you get:

- **One-Click Deployment**: Start the runtime from the App Store with a generated HTTPS URL.
- **Cloud-Native Operations**: Manage probes, resources, ingress, and logs in one Canvas.
- **Easy SDK Access**: Connect local tools or SDKs to the Sealos endpoint.
- **AI Ops Workflow**: Describe runtime changes in the AI dialog and let Sealos apply them.
- **Resource Efficiency**: Start with a small runtime and tune CPU or memory as workloads grow.

## Deployment Guide

1. Open the [RocketRide Server template](https://sealos.io/products/app-store/rocketride-server) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access the runtime through the provided URL:
   - **Health Check**: Open `/version`
   - **Runtime API**: Use the same host with RocketRide clients and SDKs, and pass the generated `ROCKETRIDE_APIKEY`

## Configuration

After deployment, you can configure RocketRide Server through:

- **AI Dialog**: Add environment variables or adjust runtime settings.
- **Resource Cards**: Tune CPU, memory, and replica settings from the Canvas.
- **Client Configuration**: Point IDE tooling or SDK clients at the generated Sealos HTTPS URL.

## Scaling

Start with one runtime instance while validating pipeline behavior. Increase CPU and memory before increasing replicas, because pipeline runtime state and client coordination should be reviewed for each workload.

## Troubleshooting

### `/ping` Does Not Respond

- Cause: `/ping` is part of the authenticated runtime API.
- Solution: Use `/version` for unauthenticated health checks and use RocketRide clients with the generated API key for runtime calls.

### Client Cannot Connect

- Cause: The client may be using an internal URL, HTTP scheme, or wrong path.
- Solution: Use the generated Sealos HTTPS host and confirm `/ping` succeeds first.

## Additional Resources

- [Quickstart](https://docs.rocketride.org/quickstart)
- [Self-Hosting](https://docs.rocketride.org/self-hosting)
- [RocketRide Releases](https://github.com/rocketride-org/rocketride-server/releases)

## License

This Sealos template is provided under the repository license. RocketRide Server is licensed under the MIT License.
