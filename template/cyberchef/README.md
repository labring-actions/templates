# Deploy and Host CyberChef on Sealos

CyberChef is GCHQ's browser-based data workbench for encoding, decoding, encryption, compression, hashing, and forensic analysis. This Sealos template runs CyberChef 11.6.0 as a stateless Deployment with a public HTTPS endpoint.

![CyberChef interface](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cyberchef/website-screenshot.webp)

## About Hosting CyberChef

CyberChef presents a three-pane workbench: the operation list on the left, the recipe in the middle, and the input and output panes on the right. Operations can be chained into a repeatable recipe, reordered by drag and drop, and saved as a URL for later use. The **Bake** action runs the complete recipe against the current input.

This template runs one Deployment with the official `ghcr.io/gchq/cyberchef:11.6.0` image on port `8080`. A ClusterIP Service maps port `80` to the container, and a Sealos Ingress publishes the workbench over HTTPS. The workload is stateless: it has no database, no persistent volume, and no server-side session store.

Data processing happens inside the browser. The server only delivers the static application bundle, so large recipes consume browser memory while the Pod stays small. Recipes, input, and output remain in the browser tab unless you export them or save a recipe URL.

## Common Use Cases

- **Incident Response**: Decode Base64, hexadecimal, URL-encoded, JWT, and binary payloads during triage.
- **Malware Analysis**: Inspect obfuscated scripts, extract strings, and reverse simple encoding layers in an isolated tab.
- **Data Engineering**: Build repeatable recipes for hashing, compression, character-set conversion, and format conversion.
- **Security Training**: Demonstrate cryptography, encoding, and data transforms with live input and output panes.
- **Everyday Debugging**: Convert timestamps, parse JSON, diff text, and inspect file signatures from any browser.

## Dependencies for CyberChef Hosting

The template includes the CyberChef Deployment, a Service, an HTTPS Ingress, and the Sealos App entry. CyberChef needs a modern browser with JavaScript enabled. No database, object storage, cache, or external API is required.

### Deployment Dependencies

- [CyberChef official site](https://gchq.github.io/CyberChef/) - Hosted application and operation reference
- [CyberChef repository](https://github.com/gchq/CyberChef) - Source code, releases, and documentation
- [CyberChef container image](https://github.com/gchq/CyberChef/pkgs/container/cyberchef) - Official image used by this template
- [CyberChef wiki](https://github.com/gchq/CyberChef/wiki) - Operation guides and recipe examples
- [CyberChef releases](https://github.com/gchq/CyberChef/releases) - Version history and changelogs

## Implementation Details

**Architecture Components:**

- **CyberChef Deployment**: One replica running `ghcr.io/gchq/cyberchef:11.6.0` on port `8080`.
- **Service**: ClusterIP port `80` forwarding to the container HTTP port.
- **Ingress**: Sealos-managed HTTPS host with a 32Mi request-body limit and 30-day static-asset caching.
- **App entry**: Opens the public workbench URL from the Sealos desktop.

**Configuration:**

- **Image**: `ghcr.io/gchq/cyberchef:11.6.0`
- **Container port**: `8080`
- **Service port**: `80`
- **Replicas**: `1`
- **Update strategy**: `RollingUpdate` with `maxUnavailable: 1` and `maxSurge: 0`
- **Persistence**: None; recipes and data live in the browser
- **Health checks**: HTTP startup, readiness, and liveness probes against `/`

**Resource Allocation:**

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
| --- | ---: | ---: | ---: | ---: | ---: |
| CyberChef | 10m | 100m | 12Mi | 128Mi | None |

The profile passed a cold start, public page load, Base64 decode, and a stability window with zero restarts.

## Why Deploy CyberChef on Sealos?

Sealos is an AI-assisted cloud operating system built on Kubernetes that combines deployment, networking, storage, and operations in one interface. Deploying CyberChef on Sealos gives you:

- **One-Click Deployment**: Launch the workbench from the App Store without writing Kubernetes YAML.
- **Automatic HTTPS**: Receive a managed public domain and TLS certificate.
- **Lightweight Runtime**: Run a stateless service with a validated 100m CPU and 128Mi memory limit.
- **Canvas and AI Dialog**: Inspect the Deployment, Service, Ingress, logs, and resource cards, and adjust the deployment through the Sealos AI dialog.
- **Pay-as-You-Go Resources**: Start with a compact profile and raise limits when recipes need more browser throughput.
- **Kubernetes Reliability**: Use health probes, automated recovery, and declarative resource management.

## Deployment Guide

1. Open the [CyberChef template](https://sealos.io/products/app-store/cyberchef) and click **Deploy Now**.
2. Review the generated application name and host, confirm the resource plan, and start the deployment.
3. Wait for deployment to complete, typically in 2-3 minutes. Sealos opens the Canvas after the resources are created.
4. Open the public URL from the Canvas or the App Store entry.
5. Paste `SGVsbG8sIFNlYWxvcyE=` into the input pane, add the **From Base64** operation, and confirm that the output pane shows `Hello, Sealos!`.
6. Open Canvas to review the Deployment, Service, Ingress, and live logs.

## Using CyberChef

- Search the operation list by name, then drag an operation into the recipe area.
- Reorder operations to match the processing order; CyberChef applies them from top to bottom.
- Use **Save recipe** or copy the browser URL to preserve a recipe for later runs.
- Use **Auto Bake** for live output while editing the recipe.
- Keep sensitive inputs in the browser and clear the tab when the analysis is complete.

## Scaling

CyberChef is stateless, so the template can serve more browser sessions by increasing the replica count and CPU or memory limits. The default one-replica profile is sized for individual analysts and small teams. Large inputs, many concurrent recipes, or long-running operations consume browser resources first; raise the Pod limits when the application bundle and static requests need more throughput.

## Troubleshooting

### The page loads without operations

Clear the browser cache and reload the public URL. Confirm that the Deployment is Ready and that the Ingress returns HTTP 200 from `/`.

### A recipe produces unexpected output

Check the operation order and each operation's options. CyberChef applies the recipe from top to bottom, and several operations depend on the input format selected in their settings.

### The browser becomes unresponsive

Large files and auto-bake on complex recipes consume browser memory. Disable **Auto Bake**, process smaller chunks, or run the recipe in a desktop browser with more available memory.

### The recipe URL is truncated

Long recipes produce long URLs. Save the recipe as a file or use a shorter recipe when sharing through chat tools that limit URL length.

### Getting Help

- [CyberChef wiki](https://github.com/gchq/CyberChef/wiki)
- [CyberChef issues](https://github.com/gchq/CyberChef/issues)
- [Sealos documentation](https://sealos.io/docs)

## License

CyberChef is licensed under the [Apache License 2.0](https://github.com/gchq/CyberChef/blob/master/LICENSE). This Sealos template is distributed under the templates repository license.
