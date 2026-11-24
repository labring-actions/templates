# Deploy and Host Huginn on Sealos

Huginn is a self-hosted automation platform for watching events, processing data, and triggering agent workflows through a visual interface.

![Huginn project](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/huginn/website-screenshot.webp)

## About Hosting Huginn

This template runs the official Huginn image as a single StatefulSet with an embedded MariaDB database and a 1 GiB persistent volume. An administrator account named `admin` is seeded with the password supplied during deployment.

After the pod is ready, sign in at `/users/sign_in`. The **Agents** page is the main workspace: create agents, connect them through events, and schedule recurring jobs. Database content and agent definitions persist across pod restarts.

## Common Use Cases

- Monitor websites, RSS feeds, and APIs for changes.
- Forward filtered events to email, chat, or webhook endpoints.
- Build scheduled data collection and transformation pipelines.
- Combine multiple agents into event-driven automation flows.
- Prototype internal alerts and personal monitoring jobs.

## Dependencies for Huginn Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A 1 GiB persistent volume for the embedded database and application data.
- An administrator password supplied through the template input.
- Outbound network access for agents that call external websites and APIs.

## Why Deploy Huginn on Sealos?

- One-click deployment with the web interface exposed over public HTTPS.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent storage for users, agents, events, and credentials.
- Pay-as-you-go resource cards sized for personal and team automation.
- Canvas view for inspecting the StatefulSet, Service, Ingress, and PVC.
- AI dialog for deployment questions in the Sealos desktop.

## Deployment Guide

1. Open the [Huginn template](https://sealos.io/products/app-store/huginn) and click **Deploy Now**.
2. Enter the initial administrator password, keep the generated application name, and confirm the resource plan.
3. Wait 2-3 minutes for database migrations to finish, then open the public URL from the App card.
4. Sign in as `admin` with the password from step 2 and open the **Agents** page.
5. Create a test agent, then open Canvas to review the StatefulSet, Service, Ingress, and persistent volume.

## License

Huginn is released under the [MIT License](https://github.com/huginn/huginn/blob/master/LICENSE).
