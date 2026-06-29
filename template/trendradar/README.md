# Deploy and Host TrendRadar on Sealos

TrendRadar tracks trending topics, generates scheduled reports, and serves the latest HTML report through a built-in web server. This template deploys TrendRadar with local persistent storage by default and optional S3-compatible remote storage.

![TrendRadar Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/trendradar/website-screenshot.webp)

## About Hosting TrendRadar

TrendRadar collects topic signals on a cron schedule, stores generated SQLite and HTML report files, and exposes the report over HTTP. The template runs the official Docker image with an application ConfigMap and a persistent `/app/output` volume.

Local storage is the default backend. To use S3-compatible storage, set **Storage Backend** to `remote` and fill the S3 endpoint, bucket, access key, secret key, and region fields.

## Common Use Cases

- **Trend monitoring**: Track topics such as AI, cloud, startups, and product launches.
- **Scheduled reports**: Generate fresh HTML reports on a cron schedule.
- **Newsletter research**: Collect high-signal items for editorial review.
- **Lightweight intelligence dashboard**: Serve generated reports from a stable HTTPS URL.

## Dependencies for TrendRadar Hosting

The Sealos template includes the TrendRadar container, configuration files, local persistent storage, public HTTPS ingress, and optional S3-compatible storage inputs.

### Deployment Dependencies

- [GitHub Repository](https://github.com/sansan0/TrendRadar) - Source code
- [Public Demo](https://sansan0.github.io/TrendRadar) - Generated report example
- [Docker Image](https://hub.docker.com/r/wantcat/trendradar) - Upstream container image

## Implementation Details

**Architecture Components:**

- **TrendRadar**: Scheduler, crawler, report generator, and web server.
- **ConfigMap**: Minimal `config.yaml` and `frequency_words.txt` mounted into `/app/config`.
- **Persistent Storage**: `/app/output` stores generated local reports.
- **Optional S3 Storage**: Remote S3-compatible storage through `STORAGE_BACKEND=remote` and `S3_*` environment variables.

**Configuration:**

- `cron_schedule` controls report collection timing.
- `storage_backend` accepts `local` or `remote`.
- S3 fields are ordinary optional inputs; fill them when `storage_backend` is `remote`.

**License Information:**

TrendRadar is licensed under GPL-3.0.

## Why Deploy TrendRadar on Sealos?

Sealos provides automatic HTTPS, persistent storage, and a simple deployment form for cron and storage settings. The template gives TrendRadar a stable public report URL with minimal operational setup.

## Deployment Guide

1. Open the [TrendRadar template](https://sealos.io/products/app-store/trendradar) and click **Deploy Now**.
2. Configure the parameters in the popup dialog. Use `local` storage for the built-in persistent volume, or choose `remote` and fill the S3 fields.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated application URL to view the latest HTML report.

## Configuration

Edit the ConfigMap from the Sealos Canvas to change topic groups, filters, and report behavior. Use the resource card to adjust CPU, memory, storage, and environment variables.

## Additional Resources

- [TrendRadar README](https://github.com/sansan0/TrendRadar)
- [GitHub Issues](https://github.com/sansan0/TrendRadar/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This template follows the upstream TrendRadar GPL-3.0 License.
