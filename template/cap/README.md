# Deploy and Host Cap on Sealos

Cap is an open-source screen recording and video sharing platform for teams that want to own their recording workflow and data. This template deploys Cap Web with a media server, MySQL database, and S3-compatible object storage on Sealos Cloud.

![Cap app preview](https://raw.githubusercontent.com/CapSoftware/Cap/refs/heads/main/apps/web/public/landing-cover.png)

## About Hosting Cap

Cap provides a web dashboard for viewing, sharing, and managing screen recordings created with the Cap desktop app. It supports share links, team collaboration, comments, transcripts, analytics, custom storage, and self-hosted deployments for teams that need tighter control over their data.

This Sealos template provisions the services needed for a self-hosted Cap deployment. Cap Web serves the user interface, API routes, authentication flow, and dashboard, while the media server handles media processing tasks used by the web app. Sealos also creates a MySQL database and an S3-compatible object storage bucket so metadata and recording assets survive restarts.

The deployment includes public HTTPS access, service discovery between components, generated application secrets, a database initialization job, and health checks for the web and media services.

## Common Use Cases

- **Product Demos**: Record polished walkthroughs and share them with prospects, customers, or internal teams.
- **Bug Reports**: Capture reproducible issues with screen, camera, and microphone context.
- **Async Standups**: Replace status meetings with short video updates that teammates can watch on their schedule.
- **Customer Onboarding**: Build reusable tutorials, feature tours, and help videos.
- **Design and Engineering Reviews**: Share UI feedback, code walkthroughs, or implementation notes with comments attached to the recording.

## Dependencies for Cap Hosting

The Sealos template includes all required runtime dependencies for a basic self-hosted Cap deployment: Cap Web, Cap Media Server, MySQL, an S3-compatible object storage bucket, and an initialization job that prepares the `cap` database.

### Deployment Dependencies

- [Cap Website](https://cap.so) - Product website and downloads
- [Cap Documentation](https://cap.so/docs) - Official product documentation
- [Self-Hosting Guide](https://cap.so/docs/self-hosting) - Self-hosting notes and production configuration
- [Cap GitHub Repository](https://github.com/CapSoftware/Cap) - Source code, issues, and releases
- [Cap Discord](https://cap.link/discord) - Community support

### Implementation Details

**Architecture Components:**

This template deploys the following resources:

- **Cap Web**: The main Next.js web application that serves the dashboard, sharing pages, API routes, authentication, and database migrations.
- **Cap Media Server**: A companion service used by Cap Web for media processing workflows.
- **MySQL**: A KubeBlocks-managed MySQL database used for Cap metadata, users, recordings, and application state.
- **MySQL Init Job**: A startup-safe job that waits for MySQL, creates the `cap` database, and configures MySQL authentication compatibility.
- **Object Storage Bucket**: A Sealos S3-compatible bucket used for recording files and media assets.
- **Ingress and App Link**: A public HTTPS endpoint and Sealos App resource for opening Cap from the dashboard.

**Configuration:**

Cap Web receives generated defaults for `DATABASE_ENCRYPTION_KEY`, `NEXTAUTH_SECRET`, and `MEDIA_SERVER_WEBHOOK_SECRET`. It connects to MySQL through KubeBlocks-managed connection secrets and uses Sealos object storage credentials for S3-compatible uploads.

The template exposes optional `RESEND_API_KEY` and `RESEND_FROM_DOMAIN` inputs for email delivery. If these values are left empty, Cap still starts, but email verification messages are not sent through Resend; use the service logs to retrieve the development-mode verification code during testing.

**License Information:**

Cap is primarily licensed under AGPLv3, with selected capture-related crates under the MIT License. Review the [Cap license file](https://github.com/CapSoftware/Cap/blob/main/LICENSE) before using Cap in production.

## Why Deploy Cap on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from development to production deployment and operations. By deploying Cap on Sealos, you get:

- **One-Click Deployment**: Deploy the full Cap stack without hand-writing Kubernetes manifests.
- **Built-In Kubernetes Operations**: Run Cap on Kubernetes with managed networking, service discovery, and workload orchestration.
- **Persistent Data Services**: Store metadata in MySQL and recording assets in S3-compatible object storage.
- **Instant Public Access**: Get an automatic public URL with HTTPS certificates after deployment.
- **Easy Customization**: Update environment variables, resources, and storage through the Canvas, AI dialog, or resource cards.
- **Pay-as-You-Go Efficiency**: Start with a compact deployment and adjust resources as usage grows.
- **Automated Platform Management**: Let Sealos handle common infrastructure tasks while you focus on using Cap.

Deploy Cap on Sealos when you want a self-hosted screen recording platform without managing the Kubernetes plumbing yourself.

## Deployment Guide

1. Open the [Cap template](https://sealos.io/products/app-store/cap) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. For production email delivery, set `RESEND_API_KEY` and `RESEND_FROM_DOMAIN`; for testing, you can leave them empty.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Cap via the provided public URL:
   - **Cap Web**: Sign in with your email verification code or email link.
   - **Desktop App Connection**: Point Cap Desktop to your deployed Cap URL from `Settings > Cap Server URL` when using a self-hosted server.

## Configuration

After deployment, you can configure Cap through:

- **AI Dialog**: Describe environment, resource, or domain changes and let AI apply updates.
- **Resource Cards**: Open the Cap Web, Media Server, MySQL, or Object Storage cards to inspect and modify settings.
- **Email Delivery**: Set `RESEND_API_KEY` and `RESEND_FROM_DOMAIN` to send login emails through Resend.
- **Desktop Client**: Configure Cap Desktop to use your deployed URL as its Cap Server URL.
- **Secrets and URLs**: Keep generated secrets stable after users start recording, because changing encryption or auth secrets can invalidate sessions or encrypted data.

## Scaling

To scale Cap on Sealos:

1. Open the Canvas for your deployment.
2. Click the Cap Web or Cap Media Server resource card.
3. Adjust CPU, memory, or replica count based on traffic and processing needs.
4. Apply the changes in the dialog and monitor the rollout from the Canvas.

For larger teams, increase Cap Web resources first, then scale the media server if media processing becomes the bottleneck. Keep MySQL and object storage sized according to recording volume and retention requirements.

## Troubleshooting

### Common Issues

**No login email arrives**
- Cause: `RESEND_API_KEY` and `RESEND_FROM_DOMAIN` are empty or incorrect.
- Solution: Configure Resend credentials. For test deployments without email, view the Cap Web logs from the Canvas resource card and copy the development-mode verification code.

**Cap Web restarts during startup**
- Cause: The web service may need more memory while Next.js starts and migrations run.
- Solution: Increase the Cap Web memory limit from the resource card, then wait for the rollout to complete.

**Recordings upload but cannot be viewed**
- Cause: Object storage endpoint or bucket access settings may be incorrect.
- Solution: Check the Object Storage bucket, S3 environment variables, and public endpoint configuration in the Cap Web resource card.

### Getting Help

- [Cap Documentation](https://cap.so/docs)
- [Cap GitHub Issues](https://github.com/CapSoftware/Cap/issues)
- [Cap Discord](https://cap.link/discord)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Cap Self-Hosting Guide](https://cap.so/docs/self-hosting)
- [Cap Downloads](https://cap.so/download)
- [Cap GitHub Repository](https://github.com/CapSoftware/Cap)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is maintained for the Sealos templates repository. Cap itself is primarily licensed under AGPLv3, with selected capture-related crates under the MIT License; see the [Cap license file](https://github.com/CapSoftware/Cap/blob/main/LICENSE) for details.
