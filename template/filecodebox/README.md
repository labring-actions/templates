# Deploy and Host FileCodeBox on Sealos

FileCodeBox is a lightweight anonymous text and file sharing service built with FastAPI and Vue. This template deploys FileCodeBox with persistent local storage by default and an optional Sealos Object Storage switch on Sealos Cloud.

![FileCodeBox Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/filecodebox/website-screenshot.webp)

## About Hosting FileCodeBox

FileCodeBox lets users share text snippets or files and receive an access code that recipients can use to retrieve the content. The public sharing flow supports guest uploads by default, while the `/admin` panel gives administrators dashboard metrics, file management, storage settings, and security controls.

This Sealos template runs FileCodeBox as a single StatefulSet with a persistent volume mounted at `/app/data`. The volume stores the SQLite database, local uploaded files, startup lock files, and runtime configuration, so shared content and admin settings survive restarts.

The template also exposes an optional `enable_s3_storage` switch. When enabled, Sealos provisions an `ObjectStorageBucket` and the template initializes FileCodeBox with its official S3-compatible settings, using proxied downloads for private bucket access.

## Common Use Cases

- **Temporary file transfer**: Share files across devices or teams using short access codes.
- **Text and code snippet sharing**: Share notes, logs, configuration snippets, and short documents without creating user accounts.
- **Private file drop box**: Host a lightweight internal file exchange service for a team or lab.
- **API-based transfer workflows**: Integrate the REST API into scripts that upload text or files and distribute access codes.
- **S3-backed storage**: Store shared files in a Sealos-managed S3-compatible bucket while keeping FileCodeBox metadata in SQLite.

## Dependencies for FileCodeBox Hosting

The Sealos template includes the FileCodeBox container image, a StatefulSet, a persistent volume, a Kubernetes Service, an Ingress, and a Sealos App entry. When object storage is selected, the template also creates a Sealos `ObjectStorageBucket` and injects the generated S3 credentials into the application.

### Deployment Dependencies

- [FileCodeBox Documentation](https://fcb-docs.aiuo.net/en/) - Official English documentation
- [FileCodeBox GitHub Repository](https://github.com/vastsa/FileCodeBox) - Source code, Dockerfile, and issue tracker
- [Storage Configuration](https://fcb-docs.aiuo.net/en/guide/storage.html) - Official storage backend guide
- [API Documentation](https://fcb-docs.aiuo.net/en/api/) - REST API reference

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **FileCodeBox Web Service**: Runs `lanol/filecodebox` on port `12345` and serves the web UI, sharing API, admin API, and background cleanup tasks.
- **Persistent Storage**: A `1Gi` volume mounted at `/app/data` stores the SQLite database and local files.
- **Optional Object Storage**: A Sealos `ObjectStorageBucket` stores uploaded files through FileCodeBox's official S3-compatible storage settings.
- **Ingress and App Entry**: Sealos exposes FileCodeBox through an HTTPS URL and creates a dashboard entry for direct access.

**Configuration:**

The template asks for:

- `admin_password`: Initial password for the FileCodeBox `/admin` panel.
- `enable_s3_storage`: Enable Sealos Object Storage as FileCodeBox's S3-compatible file backend.

On first startup, the container initializes FileCodeBox's SQLite settings row with the selected admin password and storage mode. Later changes made in the FileCodeBox admin panel are stored in `/app/data/filecodebox.db`.

**License Information:**

FileCodeBox is licensed under the GNU Lesser General Public License v3.0. This Sealos template is deployment configuration for FileCodeBox and does not change the upstream application license.

## Why Deploy FileCodeBox on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the application lifecycle from deployment to operations. By deploying FileCodeBox on Sealos, you get:

- **One-Click Deployment**: Deploy FileCodeBox, storage, networking, and the App entry from one template.
- **Persistent Storage Included**: Keep SQLite data and uploaded files across restarts.
- **Optional Object Storage**: Create a private Sealos bucket from the same deployment form.
- **Instant Public Access**: Each deployment receives an HTTPS URL for sharing and administration.
- **Easy Customization**: Adjust resources, storage, and environment variables through the Sealos Canvas and AI dialog.
- **Pay-As-You-Go Resources**: Start with a compact resource profile for lightweight sharing workloads.

Deploy FileCodeBox on Sealos and run a small, self-hosted file sharing service with managed Kubernetes primitives underneath.

## Deployment Guide

1. Open the [FileCodeBox template](https://sealos.io/products/app-store/filecodebox) and click **Deploy Now**.
2. Enter an `admin_password` for the `/admin` panel.
3. Leave `enable_s3_storage` disabled to store uploaded files on the persistent volume mounted at `/app/data`, or enable it to provision a private Sealos Object Storage bucket and configure FileCodeBox to use S3-compatible storage.
4. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
5. Open the generated FileCodeBox URL from the App entry.
6. Share text or files from the homepage, then copy the generated access code.
7. Open `https://[your-app-url]/admin` and sign in with the configured `admin_password` to view the dashboard, manage files, and adjust FileCodeBox settings.

## Configuration

After deployment, you can configure FileCodeBox through:

- **FileCodeBox Admin Panel**: Visit `/admin`, sign in with the configured password, and update site settings, upload limits, storage settings, themes, and security options.
- **Sealos AI Dialog**: Describe environment, resource, or storage changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, Ingress, Service, App, persistent volume, or Object Storage cards in Canvas to inspect and adjust settings.

For public services, review the upload size, upload rate limit, expiration modes, and admin password immediately after deployment. FileCodeBox stores admin configuration in SQLite, so changes persist on the `/app/data` volume.

## Scaling

To scale FileCodeBox on Sealos:

1. Open the Canvas for your FileCodeBox deployment.
2. Click the FileCodeBox StatefulSet resource card.
3. Increase CPU or memory when file traffic, concurrent uploads, or API usage grows.
4. Apply the change and wait for the pod to become ready.

The default template uses one worker and a compact resource profile suitable for light sharing workloads. For larger files or sustained traffic, increase the resource limits and consider the object storage backend.

## Troubleshooting

### Admin login fails

Use the `admin_password` entered during deployment and visit `/admin` directly. After changing the password in the admin panel, use the new password for future logins.

### Uploaded files fill the persistent volume

Review expired files from the admin panel and increase the StatefulSet storage volume from the Sealos resource card when you need more local capacity. Object storage is a better fit for larger file volume.

### S3-backed downloads fail

Open `/admin`, verify `file_storage=s3`, confirm the bucket configuration, and keep proxied downloads enabled for private Sealos Object Storage buckets.

### Getting Help

- [FileCodeBox Documentation](https://fcb-docs.aiuo.net/en/)
- [FileCodeBox GitHub Issues](https://github.com/vastsa/FileCodeBox/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [FileCodeBox API Reference](https://fcb-docs.aiuo.net/en/api/)
- [FileCodeBox Storage Guide](https://fcb-docs.aiuo.net/en/guide/storage.html)
- [FileCodeBox Docker Image](https://hub.docker.com/r/lanol/filecodebox)

## License

This Sealos template is provided under the repository's template license. FileCodeBox itself is licensed under the GNU Lesser General Public License v3.0.
