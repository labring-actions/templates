# Deploy and Host copyparty on Sealos

copyparty is a portable file server with browser-based upload, download, media indexing, thumbnails, and sharing controls. This template deploys copyparty with persistent storage on Sealos Cloud.

![Application Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/copyparty/website-screenshot.webp)

## About Hosting copyparty

copyparty runs as a single web service using the official `copyparty/ac` image, which includes FFmpeg and media thumbnail support. The Sealos template provisions persistent volumes for shared files, configuration, and runtime state so uploads and generated indexes survive restarts.

The deployment exposes the browser UI over an automatically managed HTTPS domain. The template creates an `admin` account from the password you set during deployment, and the shared `/w` volume is writable for that account.

## Common Use Cases

- **Private File Drop**: Receive files from trusted users through a browser.
- **Media Browsing**: Browse uploaded audio, video, and image files with thumbnails.
- **Team File Sharing**: Host a lightweight shared file area for small teams.
- **Temporary Transfer Hub**: Create a short-lived transfer service with persistent storage.

## Dependencies for copyparty Hosting

The Sealos template includes the copyparty application container and persistent storage volumes.

### Deployment Dependencies

- [copyparty GitHub Repository](https://github.com/9001/copyparty) - Source code and documentation
- [Docker Usage Guide](https://github.com/9001/copyparty/tree/v1.20.16/scripts/docker) - Official container guidance
- [copyparty CLI Help](https://copyparty.eu/cli/) - Account, volume, and permission options

### Implementation Details

**Architecture Components:**

This template deploys one service:

- **copyparty**: Web file server listening on port `3923`
- **Persistent Storage**: Volumes mounted at `/w`, `/cfg`, and `/state`

**Configuration:**

- The default account is `admin`.
- Set `admin_password` during deployment and save it for login.
- Uploaded files are stored under `/w`.
- copyparty runtime state and history are stored under `/state`.
- For large upload limits, adjust the Ingress body size from the Canvas after deployment.

**License Information:**

copyparty is licensed under the MIT License.

## Why Deploy copyparty on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and day-2 operations. By deploying copyparty on Sealos, you get:

- **One-Click Deployment**: Deploy copyparty from the App Store without writing Kubernetes YAML.
- **Persistent Storage Included**: Keep uploaded files and indexes across restarts.
- **Instant Public Access**: Use the generated HTTPS URL immediately after deployment.
- **AI-Assisted Operations**: Use the Canvas AI dialog to adjust resources, domains, and storage.
- **Pay-as-You-Go Efficiency**: Start with small resources and scale when your workload grows.

## Deployment Guide

1. Open the [copyparty template](https://sealos.io/products/app-store/copyparty) and click **Deploy Now**.
2. Configure the `admin_password` parameter in the popup dialog.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access copyparty through the provided URL and log in with:
   - **Username**: `admin`
   - **Password**: the `admin_password` value you configured

## Configuration

After deployment, you can configure copyparty through:

- **AI Dialog**: Describe the storage, resource, or domain change you want.
- **Resource Cards**: Adjust CPU, memory, storage, and Ingress settings.
- **copyparty Config Files**: Add `.conf` files under the `/cfg` volume for advanced copyparty configuration.

## Scaling

To scale resources, open the Canvas, click the copyparty StatefulSet resource card, adjust CPU or memory, and apply the change. Keep replicas at one unless you have designed shared storage and session behavior for multiple instances.

## Troubleshooting

**Login fails**

Use username `admin` and the exact `admin_password` value from deployment.

**Large uploads are rejected**

Increase the Ingress body size from the Canvas resource card.

## Additional Resources

- [copyparty Documentation](https://github.com/9001/copyparty)
- [copyparty Docker Guide](https://github.com/9001/copyparty/tree/v1.20.16/scripts/docker)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. copyparty itself is licensed under the MIT License.
