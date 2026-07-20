# Deploy Immich on Sealos

[Immich](https://immich.app/) is a self-hosted photo and video management platform with mobile backup, albums, sharing, maps, face recognition, and semantic search. This template deploys Immich v3.0.3 with PostgreSQL, Redis, persistent media storage, HTTPS, and optional machine learning.

![Immich Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/immich/website-screenshot.webp)

## About Immich

Immich keeps the application and media library under your control. The web interface and official mobile apps use one HTTPS endpoint, while PostgreSQL stores metadata and Redis coordinates background jobs.

This template follows the upstream container topology:

- **Immich Server v3.0.3** serves the web UI and API and runs media-processing workers.
- **Immich Machine Learning v3.0.3** is optional and provides smart search, OCR, object detection, and face recognition.
- **PostgreSQL 16.4** stores users, assets, albums, jobs, and vector indexes.
- **Redis 7.2.7 with Sentinel** coordinates queues and cache data.
- **Persistent volumes** store media at `/data`, the ML model cache, and database data.

Immich Community Edition uses filesystem-backed media storage. Back up the `/data` volume together with PostgreSQL.

## Why Deploy Immich on Sealos?

- Deploy the complete application, database, cache, storage, and HTTPS route from one template.
- Keep uploads, model downloads, and database data across restarts.
- Enable or omit the machine-learning service through one deployment input.
- Adjust compute and storage later from the Sealos resource view.

## Deployment Guide

1. Open the [Immich template](https://sealos.io/products/app-store/immich) and click **Deploy Now**.
2. Choose the `enable_machine_learning` setting:
   - `true` enables smart search, OCR, face recognition, and object detection.
   - `false` deploys the core photo and video library with a smaller resource footprint.
3. Start the deployment and allow several minutes for PostgreSQL, Redis, Immich Server, and the optional ML service to initialize.
4. Open the generated Immich HTTPS URL from the Sealos application link.

## First Registration and Login

A fresh Immich deployment starts with the administrator registration screen.

1. Click **Get Started**.
2. Enter the administrator email, password, password confirmation, and display name.
3. Click **Sign Up**. The first registered account becomes the administrator.
4. Sign in with the same email and password.
5. Complete the onboarding settings, then open **Photos** or **Albums** to begin using the library.

Immich creates no preset credentials. Store the administrator credentials in a password manager. Additional users can be created from **Administration > Users**.

## Mobile App Setup

Install the official Immich mobile app and enter the generated Sealos HTTPS URL as the server endpoint. Sign in with an Immich account, then configure mobile backup folders from the app.

## Resource and Storage Baseline

The template uses the smallest resource tiers that completed a fresh deployment and an upload, thumbnail, download, album, and machine-learning workflow:

| Component | CPU limit | Memory limit | Initial storage |
| --- | ---: | ---: | ---: |
| Immich Server | 500m | 2 GiB | 1 GiB media volume |
| PostgreSQL | 500m | 2 GiB | 1 GiB data volume |
| Redis | 500m | 512 MiB | 1 GiB data volume |
| Redis Sentinel | 500m | 512 MiB | 1 GiB data volume |
| Machine Learning | 500m | 4 GiB | 1 GiB model cache |

The 2 GiB server and PostgreSQL limits cover the first startup, schema migration, and media workflow peaks. The 4 GiB ML limit preserves operating headroom while OCR, face recognition, and visual search models are loaded together. Increase storage before importing a large library, and increase memory for large videos or concurrent ML jobs.

## Configuration

- Use **Administration** in Immich to manage users, jobs, libraries, storage templates, and server settings.
- Use the Sealos resource view to resize the Immich, PostgreSQL, Redis, and ML workloads.
- Keep the media path mounted at `/data` when changing the workload.
- Keep the generated database and Redis credentials connected through their Sealos Secrets.
- The default Ingress accepts uploads up to 32 MiB. Increase `nginx.ingress.kubernetes.io/proxy-body-size` on the deployed Ingress before uploading larger media files.

## Backup and Upgrade

Create coordinated backups of the Immich `/data` volume and PostgreSQL database. The ML cache and Redis data can be regenerated, while media files and PostgreSQL metadata form the durable library state. Review the [Immich backup and restore guide](https://immich.app/docs/administration/backup-and-restore/) before upgrades.

## Troubleshooting

### The page is still starting

Wait for the PostgreSQL, Redis, and Immich pods to become ready. A fresh database initialization and the first model downloads can take several minutes.

### Smart search or face recognition is unavailable

Confirm that `enable_machine_learning` was set to `true` and that the ML pod is ready. The first request downloads models into the persistent cache.

### Uploads fail for large files

Increase `nginx.ingress.kubernetes.io/proxy-body-size` on the deployed Ingress, check free space on the `/data` volume, and increase the Immich Server resources for large videos or concurrent uploads.

## Resources

- [Immich Documentation](https://immich.app/docs/)
- [Post-installation Guide](https://immich.app/docs/install/post-install/)
- [Mobile App Guide](https://immich.app/docs/features/mobile-app/)
- [Immich GitHub Repository](https://github.com/immich-app/immich)

## License

Immich is licensed under the GNU Affero General Public License v3.0. This Sealos template follows the templates repository license.
