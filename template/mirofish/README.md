# Deploy and Host MiroFish on Sealos

MiroFish is an open-source swarm intelligence simulation engine for creating digital worlds, running multi-agent forecasts, and generating scenario reports. This template deploys the MiroFish frontend and backend with persistent upload storage and a shared HTTPS App URL on Sealos Cloud.

![MiroFish Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mirofish/website-screenshot.webp)

## About Hosting MiroFish

MiroFish runs as a two-service web application. The frontend serves the browser workspace, while the backend handles file uploads, graph construction, simulation state, report generation, and OpenAI-compatible LLM calls.

The Sealos template exposes the frontend at the root path and routes `/api` to the backend on the same public domain. Persistent storage keeps uploaded materials, generated graph data, simulation files, and reports under `/app/backend/uploads`.

## Common Use Cases

- **Scenario Forecasting**: Upload reports or source material and simulate possible future developments.
- **Public Opinion Analysis**: Build social graphs and run agent-based discussion or reaction simulations.
- **Creative Worldbuilding**: Generate interactive digital worlds for stories, research, or speculative planning.
- **Decision Rehearsal**: Test policy, communication, or product hypotheses in a multi-agent sandbox.

## Dependencies for MiroFish Hosting

The Sealos template includes the MiroFish frontend, backend API, persistent upload storage, Services, HTTPS Ingress routing, and the Sealos App link.

### Deployment Dependencies

- [GitHub Repository](https://github.com/666ghj/MiroFish) - Source code and container workflow
- [Live Demo](https://666ghj.github.io/mirofish-demo/) - Public project demo
- [Zep Cloud](https://www.getzep.com/) - Graph memory dependency used by MiroFish
- [OpenAI API](https://platform.openai.com/docs) - Compatible API contract for LLM providers

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **MiroFish Frontend**: Browser UI on port 3000.
- **MiroFish Backend**: Flask API on port 5001 for upload, graph, simulation, and report workflows.
- **Persistent Upload Storage**: Stores uploaded files, simulations, logs, generated reports, and graph data.
- **Sealos Ingress**: Routes `/` to the frontend and `/api` to the backend over HTTPS.

**Configuration:**

The deployment form requires an OpenAI-compatible LLM API key, API base URL, model name, and Zep API key. These values are required by the backend before it starts simulation and report workflows.

**License Information:**

MiroFish is licensed under AGPL-3.0. This Sealos template is provided under the repository license for Sealos templates.

## Why Deploy MiroFish on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment, storage, networking, and day-two operations. By deploying MiroFish on Sealos, you get:

- **One-Click Deployment**: Launch both frontend and backend from the App Store.
- **Unified HTTPS URL**: Use one public domain for UI and API traffic.
- **Persistent Workspace Data**: Keep uploaded source material and generated reports across restarts.
- **Easy Provider Configuration**: Set LLM and Zep credentials from the deployment form.
- **Canvas Operations**: Tune resources, inspect logs, and update runtime settings through Canvas, AI dialog, and resource cards.
- **Pay-as-You-Go Resources**: Start with modest resources and scale when simulations become heavier.

## Deployment Guide

1. Open the [MiroFish template](https://sealos.io/products/app-store/mirofish) and click **Deploy Now**.
2. Configure the required parameters in the popup dialog:
   - **LLM API Key**
   - **LLM Base URL**
   - **LLM Model Name**
   - **Zep API Key**
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access MiroFish via the provided URL.
5. Upload seed material and follow the workflow panels to build a graph, prepare a simulation, run it, and generate a report.

## Login and Registration

MiroFish does not require a separate web account in this template. Access is controlled by the Sealos App URL and the provider credentials configured during deployment.

The first useful workflow is configuration verification: open the app, upload source material, and start graph generation. Simulation and report steps require valid LLM and Zep credentials.

## Configuration

After deployment, you can configure MiroFish through:

- **Deployment Inputs**: Update LLM and Zep credentials from the template parameters.
- **Canvas Resource Cards**: Adjust CPU, memory, storage, or environment values.
- **AI Dialog**: Describe changes and let Sealos update the resources.

## Scaling

To scale MiroFish:

1. Open the Canvas for your deployment.
2. Click the frontend Deployment or backend StatefulSet resource card.
3. Increase CPU or memory for heavier uploads, graph builds, or long simulations.
4. Apply changes and monitor logs.

## Troubleshooting

### Backend does not start

- Cause: Missing or placeholder LLM/Zep credentials.
- Solution: Update the deployment inputs with valid API keys, then restart the backend StatefulSet.

### The UI loads but simulation actions fail

- Cause: Provider credentials, model name, or API base URL may be invalid.
- Solution: Check backend logs in Canvas and verify provider settings.

### Uploads or reports disappear after restart

- Cause: The backend persistent volume may have been deleted.
- Solution: Confirm the `/app/backend/uploads` PVC still exists in Canvas.

## Additional Resources

- [MiroFish GitHub](https://github.com/666ghj/MiroFish)
- [MiroFish Demo](https://666ghj.github.io/mirofish-demo/)
- [Zep Cloud](https://www.getzep.com/)

## License

This Sealos template is provided under the Sealos templates repository license. MiroFish itself is licensed under AGPL-3.0.
