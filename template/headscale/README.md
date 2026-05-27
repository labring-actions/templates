# Deploy and Host Headscale on Sealos

Headscale is an open source, self-hosted implementation of the Tailscale control server. This template deploys Headscale with Headplane, persistent storage, public Ingress access, and an optional PostgreSQL database on Sealos Cloud.

![Headscale Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/headscale/website-screenshot.webp)

## About Hosting Headscale

Headscale provides the coordination server for a private Tailscale-compatible tailnet. It handles node registration, user management, route advertisement, DNS settings, ACL policy storage, and control-plane communication while your device traffic remains peer-to-peer whenever possible.

This Sealos template runs Headscale and Headplane in one StatefulSet. Headscale serves the control plane, gRPC endpoint, and metrics endpoint, while Headplane provides a web UI for managing Headscale users, machines, routes, DNS, ACLs, and pre-auth keys.

By default, the template uses SQLite stored on persistent volume storage. If `use_postgresql` is enabled during deployment, Sealos provisions a PostgreSQL 16.4.0 cluster through KubeBlocks, creates the `headscale` database, and renders the PostgreSQL settings into Headscale's `config.yaml` file because Headscale reads database configuration from its configuration file rather than database environment variables.

## Common Use Cases

- **Private Mesh VPN Control Plane**: Host your own coordination server for Tailscale-compatible clients.
- **Homelab and Team Networks**: Connect servers, laptops, and services across networks without exposing every service publicly.
- **Route and DNS Management**: Manage advertised routes, MagicDNS-style settings, and network records from Headplane.
- **ACL and Tag Administration**: Edit ACL policy settings and organize machine access for small teams or lab environments.
- **Pre-Auth Key Workflows**: Create reusable or ephemeral pre-auth keys for onboarding devices.

## Dependencies for Headscale Hosting

The Sealos template includes all required runtime components: Headscale, Headplane, persistent storage, Service/Ingress resources, RBAC for Headplane's Kubernetes integration, and optional PostgreSQL through KubeBlocks.

### Deployment Dependencies

- [Headscale Documentation](https://headscale.net/stable/) - Official Headscale documentation
- [Headscale GitHub Repository](https://github.com/juanfont/headscale) - Source code and releases
- [Headplane GitHub Repository](https://github.com/tale/headplane) - Web UI source code and documentation
- [Tailscale Documentation](https://tailscale.com/kb/) - Client and tailnet concepts
- [Sealos Documentation](https://sealos.io/docs/) - Sealos platform documentation

### Implementation Details

**Architecture Components:**

This template deploys the following services and resources:

- **Headscale**: The control server container using `headscale/headscale:0.29.0-beta.1-debug`.
- **Headplane**: The web administration UI using `ghcr.io/tale/headplane:0.6.3`.
- **SQLite Storage**: Default database mode stored at `/var/lib/headscale/db.sqlite` on a persistent volume.
- **PostgreSQL**: Optional KubeBlocks PostgreSQL 16.4.0 cluster when `use_postgresql` is enabled.
- **PostgreSQL Init Job**: Creates the `headscale` database idempotently before the app connects.
- **ConfigMap**: Stores Headscale, DERP, and Headplane configuration files.
- **Persistent Volumes**: Store Headscale data and generated configuration under `/var/lib/headscale` and `/etc/headscale`.
- **Ingress Rules**: Expose Headplane at `/admin`, Headscale HTTP traffic on the main domain, and Headscale gRPC on a dedicated gRPC domain.

**Configuration:**

- `use_postgresql` controls whether the template uses SQLite or provisions PostgreSQL.
- Headscale database settings are rendered into `/etc/headscale/config.yaml` during initialization.
- Headplane reads `/etc/headscale/headplane.yaml` and connects to Headscale at `http://127.0.0.1:8080` inside the pod.
- The StatefulSet uses `shareProcessNamespace: true` so Headplane can use its Kubernetes integration with the Headscale process.
- Headscale and Headplane each receive conservative CPU and memory limits suitable for small deployments.

**License Information:**

Headscale is licensed under the BSD-3-Clause license. Headplane is licensed under the MIT license. This Sealos template follows the license terms of the upstream projects.

## Why Deploy Headscale on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is suitable for modern applications, internal tools, SaaS platforms, and multi-service deployments. By deploying Headscale on Sealos, you get:

- **One-Click Deployment**: Deploy Headscale and Headplane from the App Store without manually writing Kubernetes YAML.
- **Optional Database Provisioning**: Use the default SQLite setup or enable PostgreSQL with KubeBlocks-managed database resources.
- **Easy Customization**: Configure parameters, resource limits, storage, and runtime settings from the Sealos UI.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed workloads, services, persistent volumes, and Ingress without managing the cluster directly.
- **Persistent Storage Included**: Keep Headscale state and configuration available across pod restarts.
- **Instant Public Access**: Sealos provisions public URLs and TLS certificates for the deployed application.
- **AI-Assisted Operations**: Use the Canvas AI dialog for post-deployment changes, or open resource cards to adjust specific resources.
- **Pay-as-You-Go Efficiency**: Start with small resources and scale only when your tailnet needs more capacity.

Deploy Headscale on Sealos and focus on managing your private network instead of operating infrastructure.

## Deployment Guide

1. Open the [Headscale template](https://sealos.io/products/app-store/headscale) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - Keep `use_postgresql` disabled for the default SQLite deployment.
   - Enable `use_postgresql` if you want Sealos to provision a PostgreSQL database for Headscale.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Access your application via the provided URLs:
   - **Headplane Admin UI**: Open the main application URL and go to `/admin`.
   - **Headscale Server URL**: Use the main application domain as the server URL for Headscale clients.
   - **Headscale gRPC Endpoint**: Use the dedicated gRPC domain when remote CLI access requires gRPC.

## Configuration

After deployment, you can configure Headscale through:

- **Headplane Admin UI**: Manage users, machines, routes, DNS settings, ACLs, and pre-auth keys at `/admin`.
- **AI Dialog**: Describe configuration changes in the Sealos Canvas and let AI apply updates.
- **Resource Cards**: Open the StatefulSet, ConfigMap, Ingress, or database resource cards for manual changes.
- **Configuration Files**: Update Headscale settings in the ConfigMap and restart the workload when needed.

## Scaling

Headscale is usually deployed as a single control-plane instance because it stores state and serves one tailnet. To adjust capacity:

1. Open the Canvas for your deployment.
2. Click the Headscale StatefulSet resource card.
3. Adjust CPU or memory resources based on node count and control-plane activity.
4. Apply the changes in the dialog.

If you enabled PostgreSQL, you can also open the PostgreSQL cluster resource card to adjust database resources and storage.

## Troubleshooting

### Common Issues

**Headplane cannot manage Headscale**

- Cause: Headplane needs access to the Headscale configuration and Kubernetes integration settings.
- Solution: Confirm the Headscale pod is ready and that the Headplane container can read `/etc/headscale/config.yaml`.

**Clients cannot register**

- Cause: The client may be using the wrong server URL or a missing pre-auth key.
- Solution: Use the Sealos-provided Headscale domain as the server URL and create a pre-auth key in Headplane.

**PostgreSQL mode does not start**

- Cause: Headscale waits for the PostgreSQL database and rendered configuration before starting.
- Solution: Check the PostgreSQL cluster, the `headscale-*-pg-init` Job, and the Headscale pod events in Canvas.

### Getting Help

- [Headscale Documentation](https://headscale.net/stable/)
- [Headscale GitHub Issues](https://github.com/juanfont/headscale/issues)
- [Headplane GitHub Issues](https://github.com/tale/headplane/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Headscale Stable Documentation](https://headscale.net/stable/)
- [Headscale GitHub Repository](https://github.com/juanfont/headscale)
- [Headplane GitHub Repository](https://github.com/tale/headplane)
- [Tailscale Knowledge Base](https://tailscale.com/kb/)
- [Sealos Documentation](https://sealos.io/docs/)

## License

This Sealos template is provided under the repository license for Sealos templates. Headscale is licensed under the BSD-3-Clause license, and Headplane is licensed under the MIT license.
