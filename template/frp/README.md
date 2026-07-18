# Deploy and Host frp on Sealos

frp is a fast reverse proxy that helps expose local services behind NAT or firewalls to the internet. This template deploys the frp server (`frps`) with a web dashboard, HTTP virtual host entry, and public TCP ports on Sealos Cloud.

![frp Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/frp/website-screenshot.webp)

## About Hosting frp

frp uses a public server and local clients to build reverse proxy tunnels. The Sealos template runs the public `frps` service, exposes the built-in dashboard through an HTTPS Ingress, and keeps TCP NodePort access for frpc connections and TCP proxy traffic.

The deployment includes automatic SSL certificate provisioning for the dashboard and HTTP virtual host domains. It also creates a NodePort service because frp needs public TCP ports beyond the HTTP dashboard, especially the frpc server port and user-defined TCP remote ports.

## Common Use Cases

- **Expose local web services**: Publish a local HTTP service through the frp HTTP virtual host domain.
- **SSH access to private machines**: Proxy SSH traffic from a private network through the public frp server.
- **Self-hosted tunneling**: Run your own tunnel infrastructure instead of relying on a managed tunnel provider.
- **Protocol testing**: Validate TCP and HTTP proxy behavior in development or lab environments.

## Dependencies for frp Hosting

The Sealos template includes all required runtime components for the frp server. It does not provision a database, object storage bucket, or persistent volume.

### Deployment Dependencies

- [Official frp Documentation](https://gofrp.org/en/docs/) - frp documentation
- [Server Configuration](https://gofrp.org/en/docs/reference/server-configures/) - frps configuration reference
- [Web Interface](https://gofrp.org/en/docs/features/common/ui/) - dashboard configuration
- [GitHub Repository](https://github.com/fatedier/frp) - source code and releases

## Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **frps Deployment**: Runs `fatedier/frps:v0.69.1` with a mounted `frps.toml` configuration.
- **ConfigMap**: Stores the frp server configuration, including dashboard credentials from `ADMIN_USER` and `ADMIN_PASSWORD`.
- **NodePort Service**: Exposes dashboard, HTTP virtual host, frpc server, and TCP proxy ports.
- **Ingress**: Routes the dashboard host to port `7500` and the HTTP virtual host to port `80`.
- **App Link**: Opens the frp dashboard from the Sealos desktop.

**Configuration:**

- `bindPort = 7000` is the frpc server port.
- `vhostHTTPPort = 80` handles HTTP proxy traffic.
- `webServer.port = 7500` serves the dashboard.
- `ADMIN_USER` and `ADMIN_PASSWORD` become the dashboard login credentials.

**License Information:**

frp is licensed under Apache License 2.0. This Sealos template follows the same deployment assumptions documented by the frp project.

## Why Deploy frp on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, public networking, and resource management. By deploying frp on Sealos, you get:

- **One-Click Deployment**: Open the template page, configure credentials, and deploy without writing Kubernetes manifests.
- **Instant Public Access**: Sealos provides HTTPS domains for the dashboard and HTTP virtual host entry.
- **Public TCP Access**: NodePort services expose the frpc server port and TCP proxy port for non-HTTP tunnels.
- **Resource Efficiency**: The template runs frp with a lightweight resource profile and pay-as-you-go infrastructure.
- **Easy Operations**: Use Canvas, AI dialog, and resource cards to inspect or adjust the deployment after it starts.

## Deployment Guide

1. Open the [frp template](https://sealos.io/products/app-store/frp) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - `ADMIN_USER`: dashboard username.
   - `ADMIN_PASSWORD`: dashboard password.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your frp services:
   - **Dashboard**: Open the Sealos app link and log in with `ADMIN_USER` and `ADMIN_PASSWORD`.
   - **HTTP virtual host**: Use the HTTP Ingress domain as the `customDomains` value in frpc HTTP proxy configuration.
   - **frpc server**: In the Service details, use the NodePort assigned to the `server` port as `serverPort`.
   - **TCP proxy**: In the Service details, use the NodePort assigned to `tcp-proxy` as the `remotePort` value.

## Example frpc Configuration

For an HTTP service running locally on port `8080`:

```toml
serverAddr = "<your-frp-node-address-or-domain>"
serverPort = <server-node-port>

[[proxies]]
name = "web"
type = "http"
localPort = 8080
customDomains = ["<your-http-virtual-host-domain>"]
```

For SSH access:

```toml
serverAddr = "<your-frp-node-address-or-domain>"
serverPort = <server-node-port>

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = <tcp-proxy-node-port>
```

## Configuration

After deployment, you can manage frp through:

- **Dashboard**: Open the Sealos app link and log in with the configured credentials.
- **Canvas AI Dialog**: Describe resource or configuration changes and let AI apply updates.
- **Resource Cards**: Open Deployment, Service, Ingress, or ConfigMap cards to inspect the generated resources.

## Troubleshooting

### Dashboard login fails

- Cause: The entered username or password differs from `ADMIN_USER` or `ADMIN_PASSWORD`.
- Solution: Check the template input values or update the ConfigMap and restart the Deployment.

### frpc cannot connect

- Cause: The frpc `serverPort` does not match the Service NodePort assigned to the `server` port.
- Solution: Open the Service resource details and copy the current NodePort for `server`.

### TCP proxy cannot open

- Cause: The frpc `remotePort` does not match the Service NodePort assigned to `tcp-proxy`.
- Solution: Open the Service resource details and copy the current NodePort for `tcp-proxy`.

## Additional Resources

- [frp Documentation](https://gofrp.org/en/docs/)
- [frp Web Interface](https://gofrp.org/en/docs/features/common/ui/)
- [frp Releases](https://github.com/fatedier/frp/releases)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository license. frp itself is licensed under Apache License 2.0.
