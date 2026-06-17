# Deploy and Host MLflow on Sealos

MLflow is an open-source platform for tracking machine learning experiments, organizing model metadata, and storing model artifacts. This template deploys MLflow with PostgreSQL metadata storage and S3-compatible artifact storage on Sealos Cloud.

## About Hosting MLflow

MLflow runs as a web service that exposes the experiment tracking UI and REST API on port 5000. The Sealos template provisions PostgreSQL for the backend store and an Object Storage bucket for artifacts, so experiment metadata and uploaded files remain persistent across restarts.

MLflow does not include built-in login or user authentication in this deployment. Treat the generated Sealos URL as an application endpoint for your workspace, and add an external authentication layer or network access control if you need multi-user or public access protection.

## Common Use Cases

- **Experiment Tracking**: Record parameters, metrics, tags, and artifacts for model training runs.
- **Model Registry Workflows**: Organize model versions and metadata for review and promotion workflows.
- **Artifact Storage**: Store training outputs, plots, model files, and evaluation reports in S3-compatible storage.
- **Team ML Operations**: Share a central tracking server across notebooks, scripts, and CI jobs.

## Dependencies for MLflow Hosting

The Sealos template includes all required runtime dependencies: the MLflow server container, a KubeBlocks PostgreSQL 16.4 cluster for metadata, and a private Object Storage bucket for artifacts.

### Deployment Dependencies

- [MLflow Documentation](https://mlflow.org/docs/latest/) - Official documentation
- [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) - Tracking UI and API guide
- [MLflow GitHub Repository](https://github.com/mlflow/mlflow) - Source code and issues

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **MLflow Server**: Serves the web UI and REST API at port 5000.
- **PostgreSQL**: Stores experiment, run, parameter, metric, and model metadata.
- **Object Storage**: Stores MLflow artifacts through the S3 API.
- **Ingress and App Link**: Provides the public HTTPS endpoint managed by Sealos.

**Configuration:**

The server starts with `--backend-store-uri` pointing to PostgreSQL and `--default-artifact-root` pointing to the generated S3 bucket. Sealos injects database credentials and object storage credentials through managed secrets, so no manual credential entry is required during deployment.

**Access and Authentication:**

MLflow is available immediately after deployment at the generated HTTPS URL. This template does not configure username/password login because upstream MLflow tracking server does not provide a built-in login screen for this mode. Use Sealos workspace controls, private sharing practices, or an external proxy/authentication layer when the endpoint should not be publicly reachable.

**License Information:**

MLflow is licensed under the Apache License 2.0. This Sealos template is provided under the repository license for the Sealos templates project.

## Why Deploy MLflow on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment, networking, storage, and day-2 operations. By deploying MLflow on Sealos, you get:

- **One-Click Deployment**: Deploy MLflow, PostgreSQL, object storage, service, ingress, and app link from one template.
- **Persistent Metadata and Artifacts**: Keep MLflow metadata in PostgreSQL and artifacts in managed S3-compatible storage.
- **Instant Public Access**: Get an HTTPS endpoint after deployment without manually configuring ingress or certificates.
- **Easy Customization**: Adjust CPU, memory, environment variables, and storage from the Sealos Canvas after deployment.
- **Kubernetes Foundation**: Run MLflow on Kubernetes without managing raw manifests yourself.
- **Pay-as-You-Go Resources**: Start with the template defaults and scale resources when workloads grow.

## Deployment Guide

1. Open the [MLflow template](https://sealos.io/products/app-store/mlflow) and click **Deploy Now**.
2. Keep the default parameters unless you need a custom app name or hostname.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
4. Access your application via the provided URL:
   - **MLflow UI**: Open the generated HTTPS app URL. No default username or password is created.
   - **Tracking API**: Use the same generated URL as `MLFLOW_TRACKING_URI` in MLflow clients.

## Configuration

After deployment, you can configure MLflow through:

- **AI Dialog**: Describe the changes you want and let Sealos apply updates.
- **Resource Cards**: Open the Deployment, PostgreSQL, Object Storage, or Ingress cards to adjust resources and settings.
- **MLflow Clients**: Set `MLFLOW_TRACKING_URI` to the generated app URL in notebooks, training scripts, or CI jobs.
- **External Access Control**: Add an authentication proxy or restrict access if your tracking server contains sensitive experiment data.

## Scaling

To scale MLflow resources:

1. Open the Canvas for your deployment.
2. Click the MLflow Deployment resource card.
3. Adjust CPU and memory based on request volume, artifact activity, and UI usage.
4. Apply the changes in the dialog and wait for the new pod to become ready.

## Troubleshooting

### The MLflow URL opens without a login page

MLflow tracking server does not provide built-in login in this deployment mode. This is expected. Protect the endpoint with workspace access rules, private sharing, or an external authentication proxy if needed.

### Clients cannot log runs

Confirm that `MLFLOW_TRACKING_URI` uses the generated HTTPS URL. If your run uploads artifacts, also confirm that the deployment is healthy and the Object Storage bucket exists in the Canvas.

### Deployment takes longer than expected

PostgreSQL and the MLflow container need time to initialize. If the app is not ready after several minutes, inspect the Deployment and PostgreSQL resource cards in Canvas.

### Getting Help

- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [MLflow GitHub Issues](https://github.com/mlflow/mlflow/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [MLflow Tracking API](https://mlflow.org/docs/latest/api_reference/rest-api.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

This Sealos template is provided under the repository license for Sealos templates. MLflow itself is licensed under the Apache License 2.0.
