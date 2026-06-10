# Deploy and Host Crawl4AI on Sealos

Crawl4AI is an open-source LLM-friendly web crawler and scraper. This template deploys the official Crawl4AI API server with its dashboard and playground on Sealos Cloud.

![Crawl4AI Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/crawl4ai/website-screenshot.webp)

## About Hosting Crawl4AI

Crawl4AI runs as a single API/Web service on port `11235`. The deployment exposes the dashboard, playground, crawl API, task API, and browser-backed scraping features through a public HTTPS URL.

The template provisions persistent storage for browser shared memory and runtime cache paths. Sealos handles TLS, ingress routing, restart management, and resource controls.

## Common Use Cases

- **LLM-ready extraction**: Crawl pages and produce markdown or structured content for AI workflows.
- **Scraping API**: Submit crawl jobs through `/crawl` and retrieve results through `/task/{id}`.
- **Interactive testing**: Use `/playground` to test requests and generate example code.
- **Self-hosted crawling backend**: Run Crawl4AI as a shared service for internal automation.

## Dependencies for Crawl4AI Hosting

The Sealos template includes the Crawl4AI Docker server image, persistent cache storage, public HTTPS ingress, and the App shortcut.

### Deployment Dependencies

- [Crawl4AI Documentation](https://docs.crawl4ai.com/) - Official documentation
- [Self-Hosting Guide](https://docs.crawl4ai.com/core/self-hosting/) - Docker server reference
- [Crawl4AI GitHub Repository](https://github.com/unclecode/crawl4ai) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Crawl4AI StatefulSet**: Runs `unclecode/crawl4ai:0.8.9` on port `11235`.
- **Persistent `/dev/shm` volume**: Provides browser shared-memory space through a persistent volume because Sealos templates use persistent volumes for runtime storage.
- **Persistent cache volume**: Stores `/app/.cache`.
- **Ingress and App**: Publish `/playground`, `/dashboard`, and API endpoints through HTTPS.

**Configuration:**

- The App shortcut opens `/playground`.
- API base URL is the root deployment URL.
- Health checks use `/health`.

**License Information:**

Crawl4AI is licensed under Apache-2.0. This Sealos template is provided under the repository license.

## Why Deploy Crawl4AI on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Crawl4AI on Sealos, you get:

- **One-Click Deployment**: Deploy the Crawl4AI API server quickly.
- **Public HTTPS API**: Use the crawl API from browsers, scripts, and AI tools.
- **Persistent Runtime Paths**: Keep runtime cache paths across restarts.
- **Easy Resource Tuning**: Increase CPU and memory from the Canvas for heavier crawl jobs.
- **Integrated Management**: Restart, inspect logs, and adjust settings from Sealos.

## Deployment Guide

1. Open the [Crawl4AI template](https://sealos.io/products/app-store/crawl4ai) and click **Deploy Now**.
2. Review the default resources and deploy.
3. Wait for deployment to complete. After deployment, you will be redirected to the Canvas.
4. Access the application via:
   - **Playground**: `https://<your-app-url>/playground`
   - **Dashboard**: `https://<your-app-url>/dashboard`
   - **API**: `https://<your-app-url>/crawl`

## Configuration

After deployment, configure Crawl4AI through:

- **Playground**: Test crawl requests interactively.
- **API clients**: Send requests to `/crawl` and poll `/task/{id}`.
- **Resource Cards**: Increase CPU, memory, or storage for larger crawls.

## Troubleshooting

### Browser-backed crawls fail under load

- Cause: The deployment needs more CPU, memory, or browser shared-memory space for the requested workload.
- Solution: Increase StatefulSet CPU and memory from the Canvas, then retry with a smaller crawl batch.

### API request times out

- Cause: The target site is slow or the crawl job is large.
- Solution: Use async task polling through `/task/{id}` and increase proxy read timeout only for long-running internal workloads.

## Additional Resources

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [Docker Examples](https://github.com/unclecode/crawl4ai/blob/main/docs/examples/docker_example.py)
- [Self-Hosting Guide](https://docs.crawl4ai.com/core/self-hosting/)

## License

This Sealos template is provided under the repository license. Crawl4AI itself is licensed under Apache-2.0.
