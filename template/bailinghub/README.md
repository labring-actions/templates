# BailingHub

![BailingHub Console](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bailinghub/website-screenshot.webp)

BailingHub is an open-source governance control plane for connecting AI agents to existing business systems. It keeps business credentials and final authorization outside the model while providing controlled tool exposure, approval, audit, idempotency, job state, and traceable execution.

## What this template deploys

- BailingHub `0.1.14`
- A Sealos-managed MySQL database
- A deterministic demo business service with order, support-ticket, refund-approval, and failure-trace examples
- A public HTTPS endpoint for the BailingHub console

The database and demo business service are cluster-internal. Only the BailingHub console is exposed through Ingress.

## Installation

1. Choose a unique administrator username.
2. Enter a strong administrator password and store it safely.
3. Deploy the template.
4. Wait until the BailingHub workload is ready.
5. Open the application and sign in with the credentials entered during deployment.

The template generates the internal server token and demo integration secrets automatically.

## First run

The built-in demo is seeded on first startup. It lets you inspect a complete governed-action path without connecting a real production system:

- query a demo order;
- create a demo support ticket;
- send a high-risk refund request through approval;
- inspect an intentional business-tool failure in the trace view.

Demo data and demo actions are not production integrations.

## Security boundaries

- BailingHub controls which agent-facing capabilities are reachable and how execution is governed.
- The business system remains the final authority for user permission, tenant isolation, and current business-state validation.
- The initial administrator password is used only when the first administrator is created. Restarting or upgrading BailingHub does not reset an existing administrator password.
- Generated tokens are stored in Kubernetes Secrets. Rotate them before connecting production systems.
- Keep MySQL and the demo business service private to the cluster.

## Upgrades

This template pins immutable BailingHub and demo-business image versions. Upgrade through a reviewed template revision that changes both image tags together.

Before upgrading:

1. back up the MySQL database;
2. review the BailingHub release notes;
3. verify the target image version in a non-production installation.

## Backup and deletion

Application state is stored in the managed MySQL database. Back up the database before deleting the installation.

In the Sealos console, verify that all three resources created by this template are removed:

1. the main BailingHub application;
2. the internal demo-business application;
3. the managed MySQL database cluster.

Deleting only the main application does not guarantee that the separately managed database has been removed. Confirm the database deletion explicitly to avoid retaining persistent data and incurring continued resource charges.

## Links

- [Website](https://www.bailinghub.com)
- [Documentation](https://www.bailinghub.com/en/docs)
- [GitHub](https://github.com/bailinghub/bailinghub)
- [ACC](https://agentcapability.org)
- [Issues](https://github.com/bailinghub/bailinghub/issues)

## License

BailingHub is released under the [Apache License 2.0](https://github.com/bailinghub/bailinghub/blob/main/LICENSE).
