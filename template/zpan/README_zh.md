# ZPan

ZPan 是一个面向 S3 兼容存储的开源文件托管平台，支持网盘、文件分享、图床、WebDAV、浏览器直传对象存储和远程下载工作流。

本模板同时部署 ZPan Web 服务和 downloader 节点。首次启动后，请查看 downloader 容器日志中的设备授权链接，使用管理员账号打开并完成授权，downloader 才会注册并处理远程下载任务。

部署后：

1. 打开 ZPan 并创建第一个用户，第一个用户会成为管理员。
2. 进入 **管理后台 -> 存储** 添加 S3 兼容存储桶。
3. 确保存储端点可以被浏览器访问，因为上传通过预签名 URL 从客户端直接传到对象存储。

兼容存储包括 Cloudflare R2、AWS S3、Backblaze B2、MinIO、RustFS、Tigris 以及其他 S3 兼容服务。
