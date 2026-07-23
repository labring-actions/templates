# Penpot

Open-source design and prototyping for collaborative product teams. This template deploys Penpot 2.16.2 with dedicated frontend, backend, exporter, PostgreSQL, and Redis services on Sealos Cloud.

![Penpot workspace](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/penpot/website-screenshot.webp)

## Features

- Collaborative interface design, prototyping, design systems, and developer handoff
- Browser-based registration and password login enabled at first launch
- Private PostgreSQL database and authenticated Redis service managed by KubeBlocks
- Persistent filesystem storage by default, with optional private Sealos Object Storage
- Automatic HTTPS, public domain, health checks, and application monitoring

## Architecture

This template deploys the following services:

- **Penpot Frontend** serves the web interface and proxies API, asset, WebSocket, and export requests.
- **Penpot Backend** handles authentication, projects, files, collaboration, and asset storage.
- **Penpot Exporter** renders downloadable design exports in an isolated service.
- **PostgreSQL** stores accounts, teams, projects, files, and application metadata.
- **Redis** provides authenticated messaging and real-time notification coordination.
- **Sealos Object Storage** is created only when `enable_s3_storage` is enabled.

The default filesystem mode provisions one shared persistent volume for frontend and backend asset delivery. The S3 mode stores uploaded objects in a private Sealos bucket while keeping the same application and database topology.

## Deployment Guide

1. Open the [Penpot template](https://sealos.io/products/app-store/penpot) and click **Deploy Now**.
2. Keep the default filesystem storage or enable **S3 storage** to provision a private Sealos Object Storage bucket.
3. Confirm the deployment. Sealos creates the application, databases, storage, HTTPS domain, and dashboard entry automatically.
4. Wait for deployment to complete, typically 2-3 minutes. You will be redirected to the Canvas when the resources are ready.
5. Open the Penpot application card from the Canvas.

For later changes, describe the update in the Canvas AI dialog or open the relevant resource card to adjust configuration and resources.

## Register and Sign In

Penpot opens at the sign-in page.

1. Click **Create an account**.
2. Enter your full name, work email, and a password with at least 8 characters.
3. Complete the short onboarding flow to reach the dashboard.
4. Create a project, then create a design file to start working.

Email verification is disabled for this self-hosted template, so the account becomes active immediately. Returning users can sign in with the same email and password. Configure SMTP and enable email verification through the Penpot backend settings before using an internet-facing deployment with unrestricted registration.

## Storage Options

### Persistent filesystem

The default mode stores uploaded assets on a 1 GiB ReadWriteOnce volume shared by the frontend and backend. The scheduler co-locates both workloads on one node and prefers that node during backend replacement. This mode fits a personal workspace or evaluation deployment.

### Sealos Object Storage

Enable `enable_s3_storage` during deployment to create a private bucket and inject its S3-compatible credentials into Penpot. This mode keeps application assets independent from workload scheduling and is the recommended choice for long-lived or multi-node deployments.

The public upload path uses a consistent 32 MiB per-file limit across Penpot Frontend, Penpot Backend, and the Sealos Ingress.

## Operations

Use the Sealos Canvas after deployment to:

- View frontend, backend, exporter, PostgreSQL, and Redis status
- Inspect logs and health checks for each service
- Update resource limits or environment settings through the resource cards
- Open the database or object storage management surfaces
- Manage the generated HTTPS domain

## Learn More

- [Penpot website](https://penpot.app/)
- [Penpot documentation](https://help.penpot.app/)
- [Penpot source code](https://github.com/penpot/penpot)
- [Sealos documentation](https://sealos.io/docs/)
