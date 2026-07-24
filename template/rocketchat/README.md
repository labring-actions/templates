# Deploy and Host Rocket.Chat on Sealos

Rocket.Chat is an open-source communications platform for private team messaging, channels, file sharing, and workspace administration. This template deploys Rocket.Chat 8.6.1 with a dedicated MongoDB 8.0.4 replica set on Sealos Cloud.

![Rocket.Chat workspace](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rocketchat/website-screenshot.webp)

## Features

- Team channels, direct messages, file sharing, search, and workspace administration
- Initial administrator account created from deployment inputs
- Private MongoDB database managed by KubeBlocks
- GridFS upload storage by default, with optional private Sealos Object Storage
- Automatic HTTPS, public domain, health checks, and Prometheus metrics
- Restricted non-root container security context

## Common Use Cases

- Private communication for distributed teams and regulated organizations
- Incident response and operational coordination channels
- Self-hosted alternatives to third-party workplace messaging services
- Internal communities with controlled data residency

## Architecture

This template deploys the following resources:

- **Rocket.Chat 8.6.1** runs as a single monolithic StatefulSet and serves the web interface, REST API, real-time messaging, and administration tools.
- **MongoDB 8.0.4** runs as a one-member KubeBlocks replica set and stores users, rooms, messages, settings, and GridFS uploads.
- **Sealos Object Storage** is created when `enable_s3_storage` is enabled and stores uploaded files in a private S3-compatible bucket.
- **Sealos Ingress** publishes the workspace through an automatically generated HTTPS domain.

The application starts with a tested resource floor of 200 millicores and 2 GiB memory. MongoDB uses 500 millicores and 512 MiB memory. A cold application start typically takes about two minutes after MongoDB becomes ready.

## Dependencies

- A Sealos Cloud account and workspace
- A modern web browser for deployment and workspace access
- A reachable administrator email address when connecting to Rocket.Chat Cloud

Sealos provisions the Kubernetes runtime, KubeBlocks database, persistent volumes, networking, and optional object storage as part of the deployment.

## Deployment Inputs

| Input | Required | Purpose |
| --- | --- | --- |
| `admin_username` | Yes | Username for the initial workspace administrator |
| `admin_name` | Yes | Display name for the initial workspace administrator |
| `admin_email` | Yes | Email address for the initial workspace administrator |
| `admin_password` | Yes | Password for the initial workspace administrator |
| `enable_s3_storage` | No | Creates private Sealos Object Storage for uploaded files; defaults to GridFS |

Use a reachable email address when you plan to connect the workspace to Rocket.Chat Cloud during the setup wizard.

## Deployment Guide

1. Open the [Rocket.Chat template](https://sealos.io/products/app-store/rocketchat) and click **Deploy Now**.
2. Enter the initial administrator username, display name, email address, and password.
3. Keep GridFS as the upload store or enable **S3 storage** to provision a private Sealos Object Storage bucket.
4. Confirm the deployment. Sealos creates the application, MongoDB, storage, HTTPS domain, and dashboard entry.
5. Wait for deployment to complete, typically 2-3 minutes, then open the Rocket.Chat application card from the Canvas.

For later changes, use the Canvas AI dialog or open the relevant resource card to adjust configuration and resources.

## Why Deploy on Sealos

- Deploy the complete Rocket.Chat and MongoDB topology from one template
- Use a managed KubeBlocks database and an optional private object storage bucket
- Receive an HTTPS domain and application dashboard automatically
- Inspect logs, health, and resource usage from the same Canvas workspace

## First Sign-In

1. Open the generated Rocket.Chat URL.
2. Sign in with the `admin_username` and `admin_password` entered during deployment.
3. Complete the organization details in the setup wizard.
4. When connecting to Rocket.Chat Cloud, accept the terms and use the confirmation link sent to the administrator email address.
5. Return to the workspace and create a channel or invite team members.

Returning administrators use the same username or email address and password. Additional users can use **Create account** when workspace registration is enabled by the administrator.

## Storage Options

### GridFS

GridFS is the default storage mode. Uploaded files are stored inside MongoDB and follow the database lifecycle. This mode is suitable for evaluation and small workspaces.

### Sealos Object Storage

Enable `enable_s3_storage` during deployment to create a private S3-compatible bucket. Rocket.Chat receives the bucket endpoint and credentials through Sealos-managed secrets, uses path-style access, and protects file links with short-lived signed URLs. This mode keeps uploaded objects separate from the database and is the recommended option for long-lived workspaces.

## Operations

Use the Sealos Canvas after deployment to:

- Check Rocket.Chat and MongoDB health, resource usage, and logs
- Open the generated HTTPS domain
- Manage the MongoDB database and optional object storage bucket
- Adjust resource limits and application settings
- Back up persistent application data through Sealos services

## Learn More

- [Rocket.Chat website](https://rocket.chat/)
- [Rocket.Chat documentation](https://docs.rocket.chat/)
- [Docker deployment guide](https://docs.rocket.chat/deploy-with-docker-docker-compose)
- [Rocket.Chat source code](https://github.com/RocketChat/Rocket.Chat)
- [Sealos documentation](https://sealos.io/docs/)

## License

Rocket.Chat 8.6.1 uses a mixed license model. Community source outside the enterprise directories is available under the MIT License, while source under `apps/meteor/ee/` and `ee/` follows the Rocket.Chat Enterprise Edition license. Review the [official 8.6.1 license](https://github.com/RocketChat/Rocket.Chat/blob/8.6.1/LICENSE) and the applicable subscription terms before production use.
