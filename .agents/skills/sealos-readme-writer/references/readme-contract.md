# Sealos README Contract

## Index inputs

Read `template/<app>/index.yaml` first and derive these values from it:

- `metadata.name` for the App Store slug and template folder name
- `spec.title` for the application name in the H1
- `spec.readme` and `spec.i18n.zh.readme` for README targets
- `spec.screenshots` for screenshot availability
- `spec.inputs` for user-facing fields and defaults
- `spec.defaults.app_name` and `spec.defaults.app_host` for generated names
- `kind: App` for the generated public URL

Read the workload, Service, Ingress, volume, probe, and input resources for the runtime facts that the README must state.

## Quality baseline

Read the two most recently merged README pairs before writing. Current reference pairs: `template/actual` and `template/beszel`.

Match their section set, specificity, and runtime evidence. Every section that applies to the target template appears in both languages with the same headings, links, values, and tables.

## English README

Use this section order:

1. `# Deploy and Host <title> on Sealos`
2. `## About Hosting <title>`
3. `## Common Use Cases`
4. `## Dependencies for <title> Hosting`
5. `## Implementation Details`
6. `## Why Deploy <title> on Sealos?`
7. `## Deployment Guide`
8. Post-deploy sections such as `## Using <title>`, `## Login and Access`, and feature-specific guides
9. `## Scaling`
10. `## Troubleshooting`
11. `## License`

`## Dependencies for <title> Hosting` contains a `### Deployment Dependencies` subsection with the official website, Docker or installation guide, GitHub repository, and support or Helm documentation when available.

`## Implementation Details` contains three labeled blocks:

- `**Architecture Components:**` lists every workload, database, cache, object storage bucket, init job, Service, Ingress, App entry, and volume.
- `**Configuration:**` lists the image and tag, ports, public URL variables, timezone, persistence path and size, health probes, runtime user, input-driven credentials, and first-boot behavior.
- `**Resource Allocation:**` contains a Markdown table with CPU request, CPU limit, memory request, memory limit, and storage for every workload and init container, followed by one sentence of measured validation evidence.

Add a login or access section when the application has authentication. State the entry URL, username source, default credentials or first-user rule, first-login steps, and password recovery path.

`## Scaling` states the supported replica model and its constraint, the resource adjustment path, and the storage growth path.

`## Troubleshooting` contains at least two concrete failure modes with symptom and fix, plus official support links.

Deployment Guide step 1 must open the App Store template page and click `Deploy Now`.
The step should use `https://sealos.io/products/app-store/<slug>`.
Step 3 should mention the typical 2-3 minute deployment time and place Canvas after deployment.

## Chinese README

Use this section order:

1. `# 在 Sealos 上部署和托管 <title>`
2. `## 关于...` or `## ...托管...`
3. `## 常见使用场景`
4. `## ...依赖...`
5. `## 实现细节`
6. `## 为什么在 Sealos 上部署...`
7. `## 部署指南`
8. Usage and login sections
9. `## 扩缩容`
10. `## 故障排查`
11. `## 许可证`

Use the same App Store slug and `https://sealos.io/products/app-store/<slug>` in the Chinese README.
Preserve Markdown structure, tables, code blocks, and URLs.

`## 实现细节` uses `**架构组件：**`, `**配置：**`, and `**资源分配：**` with the same content and resource table as the English README.

## Runtime coverage

- Every workload, init job, and persistent volume appears in `Architecture Components`.
- Every input that changes runtime behavior appears in `Configuration` or the login section.
- Every public port and route appears in `Configuration`.
- The resource table matches the requests, limits, and storage in `index.yaml`.
- Login-gated applications document the verified credential source and first-login flow.

## Validation checklist

- README files exist
- H1 matches the template title
- Required heading order is present, including `Implementation Details` and `Scaling`/`Troubleshooting`
- `Deployment Dependencies` contains at least two official links
- `Architecture Components` lists at least two components
- `Configuration` lists at least three settings
- `Resource Allocation` contains a CPU and memory table
- `Scaling` explains the replica model and resource adjustment path
- `Troubleshooting` contains at least two concrete failure modes
- Deployment Guide step 1 starts from the template page
- App Store slug matches `metadata.name`
- Chinese README uses `https://sealos.io`
- Screenshot references align with `website-screenshot.webp`
