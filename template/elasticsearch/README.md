# Deploy and Host Elasticsearch on Sealos

Elasticsearch is a distributed search and analytics engine for logs, metrics, vectors, and application data. This template deploys Elasticsearch as a fixed 3-node high-availability cluster on Sealos Cloud.

![Elasticsearch Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/elasticsearch/website-screenshot.webp)

## About Hosting Elasticsearch

Elasticsearch stores and searches structured, unstructured, and vector data through a REST API. This Sealos template runs Elasticsearch with three StatefulSet replicas so the cluster can elect a master node and keep serving queries when a node restarts.

The template provisions stable pod DNS through a headless service, one persistent volume per node, an HTTPS ingress for REST API access, and Kubernetes health probes. Sealos handles domain routing, TLS termination, persistent storage attachment, and lifecycle management from the Canvas after deployment.

This template disables Elasticsearch built-in security by default to keep the 3-node cluster bootstrap simple without generating shared transport TLS certificates. Use it in trusted networks, or place an authenticated gateway in front of the public endpoint before production use.

## Common Use Cases

- **Application Search**: Power fast full-text search for product catalogs, documentation, and internal content.
- **Log and Event Analytics**: Index operational logs and events for troubleshooting and trend analysis.
- **Vector Search Prototyping**: Store embeddings and test similarity search workloads through Elasticsearch APIs.
- **Metrics Exploration**: Query time-series style operational data for dashboards and reporting.

## Dependencies for Elasticsearch Hosting

The Sealos template includes the required runtime components for a self-contained Elasticsearch deployment: the official Elasticsearch container image, a StatefulSet, persistent volume claims, a headless service, an ingress, and an App link.

### Deployment Dependencies

- [Elasticsearch Documentation](https://www.elastic.co/docs/solutions/search) - Official Elasticsearch documentation
- [Elasticsearch REST APIs](https://www.elastic.co/docs/api/doc/elasticsearch) - API reference
- [Elasticsearch GitHub Repository](https://github.com/elastic/elasticsearch) - Source repository
- [Sealos Documentation](https://sealos.io/docs) - Sealos platform documentation

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Elasticsearch StatefulSet**: Three Elasticsearch 9.4.1 pods with stable names and persistent data directories.
- **Headless Service**: Provides stable DNS records for node discovery and inter-node transport traffic.
- **Ingress**: Exposes the REST API over HTTPS through the Sealos-managed domain.
- **App Link**: Adds the deployed endpoint to the Sealos application list.

**Configuration:**

- `replicas` is fixed to `3` for high availability.
- `cluster.initial_master_nodes` points to the three StatefulSet pod names.
- `discovery.seed_hosts` uses the headless service DNS names for all three pods.
- Each node receives a `500m` CPU limit, `1024Mi` memory limit, `50m` CPU request, `102Mi` memory request, and a `512Mi` Elasticsearch heap.
- Each node gets a `1Gi` persistent volume mounted at `/usr/share/elasticsearch/data`.
- Elasticsearch security is disabled by default; no login is required after deployment.

**License Information:**

Elasticsearch is provided by Elastic under the Elastic License and related licensing terms. Review the official Elastic licensing information before using it in production.

## Why Deploy Elasticsearch on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is suitable for search services, AI applications, SaaS platforms, and microservice architectures. By deploying Elasticsearch on Sealos, you get:

- **One-Click Deployment**: Deploy Elasticsearch from the App Store without writing Kubernetes YAML.
- **Kubernetes Foundation**: Run Elasticsearch on a Kubernetes-based platform with StatefulSet scheduling and service discovery.
- **Easy Customization**: Adjust resources and operational settings through the Canvas, AI dialog, or resource cards.
- **Persistent Storage Included**: Keep search data across pod restarts through per-node persistent volumes.
- **Instant Public Access**: Get an HTTPS endpoint with Sealos-managed domain and TLS termination.
- **Pay-as-You-Go Resources**: Start with a compact HA footprint and adjust resources as usage grows.

Deploy Elasticsearch on Sealos and focus on search features instead of cluster plumbing.

## Deployment Guide

1. Open the [Elasticsearch template](https://sealos.io/products/app-store/elasticsearch) and click **Deploy Now**.
2. Review the generated app name and host values in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Access your Elasticsearch endpoint through the provided URL:
   - **REST API**: `https://<your-elasticsearch-domain>`
   - **Health Check**: `https://<your-elasticsearch-domain>/_cluster/health?pretty`

## Login and Access

This template does not deploy a web UI and does not require registration or login. Elasticsearch is exposed as a REST API service.

Because Elasticsearch built-in security is disabled in this HA template, clients can call the API directly from trusted environments. For production or public access, add authentication at a gateway, VPN, private network boundary, or a dedicated security layer before exposing the endpoint to users.

## Scaling

This template is intentionally fixed at three replicas to provide a small high-availability cluster. To change resources after deployment:

1. Open the Canvas for your deployment.
2. Click the Elasticsearch StatefulSet resource card.
3. Adjust CPU, memory, or storage according to your workload.
4. Apply the change through the dialog.

Keep the replica count at `3` unless you also update Elasticsearch discovery and master-node settings.

## Troubleshooting

### Cluster health is yellow or red

- Cause: A pod may still be starting, or a node may not have joined the cluster.
- Solution: Check the StatefulSet and Pod resource cards in Canvas. Wait for all three pods to become ready, then check `/_cluster/health?pretty` again.

### API endpoint is reachable without a password

- Cause: The HA template disables Elasticsearch built-in security by default.
- Solution: Use the endpoint only in trusted environments, or add an authenticated gateway before public production use.

### A node restarts repeatedly

- Cause: Elasticsearch may need more memory for your index or query workload.
- Solution: Increase the StatefulSet memory limit and Elasticsearch heap proportionally through the Canvas resource card.

### Getting Help

- [Elasticsearch Documentation](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch REST APIs](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Elasticsearch Guide](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch API Reference](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository license. Elasticsearch itself is distributed under Elastic licensing terms.
