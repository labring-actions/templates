# Deploy and Host Strapi on Sealos

Strapi is an open-source headless CMS for creating content models, managing content, and serving REST APIs. This template builds Strapi 5.50.1 with Node.js 22 and runs it in production mode on Sealos Cloud.

![Strapi Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/strapi/website-screenshot.webp)

## About Hosting Strapi

Strapi provides an administration interface for editors and an API layer for websites, mobile apps, and other clients. Its project files, SQLite data, and local media uploads share persistent application storage, so they survive pod restarts.

The template offers two independent storage choices. PostgreSQL 16 is the default production database, while SQLite provides a compact single-instance option. Media can use persistent local storage or a private Sealos Object Storage bucket through Strapi's AWS S3 upload provider.

## Common Use Cases

- **Website CMS**: Manage structured content for frontend frameworks and static sites
- **Mobile Backend**: Publish content through REST APIs
- **Product Catalog**: Model products, categories, media, and relationships
- **Editorial Platform**: Give content teams a dedicated administration workflow
- **Internal API**: Build custom content APIs with role-based access control

## Dependencies for Strapi Hosting

The template includes a digest-pinned Node.js 22 runtime, a verified Strapi 5.50.1 package lock, persistent application storage, and optional managed PostgreSQL and Object Storage resources.

### Deployment Dependencies

- [Strapi Documentation](https://docs.strapi.io/) - Product and developer documentation
- [Strapi Deployment Guide](https://docs.strapi.io/cms/deployment) - Production deployment guidance
- [Strapi AWS S3 Provider](https://docs.strapi.io/cms/configurations/media-library-providers#amazon-s3) - S3 upload provider configuration
- [PostgreSQL Documentation](https://www.postgresql.org/docs/16/) - PostgreSQL 16 documentation

## Implementation Details

### Architecture Components

- **Strapi Application**: Strapi 5.50.1 installed with `npm ci`, built, and started with a digest-pinned Node.js 22 image
- **Application Storage**: A 1Gi persistent volume for project files, SQLite data, and local uploads
- **Dependency Storage**: A separate 1Gi persistent volume populated from the verified dependency archive on each cold start
- **PostgreSQL 16**: An independent KubeBlocks database when `use_postgresql` is enabled
- **Sealos Object Storage**: A private bucket and managed credentials when `enable_s3_storage` is enabled
- **Ingress**: HTTPS access to the admin interface and content APIs

### Configuration Choices

| Input | Default | Result |
| --- | --- | --- |
| `admin_email` | User supplied | Creates the initial administrator before public startup |
| `admin_password` | User supplied | Sets the required initial administrator password |
| `admin_firstname` | `Admin` | Sets the initial administrator first name |
| `admin_lastname` | `User` | Sets the initial administrator last name |
| `use_postgresql` | `true` | Uses the managed PostgreSQL 16 database |
| `use_postgresql` | `false` | Uses SQLite at `.tmp/data.db` on persistent storage |
| `enable_s3_storage` | `false` | Stores uploads in `public/uploads` on persistent storage |
| `enable_s3_storage` | `true` | Uses a private Sealos Object Storage bucket through the AWS S3 provider |

The template generates Strapi's application keys, JWT secrets, token salts, and `ENCRYPTION_KEY` during deployment. It creates the initial administrator inside the build init container before the public application becomes Ready. Strapi consumes the KubeBlocks-managed PostgreSQL connection secret directly. A least-privilege Job and CronJob track that secret's revision and restart only the Strapi Pod after credential rotation. Object Storage credentials come from Sealos-managed secrets.

## Why Deploy Strapi on Sealos?

Sealos is a Kubernetes-based cloud operating system that manages application resources through a visual Canvas and AI-assisted operations. This Strapi deployment provides:

- **One-Click Deployment**: Provision the application and selected managed services from one form
- **Persistent Data**: Keep project files, SQLite data, and local uploads across restarts
- **Managed Services**: Add PostgreSQL 16 and private Object Storage through explicit options
- **Secure Public Access**: Receive an HTTPS endpoint and managed certificate
- **Resource Control**: Adjust CPU, memory, and storage from the Canvas
- **Pay-as-You-Go Resources**: Allocate the services required by the selected architecture

## Deployment Guide

1. Open the [Strapi template](https://sealos.io/products/app-store/strapi) and click **Deploy Now**.
2. Enter the initial administrator email, password, first name, and last name. The password must contain uppercase, lowercase, number, and special characters.
3. Keep PostgreSQL enabled for a production database, or clear it for persistent SQLite.
4. Enable Sealos Object Storage for S3-backed media, or keep local persistent uploads.
5. Submit the form and wait for deployment to complete. The first verified dependency install and administration build can take several minutes.
6. Open the application URL at `/admin/auth/login` and sign in with the administrator credentials from the deployment form.

## Login

The template creates the first Strapi administrator before the application Service becomes Ready, which closes the public first-user registration window. Sign in at `/admin/auth/login` with the `admin_email` and `admin_password` values supplied during deployment. Store these credentials in a password manager; later administrators can be managed from the Strapi administration interface.

## Configuration

After deployment, use the Strapi administration interface to manage content entries, configure roles, and generate API tokens. Strapi's Content-Type Builder runs in development mode, so production content-model changes should be prepared in project code and deployed through a controlled build. The main endpoints are:

| Endpoint | Purpose |
| --- | --- |
| `/admin/auth/login` | Sign in to the administration interface |
| `/admin` | Open the administration interface |
| `/api` | Access generated REST endpoints |
| `/_health` | Check application health |

Use the Sealos Canvas AI dialog or resource cards for later resource changes. Keep one Strapi replica when using SQLite or local uploads because those modes use a single persistent volume.

## Troubleshooting

### The Admin Page Is Still Starting

The first deployment verifies the embedded package lock, runs `npm ci`, creates the initial administrator, packs runtime dependencies, and builds the administration interface. Check the `strapi-build` and `strapi-runtime-deps` init-container logs in the Canvas and allow both stages to finish.

### PostgreSQL Startup Fails

Confirm the PostgreSQL resource reaches the running state. The idempotent `pg-init` Job creates the `strapi` database through the generated connection secret, and the `wait-postgresql` init container gates application startup until that database is ready.

### Media Uploads Fail

For local uploads, confirm the application volume has free capacity. For Object Storage, confirm the bucket resource and its generated bucket secret are ready.

### API Requests Return 403

Configure the required permissions under **Settings > Users & Permissions plugin > Roles** in the Strapi administration interface.

### Getting Help

- [Strapi Documentation](https://docs.strapi.io/)
- [Strapi GitHub Issues](https://github.com/strapi/strapi/issues)
- [Strapi Community Forum](https://forum.strapi.io/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the MIT License. Strapi uses its own licensing terms; see the [Strapi license](https://github.com/strapi/strapi/blob/develop/LICENSE) for details.
