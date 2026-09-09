# Deploy and Host FXServer on Sealos

FXServer runs FiveM multiplayer servers with the built-in txAdmin management interface. This template deploys one server with persistent data, an HTTPS management URL, and public TCP/UDP game ports on Sealos.

![Official FiveM website](./website-screenshot.webp)

## About Hosting FXServer

The container starts txAdmin, which guides you through account setup, installing a server recipe, and entering your Cfx.re server license key. Its dashboard includes server settings, a live console, player management, and restart scheduling.

Sealos provisions one StatefulSet and a 1Gi persistent volume at `/txdata`. Account settings, player data, logs, and server recipes installed under this directory survive Pod replacement. The game executable remains available from the pinned container image. Use one replica for each independent game server.

### Architecture Components

- **FXServer and txAdmin:** One container using the upstream `35245` build and its verified image digest.
- **Persistent storage:** A 1Gi volume for `/txdata`; install recipes and resources inside this directory.
- **Management access:** An HTTPS Ingress routes through the application's ClusterIP Service to txAdmin on port `40120`.
- **Game access:** A separate `<app-name>-nodeport` Service exposes TCP and UDP `30120` through one shared public game port.

The selected vanilla server setup uses local storage. Framework recipes that require a database need their documented dependencies configured separately.

## Common Use Cases

- **Private multiplayer:** Run a FiveM server for a small group with your chosen server rules.
- **Resource development:** Install and test FiveM resources on a persistent development server.
- **Community administration:** Manage players, scheduled restarts, and server settings through txAdmin.
- **Recipe evaluation:** Try the CFX Default FiveM recipe before configuring a larger server.

## Dependencies for FXServer Hosting

The template includes the FXServer runtime, txAdmin, persistent storage, and network resources. Bring a Cfx.re account for the first administrator setup and a valid server license key for the game server. Players need the software and game entitlement required by FiveM.

- [Container documentation](https://github.com/routmoute/fxserver)
- [Official txAdmin setup guide](https://docs.fivem.net/docs/server-manual/setting-up-a-server-txadmin/)
- [Cfx.re Portal](https://portal.cfx.re/)
- [txAdmin documentation](https://github.com/citizenfx/txAdmin)

## Why Deploy FXServer on Sealos?

Sealos provides one-click deployment on Kubernetes with pay-as-you-go CPU, memory, and storage. Persistent storage keeps server state across restarts, and the management interface receives a public HTTPS address.

After deployment, use Canvas to inspect your server. Describe configuration changes in the AI dialog or open a resource card to adjust CPU, memory, storage, and networking. Size resources for your chosen recipe and player count while keeping a single server replica.

## Deployment Guide

1. Open the [FXServer template](https://sealos.io/products/app-store/fxserver) and click **Deploy Now**.
2. Review the deployment settings and start deployment. Resource creation typically takes **2-3 minutes**, after which you can manage the deployment in Canvas.
3. Open the generated HTTPS application URL. On the first visit, txAdmin displays **No Cfx.re account linked** and asks for a PIN. Open the server resource card in Canvas, view the container logs, and find the txAdmin setup PIN.
4. Enter the PIN and click **Link Account**. Sign in to Cfx.re, approve the account link, and create the backup password requested by txAdmin. Keep that password for later local password logins.
5. Follow the server setup wizard. Select the **CFX Default FiveM** recipe for the vanilla setup, keep its installation directory under `/txdata`, and enter your server license key from the [Cfx.re Portal](https://portal.cfx.re/). Run the recipe and start the server.
6. Open the `<app-name>-nodeport` Service resource card and find the public port shared by `game-tcp` and `game-udp`. Connect with your FiveM client using that game address. The HTTPS application URL opens txAdmin.

### Connecting a FiveM Client

Use the public TCP/UDP host shown for your Sealos region together with the allocated game NodePort. In the US West region, the host is `tcp.usw-1.sealos.app`. Open the FiveM F8 console and replace `GAME_NODEPORT` in this command:

```text
connect tcp.usw-1.sealos.app:GAME_NODEPORT
```

Use the game port on `game-tcp`/`game-udp`. The separately allocated port for `http` belongs to the management interface.

### Later Logins

Open the same HTTPS URL and sign in with the linked Cfx.re account or the administrator username and backup password established during setup. Administrator state is stored on the persistent volume. Retrieve a first-run PIN from the server logs; each deployment generates its own PIN.

## Configuration and Storage

Use txAdmin to edit server settings and manage resources. The template fixes the internal management port to `40120` and the internal game port to `30120`; its Service and Ingress use those values.

Keep installed recipes, server resources, and data under `/txdata`. Expand the persistent volume in Canvas as resources and logs grow. Adjust CPU and memory for the selected recipe before adding players or resource-heavy frameworks.

The initial template resource candidate is `200m` CPU and `256Mi` memory. Management startup has been checked; licensed game startup, authenticated operations, and minimum game-server resource sizing still require completion. This template remains a draft pending that acceptance.

## Troubleshooting

- **The account link screen remains visible:** Enter the PIN from this deployment's logs, finish the Cfx.re authorization, and create the backup password.
- **txAdmin opens while the game server is offline:** Finish the recipe wizard, supply a valid Cfx.re server license key, and inspect the live console for the specific startup error.
- **The client cannot connect:** Check the shared game NodePort and regional TCP/UDP host in the Service card, then confirm that the game server has started in txAdmin.
- **A recipe runs out of memory or storage:** Increase the relevant resource in Canvas and restart the server. Database-backed recipes also require their documented database configuration.

## License

FXServer and FiveM use is governed by the [Cfx.re terms](https://fivem.net/terms). txAdmin is distributed under the [MIT license](https://github.com/citizenfx/txAdmin/blob/master/LICENSE). Refer to the [container repository](https://github.com/routmoute/fxserver) and [Sealos template repository](https://github.com/labring-actions/templates) for their source and contribution information.
