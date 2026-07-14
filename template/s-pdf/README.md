# Deploy and Host Stirling-PDF on Sealos

Stirling-PDF is a self-hosted PDF toolbox for merging, splitting, conversion, OCR, compression, redaction, and other document workflows. This template deploys Stirling-PDF `2.14.2-fat` with authenticated access, persistent storage, and optional licensed PostgreSQL and Sealos S3 paths on Sealos Cloud.

![Stirling-PDF Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/s-pdf/website-screenshot.webp)

## About Hosting Stirling-PDF

Stirling-PDF serves its web interface and API on port `8080`. The template creates one StatefulSet replica, four persistent volumes, a Service, an HTTPS Ingress, and a Sealos App entry. The volumes preserve OCR language data at `/usr/share/tessdata`, application configuration and the default H2 database at `/configs`, logs at `/logs`, and secured user files at `/storage`.

Authentication is enabled for every deployment. The initial administrator credentials come from the required `SECURITY_INITIALLOGIN_USERNAME` and `SECURITY_INITIALLOGIN_PASSWORD` inputs and apply to a fresh `/configs` volume.

## Common Use Cases

- **PDF Operations Portal**: Merge, split, rotate, compress, watermark, redact, and organize PDFs from a browser.
- **Document Conversion**: Convert PDF, Office, image, HTML, and book formats with the fat image toolset.
- **OCR Workflows**: Process scanned documents with persistent OCR language data.
- **Private Team Utility**: Protect document tools and stored files with administrator login.

## Dependencies for Stirling-PDF Hosting

The community topology uses Stirling-PDF's embedded H2 database and local persistent file storage. Optional paths add a KubeBlocks PostgreSQL 16 cluster or a private Sealos S3-compatible bucket.

### Implementation Details

**Architecture Components:**

- **Stirling-PDF**: `stirlingtools/stirling-pdf:2.14.2-fat`, pinned to the official release whose multi-architecture digest is `sha256:aa91c68b85992986302fbdb6735f2c0824e329304e43c814a9b77c9dd0dbe410`.
- **Persistent storage**: Four `1Gi` claims for OCR data, configuration/H2, logs, and secured user files.
- **PostgreSQL**: An independent KubeBlocks `postgresql-16.4.0` cluster plus an idempotent `stirling_pdf` database initialization Job when `use_postgresql=true`.
- **Object storage**: A private `ObjectStorageBucket` with bucket-scoped Sealos credentials when `enable_s3_storage=true`.

**License Boundary:**

The default H2 and local-storage topology runs with the community license. Stirling-PDF gates custom PostgreSQL and S3-backed storage behind a valid Pro or Enterprise license. Set `PREMIUM_KEY` when either licensed branch is enabled. The template provisions infrastructure and passes the official runtime settings; Stirling-PDF validates license entitlement during startup.

## Why Deploy Stirling-PDF on Sealos?

- **One-click topology**: Deploy the application, HTTPS route, persistent claims, and selected managed services together.
- **Managed credentials**: PostgreSQL and S3 connection values come from Sealos-managed secrets.
- **Resource control**: Tune CPU and memory from Canvas while preserving a single application replica.

## Deployment Guide

1. Open the [Stirling-PDF template](https://sealos.io/products/app-store/s-pdf) and click **Deploy Now**.
2. Enter the initial administrator username and password.
3. Keep `use_postgresql=false` and `enable_s3_storage=false` for the community H2/local-storage topology.
4. Enable PostgreSQL, Sealos S3, or both for a licensed topology, then enter a valid `PREMIUM_KEY`.
5. Select the locale and advanced book/HTML conversion setting.
6. Wait 2-3 minutes for the StatefulSet and selected managed services to become ready, then open the generated HTTPS URL from Canvas.

## Configuration

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `SECURITY_INITIALLOGIN_USERNAME` | Initial administrator username for a fresh configuration volume. | `true` | User input |
| `SECURITY_INITIALLOGIN_PASSWORD` | Initial administrator password for a fresh configuration volume. | `true` | User input |
| `use_postgresql` | Provision and use independent PostgreSQL. Requires Pro or Enterprise. | `false` | `false` |
| `enable_s3_storage` | Store secured user files in Sealos S3. Requires Pro or Enterprise. | `false` | `false` |
| `PREMIUM_KEY` | Stirling-PDF license key for either licensed branch. | Conditional | Empty |
| `SYSTEM_DEFAULTLOCALE` | Default interface locale. | `false` | `en-US` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | Enable Calibre-backed book and advanced HTML conversion. | `false` | `false` |

## Topology Options

| PostgreSQL | Sealos S3 | Runtime topology | License |
|------------|-----------|------------------|---------|
| `false` | `false` | Embedded H2 + persistent `/storage` | Community |
| `true` | `false` | KubeBlocks PostgreSQL + persistent `/storage` | Pro or Enterprise |
| `false` | `true` | Embedded H2 + Sealos S3 | Pro or Enterprise |
| `true` | `true` | KubeBlocks PostgreSQL + Sealos S3 | Pro or Enterprise |

## Troubleshooting

### Initial credentials are rejected

The initial credential inputs apply once to a fresh `/configs` volume. Use the administrator account already stored in that volume after subsequent restarts.

### A licensed branch stops during startup

Confirm that `PREMIUM_KEY` carries an active Stirling-PDF Pro or Enterprise entitlement. PostgreSQL and S3 configuration becomes active after license validation succeeds.

### Large conversions need more capacity

Increase the StatefulSet CPU and memory through Sealos Canvas before large OCR batches, book conversions, or concurrent team usage.

## Additional Resources

- [Stirling-PDF Documentation](https://docs.stirlingpdf.com/)
- [Stirling-PDF Source Code](https://github.com/Stirling-Tools/Stirling-PDF)
- [Stirling-PDF Releases](https://github.com/Stirling-Tools/Stirling-PDF/releases)
- [Sealos Documentation](https://sealos.io/docs)

## License

Stirling-PDF's community code is available under the MIT License, with proprietary directories governed by their upstream licenses. Custom PostgreSQL and S3 storage require a paid Stirling-PDF Pro or Enterprise entitlement. This Sealos template follows the template repository license.
