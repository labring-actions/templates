# Deploy and Host Stirling-PDF on Sealos

Stirling-PDF is a self-hosted PDF toolbox for merging, splitting, conversion, OCR, compression, redaction, and other document workflows. This template deploys Stirling-PDF with persistent storage, optional PostgreSQL, and HTTPS access on Sealos Cloud.

![Stirling-PDF Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/s-pdf/website-screenshot.webp)

## About Hosting Stirling-PDF

Stirling-PDF runs as a web application on port `8080`. The Sealos template creates a StatefulSet, persistent volumes for OCR data and working directories, a Service, an Ingress, and a Sealos App entry.

The default deployment opens the PDF toolbox directly. To require login, set `DOCKER_ENABLE_SECURITY=true` and `SECURITY_ENABLELOGIN=true`. On a fresh data volume, sign in with `SECURITY_INITIALLOGIN_USERNAME` and `SECURITY_INITIALLOGIN_PASSWORD`.

## Common Use Cases

- **PDF Operations Portal**: Merge, split, rotate, compress, watermark, and redact PDF files from a browser.
- **Document Conversion**: Convert PDF, Office, image, and book formats when the advanced tooling option is enabled.
- **OCR Workflows**: Use bundled language packs for scanned documents and multilingual text extraction.
- **Internal Team Utility**: Run a private document toolbox with password login and persistent configuration.

## Deployment Guide

1. Open the [Stirling-PDF template](https://sealos.io/products/app-store/s-pdf) and click **Deploy Now**.
2. Keep `use_postgresql=false` for lightweight personal usage, or set `use_postgresql=true` for a separate PostgreSQL database and stronger persistence.
3. To enable login, set:
   - `DISABLE_ADDITIONAL_FEATURES=false`
   - `DOCKER_ENABLE_SECURITY=true`
   - `SECURITY_ENABLELOGIN=true`
   - `SECURITY_INITIALLOGIN_USERNAME`: initial admin username
   - `SECURITY_INITIALLOGIN_PASSWORD`: initial admin password
4. Choose `SYSTEM_DEFAULTLOCALE`, `LANGS`, and advanced conversion options for your document workload.
5. Wait for the StatefulSet and optional PostgreSQL cluster to become ready, then open the generated HTTPS URL from Sealos Canvas.

## Configuration

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `use_postgresql` | Create and use a PostgreSQL database for production workloads. | `false` | `false` |
| `DOCKER_ENABLE_SECURITY` | Enable Stirling-PDF security components required for login. | `false` | `false` |
| `DISABLE_ADDITIONAL_FEATURES` | Keep authentication and additional features available. | `false` | `false` |
| `SECURITY_ENABLELOGIN` | Enable the login screen. | `false` | `false` |
| `SECURITY_INITIALLOGIN_USERNAME` | Initial admin username for a fresh data volume when login is enabled. | `false` | `admin` |
| `SECURITY_INITIALLOGIN_PASSWORD` | Initial admin password for a fresh data volume when login is enabled. | `false` | `<redacted>` |
| `LANGS` | Font and OCR language packs to install for document conversion. | `false` | `en-GB,en-US,zh-CN,zh-TW` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | Install Calibre for book conversion and advanced HTML conversion. | `false` | `true` |
| `SYSTEM_DEFAULTLOCALE` | Default UI language. | `false` | `en-US` |
| `UI_APPNAME` | Visible application name. | `false` | `Stirling-PDF` |
| `UI_HOMEDESCRIPTION` | Homepage tagline. | `false` | `Demo site for Stirling-PDF` |
| `UI_APPNAMENAVBAR` | Name shown in the navigation bar. | `false` | `Stirling-PDF` |
| `METRICS_ENABLED` | Enable `/api/*` information endpoints. | `false` | `true` |
| `SYSTEM_GOOGLEVISIBILITY` | Publish robots.txt rules that allow search engine visibility. | `false` | `true` |

Store private passwords in Sealos-managed inputs.

## PostgreSQL Option

When `use_postgresql=true`, the template creates a Kubeblocks-managed PostgreSQL `postgresql-16.4.0` cluster and an idempotent init Job for the `stirling_pdf` database. Stirling-PDF then receives the database host, port, username, and password from Sealos-managed secrets.

## Scaling

The template reserves enough memory for the common PDF and OCR paths. Increase memory and CPU from Sealos Canvas before large OCR batches, book conversions, or concurrent team usage.

## Troubleshooting

### Login screen appears

Use the configured `SECURITY_INITIALLOGIN_USERNAME` and `SECURITY_INITIALLOGIN_PASSWORD`. The upstream defaults are `admin` and `stirling` on a fresh data volume.

### OCR or conversion is slow

Increase CPU and memory on the StatefulSet, then retry the operation. Large PDFs and language-heavy OCR tasks need more memory than basic merge or split tasks.

### PostgreSQL startup takes time

Wait for the PostgreSQL cluster and init Job to complete before opening the application. The app readiness probe turns healthy after Stirling-PDF can answer the status API.

## Additional Resources

- [Stirling-PDF Website](https://www.stirlingpdf.com/)
- [Stirling-PDF Source Code](https://github.com/Stirling-Tools/Stirling-PDF)
- [Stirling-PDF Security Documentation](https://docs.stirlingpdf.com/Configuration/System%20and%20Security/)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. Stirling-PDF is licensed by its upstream project.
