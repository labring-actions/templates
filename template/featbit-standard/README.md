# Deploy and Host FeatBit Standard on Sealos

FeatBit Standard is an open-source feature flag and experimentation platform for progressive delivery. This template deploys FeatBit Standard as a multi-service application with PostgreSQL, Redis, public UI, API, and evaluation endpoints on Sealos Cloud.

![FeatBit Standard Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/featbit-standard/website-screenshot.webp)

## About Hosting FeatBit Standard

FeatBit helps teams release features safely by separating deployment from release. Developers can create feature flags, target users or segments, run controlled rollouts, and evaluate changes without redeploying the application.

This Sealos template runs the Standard Edition using four application services: a web UI, an API server, a data analytics server, and an evaluation server. Sealos also provisions PostgreSQL for FeatBit data and Redis for messaging, cache, and runtime coordination.

The template includes automatic public HTTPS endpoints for the UI, API, and evaluation service. Database credentials and service discovery are wired through Sealos-managed Kubernetes resources, so you can deploy the full stack without manually preparing infrastructure.

## Common Use Cases

- **Feature Flag Management**: Roll out features gradually, disable risky changes quickly, and manage release state independently from deployments.
- **Progressive Delivery**: Target features to specific environments, users, or segments before a full release.
- **Experimentation**: Run controlled product experiments and compare feature behavior across audiences.
- **Kill Switches**: Add operational controls for high-risk features, integrations, or backend behavior.
- **Developer Platform Enablement**: Provide product and engineering teams with a centralized flag management system.

## Dependencies for FeatBit Standard Hosting

The Sealos template includes all required runtime dependencies: FeatBit UI, API server, data analytics server, evaluation server, PostgreSQL 16.4, Redis 7.2, Kubernetes Services, Ingress resources, and an initialization Job for the FeatBit database schema.

### Deployment Dependencies

- [FeatBit Official Website](https://www.featbit.co/) - Product overview and feature information
- [FeatBit Documentation](https://docs.featbit.co/) - Official usage and administration documentation
- [FeatBit GitHub Repository](https://github.com/featbit/featbit) - Source code, releases, and issue tracking
- [Sealos App Store](https://sealos.io/products/app-store/featbit-standard) - One-click deployment entry

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **UI Service**: Hosts the FeatBit web console for managing feature flags, environments, targeting rules, and rollout settings.
- **API Server**: Provides the backend API used by the UI and integrations.
- **Data Analytics Server**: Processes analytics and operational data used by FeatBit.
- **Evaluation Server**: Serves feature evaluation traffic for SDK and runtime access.
- **PostgreSQL**: Stores application data, configuration, users, environments, flags, and schema-managed records.
- **Redis**: Provides cache, message, and coordination support required by FeatBit services.

**Configuration:**

The template exposes three public endpoints by default: one for the UI, one for the API server, and one for the evaluation server. The UI is configured with the generated API and evaluation URLs during deployment.

PostgreSQL and Redis are created as managed database clusters. The application services receive database host, port, username, and password values from Sealos-managed secrets, while internal services communicate through Kubernetes service discovery.

The application containers are tuned to the smallest validated Sealos resource ladder profile for this template: UI, API, and evaluation services run with `100m` CPU and `128Mi` memory limits, while the data analytics server runs with `100m` CPU and `512Mi` memory limits. PostgreSQL and Redis use the database resource profile required by the Sealos database template rules.

**License Information:**

FeatBit is released as an open-source project. Review the [FeatBit repository](https://github.com/featbit/featbit) for the current application license and component-specific notices.

## Why Deploy FeatBit Standard on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle, from development in cloud IDEs to production deployment and management. It is suitable for SaaS platforms, developer tools, and multi-service applications that need managed networking, storage, and operations. By deploying FeatBit Standard on Sealos, you get:

- **One-Click Deployment**: Deploy the complete FeatBit stack from the App Store without writing Kubernetes YAML.
- **Managed Databases**: PostgreSQL and Redis are provisioned together with the application and connected through managed secrets.
- **Instant Public Access**: The UI, API, and evaluation service receive public HTTPS endpoints automatically.
- **Resource Efficiency**: The template uses validated resource settings on the Sealos ladder, helping control cost while keeping the services runnable.
- **Easy Customization**: Adjust environment variables, resource limits, or replicas from the Canvas after deployment.
- **AI-Assisted Operations**: Describe the change you need in the Sealos AI dialog, or open resource cards to edit specific workloads.
- **Kubernetes Foundation**: Run FeatBit on Kubernetes-backed infrastructure without managing cluster internals yourself.

Deploy FeatBit Standard on Sealos and focus on release management instead of infrastructure setup.

## Deployment Guide

1. Open the [FeatBit Standard template](https://sealos.io/products/app-store/featbit-standard) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. The default generated names and hostnames are enough for a standard deployment.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URLs:
   - **FeatBit UI**: Open the generated UI URL and use the FeatBit console.
   - **API Endpoint**: Use the generated API URL for backend or integration access.
   - **Evaluation Endpoint**: Use the generated evaluation URL for SDK or runtime evaluation traffic.

## Configuration

After deployment, you can configure FeatBit Standard through:

- **AI Dialog**: Describe the changes you want, such as resource adjustments or environment variable updates, and let AI apply them.
- **Resource Cards**: Open the UI, API server, data analytics server, evaluation server, PostgreSQL, or Redis resource cards to inspect and modify settings.
- **FeatBit Console**: Manage feature flags, environments, users, segments, and rollout rules from the web UI.
- **Public Endpoints**: Use the generated API and evaluation URLs when configuring SDKs or integrations.

## Scaling

To scale FeatBit Standard:

1. Open the Canvas for your deployment.
2. Click the relevant Deployment resource card, such as the API server, evaluation server, or UI.
3. Adjust CPU, memory, or replica count based on traffic and evaluation load.
4. Apply the changes in the dialog and monitor the workload status.

For database-related scaling, open the PostgreSQL or Redis resource card and review the available database options before applying changes.

## Troubleshooting

### Common Issues

**The UI loads but API requests fail**
- Cause: The API endpoint or generated API hostname may not match the deployed public URL.
- Solution: Open the UI and API resource cards in Canvas and confirm that the UI environment points to the generated API URL.

**SDK evaluation requests fail**
- Cause: The SDK may be configured with the UI URL instead of the evaluation endpoint.
- Solution: Use the generated evaluation URL for SDK or runtime evaluation traffic.

**Services wait for database initialization**
- Cause: FeatBit services depend on the PostgreSQL schema created by the initialization Job.
- Solution: Check the PostgreSQL cluster and initialization Job status in Canvas, then restart dependent services if needed.

### Getting Help

- [FeatBit Documentation](https://docs.featbit.co/)
- [FeatBit GitHub Issues](https://github.com/featbit/featbit/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [FeatBit Website](https://www.featbit.co/)
- [FeatBit Documentation](https://docs.featbit.co/)
- [FeatBit GitHub Repository](https://github.com/featbit/featbit)
- [Sealos](https://sealos.io/)

## License

This Sealos template is provided under the license used by the template repository. FeatBit itself is licensed by the FeatBit project; review the [FeatBit GitHub repository](https://github.com/featbit/featbit) for current license details.
