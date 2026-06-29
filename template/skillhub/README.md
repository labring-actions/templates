# Deploy and Host SkillHub on Sealos

SkillHub is a self-hosted agent skill registry for publishing, discovering, governing, and installing reusable agent skills. This template deploys the official SkillHub web, server, and scanner containers with KubeBlocks PostgreSQL and Redis on Sealos Cloud.

![SkillHub Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/skillhub/website-screenshot.webp)

## About Hosting SkillHub

SkillHub gives teams a private registry for agent skills, namespaces, reviews, ratings, downloads, API tokens, and CLI-based installation. It is designed for organizations that want reusable skills behind their own infrastructure boundary.

This Sealos template follows the official release topology from `iflytek/skillhub`: `skillhub-web`, `skillhub-server`, `skillhub-scanner`, PostgreSQL, and Redis. The default deployment uses local persistent storage for packages, and the template exposes an external S3-compatible storage option for production object storage.

## Common Use Cases

- **Private skill registry**: Publish internal agent skills for Codex, Claude, and other agent workflows.
- **Team governance**: Manage namespaces, roles, review policies, ratings, and audit logs.
- **CLI distribution**: Let users search, install, and update skills through the SkillHub CLI.
- **Enterprise self-hosting**: Run the registry with managed PostgreSQL, Redis, and HTTPS ingress.

## Dependencies for SkillHub Hosting

The Sealos template includes all required runtime dependencies for a standalone SkillHub deployment.

### Deployment Dependencies

- [SkillHub GitHub Repository](https://github.com/iflytek/skillhub) - Source code and releases
- [SkillHub User Guide](https://iflytek.github.io/skillhub/) - Official user guide
- [SkillHub Developer Docs](https://zread.ai/iflytek/skillhub) - Architecture and operations documentation

### Implementation Details

**Architecture Components:**

- **SkillHub Web**: Nginx-served React frontend on port `80`
- **SkillHub Server**: Spring Boot API service on port `8080`
- **Skill Scanner**: Security scanner service on port `8000`
- **PostgreSQL**: KubeBlocks-managed `postgresql-16.4.0` database for application metadata
- **Redis**: KubeBlocks Redis `redis-7.2.7` for Spring sessions and runtime coordination
- **Storage**: Local persistent storage by default, with optional external S3-compatible storage inputs

**Configuration:**

- `SKILLHUB_PUBLIC_BASE_URL` points to the generated Sealos HTTPS URL.
- Direct username/password login is enabled for the bootstrap administrator.
- `BOOTSTRAP_ADMIN_USERNAME`, `BOOTSTRAP_ADMIN_PASSWORD`, and `BOOTSTRAP_ADMIN_EMAIL` are deployment inputs.
- External S3 fields are shown only when `enable_external_s3` is set to `true`.

**License Information:**

SkillHub is licensed under Apache-2.0.

## Why Deploy SkillHub on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and operations. By deploying SkillHub on Sealos, you get:

- **One-Click Deployment**: Deploy SkillHub web, server, scanner, PostgreSQL, Redis, storage, and HTTPS ingress from one template.
- **Managed Datastores**: Use KubeBlocks PostgreSQL and Redis with predictable resource settings.
- **Instant Public Access**: Open the generated HTTPS App URL after deployment.
- **Production Storage Choice**: Keep the default persistent volume or connect an external S3-compatible bucket.
- **Easy Customization**: Adjust resources and environment variables through Sealos resource cards or the AI dialog.

## Deployment Guide

1. Open the [SkillHub template](https://sealos.io/products/app-store/skillhub) and click **Deploy Now**.
2. Configure the deployment parameters:
   - `admin_username`: bootstrap administrator username.
   - `admin_password`: bootstrap administrator password. The template generates a random value by default; save the final value before opening SkillHub.
   - `admin_email`: bootstrap administrator email.
   - `enable_external_s3`: choose `true` only when you have an existing S3-compatible bucket and credentials.
3. Wait for deployment to complete, typically 4-6 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated SkillHub URL from the App card.
5. Log in with `admin_username` and `admin_password`, then rotate the administrator password inside SkillHub.

## Configuration

After deployment, you can configure SkillHub through:

- **SkillHub UI**: Manage skills, namespaces, reviews, users, API tokens, and registry settings.
- **External S3 inputs**: Set `enable_external_s3=true` during deployment to use official S3-compatible storage variables.
- **AI Dialog**: Describe resource changes for Sealos to apply.
- **Resource Cards**: Click the web, server, scanner, PostgreSQL, Redis, Service, Ingress, or PVC cards to modify settings.

## Scaling

SkillHub runs as single-replica web, server, and scanner components by default. Scale CPU and memory from the related resource cards after observing real traffic and scanner workload.

## Troubleshooting

### Cannot log in

Confirm that you are using the exact `admin_username` and `admin_password` configured during deployment. The bootstrap administrator is initialized during first server startup.

### Skill uploads fail

Check the server logs and storage settings. With the default configuration, packages are saved under the `/var/lib/skillhub/storage` persistent volume. With external S3 enabled, confirm endpoint, bucket, access key, secret key, region, and path-style mode.

### Application is still starting

SkillHub waits for PostgreSQL, Redis, Flyway migrations, and the scanner service during cold start. Wait for the web, server, scanner, PostgreSQL, and Redis resources to show Ready in the Sealos Canvas.

### Getting Help

- [SkillHub User Guide](https://iflytek.github.io/skillhub/)
- [SkillHub GitHub Issues](https://github.com/iflytek/skillhub/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [SkillHub GitHub Repository](https://github.com/iflytek/skillhub)
- [SkillHub Developer Docs](https://zread.ai/iflytek/skillhub)
- [SkillHub CLI Package](https://www.npmjs.com/package/@astron-team/skillhub)

## License

This Sealos template is provided under the repository license. SkillHub itself is licensed under Apache-2.0.
