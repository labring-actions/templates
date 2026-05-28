# Deploy and Host Derper on Sealos

Derper is a slim build of the Tailscale DERP relay server for self-hosted relay and STUN service. This template deploys Derper as a single NodePort service on Sealos Cloud.

![Derper Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/derper/website-screenshot.webp)

## About Hosting Derper

Derper provides a self-hosted DERP relay that Tailscale-compatible clients can use when direct peer-to-peer connectivity is unavailable. It also exposes a STUN port, which helps clients discover their public address and improves NAT traversal.

This template runs Derper as one lightweight container with TCP service for DERP traffic and UDP service for STUN. A startup job detects the allocated Sealos NodePort values, patches the service and deployment, and then starts the Derper workload with the final ports.

Derper is not a web application and does not provide a browser login or registration flow. After deployment, configure your Headscale or Tailscale DERP map to use the generated host and ports shown in the service details.

## Common Use Cases

- **Self-hosted DERP relay**: Provide a private relay server for Tailscale or Headscale networks.
- **NAT traversal support**: Enable STUN alongside DERP so clients can improve connectivity through NAT.
- **Private network labs**: Test custom DERP maps and relay behavior without managing servers manually.
- **Regional relay placement**: Deploy an additional relay close to users or devices that need better connectivity.

## Dependencies for Derper Hosting

The Sealos template includes all required runtime resources: one Derper container, one NodePort service for DERP and STUN traffic, and a short-lived configuration job. No external database, object storage, or persistent volume is required.

### Deployment Dependencies

- [Derper Source Repository](https://github.com/yangchuansheng/derper) - Image source and runtime notes
- [Tailscale Custom DERP Servers](https://tailscale.com/kb/1118/custom-derp-servers) - Custom DERP map concepts
- [Headscale DERP Documentation](https://headscale.net/stable/ref/derp/) - Headscale DERP configuration
- [Sealos App Store](https://sealos.io/products/app-store/derper) - One-click deployment entry

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Derper Deployment**: Runs `ghcr.io/yangchuansheng/derper:v1.99.0-pre` with DERP and STUN enabled.
- **NodePort Service**: Exposes one TCP port for DERP traffic and one UDP port for STUN.
- **Configuration Job**: Reads allocated NodePort values, patches service ports, patches Derper environment variables, and scales the deployment to one replica.

**Configuration:**

- `enable_stun` controls whether the STUN service is enabled. The default value is `true`.
- `DERP_DOMAIN` is set to `tcp.${{ SEALOS_CLOUD_DOMAIN }}` so clients can use the Sealos TCP gateway domain for the current region.
- `DERP_VERIFY_CLIENTS` is set to `false` for simple self-hosted operation.
- The deployment uses the minimum tested Sealos resource tier: `100m` CPU and `128Mi` memory.

**License Information:**

Derper follows the license terms of the upstream repositories it builds from. Review the [Derper repository](https://github.com/yangchuansheng/derper) and the [Tailscale repository](https://github.com/tailscale/tailscale) before production use.

## Why Deploy Derper on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is suitable for deploying lightweight networking tools, self-hosted services, and production workloads without manually operating Kubernetes.

By deploying Derper on Sealos, you get:

- **One-Click Deployment**: Open the template and deploy without writing Kubernetes YAML.
- **NodePort Networking**: Expose DERP TCP and STUN UDP ports with Sealos-managed service resources.
- **Easy Customization**: Adjust inputs and resource settings from the deployment dialog or Canvas.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed scheduling and lifecycle management through a visual workflow.
- **Pay-as-You-Go Resources**: Start with the minimum tested quota and scale only when needed.
- **AI-Assisted Operations**: After deployment, use the Canvas AI dialog or resource cards to adjust settings.

Deploy Derper on Sealos and focus on configuring your tailnet instead of managing server infrastructure.

## Deployment Guide

1. Open the [Derper template](https://sealos.io/products/app-store/derper) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. Keep `enable_stun` set to `true` unless you only need DERP TCP relay traffic.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Open the Derper service details in Canvas and note the allocated ports:
   - **DERP TCP**: Use the `derp-tcp` NodePort with `tcp.${{ SEALOS_CLOUD_DOMAIN }}`.
   - **STUN UDP**: Use the `stun-udp` NodePort with `tcp.${{ SEALOS_CLOUD_DOMAIN }}` if STUN is enabled.
5. Add these values to your Headscale or Tailscale DERP map. This app has no web login or registration page.

## Configuration

Derper is configured mainly through environment variables. This template preconfigures the upstream Derper settings for Sealos NodePort networking, then lets you inspect or adjust them from Canvas after deployment.

You can configure Derper through:

- **AI Dialog**: Describe the changes you want and let AI apply updates.
- **Resource Cards**: Click the deployment or service resource card to inspect ports, environment variables, and resource limits.
- **DERP Map**: Update your Headscale or Tailscale configuration to point clients to the generated host and ports.

### Runtime Settings

| Variable | Template value | Purpose |
|----------|----------------|---------|
| `DERP_DOMAIN` | `tcp.${{ SEALOS_CLOUD_DOMAIN }}` | Hostname advertised by Derper. Keep it consistent with the hostname clients dial. |
| `DERP_CERT_MODE` | `manual` | Reads certificates from `DERP_CERT_DIR`; the image auto-generates self-signed certificates when files are missing. |
| `DERP_CERT_DIR` | `/cert` | Directory for generated or supplied `*.crt` and `*.key` files. |
| `DERP_ADDR` | Patched to `:<derp-tcp-nodeport>` | DERP TCP listen address. The configuration job replaces the placeholder port with the allocated NodePort. |
| `DERP_STUN` | `${{ inputs.enable_stun }}` | Enables or disables STUN. Keep the default `true` unless you only need DERP relay traffic. |
| `DERP_STUN_PORT` | Patched to `<stun-udp-nodeport>` | STUN UDP port. The configuration job replaces the placeholder port with the allocated NodePort. |
| `DERP_HTTP_PORT` | `-1` | Keeps the optional HTTP debug endpoint disabled. |
| `DERP_VERIFY_CLIENTS` | `false` | Disables DERP peer verification for simple self-hosted operation. |
| `DERP_VERIFY_CLIENT_URL` | Not set | Optional upstream setting for fetching verification keys; not exposed by this template by default. |

The upstream image can generate a two-year self-signed certificate when `DERP_CERT_MODE=manual` and no certificate exists. Because this build is designed for self-hosted setups and relaxes certificate verification, use it only in controlled environments where you understand the trust model.

### Headscale or Tailscale DERP Map

After deployment, open the service resource card and copy the current `derp-tcp` and `stun-udp` NodePort values. Use those values in your DERP map instead of hardcoding the example ports below.

Example Headscale DERP node fields:

```json
{
  "HostName": "tcp.<your-sealos-cloud-domain>",
  "DERPPort": 12345,
  "STUNPort": 3478,
  "InsecureForTests": true
}
```

Set `InsecureForTests` only when your clients must accept the self-signed certificate used by this Derper build. For stricter production environments, replace the self-signed certificate strategy with a trusted certificate setup.

## Scaling

Derper usually runs as a single replica because relay clients connect to specific advertised host and port values. To adjust resources:

1. Open the Canvas for your deployment.
2. Click the Derper deployment resource card.
3. Adjust CPU and memory to the next Sealos resource tier if traffic grows.
4. Apply the changes in the dialog.

## Troubleshooting

### Common Issues

**Clients cannot connect to the DERP server**
- Cause: The DERP map may use the wrong host or NodePort.
- Solution: Check the service resource card and copy the current `derp-tcp` NodePort into your DERP map.

**STUN does not work**
- Cause: STUN may be disabled or the UDP NodePort may be missing from the client configuration.
- Solution: Keep `enable_stun` set to `true` and use the `stun-udp` NodePort shown in the service details.

**Self-signed certificate warnings appear**
- Cause: This Derper image is designed for self-hosted setups and can use self-signed certificates.
- Solution: For Headscale testing, set `InsecureForTests` in your DERP map. For stricter production setups, provide a trusted certificate strategy outside this template.

### Getting Help

- [Derper Source Repository](https://github.com/yangchuansheng/derper)
- [Tailscale Custom DERP Servers](https://tailscale.com/kb/1118/custom-derp-servers)
- [Headscale DERP Documentation](https://headscale.net/stable/ref/derp/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Tailscale DERP Overview](https://tailscale.com/blog/how-tailscale-works/)
- [Tailscale ACL DERP Servers](https://tailscale.com/kb/1192/acl-derp-servers)
- [Headscale Documentation](https://headscale.net/stable/)

## License

This Sealos template is provided under the repository license. Derper and its upstream components are licensed by their respective upstream projects.
