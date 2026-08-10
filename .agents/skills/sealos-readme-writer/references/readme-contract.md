# Sealos README Contract

## Index inputs

Read `template/<app>/index.yaml` first and derive these values from it:

- `metadata.name` for the App Store slug and template folder name
- `spec.title` for the application name in the H1
- `spec.readme` and `spec.i18n.zh.readme` for README targets
- `spec.screenshots` for screenshot availability
- `spec.defaults.app_name` and `spec.defaults.app_host` for generated names
- `kind: App` for the generated public URL

## English README

Use this section order:

1. `# Deploy and Host <title> on Sealos`
2. `## About Hosting <title>`
3. `## Common Use Cases`
4. `## Dependencies for <title> Hosting`
5. `## Why Deploy <title> on Sealos?`
6. `## Deployment Guide`
7. Optional post-deploy sections
8. `## License`

Deployment Guide step 1 must open the App Store template page and click `Deploy Now`.
The step should use `https://sealos.io/products/app-store/<slug>`.
Step 3 should mention the typical 2-3 minute deployment time and place Canvas after deployment.

## Chinese README

Use this section order:

1. `# 在 Sealos 上部署和托管 <title>`
2. `## 关于...` or `## ...托管...`
3. `## 常见使用场景`
4. `## ...依赖...`
5. `## 为什么在 Sealos 上部署...`
6. `## 部署指南`
7. Optional post-deploy sections
8. `## 许可证`

Use the same App Store slug and `https://sealos.io/products/app-store/<slug>` in the Chinese README.
Preserve Markdown structure, code blocks, and URLs.

## Multi-service signal

Treat the template as multi-service when the template resources include clusters, workers, object storage, or init jobs.
Add `Architecture Components` and describe how the services interact.

## Validation checklist

- README files exist
- H1 matches the template title
- Required heading order is present
- Deployment Guide step 1 starts from the template page
- App Store slug matches `metadata.name`
- Chinese README uses `https://sealos.io`
- Multi-service templates include `Architecture Components`
- Screenshot references align with `website-screenshot.webp`
