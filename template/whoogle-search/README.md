# Deploy and Host Whoogle Search on Sealos

Whoogle Search is a self-hosted metasearch frontend for Google Search results with privacy controls, optional Basic Auth, and no tracking-heavy client scripts. This template deploys Whoogle Search as a single web service on Sealos.

![Whoogle Search Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/whoogle-search/website-screenshot.webp)

## About Hosting Whoogle Search

Whoogle Search runs the official container image and exposes the search UI on port `5000`. Sealos provisions the workload, internal Service, HTTPS Ingress, public App entry, and resource limits aligned with the official Docker Compose memory setting.

The template supports optional HTTP Basic authentication through deployment inputs. Leave both fields empty for an open private search page, or set both the username and password to protect the UI.

## Common Use Cases

- **Private Search Frontend**: Search from a self-hosted UI with reduced tracking and ad-heavy page elements.
- **Team Search Utility**: Share a protected search endpoint with a small team.
- **Browser Search Engine**: Add the deployed URL as a custom browser search engine.
- **Google CSE Fallback**: Configure Custom Search Engine credentials inside Whoogle after deployment when scraping is unreliable.

## Dependencies for Whoogle Search Hosting

The Sealos template includes the Whoogle Search container, a Kubernetes Service, HTTPS Ingress, and a Sealos App entry.

### Deployment Dependencies

- [Official Repository](https://github.com/benbusby/whoogle-search) - Source code and deployment notes
- [Environment Variables](https://github.com/benbusby/whoogle-search#environment-variables) - Runtime configuration reference
- [Sealos](https://sealos.io) - Kubernetes-based application hosting

### Implementation Details

**Architecture Components:**

- **Whoogle Search Web Service**: Runs `benbusby/whoogle-search:1.2.4` and serves the UI on port `5000`.
- **Service and Ingress**: Provides internal routing and public HTTPS access.
- **Sealos App Entry**: Opens the generated public URL from the Sealos dashboard.

**Configuration:**

The template sets `WHOOGLE_CONFIG_URL` to the generated HTTPS URL and exposes optional `WHOOGLE_USER` and `WHOOGLE_PASS` inputs. Whoogle stores lightweight runtime configuration in the container-managed config path.

**License Information:**

This Sealos template is provided under the repository license. Whoogle Search is licensed under the MIT License.

## Why Deploy Whoogle Search on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, public access, and operations. By deploying Whoogle Search on Sealos, you get:

- **One-Click Deployment**: Launch the search frontend from the App Store template page.
- **Instant Public Access**: Sealos creates an HTTPS URL automatically.
- **Resource Controls**: CPU and memory limits are defined in the template.
- **Operational Canvas**: Update inputs and resources from the Sealos Canvas after deployment.

## Deployment Guide

1. Open the [Whoogle Search template](https://sealos.io/products/app-store/whoogle-search) and click **Deploy Now**.
2. Configure optional Basic Auth inputs. Set both username and password to enable login protection, or leave both empty for direct access.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access Whoogle Search through the provided App URL. When Basic Auth is enabled, sign in with the username and password from step 2.

## Configuration

After deployment, you can adjust optional search behavior from the Whoogle UI configuration menu. For infrastructure changes, use the Sealos Canvas, AI dialog, or workload resource card.

## Additional Resources

- [Whoogle Search README](https://github.com/benbusby/whoogle-search)
- [Custom Search Engine Setup](https://github.com/benbusby/whoogle-search#google-custom-search-byok)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the repository license. Whoogle Search is licensed under the MIT License.
