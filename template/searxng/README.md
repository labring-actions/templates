# Deploy and Host SearXNG on Sealos

SearXNG is a privacy-respecting metasearch engine that aggregates results from multiple sources without building user profiles.

![SearXNG search results](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/searxng/website-screenshot.webp)

## About Hosting SearXNG

This template runs SearXNG as a StatefulSet with a dedicated KubeBlocks Redis Cluster for caching and rate limiting. The web interface is published over public HTTPS, and a generated secret protects session data.

The bundled configuration enables the `360search` engine and keeps the remaining engines disabled. Add engines that are reachable from your workspace in the SearXNG settings, then restart the workload to apply the change.

## Architecture Components

- **SearXNG StatefulSet**: serves the search interface and aggregates engine results.
- **KubeBlocks Redis Cluster**: provides a one-replica Redis service with one sentinel for cache and limiter state.
- **Service and Ingress**: expose the web interface over public HTTPS.
- **ConfigMap**: holds the SearXNG settings, enabled engines, and timeout values.

## Common Use Cases

- Provide a private metasearch front end for a team or family.
- Query multiple search engines from a single interface.
- Avoid search profiling on shared networks.
- Add a self-hosted search endpoint to internal tools.
- Test engine coverage before exposing search to end users.

## Dependencies for SearXNG Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A KubeBlocks Redis Cluster provisioned by this template.
- Outbound HTTPS access to every search engine you enable.
- Storage for the Redis data volume.

## Why Deploy SearXNG on Sealos?

- One-click deployment of both SearXNG and its Redis dependency.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent cache storage backed by KubeBlocks.
- Pay-as-you-go resource cards for the web and database components.
- Canvas view for the StatefulSet, Redis Cluster, Services, and Ingress.
- AI dialog for deployment guidance in the Sealos desktop.

## Deployment Guide

1. Open the [SearXNG template](https://sealos.io/products/app-store/searxng) and click **Deploy Now**.
2. Keep the generated application name, confirm the resource plan, and submit the deployment.
3. Wait 2-3 minutes for the SearXNG pod and Redis Cluster to become ready, then open the public URL from the App card.
4. Run a search query and confirm that results are returned from the enabled engine.
5. Edit the ConfigMap to enable additional engines reachable from your workspace, then restart the pod.

## License

SearXNG is released under the [GNU Affero General Public License v3.0](https://github.com/searxng/searxng/blob/master/LICENSE).
