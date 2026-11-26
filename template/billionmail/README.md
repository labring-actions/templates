# Deploy and Host BillionMail on Sealos

BillionMail is an open-source mail server, newsletter, and email marketing platform. This template deploys the pinned BillionMail 4.9 service bundle, PostgreSQL, Redis, and persistent storage on Sealos Cloud.

![BillionMail Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/billionmail/website-screenshot.webp)

## About Hosting BillionMail

BillionMail provides a self-hosted control plane for domains, mailboxes, campaign sending, newsletter operations, and mail service management. The Sealos template runs the official BillionMail service set with a public HTTPS web console and internal mail service coordination.

The deployment includes the BillionMail core web/API service, Postfix for SMTP, Dovecot for IMAP/POP3 mailbox access, Rspamd for anti-spam processing, and Roundcube webmail under `/roundcube`. Sealos also provisions KubeBlocks PostgreSQL, KubeBlocks Redis, persistent storage, service discovery, ingress, and TLS for the web console.

## Common Use Cases

- **Self-hosted mail operations**: Manage domains, mailboxes, and server-side mail settings from a web console.
- **Newsletter publishing**: Run newsletter lists and campaign sending from your own infrastructure.
- **Email marketing workflows**: Operate outbound campaigns while keeping data and configuration under your control.
- **Team mailbox administration**: Create mailboxes, manage credentials, and provide webmail access with Roundcube.
- **Deliverability testing**: Tune DNS, sending domains, and mail routing for controlled environments.

## Dependencies for BillionMail Hosting

The Sealos template includes all required runtime dependencies: BillionMail Core 4.9.3, Postfix 1.6, Dovecot 1.6, Rspamd 1.2, Roundcube 1.6.11, PostgreSQL 16.4, Redis 7.2, and a persistent data volume. Application data uses local persistent storage, following the official compose topology. PostgreSQL and Redis are required backends for this bundle.

### Deployment Dependencies

- [BillionMail Website](https://www.billionmail.com/) - Official website
- [BillionMail GitHub](https://github.com/Billionmail/BillionMail) - Source code and upstream documentation
- [BillionMail Template on Sealos](https://sealos.io/products/app-store/billionmail) - One-click Sealos deployment
- [Sealos Discord](https://discord.gg/wdUn538zVP) - Sealos community support

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **BillionMail Core**: Main web console and API service exposed through the Sealos App URL.
- **Postfix**: SMTP, SMTPS, and Submission service for mail sending.
- **Dovecot**: IMAP, IMAPS, POP3, and POP3S service for mailbox access.
- **Rspamd**: Anti-spam and mail filtering service.
- **Roundcube**: Webmail interface served at `/roundcube`.
- **PostgreSQL**: KubeBlocks PostgreSQL 16.4 cluster for BillionMail and webmail data.
- **Redis**: KubeBlocks Redis 7.2 cluster for cache, sessions, and coordination.
- **Persistent Volume**: Stores mail data, mutable configuration, TLS files, logs, webmail data, and mail service state.

The workload keeps one StatefulSet replica because the mail services share one ReadWriteOnce data volume. PostgreSQL runs one replica, while Redis runs one Redis replica and one Sentinel replica. The application images are pinned to immutable digests from the official compose bundle at commit `fc36c76c050c3775c5e899faf7403cf0262d2744`.

**Configuration:**

- The Sealos App URL opens BillionMail at the root path, for example `https://<app-host>.<sealos-domain>`.
- The initial administrator account is created from the `admin_username` and `admin_password` deployment parameters.
- `mail_hostname` is used by Postfix and DNS guidance, for example `mail.example.com`.
- `timezone` configures container time, and `retention_days` controls BillionMail log backup retention.

**License Information:**

This Sealos template is provided under the templates repository license. Review the upstream BillionMail repository for the current application license terms before production use.

## Why Deploy BillionMail on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operation, and resource management. By deploying BillionMail on Sealos, you get:

- **One-Click Deployment**: Start the full BillionMail stack through a template-driven workflow.
- **Managed Cloud Resources**: Use KubeBlocks PostgreSQL, KubeBlocks Redis, persistent storage, ingress, and TLS from one platform.
- **Canvas Operations**: Adjust resources, inspect workloads, and update settings through Canvas, AI dialog, and resource cards after deployment.
- **Resource Efficiency**: Run the stack with pay-as-you-go resources and tune CPU, memory, and storage as usage grows.
- **Kubernetes Foundation**: Keep the deployment portable and observable, with routine changes handled through Sealos.

## Deployment Guide

1. Open the [BillionMail template](https://sealos.io/products/app-store/billionmail) and click **Deploy Now**.
2. Configure the deployment parameters in the popup dialog:
   - **Admin Username**: Required initial BillionMail administrator username.
   - **Admin Password**: Required initial BillionMail administrator password. Set a strong, unique value.
   - **Mail Hostname**: Hostname used for mail service and DNS guidance, such as `mail.example.com`.
   - **Timezone**: Container timezone, such as `Etc/UTC`.
   - **Retention Days**: Number of days to keep BillionMail log backups.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, Sealos redirects you to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards.
4. Open the provided BillionMail App URL. The console is served at the root path, for example `https://<app-host>.<sealos-domain>`.
5. Log in with the exact administrator username and password configured in step 2. The initial administrator account is created during deployment, and first access uses these deployment credentials directly.
6. After logging in, create mail domains and mailboxes before using mail delivery or Roundcube webmail.

## First Login and Webmail

Use the administrator username and password from the deployment parameters on the BillionMail login page. Keep the password in your own password manager because the template input is the source of the initial administrator credential.

Roundcube webmail is available at:

```text
https://<app-host>.<sealos-domain>/roundcube
```

Create a domain and mailbox in the BillionMail console before signing in to Roundcube.

## Mail DNS and Ports

BillionMail exposes SMTP, SMTPS, Submission, IMAP, IMAPS, POP3, and POP3S through its Kubernetes ClusterIP Service. The template publishes only the HTTPS web console through the Sealos App URL. Internet mail delivery requires a separately configured public L4 route plus DNS and network planning:

- Point MX records to the configured `mail_hostname`.
- Configure SPF, DKIM, and DMARC records for each sending domain.
- Publish the required SMTP and IMAP/POP ports through an approved public network path.
- Use Submission port `587` for authenticated sending when port `25` is restricted by your environment.

## Scaling

For resource tuning, open the deployment Canvas and adjust CPU, memory, and storage on the relevant workload, database, or volume resource cards. Keep the shared mail StatefulSet at one replica with the default ReadWriteOnce volume. Validate mail flow after every storage or networking change.

## Troubleshooting

### Admin Login Fails

- Confirm that you are opening the root App URL from Sealos.
- Use the `admin_username` and `admin_password` values configured during deployment.
- Wait until the BillionMail workload, PostgreSQL cluster, Redis cluster, and initialization job are complete before retrying.

### Mail Delivery Fails

- Check MX, SPF, DKIM, and DMARC records for the sending domain.
- Confirm that `mail_hostname` points to the intended mail host.
- Review whether your cloud or network provider restricts SMTP port `25`.

### Webmail Login Fails

- Create the domain and mailbox in BillionMail first.
- Open Roundcube at `/roundcube` and use the mailbox credentials.

## Additional Resources

- [BillionMail Website](https://www.billionmail.com/)
- [BillionMail GitHub](https://github.com/Billionmail/BillionMail)
- [BillionMail Template on Sealos](https://sealos.io/products/app-store/billionmail)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This Sealos template is provided under the templates repository license. BillionMail is distributed by its upstream project; review the [BillionMail GitHub repository](https://github.com/Billionmail/BillionMail) for current license terms.
