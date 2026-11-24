# Deploy and Host Pi-hole on Sealos

Pi-hole is a self-hosted DNS sinkhole that blocks ads and trackers for every device on a network and reports activity through a web dashboard.

![Pi-hole dashboard](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pi-hole/website-screenshot.webp)

## About Hosting Pi-hole

This template runs the official Pi-hole image as a single StatefulSet with a 1 GiB persistent volume for `/etc/pihole`. The web console is published over HTTPS, and the administrator password is supplied during deployment.

Sign in at `/admin` with the password from the template inputs. Query logs, blocklists, local DNS records, and upstream resolvers are managed from the dashboard and persist across pod restarts.

## Common Use Cases

- Block advertising and tracking domains for a home or office network.
- Inspect DNS query volume and top blocked domains from one dashboard.
- Add local DNS records for lab services and internal hostnames.
- Test blocklists and allowlists before rolling them out network-wide.
- Keep a private DNS management console for a small team.

## Dependencies for Pi-hole Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A 1 GiB persistent volume for Pi-hole configuration and query history.
- An administrator password supplied through the template input.
- A UDP/TCP port 53 Service when client devices query this instance for DNS.

## Why Deploy Pi-hole on Sealos?

- One-click deployment with the web console exposed over public HTTPS.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent storage for blocklists, settings, and query history.
- Pay-as-you-go resource cards that suit small DNS deployments.
- Canvas view for the StatefulSet, Service, Ingress, and PVC.
- AI dialog for deployment guidance in the Sealos desktop.

## Deployment Guide

1. Open the [Pi-hole template](https://sealos.io/products/app-store/pi-hole) and click **Deploy Now**.
2. Enter an administrator password, keep the generated application name, and confirm the 1 GiB storage plan.
3. Wait 2-3 minutes for the StatefulSet to become ready, then open the public URL and append `/admin`.
4. Sign in with the password from step 2 and open **Query Log** to confirm the dashboard is responding.
5. For client DNS traffic, add a Service that exposes UDP and TCP port 53, then point your devices at its address.

## License

Pi-hole uses its own upstream license. See the [Pi-hole license](https://github.com/pi-hole/pi-hole/blob/master/LICENSE) for the full terms.
