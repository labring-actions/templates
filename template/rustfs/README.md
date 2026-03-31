# Deploy RustFS on Sealos

RustFS is a high-performance, distributed object storage system built in Rust. This Sealos template deploys RustFS as a 4-replica distributed cluster with persistent storage, a headless service for intra-cluster communication, and a public HTTPS console entrypoint.

## About RustFS Hosting

RustFS is designed for distributed object storage workloads and exposes an S3-compatible API. In this template, each replica mounts four data volumes and participates in the shared storage topology defined by `RUSTFS_VOLUMES`. The deployment also includes a web console for browser-based management.

This template is suitable when you want a self-hosted object storage service on Sealos without manually wiring StatefulSet networking, persistent volumes, or ingress rules.

## What This Template Deploys

- A `StatefulSet` with 4 RustFS replicas
- One `Secret` storing the RustFS access key and secret key
- One `ConfigMap` storing the shared RustFS runtime configuration
- One headless `Service` for peer discovery
- One cluster `Service` exposing ports `9000` and `9001`
- One HTTPS `Ingress` for the RustFS console
- One Sealos `App` resource for console access in the UI
- Five persistent volume claims per pod:
  - 4 data volumes mounted at `/data/rustfs0` to `/data/rustfs3`
  - 1 logs volume mounted at `/logs`
- In total, a default deployment creates 20 PVCs across the 4 replicas:
  - 16 data PVCs
  - 4 logs PVCs

## Default Runtime Configuration

- Image: `rustfs/rustfs:1.0.0-alpha.85`
- Replicas: `4`
- S3 endpoint port: `9000`
- Console port: `9001`
- Default region: `us-east-1`
- Erasure set drive count: `16`
- Storage class: `openebs-hostpath`

## Template Parameters

| Parameter | Description | Required | Default |
| --- | --- | --- | --- |
| `access_key` | S3 access key used by RustFS | Yes | `''` |
| `secret_key` | S3 secret key used by RustFS | Yes | `''` |
| `data_volume_size` | Size in GiB for each data PVC. The template creates 16 data PVCs in total across 4 replicas. | No | `1` |
| `logs_volume_size` | Size in GiB for each logs PVC. The template creates 4 logs PVCs in total across 4 replicas. | No | `1` |

## Deployment Guide

1. Open the RustFS template in Sealos App Store.
2. Fill in the required parameters:
   - `access_key`
   - `secret_key`
3. Adjust optional parameters such as data and logs volume size.
4. Click **Deploy** and wait for the StatefulSet to become ready.
5. Open the generated application URL to access the RustFS web console over HTTPS.

## Access Information

- Console URL: `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- Internal S3 service: `<app_name>:9000`
- Internal console service: `<app_name>:9001`

The public ingress in this template is configured for the web console on port `9001`. The S3 API remains available inside the cluster through the generated Service.

## Operational Notes

- RustFS in this template runs as a distributed 4-replica StatefulSet.
- Each pod gets its own PVC set, so total storage consumption scales with replica count.
- With the default values, the cluster requests 20Gi of persistent storage in total:
  - 16 data PVCs x `1Gi`
  - 4 logs PVCs x `1Gi`
- The deployment retains PVCs when the StatefulSet is deleted or scaled down.
- Health checks use `/health` for liveness and `/health/ready` for readiness.

## Common Use Cases

- Self-hosted S3-compatible object storage
- Internal application artifact and file storage
- Development and testing of object-storage workloads
- Lightweight distributed storage deployment on Sealos

## Troubleshooting

### Console cannot be opened

- Confirm that the application is in `Running` state in Sealos.
- Check whether ingress provisioning has completed.
- Check that all 20 PVCs created by the 4-replica cluster have been provisioned successfully.

### Pods are not becoming ready

- Check PVC provisioning status for the five volume claims created by each pod.
- Confirm the selected storage class supports the requested access mode and capacity.
- Inspect pod logs for RustFS startup or credential-related errors.

### S3 client cannot connect from outside the cluster

- This template only exposes the console publicly by default.
- If you need external S3 API access, add another ingress or service exposure strategy for port `9000`.

## Resources

- [RustFS GitHub Repository](https://github.com/rustfs/rustfs)
- [RustFS Official Website](https://rustfs.com/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This template follows the templates repository license policy. Refer to the RustFS upstream project for its own licensing terms.
