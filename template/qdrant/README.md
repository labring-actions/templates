# Deploy and Host Qdrant on Sealos

Qdrant is a high-performance vector database and similarity search engine for embeddings, recommendations, and retrieval-augmented AI applications. This Sealos template runs Qdrant 1.20.2 as a single-replica StatefulSet with a 1Gi storage volume and a public HTTPS REST endpoint.

![Qdrant website](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/qdrant/website-screenshot.webp)

## About Hosting Qdrant

Qdrant stores vectors with JSON payloads, builds similarity indexes, and serves search and recommendation queries through REST and gRPC APIs. The web dashboard provides collection management, point inspection, and query testing.

This template runs one StatefulSet with `qdrant/qdrant:v1.20.2`. The REST API listens on `6333` and gRPC on `6334`. A 1Gi volume at `/qdrant/storage` stores collections, payloads, indexes, and WAL data. The Service maps public HTTP port `80` to `6333` and also exposes gRPC port `6334` inside the cluster.

The Sealos Ingress publishes the REST API and dashboard over HTTPS; the App entry opens `/dashboard`. The template starts without an API key, so the public endpoint accepts unauthenticated requests until an API key is configured.

## Common Use Cases

- **RAG and Semantic Search**: Store document embeddings and retrieve relevant context for AI applications.
- **Recommendations**: Find similar items from user, product, or content vectors.
- **Vector Search Prototyping**: Create collections and test queries from the dashboard.
- **AI Agent Memory**: Keep long-term semantic memory in a dedicated vector store.
- **Benchmarking**: Evaluate collection layouts and index settings before production rollout.

## Dependencies for Qdrant Hosting

The template includes the Qdrant StatefulSet, a 1Gi volume, a Service, an HTTPS Ingress, and the Sealos App entry. Qdrant needs no external database or cache.

Applications need an embedding model or service to produce vectors. Production deployments should configure an API key before exposing the endpoint to untrusted clients. gRPC clients can use the in-cluster Service on port `6334`.

### Deployment Dependencies

- [Qdrant documentation](https://qdrant.tech/documentation/) - Quick start, concepts, and API guides
- [Qdrant repository](https://github.com/qdrant/qdrant) - Source code and issue tracker
- [Qdrant container image](https://hub.docker.com/r/qdrant/qdrant) - Official image used by this template
- [Qdrant REST API](https://qdrant.tech/documentation/interfaces/#rest) - REST endpoint reference
- [Qdrant gRPC API](https://qdrant.tech/documentation/interfaces/#grpc) - gRPC interface reference

## Implementation Details

**Architecture Components:**

- **Qdrant StatefulSet**: One replica running `qdrant/qdrant:v1.20.2`.
- **REST API**: Container port `6333`, published through Service port `80` and the HTTPS Ingress.
- **gRPC API**: Container and Service port `6334` for in-cluster clients.
- **Persistent volume**: A 1Gi volume at `/qdrant/storage` for collections and indexes.
- **Dashboard**: Served at `/dashboard` on the public host.

**Configuration:**

- **Image**: `qdrant/qdrant:v1.20.2`
- **REST port**: `6333`
- **gRPC port**: `6334`
- **Public HTTP port**: `80`
- **Persistence**: 1Gi ReadWriteOnce volume at `/qdrant/storage`
- **Authentication**: No API key in the default template
- **Replicas**: `1`
- **Health checks**: `/readyz` for startup and readiness, `/healthz` for liveness

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qdrant | 10m | 100m | 12Mi | 128Mi | 1Gi |

The profile passed a cold start, `/readyz` check, dashboard load, REST API request, and a stability window with zero restarts.

## Why Deploy Qdrant on Sealos?

Sealos is an AI-assisted cloud operating system built on Kubernetes that unifies deployment, networking, storage, and operations. Deploying Qdrant on Sealos gives you:

- **One-Click Vector Database**: Provision Qdrant, storage, and a public HTTPS endpoint from one template.
- **Persistent Collections**: Keep vectors, payloads, and indexes across Pod restarts.
- **Compact Start**: Run a development or small production dataset with a validated 100m CPU and 128Mi memory limit.
- **Canvas and AI Dialog**: Inspect the StatefulSet, Service, Ingress, PVC, logs, and resource cards, and adjust the deployment through the Sealos AI dialog.
- **REST and gRPC Access**: Use the public REST API or connect in-cluster gRPC clients.
- **Kubernetes Reliability**: Use health probes, automated recovery, and declarative resource management.

## Deployment Guide

1. Open the [Qdrant template](https://sealos.io/products/app-store/qdrant) and click **Deploy Now**.
2. Review the generated application name, confirm the 1Gi storage plan, and start the deployment.
3. Wait for deployment to complete, typically in 2-3 minutes. Sealos opens the Canvas after the resources are created.
4. Open the public URL and append `/dashboard` if the App entry does not open it directly.
5. Create a collection from the dashboard or REST API, insert a few test vectors, and run a similarity query.
6. Open Canvas to review the StatefulSet, Service, Ingress, PVC, and live logs.

## Access and Security

The default template has no API key. Keep the public URL private while evaluating Qdrant, and configure `service.api_key` in a mounted Qdrant configuration before exposing it to production clients. REST clients then send the key in the `api-key` header; gRPC clients pass it as request metadata.

The Ingress publishes the REST API and dashboard on port `80`. gRPC port `6334` is available through the ClusterIP Service for workloads inside the same cluster.

## Scaling

Keep the template at one replica because the local storage volume is a ReadWriteOnce disk. Increase CPU and memory limits for larger collections, higher query rates, and more concurrent searches. Expand the 1Gi volume from the StatefulSet resource card as vectors and indexes grow. For high availability, deploy Qdrant with distributed mode and shared storage, then adjust the topology and replica count together.

## Troubleshooting

### The REST API returns 401

An API key is configured. Send the key in the `api-key` header. If the key is unknown, update the mounted Qdrant configuration and restart the Pod.

### Collection creation fails with disk errors

Check PVC usage and the Pod logs. The template starts with a 1Gi volume; expand it from the StatefulSet resource card before loading large datasets.

### gRPC clients cannot connect

Use `qdrant-service.namespace.svc.cluster.local:6334` from inside the cluster. The public Ingress publishes HTTP port `80`; gRPC remains a cluster-internal Service port.

### Searches return unexpected results

Confirm that the collection distance metric matches the embedding model, that vectors have the expected dimensions, and that payload filters use the indexed fields.

### Getting Help

- [Qdrant documentation](https://qdrant.tech/documentation/)
- [Qdrant issues](https://github.com/qdrant/qdrant/issues)
- [Sealos documentation](https://sealos.io/docs)

## License

Qdrant is licensed under the [Apache License 2.0](https://github.com/qdrant/qdrant/blob/master/LICENSE). This Sealos template is distributed under the templates repository license.
