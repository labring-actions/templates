# Deploy and Host RSSHub on Sealos

RSSHub converts content from hundreds of websites into standard RSS feeds for feed readers and automation tools. This template deploys RSSHub with Redis caching and a dedicated Browserless service on Sealos Cloud.

![RSSHub Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rsshub/website-screenshot.webp)

## About Hosting RSSHub

RSSHub exposes HTTP routes that collect source content and return RSS output. Feed readers, notification services, and automation systems can subscribe to those routes through the public application URL.

The Sealos template provisions RSSHub, a KubeBlocks Redis service for shared caching, and Browserless Chrome for routes that require browser rendering. Sealos also creates health probes, internal service discovery, a TLS-enabled public endpoint, and persistent Redis storage.

## Common Use Cases

- **Feed Reader Sources**: Add RSS feeds for websites that provide limited syndication options.
- **Content Monitoring**: Track updates from supported sites in one consistent feed format.
- **Automation Inputs**: Send RSS items into workflow, notification, or archival systems.
- **Team Feed Service**: Host a shared RSSHub endpoint with centralized caching.

## Dependencies for RSSHub Hosting

The template includes RSSHub, KubeBlocks Redis, Browserless Chrome, internal Services, health probes, a public Ingress, and the Sealos application entry. The default configuration is ready to deploy without user-provided parameters.

### Deployment Dependencies

- [RSSHub Documentation](https://docs.rsshub.app/) - Route catalog, deployment, and usage documentation
- [RSSHub Routes](https://docs.rsshub.app/routes/) - Supported sites and route parameters
- [RSSHub Source](https://github.com/DIYgod/RSSHub) - Source code, releases, and issue tracker
- [Browserless Documentation](https://docs.browserless.io/) - Browser automation service documentation

### Implementation Details

**Architecture Components:**

- **RSSHub**: The public feed API, running the `2026-07-23` image on port 1200.
- **Redis**: A KubeBlocks Redis 7.2.7 cluster used for shared route caching.
- **Browserless**: Browserless Chrome 2.55.0 on an internal service for browser-rendered routes.
- **Public Endpoint**: A Sealos-managed HTTPS Ingress exposing RSSHub while Redis and Browserless remain internal.

RSSHub connects to Redis with Sealos-managed database credentials and reaches Browserless through its Playwright WebSocket endpoint. The application, browser service, and database use independently validated resource settings. RSSHub is licensed under the GNU Affero General Public License v3.0.

## Why Deploy RSSHub on Sealos?

- **One-Click Deployment**: Provision the feed service, cache, browser runtime, storage, network, and TLS endpoint together.
- **Shared Route Cache**: Reduce repeated source requests through the included Redis service.
- **Browser-Rendered Routes**: Support routes that need a real browser through the dedicated Browserless service.
- **Instant HTTPS Access**: Receive a public RSSHub URL with a managed certificate.
- **Kubernetes Operations**: Inspect and adjust each component through Sealos Canvas, AI dialog, and resource cards.

## Deployment Guide

1. Open the [RSSHub template](https://sealos.io/products/app-store/rsshub) and click **Deploy Now**.
2. Review the generated application name and public hostname, then start the deployment.
3. Wait for deployment to complete, typically 2-3 minutes. Redis can require additional startup time while its account secret and service become ready.
4. Open the RSSHub application URL shown in Sealos.

## Use RSSHub Routes

The root page confirms the RSSHub service is available. Build a feed URL by appending a documented route to the public application URL:

```text
https://<your-rsshub-domain>/<route-and-parameters>
```

For example, select a route from the [RSSHub route catalog](https://docs.rsshub.app/routes/), replace the documented `https://rsshub.app` prefix with your Sealos application URL, and add the resulting URL to a feed reader. The health endpoint is available at `/healthz` for operational checks.

## Configuration

RSSHub route behavior can be adjusted through supported environment variables on the RSSHub Deployment card. Keep `REDIS_URL` connected to the included KubeBlocks Redis service and `PLAYWRIGHT_WS_ENDPOINT` connected to the internal Browserless service.

For deployment changes, use the Sealos Canvas AI dialog or open the RSSHub, Browserless, Redis, and network resource cards directly.

## Scaling

Increase RSSHub CPU and memory for more concurrent or computationally intensive routes. Scale Browserless resources for browser-heavy workloads, and review Redis capacity as cache volume grows. Validate route behavior after every replica or resource change.

## Troubleshooting

### A route returns an error

Confirm the route path and required parameters against the current route documentation. Review the RSSHub Pod logs for source-site, network, rate-limit, or parsing details.

### Browser-rendered routes fail

Confirm that the Browserless Pod is Ready and that its internal Service has an endpoint. Review both RSSHub and Browserless logs for Playwright connection or page-load errors.

### Redis takes longer to become ready

Wait for the KubeBlocks Redis Cluster and account Secret to become available. RSSHub connects automatically after the Redis service is ready.

### Getting Help

- [RSSHub Issues](https://github.com/DIYgod/RSSHub/issues)
- [RSSHub Community](https://docs.rsshub.app/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template follows the licensing terms of the templates repository. RSSHub is distributed under the [GNU Affero General Public License v3.0](https://github.com/DIYgod/RSSHub/blob/master/LICENSE).
