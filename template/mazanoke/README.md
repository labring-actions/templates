# Deploy and Host MAZANOKE on Sealos

MAZANOKE is a self-hosted local image optimizer that runs in the browser. This template deploys MAZANOKE as a single web service on Sealos Cloud.

![MAZANOKE Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mazanoke/website-screenshot.webp)

## About Hosting MAZANOKE

MAZANOKE serves a browser-based image optimization interface where users can compress, resize, and convert images without uploading them to a remote processing service. The application assets are served by Nginx, while image processing runs client-side in the user's browser.

The Sealos template provisions the web container, service, HTTPS ingress, and App entry. MAZANOKE is account-free by default, so users can open the app and start processing images immediately.

## Common Use Cases

- **Private Image Compression**: Reduce image file sizes while keeping image data on the user's device.
- **Format Conversion**: Convert images between JPG, PNG, WebP, and ICO, with input support for formats such as HEIC, AVIF, TIFF, GIF, and SVG.
- **Offline-Friendly Utility**: Install MAZANOKE as a web app and continue using it after the initial load.
- **Team Utility Portal**: Provide a simple internal image optimization tool behind your Sealos domain.

## Dependencies for MAZANOKE Hosting

The Sealos template includes all required runtime dependencies for MAZANOKE: the official container image, an internal Kubernetes Service, public HTTPS ingress, and the Sealos App launcher entry.

### Deployment Dependencies

- [Official Website](https://mazanoke.com/) - Public MAZANOKE instance
- [GitHub Repository](https://github.com/civilblur/mazanoke) - Source code and releases
- [Docker Configuration](https://github.com/civilblur/mazanoke/blob/main/docs/configuration.md) - Optional basic authentication environment variables
- [Web App Installation Guide](https://github.com/civilblur/mazanoke/blob/main/docs/install-web-app.md) - PWA installation instructions

### Implementation Details

**Architecture Components:**

This template deploys one service:

- **MAZANOKE Web**: Nginx-based web container serving the MAZANOKE static application on port 80.

**Configuration:**

MAZANOKE runs without registration, login, databases, or object storage. Image files are processed in the browser, so the deployment does not store uploaded images on the server.

The upstream container supports optional basic authentication through `USERNAME` and `PASSWORD` environment variables. The template keeps the default account-free flow for one-click use; add those variables to the Deployment later when you want an access prompt.

**License Information:**

MAZANOKE is licensed under the GNU General Public License v3.0.

## Why Deploy MAZANOKE on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, operations, and management. By deploying MAZANOKE on Sealos, you get:

- **One-Click Deployment**: Deploy MAZANOKE from the App Store without writing Kubernetes YAML.
- **Automatic HTTPS**: Each deployment gets a public URL with SSL certificates managed by the platform.
- **Simple Operations**: Use the Canvas, AI dialog, and resource cards to adjust resources or environment variables after deployment.
- **Persistent Platform Management**: Kubernetes-native health checks, service discovery, and workload management are handled by Sealos.
- **Pay-As-You-Go Efficiency**: Run a lightweight image utility with a small resource profile and adjust capacity when needed.

Deploy MAZANOKE on Sealos and give users a private, browser-based image optimizer without managing infrastructure.

## Deployment Guide

1. Open the [MAZANOKE template](https://sealos.io/products/app-store/mazanoke) and click **Deploy Now**.
2. Keep the default parameters or adjust the app name and public host if needed.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access MAZANOKE through the provided public URL and start optimizing images. No registration or login is required.

## Configuration

After deployment, you can configure MAZANOKE through:

- **AI Dialog**: Describe changes such as adding environment variables or adjusting resource limits.
- **Resource Cards**: Click the Deployment card to edit CPU, memory, replicas, or environment variables.
- **Basic Authentication**: Add `USERNAME` and `PASSWORD` environment variables to enable the upstream container's built-in HTTP basic authentication.

## Scaling

To scale MAZANOKE:

1. Open the Canvas for your deployment.
2. Click the Deployment resource card.
3. Adjust CPU, memory, or replica count.
4. Apply the changes in the dialog.

MAZANOKE does image processing in the browser, so server-side resource needs are usually small.

## Troubleshooting

### The page loads, but image processing feels slow

- Cause: Compression and conversion run on the user's browser device.
- Solution: Test with a smaller source image, use a modern browser, or reduce the number of images processed at once.

### Basic authentication does not appear

- Cause: The upstream container enables basic authentication only when both `USERNAME` and `PASSWORD` are set.
- Solution: Add both environment variables to the Deployment and restart the workload.

### Getting Help

- [GitHub Issues](https://github.com/civilblur/mazanoke/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Official Website](https://mazanoke.com/)
- [GitHub Repository](https://github.com/civilblur/mazanoke)
- [Attributions](https://github.com/civilblur/mazanoke/blob/main/docs/ATTRIBUTIONS.md)

## License

This Sealos template is provided under the Apache License 2.0. MAZANOKE itself is licensed under the GNU General Public License v3.0.
