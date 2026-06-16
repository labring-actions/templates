# Deploy and Host Tududi on Sealos

Tududi is a self-hosted productivity app for managing tasks, projects, notes, areas, and personal workflows. This template deploys Tududi as a single persistent web application on Sealos Cloud.

![Tududi Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tududi/website-screenshot.webp)

## About Hosting Tududi

Tududi brings tasks, projects, notes, smart views, areas, tags, and personal planning into one calm workspace. It is designed for self-hosting and creates the initial administrator account from deployment environment variables.

This Sealos template runs the official Tududi container with persistent storage for the SQLite database and uploaded files. Sealos provides the public HTTPS URL, ingress, service discovery, resource controls, and persistent volumes around the application.

## Common Use Cases

- **Personal task management**: Capture inbox items, plan today, review upcoming work, and organize recurring tasks.
- **Project planning**: Group tasks into projects, track statuses, and keep related work in one place.
- **Notes and knowledge capture**: Store notes alongside tasks, projects, areas, and tags.
- **Self-hosted productivity**: Keep your workflow data in your own deployment with a lightweight SQLite-backed app.

## Dependencies for Tududi Hosting

The Sealos template includes all required runtime dependencies in the official Tududi image. It provisions two persistent volumes: one for the SQLite database and one for uploaded files.

### Deployment Dependencies

- [Official Website](https://tududi.com/) - Product website
- [Official Documentation](https://docs.tududi.com/) - Tududi documentation
- [GitHub Repository](https://github.com/chrisvel/tududi) - Source code and issue tracker

## Implementation Details

### Architecture Components

This template deploys the following resources:

- **Tududi StatefulSet**: Runs `chrisvel/tududi:1.1.0` on port `3002`.
- **SQLite database volume**: Persists `/app/backend/db`, including the production SQLite database and automatic database backups.
- **Uploads volume**: Persists `/app/backend/uploads` for user-uploaded files.
- **Service and Ingress**: Expose Tududi through a Sealos-managed HTTPS URL.
- **Sealos App entry**: Adds Tududi to the Sealos application launcher.

### Configuration

The template configures Tududi with the initial administrator email, administrator password, session secret, public URL, secure cookies, trusted proxy handling, and upload directory. Tududi uses SQLite in production according to the official application configuration, so this template keeps the database in the application volume.

The deployment uses one replica because Tududi stores the SQLite database and uploads on local persistent volumes. Keep the replica count at one to preserve data consistency. Upstream clustered database and shared object storage support can make multi-replica deployments viable later.

### License Information

Tududi is licensed under the MIT License.

## Why Deploy Tududi on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Tududi on Sealos, you get:

- **One-click deployment**: Deploy Tududi from the App Store with a simple form.
- **Automatic HTTPS access**: Sealos provisions a public URL and TLS certificate for the app.
- **Persistent storage included**: The database and uploads survive restarts and upgrades.
- **Resource controls**: Adjust CPU and memory from the Sealos dashboard as your workspace grows.
- **Operational visibility**: Check pods, logs, events, and storage from the same platform.

## Deployment Guide

1. Open the [Tududi template](https://sealos.io/products/app-store/tududi) and click **Deploy Now**.
2. Configure the parameters in the popup dialog:
   - **Initial administrator email address**: Email used for the first login.
   - **Initial administrator password**: Password used for the first login. Save this value and change it after first login.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Open the Tududi public URL from the App entry or the Ingress card.
5. Log in with the administrator email and password configured during deployment.

## Configuration

After deployment, you can manage Tududi through:

- **Tududi user menu**: Update account settings after login.
- **Sealos AI dialog**: Describe environment variable or resource changes and let Sealos apply updates.
- **Resource cards**: Click the StatefulSet, Ingress, Service, or volume cards to inspect and modify runtime settings.

Keep the administrator email and password in a secure password manager. For production deployments, change the initial password after the first login.

## Scaling

Tududi runs as a single-replica StatefulSet because the official production configuration uses SQLite. To increase capacity:

1. Open the Canvas for your Tududi deployment.
2. Click the StatefulSet resource card.
3. Increase CPU or memory resources.
4. Apply the changes and wait for the pod to become ready.

## Troubleshooting

### Login fails

- Cause: The email or password differs from the values entered during deployment.
- Solution: Check the deployment inputs in Sealos and reset the administrator credentials through the Tududi database or by redeploying with the intended values.

### Uploaded files disappear after restart

- Cause: The uploads volume was modified or removed.
- Solution: Confirm that `/app/backend/uploads` is mounted to the persistent uploads volume.

### The app starts slowly after an upgrade

- Cause: Tududi may run database migrations and create automatic SQLite backups on startup.
- Solution: Check the application logs from the StatefulSet resource card and wait for migrations to finish.

### Getting Help

- [Official Documentation](https://docs.tududi.com/)
- [GitHub Issues](https://github.com/chrisvel/tududi/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Tududi Website](https://tududi.com/)
- [Tududi GitHub](https://github.com/chrisvel/tududi)
- [Tududi Docker Image](https://hub.docker.com/r/chrisvel/tududi)

## License

This Sealos template is provided under the repository license. Tududi itself is licensed under the MIT License.
