# Deploy and Host Crawl4AI on Sealos

Crawl4AI is an open-source LLM-friendly web crawler and scraper. This template deploys the official Crawl4AI API server with its dashboard and playground on Sealos Cloud.

![Crawl4AI Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/crawl4ai/website-screenshot.webp)

## About Hosting Crawl4AI

Crawl4AI runs as a single API/Web service on port `11235`. The deployment exposes the dashboard, playground, crawl APIs, and browser-backed scraping features through a public HTTPS URL protected by `CRAWL4AI_API_TOKEN`.

The template provisions a 1 GiB persistent Playwright browser cache, 1 GiB of persistent browser shared memory at `/dev/shm`, and persistent screenshot and PDF artifact storage at `/var/lib/crawl4ai/outputs`. An init container installs the image-compatible Chromium revision into the cache, while Sealos handles TLS, ingress routing, restart management, and resource controls.

## Common Use Cases

- **LLM-ready extraction**: Crawl pages and produce markdown or structured content for AI workflows.
- **Scraping API**: Run synchronous crawls through `/crawl`, or submit asynchronous jobs through `/crawl/job` and retrieve results through `/crawl/job/{task_id}`.
- **Interactive testing**: Use `/playground` to test requests and generate example code.
- **Self-hosted crawling backend**: Run Crawl4AI as a shared service for internal automation.

## Dependencies for Crawl4AI Hosting

The Sealos template includes the Crawl4AI Docker server image, persistent output storage, browser shared memory, public HTTPS ingress, and the App shortcut.

### Deployment Dependencies

- [Crawl4AI Documentation](https://docs.crawl4ai.com/) - Official documentation
- [Self-Hosting Guide](https://docs.crawl4ai.com/core/self-hosting/) - Docker server reference
- [Crawl4AI GitHub Repository](https://github.com/unclecode/crawl4ai) - Source code and releases

### Implementation Details

**Architecture Components:**

- **Crawl4AI StatefulSet**: Runs `unclecode/crawl4ai:0.9.1` on port `11235` with token authentication enabled.
- **Persistent Playwright cache**: Installs and retains the exact Chromium revision required by the image.
- **Persistent `/dev/shm` volume**: Provides 1 GiB of browser shared-memory space through a Sealos-compatible persistent volume.
- **Persistent output volume**: Stores generated crawl artifacts at `/var/lib/crawl4ai/outputs` across restarts.
- **Ingress and App**: Publish `/playground/`, `/dashboard/`, and API endpoints through HTTPS.

**Configuration:**

- The App shortcut opens `/playground/`; requests to `/` redirect there.
- API base URL is the root deployment URL.
- Playground, Dashboard, and protected API endpoints use the deployment value of `CRAWL4AI_API_TOKEN`.
- The public Ingress disables access logs so Dashboard WebSocket token query parameters stay out of ingress request logs.
- A generated `SECRET_KEY` keeps issued session credentials valid across Pod restarts.
- Health checks use the public `/health` endpoint.

**License Information:**

Crawl4AI is licensed under Apache-2.0. This Sealos template is provided under the repository license.

## Why Deploy Crawl4AI on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Crawl4AI on Sealos, you get:

- **One-Click Deployment**: Deploy the Crawl4AI API server quickly.
- **Public HTTPS API**: Use the crawl API from browsers, scripts, and AI tools.
- **Protected Public Access**: Require the deployment API token for Playground, Dashboard, and crawl requests.
- **Persistent Crawl Outputs**: Keep generated crawl artifacts across restarts.
- **Easy Resource Tuning**: Increase CPU and memory from the Canvas for heavier crawl jobs.
- **Integrated Management**: Restart, inspect logs, and adjust settings from Sealos.

## Deployment Guide

1. Open the [Crawl4AI template](https://sealos.io/products/app-store/crawl4ai) and click **Deploy Now**.
2. Keep the generated **API token** or replace it with your own strong value, then deploy. Save this value for the Playground, Dashboard, and API clients.
3. Wait 2-3 minutes for deployment to complete. After deployment, you will be redirected to the Canvas, where the AI dialog and resource cards support later changes.
4. Access the application via:
   - **Playground**: Open `https://<your-app-url>/playground/` and enter the deployment API token in the API token field when prompted.
   - **Dashboard**: Open `https://<your-app-url>/dashboard/` and enter the same API token in the API token field when prompted.
   - **API**: Send requests to `https://<your-app-url>/crawl` with `Authorization: Bearer <CRAWL4AI_API_TOKEN>`.
   - **Health**: Check the public endpoint at `https://<your-app-url>/health`.

## Configuration

After deployment, configure Crawl4AI through:

- **Playground and Dashboard**: Enter the exact `CRAWL4AI_API_TOKEN` value selected during deployment in each interface's API token field.
- **API clients**: Send synchronous requests to `/crawl`, or create asynchronous jobs at `/crawl/job` and poll `/crawl/job/{task_id}` with the bearer token.
- **Persistent outputs**: Retrieve generated artifacts from `/var/lib/crawl4ai/outputs` inside the StatefulSet.
- **Resource Cards**: Increase CPU, memory, or storage for larger crawls.

## Troubleshooting

### Browser-backed crawls fail under load

- Cause: The deployment needs more CPU, memory, or browser shared-memory space for the requested workload.
- Solution: Increase StatefulSet CPU and memory from the Canvas, then retry with a smaller crawl batch.

### Playground, Dashboard, or API returns an authorization error

- Cause: The submitted token differs from the deployment value of `CRAWL4AI_API_TOKEN`.
- Solution: Enter the deployment API token in the Playground or Dashboard API token field, or send it as a bearer token from API clients.

### API request times out

- Cause: The target site is slow or the crawl job is large.
- Solution: Submit an asynchronous job through `/crawl/job`, poll `/crawl/job/{task_id}`, and tune the proxy read timeout for long-running internal workloads.

## Additional Resources

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [Docker Examples](https://github.com/unclecode/crawl4ai/blob/main/docs/examples/docker_example.py)
- [Self-Hosting Guide](https://docs.crawl4ai.com/core/self-hosting/)

## License

This Sealos template is provided under the repository license. Crawl4AI itself is licensed under Apache-2.0.
