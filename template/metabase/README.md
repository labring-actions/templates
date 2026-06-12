# Deploy and Host Metabase on Sealos

Metabase is an open source business intelligence platform for dashboards, SQL exploration, and self-service analytics. This template deploys Metabase 0.61.3 with PostgreSQL, persistent plugin storage, and a public HTTPS endpoint on Sealos Cloud.

![Metabase Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/metabase/website-screenshot.webp)

## About Hosting Metabase

Metabase helps teams connect to databases, ask questions, build dashboards, and share analytics without requiring every user to write SQL. It works well for internal reporting, product analytics, operational metrics, and lightweight embedded BI workflows.

This Sealos template runs Metabase as a StatefulSet and provisions a Kubeblocks PostgreSQL database for the Metabase application database. A persistent volume is mounted at `/plugins` so custom database drivers and plugin files can survive restarts.

Sealos also configures the Kubernetes Service, HTTPS Ingress, generated public URL, and App entry automatically. On first access, Metabase shows its setup flow so you can create the first administrator account and finish the workspace configuration.

## Common Use Cases

- **Self-service BI**: Let business users explore data, save questions, and build dashboards.
- **Operational dashboards**: Track revenue, product usage, support queues, or infrastructure data from connected databases.
- **SQL exploration**: Provide analysts with a browser-based SQL editor and shared result sets.
- **Embedded reporting**: Share dashboards or questions with teammates and stakeholders.
- **Internal analytics portal**: Centralize metrics across teams without running a large BI stack.

## Dependencies for Metabase Hosting

The Sealos template includes the required runtime components: the Metabase container image, a PostgreSQL `postgresql-16.4.0` database, a database initialization job for `metabaseappdb`, persistent plugin storage, a Kubernetes Service, an Ingress, and a Sealos App entry.

### Deployment Dependencies

- [Metabase Website](https://www.metabase.com/) - Product overview and commercial options
- [Metabase Documentation](https://www.metabase.com/docs/latest/) - Administration, setup, and user documentation
- [Metabase GitHub Repository](https://github.com/metabase/metabase) - Source code and releases
- [Metabase Docker Image](https://hub.docker.com/r/metabase/metabase) - Official container image tags

### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **Metabase Web Service**: Runs `metabase/metabase:v0.61.3` on port `3000` and serves the web UI, API, and background application tasks.
- **PostgreSQL**: Kubeblocks-managed PostgreSQL `postgresql-16.4.0` stores Metabase users, permissions, dashboard metadata, questions, and saved settings.
- **PostgreSQL Init Job**: Creates the `metabaseappdb` database idempotently after PostgreSQL is ready.
- **Persistent Plugin Storage**: A `1Gi` volume mounted at `/plugins` keeps custom drivers and plugin files across restarts.
- **Ingress and App Entry**: Sealos exposes Metabase through an HTTPS domain and creates a dashboard entry for direct access.

**Configuration:**

The template configures Metabase with PostgreSQL environment variables from the Kubeblocks connection Secret:

- `MB_DB_TYPE=postgres`
- `MB_DB_DBNAME=metabaseappdb`
- `MB_DB_HOST`, `MB_DB_PORT`, `MB_DB_USER`, and `MB_DB_PASS` from `${{ defaults.app_name }}-pg-conn-credential`
- `JAVA_OPTS=-XX:MaxRAMPercentage=75 -XX:InitialRAMPercentage=25` for stable JVM sizing inside the container limit

No required user inputs are needed during deployment. After the first administrator is created, database connections, users, SSO, email, and embedding settings are managed inside the Metabase admin interface.

**License Information:**

Metabase Open Source Edition is distributed under the AGPLv3 License. This Sealos template is provided as deployment configuration for Metabase and does not change the upstream application license.

## Why Deploy Metabase on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. By deploying Metabase on Sealos, you get:

- **One-Click Deployment**: Deploy Metabase, PostgreSQL, storage, networking, and the App entry from one template.
- **Zero Kubernetes Expertise Required**: Use Kubernetes-backed reliability without writing manifests manually.
- **Persistent Storage Included**: Keep Metabase metadata in PostgreSQL and plugin files on persistent storage.
- **Instant Public Access**: Each deployment receives an HTTPS URL for setup, login, and dashboard sharing.
- **Easy Customization**: Adjust resources, environment variables, and storage through the Sealos Canvas and AI dialog.
- **Pay-As-You-Go Resources**: Start with a validated resource profile and scale when usage grows.

Deploy Metabase on Sealos and focus on analytics instead of infrastructure management.

## Deployment Guide

1. Open the [Metabase template](https://sealos.io/products/app-store/metabase) and click **Deploy Now**.
2. Keep the default parameters unless you need a custom generated name or host.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog or click the relevant resource cards to modify settings.
4. Open the generated Metabase URL from the App entry.
5. Complete the first-run setup wizard:
   - Enter the first administrator's name, email address, and password.
   - Set the organization or site name.
   - Choose whether to connect your first analytics database immediately or skip and add it later.
   - Review usage data preferences and finish setup.
6. After setup, use the same administrator email and password on the login page for future access.

Metabase does not create a public self-registration flow in this template. The first user created during setup becomes the administrator.

## Configuration

After deployment, you can configure Metabase through:

- **Initial Setup Wizard**: Creates the first administrator account and baseline site settings.
- **Metabase Admin Settings**: Add data sources, users, groups, permissions, email, SSO, embedding, and localization settings.
- **Sealos AI Dialog**: Describe environment, resource, or storage changes and let AI apply updates.
- **Resource Cards**: Click the StatefulSet, PostgreSQL, Ingress, or storage cards in Canvas to inspect and adjust settings.

If you add custom database drivers, upload the driver JAR to `/plugins` and restart the Metabase workload. Keep database credentials inside Metabase or Sealos-managed settings instead of committing them to the template repository.

## Scaling

To scale Metabase on Sealos:

1. Open the Canvas for your Metabase deployment.
2. Click the Metabase StatefulSet resource card.
3. Increase CPU or memory when startup, migrations, dashboard rendering, or concurrent query activity requires more capacity.
4. Increase PostgreSQL or storage resources if metadata or plugin usage grows.
5. Apply the change and wait for the pod to become ready again.

The default application profile is `1` CPU and `2G` memory. Live validation showed `1024Mi` can fail during cold start or restart for Metabase 0.61.3, while `2G` completed cold start, first-run setup, restart, and login checks.

## Troubleshooting

### The app opens the setup wizard

This is expected on a fresh deployment. Complete the wizard to create the first administrator account. After setup, unauthenticated visitors will see the login page.

### The app is slow or restarts during startup

Metabase performs JVM startup and database migrations on cold start. Wait a few minutes during first deployment. If the workload restarts or dashboards are slow, increase memory first and then CPU from the StatefulSet resource card.

### Cannot connect an analytics database

Verify the target database host, port, username, password, network access, and TLS requirements in Metabase Admin Settings. For databases that require custom JDBC drivers, place the driver file in `/plugins` and restart the workload.

### Getting Help

- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [Metabase Troubleshooting Guide](https://www.metabase.com/docs/latest/troubleshooting-guide/)
- [Metabase GitHub Issues](https://github.com/metabase/metabase/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## Additional Resources

- [Metabase Setup Guide](https://www.metabase.com/docs/latest/configuring-metabase/setting-up-metabase)
- [Metabase Administration Guide](https://www.metabase.com/docs/latest/configuring-metabase/)
- [Running Metabase on Docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)

## License

This Sealos template is provided under the repository's template license. Metabase Open Source Edition itself is licensed under AGPLv3.
