# Deploy and Host Stalwart on Sealos

Stalwart is an open-source mail and collaboration server with SMTP, IMAP, JMAP, CalDAV, CardDAV, WebDAV, spam filtering, and a web administration console. This template deploys Stalwart with a PostgreSQL data store on Sealos Cloud.

![Stalwart Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/stalwart/website-screenshot.webp)

## About Hosting Stalwart

Stalwart runs as a single-node mail and collaboration server backed by a Sealos-managed PostgreSQL database. The template follows Stalwart's official Kubernetes runtime model: a StatefulSet starts the container with `/etc/stalwart/config.json`, uses PostgreSQL as the external DataStore, and exposes the HTTP administration listener through Sealos Ingress.

The deployment provisions PostgreSQL automatically, creates the `stalwart` database, and waits for the database before starting the Stalwart container. The web administration console is available at `/admin`, while mail protocols require additional L4 port exposure and DNS records before production mail delivery.

## Common Use Cases

- **Business Mail Hosting**: Host SMTP, IMAP, POP3, and submission services for a managed domain.
- **Collaboration Server**: Provide calendars, contacts, file sharing, and JMAP-compatible access.
- **Mail Security Gateway**: Use Stalwart's spam and phishing protection for inbound and outbound mail.
- **Self-Hosted Mail Lab**: Test mail-server configuration, DNS records, and client compatibility.

## Dependencies for Stalwart Hosting

The Sealos template includes Stalwart, a PostgreSQL 16.4 KubeBlocks cluster, a database initialization Job, a Kubernetes StatefulSet, a Service, an Ingress, and a Sealos App link.

### Deployment Dependencies

- [Official Website](https://stalw.art/) - Stalwart product information
- [Official Documentation](https://stalw.art/docs/) - Installation and configuration guides
- [Kubernetes Deployment Guide](https://stalw.art/docs/cluster/orchestration/kubernetes/) - Official Kubernetes runtime model
- [GitHub Repository](https://github.com/stalwartlabs/stalwart) - Source code and releases

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Stalwart StatefulSet**: Runs `stalwartlabs/stalwart:v0.16.7` with the official `--config /etc/stalwart/config.json` startup contract.
- **PostgreSQL**: Stores Stalwart's primary data using the official PostgreSQL DataStore configuration.
- **Database Init Job**: Creates the `stalwart` database after PostgreSQL becomes reachable.
- **Sealos Ingress**: Publishes the web administration console and health endpoints over HTTPS.
- **Optional Object Storage**: When enabled, provisions a Sealos ObjectStorageBucket and injects S3-compatible credentials for later blob-store configuration in the WebUI.

**Configuration:**

- Log in at `/admin` with username `admin` and the bootstrap password configured during deployment.
- Health endpoints are available at `/healthz/live` and `/healthz/ready`.
- Stalwart's WebUI is used to configure domains, DNS records, DKIM, TLS certificates, accounts, and storage backends.
- For S3 blob storage, enable object storage during deployment, then configure the S3-compatible BlobStore in **Settings > Storage > Blob Store** with the injected credentials.

**Mail DNS and Ports:**

Sealos Ingress exposes the HTTPS administration endpoint. SMTP, submission, IMAP, POP3, and ManageSieve are L4 protocols, so production mail hosting also needs explicit TCP exposure for the required ports, MX/SPF/DKIM/DMARC records, reverse DNS, and provider-side outbound mail policy review.

**License Information:**

Stalwart is licensed under the AGPL-3.0 license. This Sealos template is provided under the repository license.

## Why Deploy Stalwart on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Stalwart on Sealos, you get:

- **One-Click Deployment**: Deploy Stalwart with PostgreSQL from the App Store template.
- **Kubernetes Foundation**: Run Stalwart as a managed Kubernetes workload with persistent database storage.
- **Easy Customization**: Adjust environment variables, resources, and storage from the Canvas.
- **Public HTTPS Access**: Access the WebUI through an automatic HTTPS URL.
- **Pay-As-You-Go Resources**: Start with a compact resource profile and scale when mail volume grows.

## Deployment Guide

1. Open the [Stalwart template](https://sealos.io/products/app-store/stalwart) and click **Deploy Now**.
2. Configure the bootstrap administrator password and choose whether to provision Sealos object storage.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **Web Admin**: Open `https://[your-stalwart-url]/admin` and log in with username `admin` and your bootstrap password.
   - **Health Check**: Use `/healthz/live` and `/healthz/ready` for web health monitoring.

## Configuration

After deployment, complete mail-server setup in the Stalwart WebUI:

- **Domains**: Add your mail domains and review generated DNS records.
- **Accounts**: Create mail users and administrator accounts.
- **DNS**: Publish MX, SPF, DKIM, DMARC, MTA-STS, and related records for real mail delivery.
- **Ports**: Expose required TCP ports for SMTP, submission, IMAP, POP3, and ManageSieve through a suitable L4 path.
- **Object Storage**: Configure S3-compatible blob storage in the WebUI when object storage was enabled during deployment.
- **Canvas**: Use the Sealos Canvas, AI dialog, and resource cards for resource and environment updates.

## Scaling

Start with the default single-node deployment for setup and evaluation. For production mail hosting, review CPU, memory, database capacity, TCP exposure, DNS reputation, and backup requirements before increasing load.

To adjust resources:

1. Open the Canvas for your deployment.
2. Click the Stalwart StatefulSet or PostgreSQL resource card.
3. Adjust CPU, memory, storage, or operational parameters.
4. Apply the changes in the dialog.

## Troubleshooting

### Admin Login

- Cause: The bootstrap password was entered incorrectly.
- Solution: Use username `admin` with the password configured during deployment.

### Health Endpoints

- Cause: PostgreSQL is still starting or the database initialization Job has not completed.
- Solution: Wait for PostgreSQL and the Stalwart StatefulSet to become ready, then retry `/healthz/ready`.

### Mail Delivery

- Cause: Web HTTPS access is working, while mail protocol ports or DNS records are still incomplete.
- Solution: Configure L4 TCP exposure and publish the DNS records generated by Stalwart before sending production mail.

### Getting Help

- [Official Documentation](https://stalw.art/docs/)
- [GitHub Issues](https://github.com/stalwartlabs/stalwart/issues)
- [Stalwart Community](https://github.com/stalwartlabs/stalwart#community)

## Additional Resources

- [Docker Installation Guide](https://stalw.art/docs/install/platform/docker/)
- [PostgreSQL Backend Docs](https://stalw.art/docs/storage/backends/postgresql/)
- [S3-Compatible Backend Docs](https://stalw.art/docs/storage/backends/s3/)
- [DNS Setup Guide](https://stalw.art/docs/install/dns/)

## License

This Sealos template is provided under the repository license. Stalwart itself is licensed under AGPL-3.0.
