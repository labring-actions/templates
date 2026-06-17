# Deploy and Host Nacos on Sealos

Nacos is a dynamic service discovery, configuration, and service management platform. This template deploys Nacos 3.2.2 with tuned Nacos JVM memory, a separate console, a standalone Nacos server, persistent storage, and a Sealos-managed MySQL database on Sealos Cloud.

## About Hosting Nacos

Nacos provides naming, service discovery, configuration management, namespace isolation, and console-based operations for microservice platforms. The Sealos template provisions the Nacos console and server as separate StatefulSets so that the web console can be exposed publicly while the service endpoint remains available inside the cluster.

The deployment also provisions a KubeBlocks MySQL 8.0 cluster and runs the Nacos schema initialization job before the application starts using the external database. Persistent volumes store Nacos logs and runtime data across restarts.

## Common Use Cases

- **Microservice service discovery**: Register services and discover healthy instances from applications running in Kubernetes or other environments.
- **Centralized configuration management**: Manage shared configuration, publish changes, and track configuration history.
- **Environment isolation**: Use namespaces to separate development, staging, and production service metadata.
- **AI and plugin registry experiments**: Use Nacos 3.x registry capabilities for newer plugin, prompt, and agent metadata workflows.

## Dependencies for Nacos Hosting

The Sealos template includes all required runtime dependencies: two Nacos application components, a MySQL database, schema initialization, persistent volumes, internal Services, an HTTPS Ingress for the console, and a Sealos App link.

### Deployment Dependencies

- [Nacos Documentation](https://nacos.io/en/docs/latest/overview/) - Official Nacos documentation
- [Nacos Docker Repository](https://github.com/nacos-group/nacos-docker) - Official Docker image and compose examples
- [Nacos GitHub Repository](https://github.com/alibaba/nacos) - Source code and release notes

### Implementation Details

**Architecture Components:**

This template deploys four main components:

- **Nacos Console**: Public web console on port 8080, exposed through Sealos Ingress.
- **Nacos Server**: Internal Nacos server on ports 8848 and 9848 for service discovery and client RPC.
- **MySQL**: KubeBlocks-managed MySQL 8.0 database for configuration, user, role, and metadata storage.
- **Initialization Job**: Loads the Nacos MySQL schema into the `nacos_devtest` database before the application components finish startup.

**Configuration:**

- Authentication is enabled for the console and server APIs.
- Console and server use `JVM_XMS=512m`, `JVM_XMX=512m`, and `JVM_XMN=256m`; each Nacos component is capped at 1024Mi memory for the validated single-node profile.
- The first console visit initializes the fixed admin username `nacos`; set your own password on that screen, then log in with `nacos` and the password you created.
- `auth_token` is generated automatically as the JWT signing secret used by Nacos authentication. If you change it later, keep the same value on both Nacos components.
- Console access uses `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`.

**License Information:**

Nacos is licensed under the Apache License 2.0. This Sealos template is provided under the repository license for Sealos templates.

## Why Deploy Nacos on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, networking, storage, and application management. By deploying Nacos on Sealos, you get:

- **One-Click Deployment**: Launch Nacos with MySQL, persistent storage, HTTPS routing, and application metadata from one template.
- **Managed Kubernetes Runtime**: Run Nacos on Kubernetes without manually writing StatefulSets, Services, Ingresses, or database resources.
- **Persistent Storage Included**: Keep Nacos logs and runtime data across pod restarts.
- **Integrated Database Provisioning**: Use a Sealos-managed MySQL cluster instead of maintaining a separate database by hand.
- **Public Console Access**: Open the Nacos console from a generated HTTPS URL after deployment.

## Deployment Guide

1. Open the [Nacos template](https://sealos.io/products/app-store/nacos) and click **Deploy Now**.
2. Configure the deployment parameters in the popup dialog. The template automatically generates the Nacos authentication token.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access the Nacos console via the generated public URL.
5. On the first visit, set the admin password for the fixed username `nacos`.
6. After initialization, log in with username `nacos` and the password you created.

## Configuration

After deployment, you can configure Nacos through:

- **Nacos Console**: Manage namespaces, configurations, services, users, roles, and permissions.
- **AI Dialog**: Describe resource or environment changes and let Sealos apply updates.
- **Resource Cards**: Click the StatefulSet, database, or Ingress cards on the Canvas to adjust settings.
- **Client Configuration**: Connect internal clients to the Nacos server Service on port 8848.

## Scaling

The template is tuned for a single-node Nacos deployment with persistent storage and MySQL. To increase resources, open the Canvas, select the relevant StatefulSet resource card, and adjust CPU or memory. For high-availability Nacos clusters, review the official Nacos clustering documentation before changing replica counts.

## Troubleshooting

### First login redirects to the initialization page

This is expected when no global admin user exists yet. Set the password for username `nacos`, submit the form, then return to the login page and sign in with that password.

### Login fails after changing the JWT secret

All Nacos components must use the same `auth_token` value. Update both application components consistently if you modify the generated token after deployment.

### Nacos cannot connect to the database

Check that the MySQL cluster is running and that the schema initialization Job completed successfully. If the Job failed, inspect its logs from the Canvas or with kubectl.

## Additional Resources

- [Nacos Quick Start](https://nacos.io/en/docs/latest/quickstart/quick-start-docker/)
- [Nacos Authentication Guide](https://nacos.io/en/docs/latest/manual/admin/auth/)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the repository license. Nacos itself is licensed under the Apache License 2.0.
