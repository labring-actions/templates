# Deploy and Host TeslaMate on Sealos

TeslaMate is a self-hosted data logger for Tesla vehicles. This template deploys TeslaMate with PostgreSQL, Mosquitto, and Grafana on Sealos Cloud.

![TeslaMate Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/teslamate/website-screenshot.webp)

## About Hosting TeslaMate

TeslaMate records vehicle data, stores it in PostgreSQL, and exposes a web UI for Tesla account sign-in and vehicle state. It also publishes telemetry events through Mosquitto for integrations such as Home Assistant.

The template provisions a KubeBlocks PostgreSQL database, a private Mosquitto broker, the TeslaMate web application, and a Grafana dashboard service. Sealos provides HTTPS ingress, persistent volumes, lifecycle management, and resource controls through the Canvas.

## Common Use Cases

- **Vehicle History**: Track drives, charges, locations, and efficiency over time.
- **Energy Monitoring**: Review charging sessions and long-term consumption trends.
- **Home Automation**: Feed vehicle state into MQTT-based automation systems.
- **Dashboarding**: Explore TeslaMate Grafana dashboards for fleet and trip analytics.

## Dependencies for TeslaMate Hosting

The Sealos template includes TeslaMate, Grafana, Mosquitto, and KubeBlocks PostgreSQL.

### Deployment Dependencies

- [TeslaMate Documentation](https://docs.teslamate.org/) - Official documentation
- [Docker Installation Guide](https://docs.teslamate.org/docs/installation/docker) - Official Docker runtime layout
- [GitHub Repository](https://github.com/teslamate-org/teslamate) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys four services:

- **TeslaMate**: Main web application on port 4000.
- **Grafana**: Dashboard service on port 3000 with persistent storage.
- **Mosquitto**: Private MQTT broker for TeslaMate event publishing.
- **PostgreSQL**: KubeBlocks-managed database for vehicle and telemetry data.

**Configuration:**

TeslaMate connects to PostgreSQL through KubeBlocks credentials and connects to Mosquitto through Kubernetes service DNS. Grafana uses the same PostgreSQL database and is exposed through its own HTTPS ingress. The encryption key is generated during deployment and used for Tesla API token encryption.

**License Information:**

TeslaMate is licensed under the MIT License. This Sealos template is provided under the repository license.

## Why Deploy TeslaMate on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operations, and scaling. By deploying TeslaMate on Sealos, you get:

- **One-Click Deployment**: Deploy TeslaMate and its supporting services from the App Store template.
- **Managed PostgreSQL**: Use KubeBlocks-managed PostgreSQL with persistent storage.
- **Instant HTTPS Access**: Receive public HTTPS URLs for TeslaMate and Grafana.
- **Canvas Operations**: Change resources, inspect services, and apply updates through Canvas, AI dialog, and resource cards.
- **Pay-as-You-Go Resources**: Run the monitoring stack with resource limits sized for the deployment.

## Deployment Guide

1. Open the [TeslaMate template](https://sealos.io/products/app-store/teslamate) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URLs:
   - **TeslaMate UI**: Sign in with your Tesla account and complete the TeslaMate setup flow.
   - **Grafana Dashboard**: Open the Grafana URL, log in with the initial Grafana credentials shown by the application, then set a secure password.

## Configuration

After deployment, you can configure TeslaMate through:

- **TeslaMate UI**: Connect your Tesla account and manage vehicle tracking.
- **Grafana UI**: Review dashboards and update Grafana user settings.
- **AI Dialog**: Describe runtime changes and let AI apply updates.
- **Resource Cards**: Adjust CPU, memory, storage, or ingress settings.

## Scaling

To scale or tune TeslaMate:

1. Open the Canvas for your deployment.
2. Click the TeslaMate, Grafana, Mosquitto, or PostgreSQL resource card.
3. Adjust CPU, memory, storage, or replica settings.
4. Apply the changes in the dialog.

## Troubleshooting

### Tesla account sign-in cannot complete

- Cause: Tesla API authentication or network access is unavailable.
- Solution: Reopen the TeslaMate UI, retry the Tesla account flow, and verify the deployment can reach external Tesla services.

### Grafana asks for an initial password

- Cause: Grafana requires the first login flow after deployment.
- Solution: Use the Grafana initial credentials, then set a secure password when prompted.

### MQTT integrations cannot connect

- Cause: Mosquitto is private inside the deployment by default.
- Solution: Connect integrations from services inside the same namespace, or expose MQTT intentionally through a controlled network path.

## Additional Resources

- [TeslaMate FAQ](https://docs.teslamate.org/docs/faq)
- [TeslaMate MQTT Integration](https://docs.teslamate.org/docs/integrations/mqtt)
- [Sealos](https://sealos.io)

## License

This Sealos template is provided under the repository license. TeslaMate itself is licensed under the MIT License.
