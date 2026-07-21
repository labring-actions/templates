# Deploy and Host Mastodon on Sealos

Mastodon is an open-source decentralized social networking server for Fediverse communities. This template deploys Mastodon 4.6.3 with PostgreSQL, Redis, Sidekiq, real-time streaming, HTTPS, and a choice of persistent local media storage or private Sealos Object Storage.

![Mastodon Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mastodon/website-screenshot.webp)

## About Hosting Mastodon

Mastodon gives a community its own social server, moderation policy, public identity, and connection to the wider Fediverse. The web process serves the user interface and API, Sidekiq handles background and federation work, and the streaming process delivers real-time updates.

This template creates the database schema and the first Owner account during deployment. Public registration can stay closed, require administrator approval, or open immediately. SMTP is optional for the initial Owner and required for reliable confirmations, invitations, notifications, and password recovery.

## Common Use Cases

- **Community social network**: Run a moderated space for an organization, creator community, or interest group.
- **Institutional presence**: Host official accounts for a school, company, nonprofit, or public organization.
- **Private instance**: Operate a closed server for an internal team or invited members.
- **Fediverse publishing**: Publish from your own server and interact with accounts on compatible servers.

## Dependencies for Mastodon Hosting

- **Mastodon web and Sidekiq**: `tootsuite/mastodon:v4.6.3`
- **Streaming**: `tootsuite/mastodon-streaming:v4.6.3`
- **Database**: KubeBlocks PostgreSQL 16 with a dedicated `mastodon_production` database
- **Queue and cache**: KubeBlocks Redis 7 with Sentinel
- **Media storage**: Shared persistent local volume by default, or optional private Sealos Object Storage
- **Initialization**: Database Job and Mastodon setup Job
- **Network entry**: Services, HTTPS Ingress, and Sealos App resource

### Deployment Dependencies

- [Mastodon Documentation](https://docs.joinmastodon.org/) - Official user and administrator documentation
- [Mastodon Configuration](https://docs.joinmastodon.org/admin/config/) - Production environment reference
- [Mastodon Object Storage](https://docs.joinmastodon.org/admin/optional/object-storage/) - Official object storage guidance
- [Mastodon GitHub Repository](https://github.com/mastodon/mastodon) - Source code and releases
- [Sealos Documentation](https://sealos.io/docs) - Platform deployment and operations guides

### Implementation Details

Local storage mode creates a shared `ReadWriteOnce` media volume for web and Sidekiq. The workloads use pod affinity and a recreate strategy so both media writers stay on the volume's node.

Optional S3 mode creates a private `ObjectStorageBucket`. Mastodon writes private objects with the generated credentials, and a stateless same-origin proxy serves authorized reads under `/__sealos_media/`. Direct anonymous object reads and writes remain blocked.

The tested minimum application baseline is:

- Web: `100m` CPU and `512Mi` memory
- Sidekiq: `100m` CPU and `512Mi` memory
- Streaming: `100m` CPU and `128Mi` memory
- Setup Job: `100m` CPU and `512Mi` memory
- Optional media proxy: `100m` CPU and `128Mi` memory

Web and Sidekiq both reached `OOMKilled` at the adjacent `256Mi` memory tier. The listed limits completed cold startup, Owner creation, login, media upload, post publication, favorite and bookmark actions, and a stability window with zero restarts.

Mastodon is licensed under the GNU Affero General Public License v3.0.

## Why Deploy Mastodon on Sealos?

- **Complete one-click stack**: Create Mastodon, PostgreSQL, Redis, storage, networking, and TLS together.
- **Managed data services**: Use generated database and Redis credentials with automatic initialization.
- **Storage choice**: Start with a persistent local volume or select private S3-compatible media storage.
- **Ready Owner account**: Sign in as soon as the setup Job and web Deployment are complete.
- **Instant HTTPS access**: Open the generated application domain from Sealos Canvas.
- **Canvas operations**: Review logs, health, resources, storage, and network routes in one workspace.

## Deployment Guide

1. Open the [Mastodon template](https://sealos.io/products/app-store/mastodon) and click **Deploy Now**.
2. Enter the initial Owner values:
   - `admin_username`: Lowercase letters, numbers, or underscores.
   - `admin_email`: Email used for the first login.
   - `admin_password`: Strong password for the Owner account.
3. Select `registration_mode`:
   - `none`: Closed registration managed by the Owner.
   - `approved`: Visitors submit signup requests for administrator approval.
   - `open`: Visitors create accounts immediately.
4. Provide one VAPID key pair for Web Push. Generate it from a Mastodon environment with:

   ```bash
   RAILS_ENV=production bundle exec rake mastodon:webpush:generate_vapid_key
   ```

5. Choose the media storage mode:
   - Keep `enable_s3_storage` disabled for the shared persistent local volume.
   - Enable `enable_s3_storage` for a private Sealos S3-compatible bucket and same-origin media proxy.
6. Enable SMTP and enter the server, port, login, password, and sender address when the instance needs account email workflows.
7. Start the deployment and allow several minutes for PostgreSQL, Redis, migrations, Owner creation, and application startup.
8. Open the generated Mastodon URL from Canvas.

## First Login and Registration

Open `https://<your-mastodon-domain>/auth/sign_in` and sign in with the configured `admin_email` or `admin_username` and `admin_password`. The setup Job confirms and approves this Owner account automatically.

After login, open **Preferences** and **Administration** to configure the server name, description, rules, moderation, roles, federation, and registration settings.

For `approved` and `open` registration modes, configure SMTP before inviting public signups. New users then receive the confirmation and account lifecycle messages expected by Mastodon.

## Configuration

- **Registration**: Change signup behavior from Administration after deployment.
- **SMTP**: Configure reliable outbound delivery for confirmations, invitations, notifications, and password recovery.
- **Storage**: Local mode stores media on the shared PVC. S3 mode stores media in the private bucket and serves reads through the application domain.
- **Domain**: Mastodon identity is tied to `LOCAL_DOMAIN`. Plan any custom-domain migration before opening the instance to a community.
- **Backups**: Protect PostgreSQL and the selected media storage together for a complete recovery point.

## Scaling

Start by increasing Web and Sidekiq CPU and memory according to request latency and queue depth. Larger communities can add Sidekiq capacity and tune queues after measuring real workload patterns. Local media mode keeps one Web replica and one colocated Sidekiq replica around the shared `ReadWriteOnce` volume. S3 mode provides the storage foundation for a future multi-replica design after federation and job-processing behavior is reviewed.

## Troubleshooting

**The sign-in page rejects the Owner credentials**

Use the exact Owner email or username and password entered in the deployment form. Confirm that the setup Job completed successfully before signing in.

**Confirmation or password recovery email is missing**

Enable SMTP and verify the sender address, server, port, login, password, TLS behavior, and provider delivery logs.

**A media upload or image read fails**

For local mode, check the shared media PVC and Web/Sidekiq scheduling. For S3 mode, check the ObjectStorageBucket, media proxy Deployment, `/__sealos_media/` route, and object storage credentials.

**Web or Sidekiq is OOM-killed**

Keep at least the tested `512Mi` memory limit for each role and increase it as community traffic grows.

**Timelines update slowly**

Review Sidekiq queue depth, Redis health, streaming logs, and federation delivery latency. Increase Sidekiq resources before raising queue concurrency.

## Additional Resources

- [Mastodon Admin Guide](https://docs.joinmastodon.org/admin/)
- [Mastodon Scaling Guide](https://docs.joinmastodon.org/admin/scaling/)
- [Mastodon Moderation Guide](https://docs.joinmastodon.org/admin/moderation/)
- [Mastodon GitHub Issues](https://github.com/mastodon/mastodon/issues)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template follows the repository license. Mastodon is distributed under the GNU Affero General Public License v3.0.
