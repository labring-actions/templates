# Deploy and Host InfluxDB on Sealos

InfluxDB is an open source time series database for real-time analytics, metrics, events, and IoT data. This template deploys InfluxDB 2.9.1 with persistent storage, a compact default resource profile, and a public web UI on Sealos Cloud.

## About Hosting InfluxDB

InfluxDB stores timestamped measurements and provides a queryable platform for dashboards, alerting systems, observability pipelines, and sensor data. This Sealos template runs InfluxDB as a single StatefulSet with a persistent volume mounted at `/var/lib/influxdb2`, so databases, buckets, tokens, and metadata survive restarts.

During first startup, the template initializes an admin user, organization, bucket, and API token from the deployment form. Sealos provisions HTTPS access through Ingress, keeps the workload on Kubernetes, and exposes the InfluxDB UI through an App entry in the Canvas.

## Common Use Cases

- **Infrastructure Monitoring**: Store CPU, memory, disk, network, and service metrics for dashboards and alerts.
- **IoT Telemetry**: Ingest high-volume sensor data from devices, gateways, and edge systems.
- **Application Analytics**: Track events, counters, timings, and product usage trends over time.
- **DevOps Observability**: Retain build, deployment, and runtime measurements for troubleshooting.
- **Real-Time Experiments**: Query recent time series data for operational analysis and prototypes.

## Dependencies for InfluxDB Hosting

The Sealos template includes the InfluxDB container image, persistent storage, a Kubernetes Service, HTTPS Ingress, and a Sealos App entry. No external database is required.

### Deployment Dependencies

- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/v2/) - Official documentation for InfluxDB 2.x
- [Docker Official Image](https://hub.docker.com/_/influxdb) - Supported InfluxDB container tags
- [InfluxDB GitHub Repository](https://github.com/influxdata/influxdb) - Source code and releases
- [Sealos](https://sealos.io) - Cloud platform used by this template

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **InfluxDB StatefulSet**: Runs `docker.io/library/influxdb:2.9.1` with `200m` CPU and `128Mi` memory limits, and stores data in `/var/lib/influxdb2`.
- **Persistent Volume**: Provides 1 GiB of durable storage for time series data and metadata.
- **Service**: Exposes the InfluxDB HTTP API and web UI on port `8086` inside the cluster.
- **Ingress**: Provides HTTPS access at the generated Sealos domain.
- **App Entry**: Adds a direct InfluxDB link in the Sealos Canvas.

**Configuration:**

The template uses InfluxDB's official first-run setup environment variables. Set the admin password and API token in the deployment form, then save them securely. The default organization is `sealos`, and the initial bucket is `primary`.

**License Information:**

InfluxDB is licensed under open source licenses published by InfluxData. This Sealos template is provided as a deployment wrapper for the official InfluxDB container image.

## Why Deploy InfluxDB on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle, from deployment to ongoing operations. By deploying InfluxDB on Sealos, you get:

- **One-Click Deployment**: Launch InfluxDB from the App Store without writing Kubernetes YAML.
- **Persistent Storage Included**: Keep time series data and metadata across restarts.
- **Instant Public Access**: Use an automatically provisioned HTTPS URL for the InfluxDB UI and API.
- **Easy Customization**: Adjust credentials, resources, and storage through the deployment form and Canvas.
- **Kubernetes Foundation**: Run on a cloud-native platform with service discovery, rollout management, and resource controls.
- **Pay-As-You-Go Resources**: Start with a small footprint and scale resources when ingestion or query volume grows.

## Deployment Guide

1. Open the [InfluxDB template](https://sealos.io/products/app-store/influxdb) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **Initial InfluxDB admin password**: Password for the `admin` web UI user.
   - **Initial InfluxDB API token**: Token for CLI, API, and client integrations.
3. Save the password and token securely before deploying. InfluxDB uses them during first initialization.
4. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
5. Access InfluxDB from the provided App URL.
6. Log in to the web UI with:
   - **Username**: `admin`
   - **Password**: the admin password you configured during deployment

InfluxDB does not provide public self-registration in this template. The initial admin account is created automatically during first startup.

## Configuration

After deployment, you can configure InfluxDB through:

- **InfluxDB UI**: Create buckets, tokens, dashboards, and data sources from the web interface.
- **InfluxDB API and CLI**: Use the API token configured during deployment for automation.
- **Sealos AI Dialog**: Describe resource or configuration changes and let AI apply updates.
- **Resource Cards**: Open the StatefulSet, Service, Ingress, or storage cards in Canvas to review or adjust settings.

## Scaling

To scale resources for higher ingestion or query volume:

1. Open the Canvas for your deployment.
2. Click the InfluxDB StatefulSet resource card.
3. Adjust CPU and memory resources according to your workload.
4. Increase persistent storage if your retention policy requires more capacity.
5. Apply the changes in the dialog and wait for the pod to become ready again.

## Troubleshooting

### Cannot log in

- Cause: The password entered in the UI does not match the value configured during first deployment.
- Solution: Use username `admin` and the initial admin password from the deployment form. If the value was lost, redeploy with a new password and token, or reset credentials manually inside InfluxDB.

### Pod is not ready

- Cause: The first initialization may still be running, or resource limits may be too small for the workload.
- Solution: Wait a few minutes, then check the StatefulSet logs from the Canvas. Increase memory if the pod restarts under load.

### API clients cannot authenticate

- Cause: The client token does not match the initial API token or a token created in the UI.
- Solution: Use the deployment token or create a new token from **Load Data → API Tokens** in the InfluxDB UI.

### Getting Help

- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/v2/)
- [InfluxDB Community](https://www.influxdata.com/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [InfluxDB Get Started](https://docs.influxdata.com/influxdb/v2/get-started/)
- [InfluxDB API Documentation](https://docs.influxdata.com/influxdb/v2/api/)
- [Line Protocol Reference](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/)

## License

This Sealos template is provided under the repository license. InfluxDB is licensed by InfluxData under the licenses published in the official project repository.
