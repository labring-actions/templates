---
name: sealos-readme-writer
description: Create and validate Sealos template READMEs with a quality baseline from recently merged templates, including English README.md, README_zh.md, deployment dependency links, implementation details, architecture components, configuration, resource allocation tables, login and access steps, scaling, troubleshooting, App Store links, and index.yaml alignment. Use when writing, updating, auditing, or fixing Sealos template documentation, or when README structure, information density, bilingual parity, deployment entry order, or metadata consistency needs review.
---

# Sealos README Writer

## Workflow

1. Read `template/<app>/index.yaml`, `README.md`, `README_zh.md`, and the two most recently merged README pairs under `template/` (for example `template/actual` and `template/beszel`). Treat those merged pairs as the quality baseline.
2. List every workload, database, cache, object storage bucket, init job, Service, Ingress, input, persisted path, public route, and credential source, together with the facts proven during live validation.
3. Write the English README with every required section and the measured runtime facts.
4. Generate `README_zh.md` after the English version is complete, keeping heading order, links, values, tables, and code blocks aligned.
5. Run `scripts/validate_readme.py <template-dir>` and fix every reported issue.
6. Compare both files against the baseline and close every specificity gap before delivery.

## Required Structure

Use this order for every English README:

1. Title and introduction
2. About Hosting
3. Common Use Cases
4. Dependencies for Hosting, with a `### Deployment Dependencies` subsection
5. Implementation Details, with `Architecture Components`, `Configuration`, and `Resource Allocation`
6. Why Deploy on Sealos?
7. Deployment Guide
8. Post-deploy usage and login sections
9. Scaling
10. Troubleshooting
11. License

Use the matching Chinese order: `关于...托管`, `常见使用场景`, `...依赖`, `实现细节`, `为什么在 Sealos 上部署...`, `部署指南`, usage and login sections, `扩缩容`, `故障排查`, `许可证`.

## Content Rules

- Use the template title from `index.yaml` in the H1.
- Describe the deployment in one sentence after the title.
- Keep `About Hosting` to 2-3 short paragraphs.
- List 3-5 realistic use cases.
- `### Deployment Dependencies` links the official website, Docker or installation guide, GitHub repository, and support or Helm documentation when available.
- `Architecture Components` lists every workload, database, cache, object storage bucket, init job, Service, Ingress, App entry, and volume, and states how they connect.
- `Configuration` lists the image and tag, ports, public URL variables, timezone, persistence path and size, health probes, runtime user, input-driven credentials, and first-boot behavior.
- `Resource Allocation` uses a Markdown table with CPU request, CPU limit, memory request, memory limit, and storage for every workload and init container, followed by one sentence of measured validation evidence.
- When the application has authentication, add a login or access section with the entry URL, username source, default credentials or first-user rule, first-login steps, and password recovery path.
- `Scaling` states the supported replica model and its constraint (SQLite, ReadWriteOnce volumes, HA topology), the resource adjustment path, and the storage growth path.
- `Troubleshooting` covers at least two concrete failure modes with symptom and fix, plus official support links.
- Describe only facts proven in the template or during live validation. Every service, input, persisted path, and credential source appears in both READMEs.
- Include Sealos benefits: one-click deployment, Kubernetes foundation, pay-as-you-go resources, persistent storage, public HTTPS, Canvas, AI dialog, and resource cards.
- Start `Deployment Guide` at the App Store template page, then `Deploy Now`.
- Mention the typical 2-3 minute deployment time.
- Use the App Store slug from `index.yaml`.
- Keep `README_zh.md` aligned with the English README and preserve Markdown structure, tables, code blocks, URLs, and the app store slug.
- Use `https://sealos.io` for Sealos links in both README files in this repository.

## Validation

- Check `README.md` and `README_zh.md` exist.
- Check the English and Chinese H1s match the application title and repo language pattern.
- Check the required section order, including `Implementation Details`, `Scaling`, and `Troubleshooting`.
- Check `Architecture Components` lists at least two components, `Configuration` lists at least three settings, and the resource table covers CPU and memory.
- Check `Deployment Dependencies` contains at least two official links.
- Check `Scaling` explains the replica model and resource adjustment path.
- Check `Troubleshooting` contains at least two concrete failure modes.
- Check `Deployment Guide` step 1 starts from the template page and includes `Deploy Now`.
- Check `README_zh.md` uses the same app store slug and `https://sealos.io`.
- Check `README.md` and `README_zh.md` align with `index.yaml`.
- Check both files against the two most recently merged README pairs and close every specificity gap.

## References

- `references/readme-contract.md` for the exact README checklist and validation rules.
- `references/sealos-template-specs.md` for template YAML structure, defaults, inputs, and resource ordering.
