# Deploy and Host DocuSeal on Sealos

DocuSeal is an open source platform for building, filling, and signing PDF forms online. This template deploys DocuSeal with PostgreSQL, persistent file storage, and a public HTTPS endpoint on Sealos Cloud.

![DocuSeal Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/docuseal/website-screenshot.webp)

## About Hosting DocuSeal

DocuSeal provides a self-hosted document workflow for uploading PDFs, adding fillable fields, collecting signatures, and managing completed submissions. It is useful when you need a controllable eSignature system that keeps data inside your own deployment.

This Sealos template runs DocuSeal as a single web service and provisions a Kubeblocks PostgreSQL database for application data. Uploaded documents and generated files are stored on a persistent volume mounted at `/data/docuseal`, so files survive restarts and rolling updates.

Sealos also configures the public HTTPS route, service discovery, persistent storage, and resource limits automatically. The template sets DocuSeal's public `APP_URL` to the generated Sealos domain so setup pages, email links, webhook URLs, and Open Graph metadata use the correct external URL.

## Common Use Cases

- **Internal document approvals**: Prepare PDF forms and collect signatures from employees, contractors, or partners.
- **Customer agreements**: Send service agreements, onboarding documents, and consent forms for online signing.
- **Operations paperwork**: Digitize repeatable forms such as handover documents, checklists, and acknowledgements.
- **API-driven signing flows**: Use DocuSeal's API and webhooks to integrate document signing into existing products.
- **Self-hosted eSignature workflows**: Keep signing data and files in your own Sealos workspace instead of relying only on a hosted SaaS account.

## Dependencies for DocuSeal Hosting

The Sealos template includes the required runtime components: the DocuSeal container image, a PostgreSQL `postgresql-16.4.0` database, a database initialization job for the `docuseal` database, persistent application storage, a Kubernetes Service, an Ingress, and a Sealos App entry.

### Deployment Dependencies

- [DocuSeal Website](https://www.docuseal.com/) - Product overview and hosted cloud option
- [DocuSeal GitHub Repository](https://github.com/docusealco/docuseal) - Source code, Docker image, and release notes
- [DocuSeal Documentation](https://www.docuseal.com/docs) - Product and integration documentation
- [DocuSeal API Reference](https://www.docuseal.com/docs/api) - API endpoints for automation and integrations

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **DocuSeal Web Service**: Runs `docuseal/docuseal:3.0.1` on port `3000` and serves the web UI, API, embedded signing pages, and background jobs.
- **PostgreSQL**: Kubeblocks-managed PostgreSQL `postgresql-16.4.0` stores users, accounts, templates, submissions, and application metadata.
- **PostgreSQL Init Job**: Creates the `docuseal` database idempotently after PostgreSQL is ready.
- **Persistent Storage**: A `1Gi` volume mounted at `/data/docuseal` stores DocuSeal runtime files and uploaded attachments.
- **Ingress and App Entry**: Sealos exposes the web service through an HTTPS domain and creates a dashboard entry for direct access.

**Configuration:**

The template automatically configures:

- `APP_URL` as `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`.
- `HOST` as the generated Sealos hostname.
- `FORCE_SSL=true` so DocuSeal treats the public route as HTTPS.
- `SECRET_KEY_BASE` as a generated secret value.
- `DATABASE_URL` from the Kubeblocks PostgreSQL connection Secret.

No required user inputs are needed during deployment. Optional SMTP, object storage, SSO, or license-related settings can be configured after deployment from the DocuSeal UI or by editing the workload environment variables in the Sealos Canvas.

**License Information:**

DocuSeal is distributed under the AGPLv3 License with additional terms from DocuSeal LLC. This Sealos template is provided as deployment configuration for DocuSeal and does not change the upstream application license.

## Why Deploy DocuSeal on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying DocuSeal on Sealos, you get:

- **One-Click Deployment**: Deploy DocuSeal, PostgreSQL, storage, networking, and the dashboard entry from one template.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed reliability without writing manifests manually.
- **Persistent Storage Included**: Keep uploaded documents, generated files, and database data across restarts.
- **Instant Public Access**: Each deployment receives an HTTPS URL suitable for setup, signing pages, and API callbacks.
- **Easy Customization**: Adjust environment variables, resources, and storage through the Sealos Canvas and AI dialog.
- **Pay-As-You-Go Resources**: Start from a compact resource profile and scale only when your signing workload grows.

Deploy DocuSeal on Sealos and focus on document workflows instead of managing infrastructure.

## Deployment Guide

1. Open the [DocuSeal template](https://sealos.io/products/app-store/docuseal) and click **Deploy Now**.
2. Keep the default parameters unless you need a custom generated name or host.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Open the generated DocuSeal URL from the App entry.
5. Complete the first-run setup form:
   - Enter the first administrator's first name and last name.
   - Enter the administrator email address.
   - Enter your company or workspace name.
   - Set the administrator password.
   - Keep the App URL field as the generated Sealos HTTPS URL unless you have configured a custom domain.
   - Select the preferred interface language and submit the form.
6. After setup, use the same email and password on the sign-in page for future logins.

## Configuration

After deployment, you can configure DocuSeal through:

- **Initial Setup Page**: Creates the first administrator account and stores the public App URL.
- **DocuSeal Account Settings**: Manage users, branding, signing preferences, webhooks, API tokens, and account-level options.
- **Sealos AI Dialog**: Describe environment or resource changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, PostgreSQL, Ingress, or storage cards in Canvas to inspect and adjust settings.

If you enable outbound email, configure SMTP-related environment variables before sending user invitations or signing emails. If you change the public domain later, update DocuSeal's App URL in account settings so generated signing links continue to use the right hostname.

## Scaling

To scale DocuSeal on Sealos:

1. Open the Canvas for your DocuSeal deployment.
2. Click the DocuSeal StatefulSet resource card.
3. Increase CPU or memory when large PDFs, frequent uploads, or high signing traffic require more capacity.
4. Apply the change and wait for the pod to become ready.

The default template uses a compact resource profile suitable for evaluation and light usage. For heavier production workloads, increase the application resources and consider external object storage for large attachment volumes.

## Troubleshooting

### The app opens the setup page

This is expected on a fresh deployment. Create the first administrator account on the setup page. After the first user exists, DocuSeal redirects unauthenticated visitors to the sign-in page.

### Generated links use the wrong domain

Open DocuSeal account settings and update the App URL to the current Sealos HTTPS URL or your custom domain. The template sets `APP_URL` automatically for new deployments, but manual domain changes should also be reflected inside DocuSeal.

### Invitation or signing emails are not sent

DocuSeal needs SMTP configuration for outbound email. Add the required SMTP environment variables in the StatefulSet resource card, restart the workload, and test email delivery from DocuSeal settings.

### Getting Help

- [DocuSeal Documentation](https://www.docuseal.com/docs)
- [DocuSeal GitHub Issues](https://github.com/docusealco/docuseal/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [DocuSeal API Reference](https://www.docuseal.com/docs/api)
- [DocuSeal Docker Image](https://hub.docker.com/r/docuseal/docuseal)
- [DocuSeal GitHub Releases](https://github.com/docusealco/docuseal/releases)

## License

This Sealos template is provided under the repository's template license. DocuSeal itself is licensed under AGPLv3 with additional terms from DocuSeal LLC.
