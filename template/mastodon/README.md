# Deploy and Host Mastodon on Sealos

Mastodon is a free, open-source decentralized social networking server for Fediverse communities. This template deploys Mastodon with PostgreSQL, Redis, Sidekiq, streaming, and Sealos Object Storage on Sealos Cloud.

![Mastodon Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mastodon/website-screenshot.webp)

## About Hosting Mastodon

Mastodon runs a federated social media server where local users can post, follow accounts across compatible servers, moderate community activity, and manage a public identity under your own domain. The web service serves the main UI and API, Sidekiq handles background jobs, and the streaming service provides real-time updates.

This Sealos template follows Mastodon's Docker and Helm deployment model. PostgreSQL stores accounts, statuses, settings, and moderation data; Redis supports cache, queues, and streaming state; Sealos Object Storage stores uploaded media through Mastodon's S3-compatible storage configuration.

The template creates an initial owner account during setup. Public registration can be disabled, approval-based, or open through the deployment form.

## Common Use Cases

- **Community Social Network**: Run a moderated social platform for an organization, creator community, or interest group.
- **Federated Publishing**: Publish posts from your own server while interacting with users across the Fediverse.
- **Private Instance**: Operate a closed server where only the initial owner and invited users can participate.
- **Research and Testing**: Evaluate Mastodon operations, moderation settings, and federation behavior.
- **Institutional Presence**: Host accounts for a team, school, company, or nonprofit under a controlled server.

## Dependencies for Mastodon Hosting

The Sealos template includes all required dependencies:

- Mastodon `4.5.11`
- Mastodon Streaming `4.5.11`
- PostgreSQL `16.4.0` through KubeBlocks
- Redis `7.2.7` with Sentinel through KubeBlocks
- Sealos `ObjectStorageBucket` for S3-compatible media storage
- Setup Job for database preparation and initial owner creation
- Web, Sidekiq, and streaming Deployments
- Kubernetes Services and HTTPS Ingress routes

### Deployment Dependencies

- [Mastodon Website](https://joinmastodon.org/) - Product overview
- [Mastodon Documentation](https://docs.joinmastodon.org/) - Official documentation
- [Mastodon Admin Install Guide](https://docs.joinmastodon.org/admin/install/) - Server installation guide
- [Mastodon Chart](https://github.com/mastodon/chart) - Official Helm chart
- [Mastodon GitHub Repository](https://github.com/mastodon/mastodon) - Source code and issue tracker
- [Sealos Documentation](https://sealos.io/docs) - Platform and operations guidance

## Implementation Details

### Architecture Components

This template deploys the following services:

- **Web**: Runs `ghcr.io/mastodon/mastodon:v4.5.11`, serves the main Mastodon UI and API on port `3000`, and exposes `/health`.
- **Sidekiq**: Runs Mastodon background queues for delivery, mailers, pull jobs, scheduler jobs, and federation work.
- **Streaming**: Runs `ghcr.io/mastodon/mastodon-streaming:v4.5.11` on port `4000` for real-time timelines and notifications.
- **PostgreSQL Cluster**: Stores Mastodon application data and is initialized with a dedicated `mastodon_production` database.
- **Redis Cluster**: Provides queue, cache, and streaming state.
- **Object Storage**: Provisions a private Sealos bucket and injects S3-compatible credentials for Mastodon media.
- **Setup Job**: Runs `db:prepare`, creates or updates the initial owner account, confirms the email, approves the user, and applies the selected registration mode.

### Configuration

- `admin_username`, `admin_email`, and `admin_password` create the first owner account.
- `registration_mode` controls public signup behavior with `none`, `approved`, or `open`.
- `vapid_private_key` and `vapid_public_key` configure Web Push signing. Generate them as one pair before deployment with `RAILS_ENV=production bundle exec rake mastodon:webpush:generate_vapid_key`.
- `smtp_enabled` controls whether SMTP fields appear in the deployment form. Configure SMTP before relying on password reset, account confirmation, and notification emails.
- Object storage is always provisioned because Mastodon's official deployment supports S3-compatible media storage and this template uses Sealos Object Storage as that backend.
- `LOCAL_DOMAIN` is generated from the Sealos application host so Mastodon uses the public HTTPS URL created by the platform.

### Login and Registration

After deployment, sign in with the configured owner username or email and password. With the default `registration_mode=none`, public signups are closed and users are managed by the owner from Mastodon administration. Use `approved` for moderated public signup requests or `open` for immediate public registration.

For production communities, configure SMTP so account emails, invitations, confirmations, and password recovery can work reliably.

### License Information

Mastodon is licensed under the GNU Affero General Public License v3.0. This Sealos template is deployment configuration for Mastodon and follows the repository's template license.

## Why Deploy Mastodon on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment and operations. By deploying Mastodon on Sealos, you get:

- **One-Click Deployment**: Launch Mastodon web, Sidekiq, streaming, PostgreSQL, Redis, object storage, and HTTPS ingress in one workflow.
- **Managed Datastores**: PostgreSQL and Redis are provisioned automatically through KubeBlocks.
- **S3-Compatible Media Storage**: Uploaded media uses Sealos Object Storage without manual bucket setup.
- **Instant HTTPS Access**: Sealos creates a public HTTPS URL for the Mastodon server.
- **Persistent Application State**: Database and media data survive pod restarts through managed storage.
- **AI-Assisted Operations**: Use Canvas and AI dialog to adjust resources, environment values, and networking.

Deploy Mastodon on Sealos to run a Fediverse server while keeping Kubernetes operations inside the platform workflow.

## Deployment Guide

1. Open the [Mastodon template](https://sealos.io/products/app-store/mastodon) and click **Deploy Now**.
2. Configure the deployment parameters:
   - `admin_username`: Initial owner username.
   - `admin_email`: Initial owner email address.
   - `admin_password`: Initial owner password.
   - `registration_mode`: Public registration mode: `none`, `approved`, or `open`.
   - `vapid_private_key` and `vapid_public_key`: Web Push key pair generated with `RAILS_ENV=production bundle exec rake mastodon:webpush:generate_vapid_key`.
   - SMTP fields: Enable and fill these when your server needs outbound email.
3. Wait for deployment to complete. Mastodon cold start includes PostgreSQL, Redis, object storage, database migrations, owner account creation, Sidekiq startup, streaming startup, and web startup.
4. Open the generated Mastodon URL from the Canvas.
5. Click **Sign in** and log in with the configured owner email or username and password.
6. Open **Preferences** and **Administration** to review server settings, profile settings, moderation tools, registration settings, and Sidekiq status.

## Configuration

After deployment, configure Mastodon through:

- **Mastodon Administration**: Manage server settings, roles, moderation, federation, signups, reports, and announcements.
- **Sealos AI Dialog**: Describe resource, environment, storage, or networking changes.
- **Resource Cards**: Open Deployments, Services, Ingresses, PostgreSQL, Redis, and Object Storage cards from Canvas.

For production use, review SMTP delivery, backup policy, moderation rules, retention settings, instance rules, media storage access, and domain strategy.

## Scaling

This template starts with one web pod, one Sidekiq pod, one streaming pod, one PostgreSQL instance, one Redis replication topology, and one object storage bucket. Scale vertically first by increasing CPU and memory on the web and Sidekiq Deployments. Larger servers can add more Sidekiq workers and tune queue allocation after traffic patterns are known.

## Troubleshooting

### Login fails after deployment

Use the `admin_email` or `admin_username` and `admin_password` values from the deployment form. Wait for the setup Job and web Deployment to finish before signing in.

### Password reset or confirmation emails fail

Enable SMTP and provide a working server, port, username, password, and sender address. Mastodon relies on outbound email for account lifecycle workflows.

### Media uploads fail

Check the Object Storage bucket, S3 credentials, and generated storage endpoint in the Mastodon environment. The template provisions a Sealos bucket and injects S3-compatible variables automatically.

### Timelines feel delayed

Review Sidekiq health and queue depth. Increase Sidekiq CPU and memory before raising concurrency or adding workers.

### Getting Help

- [Mastodon Documentation](https://docs.joinmastodon.org/)
- [Mastodon GitHub Issues](https://github.com/mastodon/mastodon/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Mastodon Admin Guide](https://docs.joinmastodon.org/admin/)
- [Mastodon Configuration Reference](https://docs.joinmastodon.org/admin/config/)
- [Mastodon Scaling Guide](https://docs.joinmastodon.org/admin/scaling/)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository's template license. Mastodon itself is licensed under the GNU Affero General Public License v3.0.
