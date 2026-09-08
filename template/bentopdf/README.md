# Deploy and Host BentoPDF on Sealos

BentoPDF is a browser-based PDF toolkit for merging, converting, editing, and organizing documents. This template deploys its official self-hosted build on Sealos Cloud with a public HTTPS address.

![BentoPDF website](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bentopdf/website-screenshot.webp)

## About Hosting BentoPDF

BentoPDF processes documents locally in your browser. The server delivers the application and its static assets, while your device performs PDF operations and saves the results. You can open the deployed address and start using the tools immediately; access is anonymous.

This template runs one Nginx container from `ghcr.io/alam00000/bentopdf-simple:2.8.8`, exposed through a Kubernetes Service and Sealos HTTPS Ingress. The self-hosted build opens the tool catalog directly. The screenshot above shows the official product website.

## Common Use Cases

- **Combine documents**: Merge reports, receipts, and application materials into one PDF.
- **Organize pages**: Rotate pages, split documents, and reorder or extract selected pages.
- **Convert and edit files**: Convert supported formats, annotate PDFs, and prepare documents for sharing.

## Dependencies for BentoPDF Hosting

The official image includes the web server and application assets. PDF processing uses the browser's memory and CPU. Some tools load WebAssembly modules from the upstream-configured CDN, so those tools require browser access to their external dependencies.

### Deployment Dependencies

- [BentoPDF documentation](https://bentopdf.com/docs/)
- [Docker deployment guide](https://bentopdf.com/docs/self-hosting/docker)
- [Kubernetes deployment guide](https://bentopdf.com/docs/self-hosting/kubernetes)
- [GitHub issues](https://github.com/alam00000/bentopdf/issues)

### Implementation Details

- **Resources**: The tested minimum server limits are `100m` CPU and `128Mi` memory, with requests of `10m` CPU and `12Mi` memory.
- **Runtime**: One stateless Nginx Deployment, one Service on port `8080`, an HTTPS Ingress, and a Sealos App entry.
- **Security**: Nginx runs as user/group `101`, with restricted Linux capabilities and service-account token mounting disabled.
- **Browser compatibility**: The image's cross-origin isolation headers pass through the Ingress so supported browsers can use `SharedArrayBuffer` for Office conversion.
- **Storage**: Documents stay on the user's device. The upstream S3 + CloudFront guide describes a separate static-website hosting architecture; this template serves the official image's bundled assets through Nginx. Its runtime has no database or application object-storage configuration.

## Why Deploy BentoPDF on Sealos?

Sealos provides one-click deployment on Kubernetes, a public HTTPS address, and resource monitoring. Pay-as-you-go resources suit a lightweight static server, while document processing uses each user's browser.

After deployment, use the Canvas AI dialog to describe configuration changes or open the Deployment, Service, and Ingress resource cards to adjust their settings.

## Deployment Guide

1. Open the [BentoPDF template](https://sealos.io/products/app-store/bentopdf) and click **Deploy Now**.
2. Review the generated application name and resource settings, then start deployment.
3. Wait for deployment to complete, typically **2-3 minutes**. Sealos then opens the Canvas for your deployment.
4. Open the BentoPDF App address. The tool catalog is immediately available with anonymous access; select a tool to begin.
5. For a first check, open **Rotate PDF**, select a local PDF, click **Right**, and click **Apply Rotations**. The resulting PDF downloads to your device.
6. Open **Merge PDF**, select two PDFs, wait until each file shows its page count and the loading dialog closes, then click **Merge PDFs** to download the combined document.

## Troubleshooting

- **Office conversion stalls**: Open the public HTTPS address in a current browser. Preserve the image's cross-origin headers when adding a custom proxy; these enable `SharedArrayBuffer`.
- **A tool waits for its processing engine**: Check the browser's connectivity to the configured WebAssembly CDN. Follow the upstream air-gapped deployment guide when operating an isolated network.
- **Large documents exhaust memory**: Process smaller batches or use a device with more available memory. PDF processing runs in the browser.

## License

BentoPDF is available under the [AGPL-3.0 license](https://github.com/alam00000/bentopdf/blob/v2.8.8/LICENSE). The upstream project also offers a commercial license; see its [licensing page](https://bentopdf.com/licensing).
