# Deploy and Host Rocket.Chat Microservices on Sealos

Rocket.Chat is an open-source team communications platform for channels, direct messages, file sharing, and integrations. This template deploys Rocket.Chat 7.9.3 with its official microservice topology, MongoDB, clustered NATS, HTTPS routing, and an optional private Sealos Object Storage bucket. Rocket.Chat documents the microservices topology as a Premium/Enterprise capability, so each deployment requires a valid Rocket.Chat entitlement or license that covers microservices.

![Rocket.Chat Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketchat-micro/website-screenshot.webp)

## About Hosting Rocket.Chat Microservices

Rocket.Chat serves the web interface and core APIs from the main application while dedicated account, authorization, presence, DDP streaming, and stream hub services process focused workloads. NATS connects these services through an internal message bus, and MongoDB stores workspace, user, room, and message data.

The template preserves the upstream 7.9.3 microservice layout: one main Rocket.Chat instance, one replica of each of the five microservices, and two NATS replicas protected by pod anti-affinity and a disruption budget. Sealos provisions internal service discovery, startup coordination, WebSocket routing, and a generated public HTTPS endpoint.

File uploads use MongoDB GridFS by default. The optional S3 mode creates a private Sealos Object Storage bucket and configures Rocket.Chat to proxy protected files through the authenticated application endpoint.

## Common Use Cases

- **Private team chat**: Run channels, direct messages, threads, and file sharing in a self-hosted workspace.
- **Customer and community collaboration**: Organize public or private rooms for support, projects, and user communities.
- **Integration hub**: Connect bots, webhooks, and external services to Rocket.Chat APIs.
- **Microservice operations**: Scale account, authorization, presence, DDP, and stream processing workloads independently.
- **Controlled file storage**: Keep uploads in MongoDB GridFS or a private S3-compatible bucket managed by Sealos.

## Dependencies for Rocket.Chat Microservices Hosting

The Sealos template includes the complete runtime stack:

- **Rocket.Chat main application**: `rocketchat/rocket.chat:7.9.3`
- **Rocket.Chat entitlement/license**: An active Premium/Enterprise entitlement that covers the official microservices capability; Rocket.Chat manages eligibility and activation
- **Account service**: `rocketchat/account-service:7.9.3`
- **Authorization service**: `rocketchat/authorization-service:7.9.3`
- **DDP streamer service**: `rocketchat/ddp-streamer-service:7.9.3`
- **Presence service**: `rocketchat/presence-service:7.9.3`
- **Stream hub service**: `rocketchat/stream-hub-service:7.9.3`
- **NATS cluster**: Two `nats:2.4.0-alpine` replicas with config reloaders; the minimal profile uses the built-in monitor endpoint on port `8222` and keeps NATS exporter and nats-box disabled
- **MongoDB**: KubeBlocks-managed MongoDB 8.0.4 with persistent storage
- **Object storage**: Optional private Sealos Object Storage bucket for file uploads
- **Public access**: HTTPS ingress plus dedicated WebSocket routes for `/sockjs` and `/websocket`

### Deployment Dependencies

- [Rocket.Chat Official Website](https://www.rocket.chat/) - Product information
- [Rocket.Chat Microservices Documentation](https://docs.rocket.chat/docs/microservices) - Architecture and service roles
- [Rocket.Chat Kubernetes Deployment Guide](https://docs.rocket.chat/docs/deploy-with-kubernetes) - Official Kubernetes guidance
- [Rocket.Chat File Upload Documentation](https://docs.rocket.chat/docs/file-upload) - Storage backend settings
- [Rocket.Chat GitHub Repository](https://github.com/RocketChat/Rocket.Chat) - Source code and releases
- [Sealos Documentation](https://sealos.io/docs) - Platform deployment and operations guides

### Implementation Details

**Architecture Components:**

- **Main Deployment**: Serves the web UI, REST APIs, administration, and core workspace functions on port `3000`.
- **Five Microservice Deployments**: Handle account, authorization, DDP streaming, presence, and stream hub workloads.
- **NATS StatefulSet**: Runs two replicas with stable identities, a per-pod 1Gi runtime PVC, pod anti-affinity, and a `minAvailable: 1` disruption budget. An init container removes stale PID state before NATS starts.
- **MongoDB Cluster**: Stores Rocket.Chat application data and the oplog used for real-time updates.
- **Startup Coordination**: Init containers wait for the MongoDB primary, NATS, and the Rocket.Chat migration lock before services accept traffic.
- **Service and Ingress Resources**: Route HTTP traffic to the main application and long-lived WebSocket traffic to the DDP streamer.
- **Optional ObjectStorageBucket**: Creates a private S3-compatible bucket and injects Sealos-managed credentials into Rocket.Chat.

**Storage Modes:**

| Mode | Deployment input | Behavior |
| --- | --- | --- |
| MongoDB GridFS | `enable_s3_storage=false` | Stores uploads in MongoDB and serves protected files through Rocket.Chat. |
| Sealos Object Storage | `enable_s3_storage=true` | Creates a private bucket, stores uploads in S3, and proxies authenticated downloads through Rocket.Chat. |

Choose the storage mode during deployment and keep that backend consistent for the workspace lifecycle.

**Tested Resource Baseline:**

| Workload | Replicas | Per-container limit |
| --- | ---: | --- |
| Rocket.Chat main | 1 | `200m` CPU, `1024Mi` memory |
| Account, authorization, DDP, presence, stream hub | 1 each | `100m` CPU, `128Mi` memory |
| NATS server | 2 | `100m` CPU, `128Mi` memory |
| NATS config reloader | 2 | `100m` CPU, `128Mi` memory |
| NATS runtime init container | 2 | `100m` CPU, `128Mi` memory |
| Startup init container | Per Rocket.Chat pod | `100m` CPU, `128Mi` memory |
| MongoDB | 1 | `500m` CPU, `512Mi` memory |

The `100m` main CPU tier crossed the five-minute startup probe budget during a repeated cold start. The `512Mi` main memory tier reached the Node.js heap limit. The template therefore uses `200m` CPU and `1024Mi` memory for repeatable startup.

**License Information:**

Rocket.Chat source outside the upstream `apps/meteor/ee/` and `ee/` directories is distributed under the MIT License. Enterprise Edition directories follow the separate license included in the Rocket.Chat repository.

Source-code licensing and the Premium/Enterprise product entitlement are separate requirements. The official microservices capability requires the applicable Rocket.Chat entitlement.

## Why Deploy Rocket.Chat Microservices on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes. It brings application deployment, networking, storage, and day-two operations into one workspace.

- **One-click topology deployment**: Launch Rocket.Chat, five microservices, MongoDB, NATS, ingress, and storage from one template.
- **Kubernetes service orchestration**: Keep service discovery, probes, pod placement, and disruption controls in a managed runtime.
- **Private S3 option**: Provision a private bucket and application credentials through one deployment choice.
- **Instant HTTPS access**: Receive a generated domain and TLS endpoint for the workspace.
- **Canvas and AI operations**: Update resources from Canvas cards or describe the desired change in the AI dialog.
- **Purpose-scoped persistent storage**: Store workspace data in MongoDB and give each NATS pod a 1Gi runtime PVC shared by the server and reloader. The NATS init container clears stale PID state on startup.
- **Pay-as-you-go resources**: Start from the tested baseline and increase capacity as workspace usage grows.

## Deployment Guide

1. Open the [Rocket.Chat Microservices template](https://sealos.io/products/app-store/rocketchat-micro) and click **Deploy Now**.
2. Confirm that your Rocket.Chat organization has an active Premium/Enterprise entitlement or license covering microservices.
3. Choose the file storage mode in the popup dialog:
   - Keep **Enable S3 storage** disabled for MongoDB GridFS.
   - Enable **Enable S3 storage** to provision a private Sealos Object Storage bucket.
4. Start the deployment. Sealos usually creates the resources in 2-3 minutes; the first MongoDB migration and all microservice readiness checks can take several additional minutes.
5. Wait until the main application, five microservices, MongoDB, and both NATS pods show a healthy state in Canvas.
6. Open the generated Rocket.Chat HTTPS URL from the application resource.

## First Login and Workspace Registration

Keep the entitled Rocket.Chat organization or account and a valid administrator email available during registration. Rocket.Chat Cloud uses the workspace registration flow to associate the deployment and maintain its entitlement and license updates.

The first browser visit opens Rocket.Chat's four-step setup wizard:

1. Enter the initial administrator's full name, username, email address, and a strong password.
2. Enter the organization name, industry, size, and country.
3. Register the workspace with a valid administrator email, accept the Rocket.Chat terms, and open the confirmation message sent by Rocket.Chat Cloud.
4. Confirm that the security code in the browser matches the email, then finish the wizard and enter the workspace home page.

The first account receives administrator and owner permissions. Later sessions use the same username or email and password from the generated Rocket.Chat URL. Add more users from **Administration > Workspace > Users** or through workspace invitations.

Workspace registration connects the instance to Rocket.Chat Cloud for entitlement recognition, license updates, and security notifications. Keep access to the administrator email during initial setup and use **Resend** or **Change email** from the confirmation page when required. The Premium/Enterprise microservices entitlement comes from the Rocket.Chat organization or subscription associated with the deployment.

## Configuration

After deployment, manage Rocket.Chat through these surfaces:

- **Rocket.Chat Administration**: Configure accounts, permissions, authentication, integrations, email, and file upload policies.
- **Canvas AI Dialog**: Describe resource, environment, or networking changes for Sealos to apply.
- **Canvas Resource Cards**: Edit each Deployment, StatefulSet, MongoDB Cluster, Service, Ingress, PVC, or bucket.
- **Deployment Input**: `enable_s3_storage` selects GridFS or private S3 storage during deployment.

In S3 mode, the bucket remains private and Rocket.Chat proxies protected uploads. Sealos-generated access keys stay in Kubernetes Secrets referenced by the application pods.

## Scaling

1. Open the Rocket.Chat deployment in Canvas.
2. Select the main application or a dedicated microservice resource card.
3. Increase CPU, memory, or replicas for the workload receiving pressure.
4. Keep at least two NATS replicas and preserve the disruption budget for broker availability.
5. Expand MongoDB and persistent volume capacity as message and file data grows.

Review Rocket.Chat's microservice documentation before changing service replica ratios. DDP streaming, presence, and authorization traffic can scale independently as concurrency increases.

## Troubleshooting

### Common Issues

**The setup wizard is still loading after deployment**

- MongoDB migrations and microservice startup checks are still converging.
- Confirm that MongoDB, both NATS pods, the main application, and all five microservices are healthy in Canvas.

**Workspace registration is waiting for confirmation**

- Use an administrator email that can receive the Rocket.Chat Cloud message.
- Compare the displayed security code with the email, or use **Resend** and **Change email** on the confirmation page.

**S3 uploads fail**

- Confirm that `enable_s3_storage=true` was selected for the deployment.
- Check that the ObjectStorageBucket is ready and the Sealos object storage Secrets exist in the workspace.
- Keep the Rocket.Chat S3 proxy and protected-file settings enabled for authenticated downloads.

**The main application restarts during cold start**

- Keep the tested `200m` CPU and `1024Mi` memory limits as the minimum baseline.
- Increase the main Deployment resources for larger workspaces, imports, or concurrent users.

**Messages reconnect repeatedly**

- Check the main HTTP ingress and the dedicated `/sockjs` and `/websocket` ingress routes.
- Confirm that the DDP streamer and both NATS replicas are ready.

### Getting Help

- [Rocket.Chat Documentation](https://docs.rocket.chat/)
- [Rocket.Chat GitHub Issues](https://github.com/RocketChat/Rocket.Chat/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Rocket.Chat Administration Guide](https://docs.rocket.chat/docs/administration)
- [Rocket.Chat Environment Variable Settings](https://docs.rocket.chat/docs/manage-settings-using-environmental-variables)
- [Rocket.Chat File Upload Recommendations](https://docs.rocket.chat/docs/recommendations-for-file-upload)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template follows the license of the templates repository. Rocket.Chat's community source uses the MIT License, while upstream Enterprise Edition directories use their included EE license.
