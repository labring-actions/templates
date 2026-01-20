# Deploy and Host n8n on Sealos

n8n is a powerful workflow automation platform that combines the flexibility of code with the speed of no-code, enabling technical teams to build complex automation workflows with ease. This template provides one-click deployment of a production-ready n8n instance with optional PostgreSQL database and Redis queue mode, allowing you to create sophisticated automation workflows and integrations on Sealos Cloud.

## About Hosting n8n

n8n runs as a Node.js application that provides a visual workflow editor and execution engine for automating tasks across hundreds of different services and APIs. The platform supports both simple automations and complex multi-step workflows with conditional logic, loops, and data transformations.

The Sealos template offers flexible deployment options: you can start with a lightweight SQLite-based setup for testing, upgrade to PostgreSQL for production workloads with better performance and data persistence, or enable queue mode with Redis for improved scalability and parallel execution. The deployment includes automatic initialization, persistent storage for workflow data, and secure public access with SSL certificates.

## Common Use Cases

- **API Integration and Data Sync**: Connect different services and sync data between platforms automatically
- **Business Process Automation**: Automate repetitive tasks like data entry, report generation, and notifications
- **Data Processing Pipelines**: Build ETL workflows to extract, transform, and load data between systems
- **Webhook Processing**: Receive and process webhooks from external services with custom logic
- **Scheduled Tasks**: Run workflows on schedules using cron expressions for periodic automation
- **Customer Communication**: Automate email campaigns, notifications, and customer support workflows
- **DevOps Automation**: Integrate CI/CD pipelines, monitoring alerts, and deployment workflows
- **Content Management**: Automate content publishing, social media posting, and content aggregation

## Dependencies for n8n Hosting

The Sealos template includes all required components: n8n application server with optional PostgreSQL database and Redis for queue mode.

### Deployment Dependencies

- [n8n Documentation](https://docs.n8n.io/) - Official n8n documentation
- [n8n Quickstart Guide](https://docs.n8n.io/try-it-out/) - Getting started with n8n
- [n8n Workflow Examples](https://n8n.io/workflows) - Community workflow templates
- [n8n Node Reference](https://docs.n8n.io/integrations/) - Available integrations and nodes
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Database backend documentation
- [Redis Documentation](https://redis.io/docs/) - Queue backend documentation

## Implementation Details

### Architecture Components

This template supports three deployment modes:

**1. Basic Mode (Default):**
- **n8n Application**: Workflow automation server with SQLite database
  - Version: n8n 2.1.4
  - Web UI: Port 5678 (exposed via Ingress with SSL)
  - Persistent storage: 1Gi for workflow data and SQLite database
  - Suitable for: Testing, development, and light production workloads

**2. PostgreSQL Mode:**
- **PostgreSQL Database**: Persistent data storage for workflows and executions
  - Version: PostgreSQL 14.8.0
  - Persistent storage: 1Gi
  - Automatic database initialization with 'n8n' database
  - Connection credentials managed via Kubernetes secrets
- **n8n Application**: Connected to PostgreSQL for better performance
  - Suitable for: Production workloads with high reliability requirements

**3. Queue Mode (Requires PostgreSQL):**
- **PostgreSQL Database**: Same as PostgreSQL mode
- **Redis**: Message queue for workflow execution
  - Version: Redis 7.0.6
  - Persistent storage: 1Gi
  - Includes Redis Sentinel for high availability
- **n8n Main Process**: Workflow editor and API server
- **n8n Worker**: Dedicated workflow execution worker
  - Supports parallel execution of workflows
  - Scalable for high-volume automation
- **n8n Runners**: External task runners for isolated code execution
  - Separate runners for main process and worker
  - Enhanced security through isolated execution environment
  - Suitable for: High-traffic production environments with many concurrent workflows

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| n8n (Basic/PostgreSQL) | 50m | 500m | 51Mi | 512Mi |
| n8n Worker (Queue Mode) | 20m | 200m | 51Mi | 512Mi |
| n8n Runners (Queue Mode) | 20m | 200m | 25Mi | 256Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |
| Redis | 50m | 500m | 51Mi | 512Mi |
| Redis Sentinel | 100m | 100m | 100Mi | 100Mi |

### Environment Configuration

The template automatically configures n8n with the following settings:

**Basic Configuration:**
- Port: 5678
- Webhook URL: Automatic (based on your deployment domain)
- Timezone: Configurable (default: America/New_York)
- Encryption Key: Automatically generated 32-character random string

**Database Configuration (when PostgreSQL is enabled):**
- Client: PostgreSQL
- Connection: Automatic via Kubernetes secrets
- Database name: `n8n`
- SSL: Disabled (internal cluster communication)

**Queue Configuration (when queue mode is enabled):**
- Execution Mode: Queue
- Redis Connection: Automatic via Kubernetes secrets
- Worker Concurrency: 10 concurrent workflow executions
- Health Checks: Enabled for both main process and workers

**Public URLs:**
- Web UI: `https://<app-host>.<domain>/`
- Webhook Endpoint: `https://<app-host>.<domain>/webhook/`
- Production Webhook: `https://<app-host>.<domain>/webhook-test/`

### Deployment Process

The deployment process varies by mode:

**Basic Mode:**
1. **Application Deployment**: n8n starts with SQLite database
2. **Persistent Storage**: Workflow data stored in persistent volume

**PostgreSQL Mode:**
1. **Database Initialization Job**: Creates the `n8n` database in PostgreSQL
2. **Application Deployment**: n8n connects to PostgreSQL and initializes schema

**Queue Mode:**
1. **Redis Deployment**: Redis cluster with Sentinel for high availability
2. **PostgreSQL Deployment**: Database for persistent storage
3. **Database Initialization Job**: Creates the `n8n` database
4. **Main Process Deployment**: n8n web UI and API server
5. **Runners Deployment**: External task runners for main process
6. **Worker Deployment**: Dedicated workflow execution worker
7. **Worker Runners Deployment**: External task runners for worker

All deployments include automatic health checks and are ready to use immediately after completion.

## Why Deploy n8n on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying n8n on Sealos, you get:

- **One-Click Deployment**: Deploy n8n with optional PostgreSQL and Redis in seconds. No complex configuration or Kubernetes expertise required.
- **Flexible Architecture**: Choose between SQLite for simplicity, PostgreSQL for production reliability, or queue mode for high-scale automation.
- **Pre-Configured Databases**: PostgreSQL and Redis are automatically provisioned, initialized, and connected with secure credentials.
- **Persistent Storage**: Built-in persistent storage ensures your workflows, credentials, and execution history survive restarts and updates.
- **Secure Public Access**: n8n gets automatic public URL with SSL certificate, allowing secure access to the web UI and webhook endpoints.
- **Timezone Support**: Configure your instance timezone for accurate scheduled workflow execution.
- **Easy Scaling**: Adjust resources through intuitive forms as your automation needs grow.
- **Automatic Security**: Encryption keys and database credentials are generated automatically with cryptographically secure random values.
- **Worker Scalability**: Queue mode enables horizontal scaling of workflow execution for high-volume automation.

Deploy n8n on Sealos and focus on building powerful automation workflows instead of managing infrastructure.

## Deployment Guide

1. Visit [n8n Template Page](https://sealos.io/products/app-store/n8n)
2. Click the "Deploy Now" button
3. Configure your deployment options:
   - **Use PostgreSQL**: Enable for production workloads (recommended for better performance and data persistence)
   - **Timezone**: Select your timezone for accurate scheduled workflow execution
   - **Use Queue Mode**: Enable for high-scale automation with parallel execution (requires PostgreSQL)
4. Wait for deployment to complete (typically 1-2 minutes)
5. Access n8n via the provided URL (shown in the canvas)
6. Create your admin account on first access

## Configuration

After deployment, you can customize your n8n instance:

### Initial Setup

1. **Create Owner Account**: On first access, you'll be prompted to create an owner account with email and password
2. **Explore Workflow Templates**: Browse the template library to get started quickly
3. **Configure Credentials**: Add credentials for the services you want to integrate
4. **Create Your First Workflow**: Use the visual editor to build your first automation

### Deployment Modes

**When to use each mode:**

- **Basic Mode (SQLite)**:
  - ✅ Testing and development
  - ✅ Personal automation projects
  - ✅ Low-volume workflows (< 100 executions/day)
  - ❌ Not recommended for production with multiple users

- **PostgreSQL Mode**:
  - ✅ Production deployments
  - ✅ Multi-user environments
  - ✅ Medium-volume workflows (100-1000 executions/day)
  - ✅ When you need reliable data persistence

- **Queue Mode**:
  - ✅ High-volume automation (> 1000 executions/day)
  - ✅ Workflows that need parallel execution
  - ✅ When you need to scale workflow execution independently
  - ✅ Production environments with high reliability requirements

### Resource Scaling

Adjust resources in the canvas based on your needs:
- **CPU/Memory (Main Process)**: Increase for better UI performance and handling more concurrent users
- **CPU/Memory (Worker)**: Increase for faster workflow execution and more concurrent workflows
- **Storage**: Expand for more workflow history and execution data

### Timezone Configuration

The timezone setting is critical for scheduled workflows:
- Affects all Cron nodes and scheduled triggers
- Can be changed after deployment by updating the deployment environment variables
- Supported timezones include major cities across all continents

### Service Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Web UI | `https://<app-host>.<domain>` | Workflow editor and management interface |
| Webhook | `https://<app-host>.<domain>/webhook/<workflow-id>` | Production webhook endpoints |
| Test Webhook | `https://<app-host>.<domain>/webhook-test/<workflow-id>` | Test webhook endpoints |
| PostgreSQL | `<app-name>-pg-postgresql.<namespace>.svc:5432` | Database (internal, if enabled) |
| Redis | `<app-name>-redis-redis.<namespace>.svc:6379` | Queue (internal, if queue mode enabled) |

## Troubleshooting

### Common Issues

**Issue 1: Cannot Create Owner Account**
- Cause: First-time setup not completed
- Solution: Access the web UI URL and follow the owner account creation wizard. This is required on first deployment.

**Issue 2: Scheduled Workflows Running at Wrong Time**
- Cause: Timezone configuration mismatch
- Solution: Verify the timezone setting in the deployment configuration matches your expected timezone. Update the `GENERIC_TIMEZONE` and `TZ` environment variables if needed.

**Issue 3: Workflows Failing with Database Errors (PostgreSQL Mode)**
- Cause: Database not initialized or connection issues
- Solution: Check that the PostgreSQL cluster is running in the canvas. Verify the init job completed successfully by examining its logs. The database connection is automatic via Kubernetes secrets.

**Issue 4: Worker Not Processing Workflows (Queue Mode)**
- Cause: Redis connection issues or worker not running
- Solution: Verify both Redis and the worker deployment are running in the canvas. Check worker logs for connection errors. Ensure PostgreSQL mode is enabled (queue mode requires it).

**Issue 5: Webhook Endpoints Not Responding**
- Cause: Workflow not activated or incorrect webhook URL
- Solution: Ensure the workflow is activated (toggle in the workflow editor). Verify you're using the correct webhook URL format. Check Ingress configuration for routing issues.

**Issue 6: High Memory Usage**
- Cause: Large workflow executions or many concurrent workflows
- Solution: Increase memory allocation in the canvas. Consider enabling queue mode to offload execution to dedicated workers. Review workflow efficiency and optimize data processing.

**Issue 7: Credentials Not Persisting**
- Cause: Storage not properly mounted or encryption key changed
- Solution: Verify persistent storage is attached. Never change the `N8N_ENCRYPTION_KEY` after initial deployment as it will invalidate all stored credentials.

### Getting Help

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n Discord](https://discord.gg/n8n)
- [Sealos Discord Community](https://discord.gg/wdUn538zVP)

## Additional Resources

- [n8n Workflow Examples](https://n8n.io/workflows) - Browse community-created workflow templates
- [n8n Node Documentation](https://docs.n8n.io/integrations/) - Complete reference for all available nodes
- [n8n Expression Reference](https://docs.n8n.io/code/expressions/) - Guide to using expressions in workflows
- [n8n Best Practices](https://docs.n8n.io/workflows/best-practices/) - Tips for building efficient workflows
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This) - Database optimization tips
- [Redis Best Practices](https://redis.io/docs/management/optimization/) - Queue optimization guide

## Development Workflow

### Creating Workflows

To create your first workflow:

1. **Access the Editor**: Navigate to your n8n URL and log in
2. **Create New Workflow**: Click "Add Workflow" in the top menu
3. **Add Nodes**: Drag and drop nodes from the left panel
4. **Configure Nodes**: Click on each node to configure its settings
5. **Connect Nodes**: Draw connections between nodes to define the flow
6. **Test Execution**: Use the "Execute Workflow" button to test
7. **Activate**: Toggle the workflow to "Active" to enable automatic execution

### Using Webhooks

n8n provides two types of webhook endpoints:

**Production Webhooks:**
```
https://<app-host>.<domain>/webhook/<workflow-id>
```
- Used when workflow is activated
- Stable URL that doesn't change
- Use for production integrations

**Test Webhooks:**
```
https://<app-host>.<domain>/webhook-test/<workflow-id>
```
- Used during workflow development
- Only works when workflow editor is open
- Use for testing before activation

### Managing Credentials

1. Go to **Credentials** in the left menu
2. Click **Add Credential**
3. Select the service type (e.g., Gmail, Slack, GitHub)
4. Enter the required authentication details
5. Test the connection
6. Save the credential
7. Use the credential in your workflow nodes

**Important**: Credentials are encrypted using the `N8N_ENCRYPTION_KEY`. Never change this key after initial deployment, or all credentials will become inaccessible.

### Workflow Best Practices

1. **Error Handling**: Always add error workflows to handle failures gracefully
2. **Data Validation**: Validate input data before processing to prevent errors
3. **Execution Limits**: Set reasonable limits on loop iterations and data processing
4. **Logging**: Use the "Set" node to log important data points for debugging
5. **Testing**: Thoroughly test workflows with various input scenarios before activation
6. **Documentation**: Add notes to complex workflows explaining the logic
7. **Modular Design**: Break complex automations into smaller, reusable workflows

### Queue Mode Optimization

When using queue mode, consider these optimization strategies:

1. **Worker Scaling**: Increase worker replicas for higher throughput
2. **Concurrency**: Adjust `N8N_CONCURRENCY` environment variable (default: 10)
3. **Workflow Design**: Design workflows to be stateless for better parallel execution
4. **Resource Allocation**: Monitor worker resource usage and adjust CPU/memory limits
5. **Redis Tuning**: For very high volumes, consider increasing Redis resources

### Monitoring and Maintenance

**Execution History:**
- View all workflow executions in the "Executions" tab
- Filter by status (success, error, waiting)
- Inspect execution data and error messages

**Performance Monitoring:**
- Monitor resource usage in the Sealos canvas
- Check execution times in the workflow execution history
- Review worker logs for queue mode deployments

**Backup and Recovery:**
- Workflow definitions are stored in the database
- Regular database backups are recommended for production
- Export important workflows as JSON for version control

### Upgrading n8n

To upgrade to a newer version of n8n:

1. Update the image tag in the StatefulSet/Deployment
2. Apply the changes through the Sealos canvas
3. n8n will automatically run database migrations on startup
4. Verify all workflows still function correctly after upgrade

**Note**: Always review the [n8n release notes](https://docs.n8n.io/release-notes/) before upgrading, especially for major version changes.

## Security Considerations

### Credential Management

- All credentials are encrypted at rest using the `N8N_ENCRYPTION_KEY`
- Never share or expose the encryption key
- Use environment-specific credentials for different deployments
- Regularly rotate API keys and tokens used in credentials

### Webhook Security

- Use webhook authentication when possible (HTTP Basic Auth, Header Auth)
- Validate webhook payloads to prevent injection attacks
- Use HTTPS (automatically provided by Sealos)
- Consider IP whitelisting for sensitive webhooks

### Access Control

- Use strong passwords for owner and user accounts
- Limit user access based on roles (owner, member, viewer)
- Regularly review user access and remove inactive accounts
- Enable two-factor authentication if available in your n8n version

### Network Security

- All external communication uses HTTPS with SSL certificates
- Internal service communication uses Kubernetes service networking
- Database and Redis are not exposed externally
- Webhook endpoints are the only public-facing entry points

## License

This Sealos template is provided under MIT License. n8n is provided under the [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) - see the license for details regarding commercial use.
