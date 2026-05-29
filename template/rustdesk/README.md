# Deploy and Host RustDesk Server on Sealos

RustDesk Server provides the self-hosted ID/rendezvous and relay services used by RustDesk clients. This template deploys the RustDesk Server S6 image with persistent key storage, NodePort exposure for client traffic, and a Sealos App entry that points to the regional TCP gateway.

## About Hosting RustDesk Server

RustDesk Server runs the `hbbs` rendezvous service and the `hbbr` relay service in one StatefulSet. The template stores the server key pair and lightweight SQLite metadata under `/data`, so the public key remains stable across restarts.

This deployment is not a web dashboard and does not require browser login or account registration. Users connect from the RustDesk desktop or mobile client by entering the Sealos TCP gateway host, the allocated NodePort values, and, when encryption is enabled, the public key printed in the pod logs.

## Common Use Cases

- **Private Remote Desktop Relay**: Route RustDesk remote desktop sessions through infrastructure you control.
- **Team Support Gateway**: Provide a shared ID and relay server for support engineers and managed devices.
- **Encrypted Client Access**: Require RustDesk clients to use the server public key by setting `ENCRYPTED_ONLY` to `1`.
- **Portable Lab Environments**: Run an isolated relay for testing remote access workflows without maintaining your own Kubernetes manifests.

## Dependencies for RustDesk Server Hosting

The Sealos template includes all required runtime resources: a RustDesk Server S6 container, persistent storage for `/data`, a NodePort Service for RustDesk client ports, and a Sealos App link for the TCP gateway host.

### Deployment Dependencies

- [RustDesk Server GitHub Repository](https://github.com/rustdesk/rustdesk-server) - Server source code and release notes
- [RustDesk Documentation](https://rustdesk.com/docs/) - RustDesk client and self-hosting documentation
- [RustDesk Server Docker Hub](https://hub.docker.com/r/rustdesk/rustdesk-server-s6) - Container image used by this template
- [Sealos App Store](https://sealos.io/products/app-store/rustdesk) - One-click deployment entry

## Implementation Details

**Architecture Components:**

This template deploys one stateful service:

- **RustDesk Server**: Runs `hbbs` for ID/rendezvous traffic and `hbbr` for relay traffic.
- **Persistent Volume**: Stores `/data`, including the generated `id_ed25519` key pair and RustDesk server metadata.
- **NodePort Service**: Exposes RustDesk client ports `21115/tcp`, `21116/tcp`, `21116/udp`, and `21117/tcp` through the Sealos TCP gateway.
- **Sealos App Link**: Shows the gateway host `tcp.${{ SEALOS_CLOUD_DOMAIN }}` in Canvas.

**Configuration:**

- `ENCRYPTED_ONLY=1` requires clients to configure the server public key. This is the recommended setting.
- `ENCRYPTED_ONLY=0` allows clients to connect without the server public key, which is easier for quick tests but less restrictive.
- The `RELAY` environment variable is set from the generated Sealos host so `hbbs` advertises the correct relay address.
- The template uses the pinned image `rustdesk/rustdesk-server-s6:1.1.15`, matching the latest RustDesk Server release stream available for the S6 server image.

**Resource Profile:**

Live Sealos testing verified the service with `1m` CPU / `5Mi` memory requests and `20m` CPU / `24Mi` memory limits while both `hbbs` and `hbbr` stayed healthy. Increase resources from Canvas if you expect many concurrent remote desktop sessions or sustained relay bandwidth.

**License Information:**

RustDesk Server is licensed under AGPL-3.0. This Sealos template is provided as deployment automation for RustDesk Server.

## Why Deploy RustDesk Server on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, public access, storage, and day-2 operations. By deploying RustDesk Server on Sealos, you get:

- **One-Click Deployment**: Deploy RustDesk Server from the App Store without writing Kubernetes YAML.
- **Persistent Key Storage**: Keep the generated RustDesk server key pair stable across restarts.
- **Instant TCP Gateway Access**: Use the Sealos regional TCP gateway and allocated NodePorts for RustDesk clients.
- **Easy Customization**: Adjust encryption mode, resources, and storage through Canvas and AI-assisted operations.
- **Pay-as-You-Go Efficiency**: Start with a minimal resource profile and scale only when your relay traffic needs it.
- **Kubernetes Foundation**: Run RustDesk Server on managed Kubernetes primitives without managing cluster internals.

## Deployment Guide

1. Open the [RustDesk template](https://sealos.io/products/app-store/rustdesk) and click **Deploy Now**.
2. Configure `ENCRYPTED_ONLY` in the popup dialog. Use `1` for encrypted-only access with a public key, or `0` for less restrictive test deployments.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Open the RustDesk Server pod logs and copy the line that starts with `Key:`. This is required when `ENCRYPTED_ONLY=1`.
5. Open the Service resource in Canvas and note the allocated NodePort values for:
   - **ID Server**: `rendezvous-tcp` / `rendezvous-udp` on port `21116`
   - **Relay Server**: `relay` on port `21117`
   - **NAT Test**: `heartbeat` on port `21115`
6. In your RustDesk client, open **Settings → Network → ID/Relay Server** and enter:
   - **ID Server**: `tcp.${{ SEALOS_CLOUD_DOMAIN }}:<rendezvous-nodeport>`
   - **Relay Server**: `tcp.${{ SEALOS_CLOUD_DOMAIN }}:<relay-nodeport>`
   - **API Server**: leave blank unless you run a separate RustDesk API service
   - **Key**: paste the pod log key when `ENCRYPTED_ONLY=1`
7. Save the settings. The RustDesk client status should become ready after it reaches the self-hosted ID server.

## Configuration

After deployment, you can configure RustDesk Server through:

- **AI Dialog**: Describe resource or environment changes and let Sealos apply updates.
- **Resource Cards**: Click the StatefulSet, Service, or storage cards in Canvas to inspect and modify settings.
- **RustDesk Client Settings**: Configure client-side ID server, relay server, and key values.

There is no built-in RustDesk Server web login in this template. Access is controlled by the RustDesk client configuration and, when enabled, the server public key.

## Scaling

To scale resources for heavier relay traffic:

1. Open the Canvas for your deployment.
2. Click the RustDesk StatefulSet resource card.
3. Increase CPU and memory limits according to active sessions and relay bandwidth.
4. Apply the changes in the dialog and wait for the pod to roll out.

Keep a single replica unless you have a custom multi-server RustDesk topology. The generated key and local metadata are tied to the StatefulSet volume.

## Troubleshooting

### Client does not become ready

- **Cause**: The client is using the wrong TCP gateway host, NodePort, or key.
- **Solution**: Recheck the Service NodePorts, use `tcp.${{ SEALOS_CLOUD_DOMAIN }}` as the host, and copy the latest `Key:` value from pod logs when `ENCRYPTED_ONLY=1`.

### Relay works inconsistently

- **Cause**: The relay NodePort or server key is missing from the client configuration.
- **Solution**: Set both the ID Server and Relay Server fields in the RustDesk client. If encrypted-only mode is enabled, also set the Key field.

### Pod is running but clients cannot connect

- **Cause**: Client traffic is not reaching the exposed NodePorts.
- **Solution**: Confirm the Service lists NodePorts for `21116/tcp`, `21116/udp`, `21117/tcp`, and `21115/tcp`, then test from a network that allows outbound TCP/UDP to the gateway.

## Additional Resources

- [RustDesk Website](https://rustdesk.com/)
- [RustDesk Server Releases](https://github.com/rustdesk/rustdesk-server/releases)
- [RustDesk Documentation](https://rustdesk.com/docs/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the repository license. RustDesk Server itself is licensed under AGPL-3.0.
