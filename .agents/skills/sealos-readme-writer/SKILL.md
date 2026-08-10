---
name: sealos-readme-writer
description: Create and validate Sealos template READMEs in template app directories, including English README.md, README_zh.md, App Store links, deployment guides, architecture sections, and index.yaml alignment. Use when writing, updating, auditing, or fixing Sealos template documentation, or when README structure, bilingual parity, deployment entry order, or metadata consistency needs review.
---

# Sealos README Writer

## Workflow

1. Read `template/<app>/index.yaml`, `README.md`, and `README_zh.md`.
2. Identify the template shape and list every service or provisioned resource.
3. Write the English README first.
4. Generate `README_zh.md` after the English version is complete.
5. Run `scripts/validate_readme.py <template-dir>` and fix every reported issue.

## Required Structure

Use this order for every English README:

1. Title and introduction
2. About Hosting
3. Common Use Cases
4. Dependencies for Hosting
5. Why Deploy on Sealos?
6. Deployment Guide
7. Optional post-deploy sections
8. License

Add `Architecture Components` when the template includes more than one service, a database, a cache, object storage, or an init job.

## Content Rules

- Use the template title from `index.yaml` in the H1.
- Describe the deployment in one sentence after the title.
- Keep `About Hosting` to 2-3 short paragraphs.
- List 3-5 realistic use cases.
- Ground dependencies and links in the template metadata and official project docs.
- Include Sealos benefits: one-click deployment, Kubernetes foundation, pay-as-you-go resources, persistent storage, public HTTPS, Canvas, AI dialog, and resource cards.
- Start `Deployment Guide` at the App Store template page, then `Deploy Now`.
- Mention the typical 2-3 minute deployment time.
- Use the App Store slug from `index.yaml`.
- Keep `README_zh.md` aligned with the English README and preserve Markdown structure, code blocks, URLs, and the app store slug.
- Use `https://sealos.io` for Sealos links in both README files in this repository.

## Validation

- Check `README.md` and `README_zh.md` exist.
- Check the English and Chinese H1s match the application title and repo language pattern.
- Check the required section order.
- Check `Deployment Guide` step 1 starts from the template page and includes `Deploy Now`.
- Check `README_zh.md` uses the same app store slug and `https://sealos.io`.
- Check multi-service templates include `Architecture Components`.
- Check `README.md` and `README_zh.md` align with `index.yaml`.

## References

- `references/readme-contract.md` for the exact README checklist and validation rules.
- `references/sealos-template-specs.md` for template YAML structure, defaults, inputs, and resource ordering.
