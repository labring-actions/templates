# Deploy and Host Strapi on Sealos

Strapi is the leading open-source headless CMS, built with 100% JavaScript/TypeScript and fully customizable. This template provides one-click deployment of a production-ready Strapi instance with PostgreSQL database backend, enabling you to build powerful content management systems and APIs with minimal setup on Sealos Cloud.

## About Hosting Strapi

Strapi runs as a Node.js application that provides both a powerful admin panel for content management and RESTful/GraphQL APIs for content delivery. The headless architecture separates content management from presentation, allowing you to use Strapi as a backend for websites, mobile apps, IoT devices, or any other platform that consumes content via APIs.

The Sealos template automatically provisions a PostgreSQL database for persistent content storage, configures all necessary environment variables including security tokens, and sets up persistent storage for uploaded media files and application data. The deployment includes an init container that handles the initial build process, ensuring your Strapi admin panel is ready to use immediately after deployment.

## Common Use Cases

- **Headless CMS for Websites**: Power modern JAMstack websites with a flexible content backend
- **Mobile App Backend**: Provide content APIs for iOS, Android, and cross-platform mobile applications
- **Multi-Channel Content Delivery**: Manage content once and deliver it across web, mobile, IoT, and other platforms
- **Custom API Development**: Build RESTful or GraphQL APIs with a visual content type builder
- **E-commerce Product Management**: Manage product catalogs, descriptions, and media assets
- **Blog and Publication Platforms**: Create content-rich publishing systems with custom workflows
- **Internal Tools and Dashboards**: Build admin panels and internal applications with rapid development

## Dependencies for Strapi Hosting

The Sealos template includes all required components: Strapi application server and PostgreSQL database with automatic initialization.

### Deployment Dependencies

- [Strapi Documentation](https://docs.strapi.io/) - Official Strapi documentation
- [Strapi Quickstart Guide](https://docs.strapi.io/dev-docs/quick-start) - Getting started with Strapi development
- [Strapi API Reference](https://docs.strapi.io/dev-docs/api/rest) - REST and GraphQL API documentation
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Database backend documentation

## Implementation Details

### Architecture Components

This template deploys two interconnected services:

- **PostgreSQL Database**: Persistent data storage for content and configuration
  - Version: PostgreSQL 14.8.0
  - Persistent storage: 1Gi
  - Automatic database initialization with 'strapi' database
  - Connection credentials managed via Kubernetes secrets

- **Strapi Application**: Headless CMS server with admin panel
  - Version: Strapi 5.33.0
  - Web UI: Port 1337 (exposed via Ingress with SSL)
  - Admin panel: `/admin` path
  - API endpoints: `/api` path
  - Persistent storage: 2Gi for application data, 1Gi for npm cache
  - Init container for automatic build process

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Strapi (Runtime) | 100m | 1000m | 25Mi | 256Mi |
| Strapi (Init Build) | 200m | 2000m | 307Mi | 3072Mi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi |

### Environment Configuration

The template automatically configures Strapi with the following settings:

**Database Configuration:**
- Client: PostgreSQL
- Connection: Automatic via Kubernetes secrets
- Database name: `strapi`
- SSL: Disabled (internal cluster communication)

**Security Tokens:**
All security tokens are automatically generated with cryptographically secure random values:
- JWT Secret: 32-character random string
- Admin JWT Secret: 32-character random string
- App Keys: 4 x 32-character random strings
- API Token Salt: 32-character random string
- Transfer Token Salt: 32-character random string

**Public URLs:**
- Admin URL: `https://<app-host>.<domain>/admin`
- Public URL: `https://<app-host>.<domain>`
- CORS: Configured for your deployment domain

### Deployment Process

The deployment includes a two-stage initialization:

1. **Database Initialization Job**: Creates the `strapi` database in PostgreSQL
2. **Application Init Container**: Builds the Strapi admin panel before the main container starts
3. **Main Container**: Runs Strapi in production or development mode

This ensures your Strapi instance is fully ready to use immediately after deployment completes.

## Why Deploy Strapi on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Strapi on Sealos, you get:

- **One-Click Deployment**: Deploy a complete Strapi CMS with PostgreSQL database in seconds. No complex configuration or Kubernetes expertise required.
- **Pre-Configured Database**: PostgreSQL is automatically provisioned, initialized, and connected to Strapi with secure credentials.
- **Automatic Build Process**: The init container handles the Strapi admin panel build, so you can start creating content immediately.
- **Persistent Storage**: Built-in persistent storage ensures your content, media uploads, and configuration survive restarts and updates.
- **Secure Public Access**: Strapi gets automatic public URL with SSL certificate, allowing secure access to both admin panel and APIs.
- **Environment Flexibility**: Choose between production and development modes to match your workflow.
- **Easy Scaling**: Adjust resources through intuitive forms as your content and traffic grow.
- **Automatic Security**: All security tokens are generated automatically with cryptographically secure random values.

Deploy Strapi on Sealos and focus on building great content experiences instead of managing infrastructure.

## Deployment Guide

1. Visit [Strapi Template Page](https://sealos.io/products/app-store/strapi)
2. Click the "Deploy Now" button
3. Select your Node environment mode:
   - **Production** (recommended): Optimized for performance and stability
   - **Development**: Enables hot-reload and development features
4. Wait for deployment to complete (typically 2-3 minutes, including build process)
5. Access Strapi via the provided URL (shown in the canvas)
6. Create your admin account on first access to the admin panel

## Configuration

After deployment, you can customize your Strapi instance:

### Initial Setup

1. **Create Admin Account**: On first access to `/admin`, you'll be prompted to create an administrator account
2. **Configure Content Types**: Use the Content-Type Builder to define your data models
3. **Set Permissions**: Configure role-based access control for API endpoints
4. **Upload Media**: Use the Media Library to manage images, videos, and other assets

### Resource Scaling

Adjust resources in the canvas based on your needs:
- **CPU/Memory**: Increase for better performance with high traffic or complex content types
- **Storage**: Expand application storage for more media uploads and content

### API Configuration

Strapi provides both REST and GraphQL APIs:
- REST API: `https://<app-host>.<domain>/api`
- GraphQL API: `https://<app-host>.<domain>/graphql` (requires GraphQL plugin)

### Service Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Admin Panel | `https://<app-host>.<domain>/admin` | Content management interface |
| REST API | `https://<app-host>.<domain>/api` | RESTful API endpoints |
| GraphQL | `https://<app-host>.<domain>/graphql` | GraphQL API (if enabled) |
| PostgreSQL | `<app-name>-pg-postgresql.<namespace>.svc:5432` | Database (internal) |

## Troubleshooting

### Common Issues

**Issue 1: Admin Panel Not Loading**
- Cause: Build process may still be running or failed
- Solution: Check the init container logs in the Terminal. The build process can take 1-2 minutes on first deployment. If the build failed, check resource limits and try redeploying.

**Issue 2: Database Connection Errors**
- Cause: PostgreSQL not ready or connection credentials incorrect
- Solution: Verify the PostgreSQL cluster is running in the canvas. Check that the `strapi` database was created by examining the init job logs. The connection is automatic via Kubernetes secrets.

**Issue 3: Media Upload Failures**
- Cause: Storage full or permission issues
- Solution: Increase the application storage allocation in the canvas. Default is 2Gi for application data.

**Issue 4: API Endpoints Return 403 Forbidden**
- Cause: Permissions not configured for public access
- Solution: In the Strapi admin panel, go to Settings → Roles → Public, and enable permissions for the endpoints you want to expose publicly.

**Issue 5: Slow Performance**
- Cause: Insufficient resources for your content volume
- Solution: Increase CPU and memory allocation in the canvas. Consider upgrading from the default 1000m CPU / 256Mi memory limits.

### Getting Help

- [Strapi Documentation](https://docs.strapi.io/)
- [Strapi Community Forum](https://forum.strapi.io/)
- [Strapi Discord](https://discord.strapi.io/)
- [Sealos Discord Community](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Strapi Content-Type Builder](https://docs.strapi.io/user-docs/content-type-builder) - Creating custom content types
- [Strapi API Documentation](https://docs.strapi.io/dev-docs/api/rest) - REST and GraphQL API reference
- [Strapi Plugins](https://market.strapi.io/) - Extend Strapi with community plugins
- [Strapi Deployment Guide](https://docs.strapi.io/dev-docs/deployment) - Advanced deployment configurations
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This) - Database optimization tips

## Development Workflow

### Connecting Your Frontend

To connect your frontend application to Strapi APIs:

```javascript
// Example: Fetching content from Strapi REST API
const response = await fetch('https://<app-host>.<domain>/api/articles?populate=*', {
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN'
  }
});
const data = await response.json();
```

### Creating API Tokens

1. Go to Settings → API Tokens in the admin panel
2. Click "Create new API Token"
3. Set token name, type (Read-only, Full access, Custom), and duration
4. Copy the generated token (shown only once)
5. Use the token in your application's API requests

### Custom Development

For custom plugin development or extending Strapi:

1. Switch to development mode by updating the `node_env` input to `development`
2. Access the application storage via the canvas to modify code
3. Changes will hot-reload automatically in development mode
4. Switch back to production mode for optimal performance

## License

This Sealos template is provided under MIT License. Strapi is provided under its own license - see [Strapi License](https://github.com/strapi/strapi/blob/develop/LICENSE) for details.
