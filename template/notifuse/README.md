# Deploy and Host Notifuse on Sealos

Notifuse is a transactional email platform with an interactive Setup Wizard, SMTP relay support, and multi-workspace isolation. This template deploys a production-ready Notifuse instance with PostgreSQL database on Sealos Cloud.

## About Hosting Notifuse

Notifuse runs as a single-service application that provides transactional email management through an intuitive web interface. The platform includes an interactive Setup Wizard that guides you through initial configuration, making it easy to get started without manual configuration files. The Sealos template automatically provisions a PostgreSQL database for storing email templates, delivery logs, workspace configurations, and user data. Persistent storage ensures your email data and settings are safely stored and survive restarts.

The deployment includes automatic SSL certificate provisioning, domain management, and integrated monitoring through the Sealos dashboard. The application waits for the database to be ready before starting, ensuring reliable initialization.

## Common Use Cases

- **Transactional Email Management**: Send password reset emails, verification codes, and notifications through a unified platform
- **Multi-Workspace Isolation**: Manage email campaigns for multiple clients or projects with complete data separation
- **SMTP Relay**: Use Notifuse as a relay to deliver emails through your existing SMTP server (Gmail, SendGrid, Amazon SES, etc.)
- **Email Template Management**: Create and manage reusable email templates with dynamic content
- **Delivery Tracking**: Monitor email delivery status, open rates, and click-through rates

## Dependencies for Notifuse Hosting

The Sealos template includes all required dependencies: PostgreSQL database, persistent storage, and SSL certificates.

### Deployment Dependencies

- [Notifuse Documentation](https://docs.notifuse.com/) - Official documentation
- [Notifuse GitHub Repository](https://github.com/notifuse/notifuse) - Source code and development
- [SMTP Configuration Guide](https://docs.notifuse.com/) - Setup instructions for SMTP providers

### Implementation Details

**Architecture Components:**

This template deploys two services:

- **Notifuse Application**: Main web application serving the UI, API, and email processing logic
- **PostgreSQL Database**: Database v14.8.0 for storing email templates, delivery logs, workspaces, and user data

**Configuration:**

The application includes an init container that waits for PostgreSQL to be ready before starting, ensuring reliable database connectivity. The Setup Wizard provides an interactive interface for configuring your SMTP settings and creating the root administrator account after deployment.

Key configuration aspects:
- **Root Email**: Required for initial administrator account creation
- **SMTP Settings**: Configure your existing SMTP server (Gmail, SendGrid, etc.) for email delivery
- **API Endpoint**: Automatically configured to use your Sealos deployment URL
- **Secret Key**: Auto-generated for secure session management

**License Information:**

Notifuse is an open-source transactional email platform. Check the [GitHub repository](https://github.com/notifuse/notifuse) for license details.

## Why Deploy Notifuse on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying Notifuse on Sealos, you get:

- **One-Click Deployment**: Deploy Notifuse with a single click. No YAML configuration, no container orchestration complexity - just point, click, and deploy.
- **Auto-Scaling Built-In**: Your application automatically scales up and down based on demand. Handle email traffic spikes without manual intervention.
- **Easy Customization**: Configure SMTP settings, root email, and resource limits with intuitive forms. Customize your setup without touching a single line of code.
- **Zero Kubernetes Expertise Required**: Get all the benefits of Kubernetes - high availability, service discovery, and container orchestration - without becoming a Kubernetes expert.
- **Persistent Storage Included**: Built-in PostgreSQL database with persistent storage ensures your email templates, logs, and settings are safe across deployments.
- **Instant Public Access**: Each deployment gets an automatic public URL with SSL certificates. Share your Notifuse instance instantly without complex networking setup.
- **Automated Backups**: Automatic backups and disaster recovery ensure your email data is always safe.

Deploy Notifuse on Sealos and focus on managing your email campaigns instead of managing infrastructure.

## Deployment Guide

1. Visit [Sealos Cloud](https://os.sealos.io/?openapp=system-brain?trial=true)
2. Click "From Template"
3. Search for "Notifuse" in the App Store
4. Configure your deployment parameters:
   - **Root Email**: Your administrator email address (e.g., admin@yourcompany.com)
   - **SMTP Host**: SMTP server host (e.g., smtp.gmail.com)
   - **SMTP Port**: SMTP server port (default: 587)
   - **SMTP Username**: SMTP username (e.g., noreply@yourcompany.com)
   - **SMTP Password**: SMTP password for authentication
   - **SMTP From Email**: Default sender email address
   - **SMTP From Name**: Default sender name (optional)
5. Click "Deploy"
6. Wait for deployment to complete (typically 1-2 minutes)
7. Access Notifuse via the provided URL (shown in the canvas)
8. Complete the Setup Wizard to create your admin account and verify SMTP configuration

## Configuration

After deployment, you can customize your Notifuse instance:

### Initial Setup

1. **Complete Setup Wizard**: On first access, the interactive wizard will guide you through creating your admin account
2. **Verify SMTP Configuration**: Send a test email to ensure your SMTP settings are correct
3. **Create First Workspace**: Set up your initial workspace for email campaigns

### Managing Workspaces

Notifuse supports multi-workspace isolation:

- Create separate workspaces for different clients or projects
- Each workspace has isolated email templates, delivery logs, and settings
- Configure SMTP providers per workspace or use a global relay

### SMTP Configuration

**Common SMTP Providers:**

- **Gmail**: Use `smtp.gmail.com` with port `587`. You may need to create an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.
- **SendGrid**: Use `smtp.sendgrid.net` with port `587` or `465`.
- **Amazon SES**: Use the SMTP endpoint provided in your AWS SES console.
- **Mailgun**: Use `smtp.mailgun.org` with port `587`.
- **Postmark**: Use `smtp.postmarkapp.com` with port `587` or `2587`.

**Troubleshooting SMTP:**
- Verify username and password are correct
- Check if your SMTP provider requires IP whitelisting
- Ensure ports 587 (STARTTLS) or 465 (SSL) are not blocked
- Test SMTP connection using telnet or openssl tools

### Service Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Web UI | `https://<app-host>.<domain>` | Admin dashboard and workspace management |
| API Endpoint | `https://<app-host>.<domain>` | REST API for programmatic access |
| PostgreSQL | `<app-name>-pg-postgresql.<namespace>.svc:5432` | Database (internal cluster communication) |

## Scaling

To scale your Notifuse deployment:

1. Open App Launchpad
2. Select your Notifuse deployment
3. Adjust CPU/Memory resources in the application settings
4. Click "Update" to apply changes

For high-volume email sending, consider:
- Increasing CPU and memory allocation
- Scaling PostgreSQL storage for larger log retention
- Using a dedicated SMTP provider for better deliverability

## Troubleshooting

### Common Issues

**Email delivery fails:**
- Cause: SMTP credentials are incorrect or the SMTP provider requires additional configuration
- Solution: Verify your SMTP settings in the Notifuse dashboard. Check that your SMTP provider allows relaying from your IP address.

**Setup Wizard doesn't appear:**
- Cause: The application may still be initializing
- Solution: Wait 1-2 minutes for the application to fully start, then refresh the page

**Database connection errors:**
- Cause: PostgreSQL is still starting up
- Solution: The init container will automatically wait for the database. If issues persist, check the application logs in the Sealos dashboard.

### Getting Help

- [Notifuse Documentation](https://docs.notifuse.com/)
- [Notifuse GitHub Issues](https://github.com/notifuse/notifuse/issues)
- [Sealos Discord](https://discord.gg/sealos)

## Additional Resources

- [Notifuse API Documentation](https://docs.notifuse.com/)
- [SMTP Provider Setup Guides](https://docs.notifuse.com/)
- [Email Template Best Practices](https://docs.notifuse.com/)

## License

This Sealos template is provided under the same license as Notifuse. Refer to the [Notifuse GitHub repository](https://github.com/notifuse/notifuse) for license details.
