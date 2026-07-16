# Deploy and Host Elasticsearch on Sealos

Elasticsearch is a distributed search and analytics engine for logs, metrics, vectors, and application data. This template deploys Elasticsearch 9.4.3 as a fixed 3-node high-availability cluster with an authenticated REST gateway on Sealos Cloud.

![Elasticsearch Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/elasticsearch/website-screenshot.webp)

## About Hosting Elasticsearch

Elasticsearch stores and searches structured, unstructured, and vector data through a REST API. Three StatefulSet replicas provide master-eligible data nodes with stable identities and dedicated persistent volumes.

The public HTTPS endpoint routes through a lightweight NGINX gateway protected by HTTP Basic Auth. A ClusterIP REST service gives the gateway a stable backend, while a headless service provides discovery and node-to-node transport. A NetworkPolicy limits both internal paths to the gateway and Elasticsearch pods. Sealos manages TLS termination, domain routing, storage attachment, and the deployment lifecycle from Canvas.

## Common Use Cases

- **Application Search**: Build full-text search for catalogs, documentation, and internal content.
- **Log and Event Analytics**: Index operational events for troubleshooting and trend analysis.
- **Vector Search**: Store embeddings and run similarity queries through Elasticsearch APIs.
- **Metrics Exploration**: Query operational time-series data for dashboards and reports.

## Dependencies for Elasticsearch Hosting

The template includes the official Elasticsearch image, three persistent volumes, headless and ClusterIP services, an authenticated NGINX gateway, an HTTPS ingress, and an App link.

### Deployment Dependencies

- [Elasticsearch Documentation](https://www.elastic.co/docs/solutions/search) - Official product documentation
- [Elasticsearch REST APIs](https://www.elastic.co/docs/api/doc/elasticsearch) - REST API reference
- [Elasticsearch GitHub Repository](https://github.com/elastic/elasticsearch) - Source repository
- [Sealos Documentation](https://sealos.io/docs) - Sealos platform documentation

### Implementation Details

**Architecture Components:**

- **Elasticsearch StatefulSet**: Three Elasticsearch 9.4.3 master-eligible data nodes with stable pod names.
- **Persistent Storage**: One `1Gi` volume per node at `/usr/share/elasticsearch/data`.
- **Headless Service**: Stable pod DNS for discovery, bootstrap identity checks, and transport traffic.
- **ClusterIP REST Service**: A stable internal endpoint used by the gateway across pod replacements.
- **REST Gateway**: One NGINX deployment that applies HTTP Basic Auth before forwarding requests to Elasticsearch.
- **NetworkPolicy**: Restricts port `9200` to the gateway and cluster pods, and port `9300` to cluster pods.
- **Ingress and App Link**: A Sealos-managed HTTPS domain for REST clients and browser access.

**Configuration:**

- The replica count stays fixed at `3`.
- StatefulSet pods start in parallel so persisted nodes can re-establish quorum after a full pod restart.
- An ordinal-0 node with an empty volume checks peer cluster UUIDs before bootstrap. It sets `cluster.initial_master_nodes` only after both peer nodes explicitly report that they lack persisted cluster identity.
- `discovery.seed_hosts` lists all three StatefulSet pod addresses.
- Each node receives a `500m` CPU limit, `2048Mi` memory limit, and a `512Mi` Elasticsearch heap. Live Sealos validation found that the next lower memory tier reached 99.8% during authenticated indexing.
- Startup and readiness checks wait for cluster health to reach `yellow`; liveness checks the local HTTP listener.
- Public REST requests require the deployment-time `auth_username` and `auth_password` values.
- The public path uses Sealos TLS and gateway authentication. Internal HTTP and transport traffic remains plaintext inside the NetworkPolicy boundary.

**License Information:**

Elasticsearch is provided by Elastic under the Elastic License and related licensing terms. Review the official licensing information before production use.

## Why Deploy Elasticsearch on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes. This template provides:

- **One-Click Deployment**: Create the full 3-node cluster and authenticated gateway from the App Store.
- **Kubernetes Foundation**: Use StatefulSet identities, service discovery, health probes, and persistent volumes.
- **Managed HTTPS Access**: Receive a Sealos domain with TLS termination and Basic Auth at the gateway.
- **Canvas Operations**: Adjust resources through the AI dialog or resource cards after deployment.
- **Pay-as-You-Go Resources**: Start from a compact HA footprint and increase capacity with workload growth.

## Deployment Guide

1. Open the [Elasticsearch template](https://sealos.io/products/app-store/elasticsearch) and click **Deploy Now**.
2. Set `auth_username` and `auth_password` in the popup dialog, then store both values in your credential manager.
3. Wait for deployment to complete, typically 2-3 minutes. Sealos then opens Canvas for the deployment.
4. Copy the HTTPS endpoint from the App link and verify cluster health:

   ```bash
   export ES_URL="https://<your-elasticsearch-domain>"
   curl --user '<auth_username>:<auth_password>' \
     "$ES_URL/_cluster/health?pretty"
   ```

## Login and Access

This template presents Elasticsearch as a REST API. Opening the App link in a browser displays an HTTP Basic Auth prompt; enter the same credentials configured during deployment.

REST clients can send the credentials with `curl --user`, an `Authorization: Basic ...` header, or the Basic Auth option in an Elasticsearch SDK. Requests with missing or invalid credentials receive `401 Unauthorized` from the gateway.

## Scaling

This template uses three replicas to preserve a small high-availability topology. To adjust compute resources:

1. Open the deployment in Canvas.
2. Select the Elasticsearch StatefulSet resource card.
3. Update CPU or memory and keep the heap at or below half of the memory limit.
4. Apply the change through the dialog.

Keep the replica count at `3` so the discovery and bootstrap topology stays aligned with the template.

## Troubleshooting

### The REST API returns 401

- Confirm that the request includes the `auth_username` and `auth_password` values entered during deployment.
- Quote credentials containing shell-special characters when using `curl --user`.

### Cluster health remains yellow or red

- Check the StatefulSet and Pod resource cards in Canvas.
- Wait for all three pods to become ready, then call `/_cluster/health?pretty` through the authenticated endpoint.

### A node restarts repeatedly

- Review the pod logs and memory usage in Canvas.
- Increase the StatefulSet memory limit and keep the Elasticsearch heap at or below 50% of that limit.

### Getting Help

- [Elasticsearch Documentation](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch REST APIs](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Elasticsearch Guide](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch API Reference](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository license. Elasticsearch is distributed under Elastic licensing terms.
