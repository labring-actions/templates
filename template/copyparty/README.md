# Deploy and Host copyparty on Sealos

copyparty is a portable file server with resumable uploads, media indexing, WebDAV access, and a browser-based file manager.

![copyparty file browser](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/copyparty/website-screenshot.webp)

## About Hosting copyparty

This template runs the official copyparty image as a single StatefulSet with a 1 GiB persistent volume mounted at `/w`. The administrator account is `admin`, and its password is supplied during deployment.

The public URL opens the file browser. Use **Upload** to add files, drag files between folders, and browse indexed media with thumbnails and previews. WebDAV clients can connect to the same share for desktop file access.

## Common Use Cases

- Share large files through a private browser-based file server.
- Collect uploads from collaborators with resumable transfers.
- Browse photo, audio, and video libraries with generated thumbnails.
- Mount the share in a desktop file manager through WebDAV.
- Keep a lightweight file drop for lab machines and internal teams.

## Dependencies for copyparty Hosting

- A Sealos workspace with CPU, memory, and storage quota.
- A 1 GiB persistent volume for uploaded files and history.
- An administrator password supplied through the template input.
- A WebDAV client for desktop mounting.

## Why Deploy copyparty on Sealos?

- One-click deployment with a public HTTPS file browser.
- Kubernetes health probes, scheduling, and automatic pod recovery.
- Persistent storage for files, media indexes, and upload history.
- Pay-as-you-go resource cards that suit personal file servers.
- Canvas view for inspecting the StatefulSet, Service, Ingress, and PVC.
- AI dialog for deployment questions in the Sealos desktop.

## Deployment Guide

1. Open the [copyparty template](https://sealos.io/products/app-store/copyparty) and click **Deploy Now**.
2. Enter the administrator password, keep the generated application name, and confirm the 1 GiB storage plan.
3. Wait 2-3 minutes for the StatefulSet to become ready, then open the public URL from the App card.
4. Sign in as `admin` with the password from step 2 and upload a small test file.
5. Connect a WebDAV client to the same HTTPS endpoint, then use Canvas to review the StatefulSet, Service, Ingress, and PVC.

## License

copyparty is released under the [MIT License](https://github.com/9001/copyparty/blob/hovudstraum/LICENSE).
