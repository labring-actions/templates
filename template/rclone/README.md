# Deploy and Host Rclone on Sealos

Rclone is a storage management tool for syncing, copying, mounting, and serving files across cloud storage providers. This template deploys Rclone in `rcd` mode with the Web GUI and RC API exposed through HTTPS on Sealos Cloud.

![Rclone Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rclone/website-screenshot.webp)

## About Hosting Rclone

Rclone runs as a single StatefulSet using the official `rclone/rclone` image. The template starts `rclone rcd` with `--rc-web-gui`, HTTP Basic Auth credentials from the deployment form, and persistent volumes for `/config` and `/data`.

The Web GUI and RC API share the same public URL. Use the configured username and password to access both the browser UI and API endpoints.

## Common Use Cases

- **Cloud storage administration**: Configure and inspect remotes from a browser.
- **Transfer automation**: Use the RC API to trigger copy, sync, and list operations.
- **Storage migration**: Move files between supported providers.
- **Backup operations**: Store Rclone configuration and cache on persistent Sealos volumes.

## Dependencies for Rclone Hosting

The Sealos template includes the official Rclone container image, persistent configuration storage, persistent cache/data storage, public HTTPS ingress, and Basic Auth inputs.

### Deployment Dependencies

- [Rclone Website](https://rclone.org/) - Official documentation
- [Rclone Remote Control](https://rclone.org/rc/) - RC API documentation
- [Rclone Web GUI](https://rclone.org/gui/) - Web GUI documentation

## Implementation Details

**Architecture Components:**

- **Rclone rcd**: Remote control daemon with Web GUI enabled.
- **Persistent Config**: `/config/rclone/rclone.conf` stores remotes and credentials.
- **Persistent Data**: `/data` stores cache and working files.

**Configuration:**

- `rc_user` and `rc_password` protect the Web GUI and RC API.
- The daemon listens on port `5572` inside the cluster and is exposed through HTTPS ingress.
- Remotes are configured after login through the Web GUI or RC API.

**License Information:**

Rclone is licensed under the MIT License.

## Why Deploy Rclone on Sealos?

Sealos provides automatic HTTPS, persistent storage, and one-click deployment for a browser-accessible Rclone control plane. It is useful for cloud storage operations that need a stable URL and persistent configuration.

## Deployment Guide

1. Open the [Rclone template](https://sealos.io/products/app-store/rclone) and click **Deploy Now**.
2. Configure the RC username and password in the popup dialog.
3. Wait for deployment to complete, typically 1-2 minutes. After deployment, you will be redirected to the Canvas.
4. Open the generated application URL and sign in with the configured Basic Auth credentials.

## Configuration

After login, create remotes from the Web GUI. You can also call RC API endpoints with the same credentials, for example `POST /core/version` and `POST /config/listremotes`.

## Additional Resources

- [Rclone Docs](https://rclone.org/docs/)
- [Rclone Commands](https://rclone.org/commands/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

This template follows the upstream Rclone MIT License.
