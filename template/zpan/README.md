# ZPan

ZPan is open-source file hosting for S3-compatible storage. It covers web drive, file sharing, image hosting, WebDAV, direct browser-to-object-storage transfers, and remote-download workflows.

This template deploys both the ZPan web service and a downloader node. On first start, check the downloader container logs for the device authorization URL, open it as an admin user, and approve the downloader registration.

After deployment:

1. Open ZPan and create the first user. The first user becomes an admin.
2. Go to **Admin -> Storage** and add your S3-compatible bucket.
3. Make sure the storage endpoint is reachable from the browser, because uploads use presigned URLs and go directly from the client to object storage.

Compatible storage includes Cloudflare R2, AWS S3, Backblaze B2, MinIO, RustFS, Tigris, and other S3-compatible services.
