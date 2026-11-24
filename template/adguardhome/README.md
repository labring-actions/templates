# Deploy and Host AdGuard Home on Sealos

AdGuard Home is a network-wide DNS server with a web management console for blocking ads, trackers, and malicious domains. This Sealos template runs AdGuard Home 1.0.0 as a single-replica StatefulSet with separate configuration and working-data volumes and a public HTTPS console.

![AdGuard Home dashboard](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/adguardhome/website-screenshot.webp)

## About Hosting AdGuard Home

AdGuard Home filters DNS queries against blocklists, forwards allowed requests to upstream resolvers, and reports query activity through its dashboard. The console manages filters, clients, DNS rewrites, upstream servers, encryption settings, and query logs.

This template runs one StatefulSet with `adguard/adguardhome:v1.0.0` on port `80`. The container starts with explicit `--config`, `--work-dir`, and `--web-addr 0.0.0.0:80` arguments so the setup wizard and dashboard are reachable through the Service. Two 1Gi volumes persist `/opt/adguardhome/conf` and `/opt/adguardhome/work`.

The Service and Ingress publish the management console over HTTPS. DNS traffic uses UDP and TCP port 53; this template leaves port 53 to a dedicated DNS Service so the web console can be managed independently from network-level resolver exposure.

## Common Use Cases

- **Network-Wide Filtering**: Block advertising and tracking domains for a home or office network.
- **Filter Development**: Test blocklists, allowlists, and custom rules before wider rollout.
- **DNS Visibility**: Inspect query volume, top clients, and blocked domains from one dashboard.
- **Internal DNS Rewrites**: Map internal services and lab hosts to private addresses.
- **Encrypted Upstreams**: Forward allowed queries to DNS-over-HTTPS or DNS-over-TLS providers.

## Dependencies for AdGuard Home Hosting

The template includes the AdGuard Home StatefulSet, two 1Gi volumes, a Service, an HTTPS Ingress, and the Sealos App entry. AdGuard Home needs at least one reachable upstream DNS resolver.

Client devices need a UDP/TCP port 53 Service pointing at this deployment. The setup wizard creates the administrator account; no password is pre-seeded by the template.

### Deployment Dependencies

- [AdGuard Home website](https://adguard.com/adguard-home/overview.html) - Product overview and downloads
- [AdGuard Home documentation](https://adguard-dns.io/kb/adguard-home/overview/) - Setup, filters, and DNS guides
- [AdGuard Home repository](https://github.com/AdguardTeam/AdGuardHome) - Source code and issue tracker
- [AdGuard Home Docker image](https://hub.docker.com/r/adguard/adguardhome) - Official image used by this template
- [AdGuard Home configuration](https://adguard-dns.io/kb/adguard-home/configuration/) - YAML configuration reference

## Implementation Details

**Architecture Components:**

- **AdGuard Home StatefulSet**: One replica running `adguard/adguardhome:v1.0.0` on port `80`.
- **Configuration volume**: A 1Gi volume at `/opt/adguardhome/conf` for `AdGuardHome.yaml`.
- **Working volume**: A 1Gi volume at `/opt/adguardhome/work` for query data and runtime files.
- **Service**: ClusterIP port `80` for the management console.
- **Ingress**: Sealos-managed HTTPS host for the console.
- **DNS exposure**: Add a separate UDP/TCP port 53 Service when clients use this resolver.

**Configuration:**

- **Image**: `adguard/adguardhome:v1.0.0`
- **Web listener**: `0.0.0.0:80`
- **Config path**: `/opt/adguardhome/conf/AdGuardHome.yaml`
- **Work directory**: `/opt/adguardhome/work`
- **Persistence**: 2 × 1Gi ReadWriteOnce volumes
- **Replicas**: `1`
- **Health checks**: HTTP startup, readiness, and liveness probes against `/`

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
| --- | ---: | ---: | ---: | ---: | ---: |
| AdGuard Home | 10m | 100m | 12Mi | 128Mi | 2Gi |

The profile passed a cold start, first-run setup, `/control/status` check, configuration persistence across a Pod restart, and a stability window with zero restarts.

## Why Deploy AdGuard Home on Sealos?

Sealos is an AI-assisted cloud operating system built on Kubernetes that unifies deployment, networking, storage, and operations. Deploying AdGuard Home on Sealos gives you:

- **One-Click Deployment**: Provision the console, configuration storage, and HTTPS endpoint from one template.
- **Persistent DNS Configuration**: Keep filters, rewrites, clients, and query data across restarts.
- **Canvas and AI Dialog**: Inspect the StatefulSet, Service, Ingress, PVCs, logs, and resource cards, and adjust the deployment through the Sealos AI dialog.
- **Pay-as-You-Go Resources**: Run a compact resolver with a validated 100m CPU and 128Mi memory limit.
- **Automatic HTTPS**: Reach the management console through a managed domain and TLS certificate.
- **Kubernetes Reliability**: Use health probes, automated recovery, and declarative resource management.

## Deployment Guide

1. Open the [AdGuard Home template](https://sealos.io/products/app-store/adguardhome) and click **Deploy Now**.
2. Review the generated application name, confirm the storage plan, and start the deployment.
3. Wait for deployment to complete, typically in 2-3 minutes. Sealos opens the Canvas after the resources are created.
4. Open the public URL from the Canvas or the App Store entry. The first visit opens the setup wizard.
5. Create an administrator username and password, keep the web address at `0.0.0.0:80`, and accept a DNS listener on port 53 inside the container.
6. Set a reachable upstream resolver, finish the wizard, then confirm the dashboard loads at `/login.html`.

## Login and Account Setup

AdGuard Home creates its administrator account through the first-run setup wizard. There is no default username or password in this template. Open the public URL on a fresh volume, choose the administrator username and password, review the web and DNS listener addresses, and select an upstream DNS provider.

After setup, the console redirects to `/login.html`. Use the account created in the wizard. The account and all settings persist in `/opt/adguardhome/conf/AdGuardHome.yaml` on the configuration volume.

## Configuration

- **Filters**: Add blocklists under **Filters → DNS blocklists**.
- **Upstream DNS**: Set resolvers under **Settings → DNS settings**.
- **DNS rewrites**: Add internal hostnames under **Filters → DNS rewrites**.
- **Clients**: Create client-specific settings under **Settings → Client settings**.
- **Query log**: Stored in the working volume; adjust retention under **Settings → General settings**.
- **DNS port**: Add a UDP/TCP 53 Service before pointing devices at the resolver.
- **Web listener**: Keep `0.0.0.0:80` so the Ingress can reach the console.

## Scaling

Keep the template at one replica because the resolver owns local configuration and query data on ReadWriteOnce volumes. Increase CPU and memory limits when query volume, large filter lists, or long retention windows need more resources. Expand the configuration or working volume from the StatefulSet resource card when filter data or query history grows.

## Troubleshooting

### The setup wizard does not appear

Confirm that the Pod is Ready and that the Ingress returns the console. If the configuration volume already contains an `AdGuardHome.yaml`, AdGuard Home skips the wizard and shows the login page.

### The console returns a redirect loop

Verify that the web listener is `0.0.0.0:80` and that the Ingress forwards plain HTTP to the Service. The template passes these values as explicit container arguments.

### Devices cannot resolve DNS through AdGuard Home

The template publishes the web console and leaves port 53 to a separate Service. Create a UDP/TCP 53 Service for the StatefulSet, then configure clients with its address.

### Configuration is lost after a restart

Confirm that both `/opt/adguardhome/conf` and `/opt/adguardhome/work` are mounted from persistent volumes. The setup wizard writes the account and settings to the configuration volume.

### Getting Help

- [AdGuard Home documentation](https://adguard-dns.io/kb/adguard-home/overview/)
- [AdGuard Home issues](https://github.com/AdguardTeam/AdGuardHome/issues)
- [Sealos documentation](https://sealos.io/docs)

## License

AdGuard Home is licensed under the [GNU General Public License v3.0](https://github.com/AdguardTeam/AdGuardHome/blob/master/LICENSE.txt). This Sealos template is distributed under the templates repository license.
