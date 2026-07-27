# Deploy and Host PDFMathTranslate on Sealos

PDFMathTranslate translates PDF documents while preserving formulas, tables, and page layout. This template runs the upstream WebUI on Sealos with persistent configuration, model caches, and generated files.

![PDFMathTranslate WebUI showing a completed English-to-Chinese translation](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pdf2zh/website-screenshot.webp)

## About Hosting PDFMathTranslate

The template deploys:

- **PDFMathTranslate `1.9.11`** from an immutable multi-architecture image digest
- **One WebUI replica** in a StatefulSet on port `7860`
- **Runtime-generated credentials** for the Gradio sign-in flow
- **A `1Gi` persistent volume** mounted at `/data`
- **Authenticated HTTPS** through a Sealos-managed Service and Ingress protected by PDFMathTranslate login credentials
- **Startup, readiness, and liveness probes** on the WebUI root
- **A restricted container context** running as UID and GID `1000`

The WebUI requires the username and password supplied during deployment. PDFMathTranslate has no registration flow, so share these credentials only with people who should access uploaded documents and saved translation-provider settings. The upstream runtime is a single service and has no database or object-storage dependency.

## Common Use Cases

- Translate research papers while retaining their visual structure
- Produce monolingual and bilingual PDF outputs
- Review foreign-language technical documents
- Translate selected pages from large documents
- Connect PDF translation to Google, Bing, DeepL, OpenAI-compatible, or self-hosted services

## Dependencies for PDFMathTranslate Hosting

- A Sealos account and workspace
- Outbound internet access for the selected translation service
- Outbound internet access during the first start if PDFMathTranslate needs to fetch layout models or fonts
- Provider credentials when using a service that requires an API key

Google and Bing work from the WebUI without user-supplied API keys. Provider availability and rate limits remain subject to their public endpoints.

## Implementation Details

| Component | Configuration |
| --- | --- |
| Image | `byaidu/pdf2zh:1.9.11` pinned to `sha256:8e083e...` |
| Workload | Single-replica StatefulSet |
| Public port | `7860` |
| Persistent mount | `/data` |
| Runtime home | `/data/home` |
| Upstream config path | `~/.config/PDFMathTranslate/config.json` |
| Deployed config path | `/data/home/.config/PDFMathTranslate/config.json` |
| Output directory | `/data/pdf2zh_files` |
| Access control | Gradio credential login from a runtime-only mode-`0600` file |
| Health checks | HTTP `GET /` |

The template injects the required deployment credentials as container environment values. A small ConfigMap startup script applies `umask 077`, writes `/tmp/pdf2zh-auth.csv`, and executes `pdf2zh -i --authorized /tmp/pdf2zh-auth.csv`. The resulting mode-`0600` authentication file stays outside the persistent volume and disappears with the container. Setting the working directory to `/data` keeps generated PDFs on the persistent volume, while `HOME=/data/home` keeps configuration, fonts, models, and translation caches across restarts.

## Why Deploy PDFMathTranslate on Sealos?

- **One-click deployment**: Sealos creates the workload, storage, HTTPS route, and application link from one template.
- **Persistent working data**: Configuration, downloaded assets, caches, and generated PDFs survive Pod replacement.
- **Built-in observability**: Inspect status, events, resource use, and logs from Sealos.
- **Simple resource tuning**: Increase CPU for faster document processing without rebuilding the image.

## Deployment Guide

1. Open the [PDFMathTranslate template](https://sealos.io/products/app-store/pdf2zh) and click **Deploy Now**.
2. Enter a WebUI username and a strong, unique WebUI password, then start the deployment.
3. Wait for the StatefulSet to become ready. The first deployment usually takes 2-3 minutes while Sealos pulls the image and PDFMathTranslate loads its layout model.
4. Open the HTTPS application address shown by Sealos.

Both WebUI credential fields are required. Keep them in a password manager because PDFMathTranslate does not provide registration or password recovery. Upstream parses the credential file as comma-separated values, so use a username and password without commas or line breaks.

## Sign In

1. Open the HTTPS application address shown by Sealos.
2. Enter the WebUI username and password supplied during deployment.
3. Continue to the translation interface.

Every user shares the same deployment-level credentials. Changing either value requires updating the StatefulSet environment through a new deployment or template update.

## Translate Your First PDF

1. Sign in to the deployed WebUI.
2. Keep **File** selected and upload a PDF, or select **Link** and enter a direct PDF URL.
3. Choose a translation service, source language, target language, and page range.
4. Click **Translate**.
5. Download **Translation (Mono)** for the translated document or **Translation (Dual)** for a bilingual document.

The **Experimental Options** panel controls thread count, translation-cache bypass, font subsetting, custom formula-font matching, and BabelDOC mode.

## Translation Services and API Keys

The service selector reveals the fields required by the chosen provider. Common examples include:

| Service | Typical fields |
| --- | --- |
| Google or Bing | No user-supplied key |
| DeepL | `DEEPL_AUTH_KEY` |
| OpenAI | `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` |
| Gemini | `GEMINI_API_KEY`, `GEMINI_MODEL` |
| DeepSeek | `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL` |
| OpenAI-liked | Compatible base URL, API key, and model |
| Ollama | Reachable `OLLAMA_HOST` and model name |

PDFMathTranslate stores provider settings in `/data/home/.config/PDFMathTranslate/config.json`. The WebUI credentials protect this persistent configuration, uploaded documents, and the ability to spend paid-provider quota. Use a strong, unique password, limit credential sharing to trusted users, and use provider keys with the narrowest practical scope.

## Persistence

| Path | Purpose |
| --- | --- |
| `/data/home/.config/PDFMathTranslate` | Language defaults and translation-service settings |
| `/data/home/.cache` | Layout models, fonts, and translation caches |
| `/data/pdf2zh_files` | Uploaded source PDFs and generated Mono/Dual PDFs |

All three locations share the template's `1Gi` ReadWriteOnce persistent volume. Monitor storage use when processing many or large documents.

## Resource Defaults

| CPU limit | Memory limit | CPU request | Memory request |
| ---: | ---: | ---: | ---: |
| `100m` | `2048Mi` | `10m` | `204Mi` |

Live cold-start and uncached translation tests established these defaults. A `512Mi` container was OOM-killed while loading the ONNX model, and `1024Mi` reached 92.93% of its cgroup limit. The `2048Mi` tier provides operating headroom. The lowest CPU tier completed the official one-page uncached sample in 77.69 seconds.

Increase CPU to `200m` or `500m` for faster translations, concurrent users, larger PDFs, or BabelDOC workloads.

## Scaling

The template uses one replica because configuration, caches, and generated files share a ReadWriteOnce volume. Vertical CPU scaling is the direct path for improving throughput. Multi-replica operation requires a shared storage design and upstream-aware job coordination.

## Troubleshooting

### The application is still starting

Check the Pod logs in Sealos. A first start can download the DocLayout ONNX model and fonts before Gradio begins listening on port `7860`.

### Translation fails with a provider error

Try Google or Bing to verify the PDF pipeline without a user-supplied key. For another provider, reopen its service fields and confirm the endpoint, key, and model.

### The WebUI rejects the credentials

Use the exact username and password entered during deployment. PDFMathTranslate has no registration or password-recovery flow; update the StatefulSet environment through a new deployment or template update when credentials need to change.

### Translation is slow

Increase the CPU limit in Sealos. PDF layout analysis is CPU-bound, and the default `100m` tier favors a small resource footprint.

### A large upload is rejected

The public Ingress accepts request bodies up to `32m`. Reduce the PDF size or raise `nginx.ingress.kubernetes.io/proxy-body-size` in the Ingress for larger documents.

### Generated files consume the volume

Remove old files from `/data/pdf2zh_files` and monitor the `1Gi` persistent volume. Models and fonts under `/data/home/.cache` also use this volume.

## Additional Resources

- [PDFMathTranslate documentation](https://pdf2zh.com/)
- [PDFMathTranslate GitHub repository](https://github.com/PDFMathTranslate/PDFMathTranslate)
- [GUI guide](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/v1.9.11/docs/README_GUI.md)
- [Sealos App Store](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

PDFMathTranslate is distributed under the [GNU Affero General Public License v3.0](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/v1.9.11/LICENSE). This repository provides the Sealos deployment template and does not change the upstream license.
