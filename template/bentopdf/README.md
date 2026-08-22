# Deploy and Host BentoPDF on Sealos

BentoPDF is a privacy-first, client-side PDF toolkit for editing, merging, converting, and processing PDF files in the browser. This template deploys the official self-hosted BentoPDF simple image on Sealos Cloud.

![BentoPDF Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bentopdf/website-screenshot.webp)

## About Hosting BentoPDF

BentoPDF serves a browser-based PDF toolkit where processing happens locally in the user's browser. The template deploys the official self-hosted simple build with NGINX and exposes it through a Sealos HTTPS endpoint.

The application does not require a database, object storage, or server-side account system for the default self-hosted build. Users open the URL and start working with PDFs directly.

## Common Use Cases

- **Merge and split PDFs**: Combine documents or extract page ranges.
- **Edit PDFs**: Annotate, crop, rotate, redact, and adjust PDF content.
- **Convert documents**: Convert images, office documents, text, markdown, and PDFs.
- **Private PDF processing**: Keep files in the browser for privacy-first workflows.

## Dependencies for BentoPDF Hosting

The Sealos template includes the official BentoPDF simple container image.

### Deployment Dependencies

- [BentoPDF Documentation](https://bentopdf.com/docs/) - Official documentation
- [BentoPDF GitHub Repository](https://github.com/alam00000/bentopdf) - Source code and releases
- [Self-Hosting Guide](https://bentopdf.com/docs/) - Deployment and configuration guidance

### Implementation Details

**Architecture Components:**

- **BentoPDF web app**: Official `ghcr.io/alam00000/bentopdf-simple:v2.8.6` image
- **NGINX runtime**: Serves the static client-side application on port 8080
- **Ingress**: Publishes the app with automatic HTTPS

**Configuration:**

The template sets `DISABLE_IPV6=true` for IPv4-only Kubernetes networking and keeps the default `PORT=8080` runtime.

**License Information:**

BentoPDF is dual-licensed. The self-hosted simple build is intended for AGPL-compatible open-source usage; review the upstream licensing page for commercial use.

## Why Deploy BentoPDF on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, storage, networking, and lifecycle management. By deploying BentoPDF on Sealos, you get:

- **One-Click Deployment**: Launch the PDF toolkit from the App Store template.
- **Instant Public Access**: Sealos creates a generated HTTPS endpoint.
- **Private by Design**: PDF work happens in the user's browser.
- **Simple Operations**: Run a single lightweight web container.
- **Easy Resource Control**: Adjust CPU and memory from the Sealos dashboard.

## Deployment Guide

1. Open the [BentoPDF template](https://sealos.io/products/app-store/bentopdf) and click **Deploy Now**.
2. Review the generated host and application name, then deploy.
3. Wait for deployment to complete, then open the generated application URL.
4. Access your application via the provided URL:
   - **BentoPDF UI**: Open the URL and use the PDF tools directly. No login or registration is required for the default self-hosted build.

## Configuration

After deployment, configure BentoPDF by updating environment variables or the container image from the Deployment resource card if you need custom branding or a commercial build.

## Scaling

BentoPDF is a static client-side web app, so a single replica is enough for small teams. Increase replicas from the Deployment resource card if you expect higher traffic.

## Troubleshooting

### Page Loads but a Tool Cannot Download External WASM Assets

- Cause: Some optional processing modules are loaded from upstream CDNs by default.
- Solution: Review the upstream WASM configuration docs for air-gapped or self-hosted module hosting.

### Browser Shows Connection Errors

- Cause: The deployment is still starting or the public URL was copied before Ingress was ready.
- Solution: Wait for the Deployment to become ready and reopen the Sealos App URL.

## Additional Resources

- [BentoPDF Documentation](https://bentopdf.com/docs/)
- [Licensing](https://bentopdf.com/licensing.html)
- [Docker Package](https://github.com/alam00000/bentopdf/pkgs/container/bentopdf-simple)

## License

This Sealos template is provided under the repository license. BentoPDF itself is dual-licensed; review upstream licensing before commercial use.
