# Deploy frp on Sealos

[frp](https://gofrp.org/en/) is a fast reverse proxy that publishes services from private networks through a public server. This template deploys the official frps v0.70.0 image with token authentication, a protected monitoring dashboard, HTTP virtual-host routing, and a dedicated TCP proxy port.

![frp Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/frp/website-screenshot.webp)

## About frp

frp uses a client-server architecture. `frps` runs on Sealos with public connectivity, and `frpc` runs beside the private service. The client opens an authenticated outbound connection to the server, then frps forwards public traffic through that connection.

Common uses include:

- Publishing a development web server from a laptop or private network.
- Reaching SSH, databases, or device services through a controlled TCP port.
- Routing multiple HTTP services by hostname.
- Monitoring connected clients, proxies, and traffic from the frps dashboard.

The frps dashboard is a monitoring interface. Proxy definitions remain in each frpc configuration.

## Why Deploy frp on Sealos?

- Run the official frps container behind Sealos networking and HTTPS.
- Use separate public surfaces for the dashboard, HTTP virtual hosts, and TCP data plane.
- Protect frpc connections with a required shared token.
- Start at the lowest Sealos compute tier verified by a real end-to-end TCP proxy test.

## Deployment Guide

1. Open the [frp template](https://sealos.io/products/app-store/frp) and click **Deploy Now**.
2. Enter all required values:
   - `dashboard_username`: username for dashboard Basic Authentication.
   - `dashboard_password`: password for dashboard Basic Authentication.
   - `frp_auth_token`: shared token used by every frpc client.
3. Deploy the template and wait for the frps workload and initialization job to complete.
4. Open the generated application URL and sign in with `dashboard_username` and `dashboard_password`.

Use long, unique values for the dashboard password and frp token. Store both values in a password manager.

## Public Endpoints

The deployment exposes four logical endpoints:

| Endpoint | Purpose |
| --- | --- |
| Dashboard HTTPS URL | frps status, clients, proxies, and traffic |
| HTTP HTTPS URL | Public entry for HTTP proxies using `customDomains` |
| `server` public TCP port | frpc control connection to frps port `7000` |
| `tcp-proxy` public TCP port | Reserved remote port for one TCP proxy |

Open the frp resource details in Sealos to find the public host and NodePort values for `server` and `tcp-proxy`.

## Connect an frpc Client

Download frpc v0.70.0 for the client machine from the [frp releases page](https://github.com/fatedier/frp/releases/tag/v0.70.0).

### Publish a TCP Service

Create `frpc.toml`:

```toml
serverAddr = "<your-public-sealos-host>"
serverPort = <server-public-port>

auth.method = "token"
auth.token = "<your-frp-auth-token>"

[[proxies]]
name = "private-service"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = <tcp-proxy-public-port>
```

Start the client:

```bash
./frpc -c ./frpc.toml
```

External users can now connect to `<your-public-sealos-host>:<tcp-proxy-public-port>`. The dashboard shows the online client and proxy after the connection is established.

### Publish an HTTP Service

Use the generated HTTP endpoint hostname as `customDomains`:

```toml
serverAddr = "<your-public-sealos-host>"
serverPort = <server-public-port>

auth.method = "token"
auth.token = "<your-frp-auth-token>"

[[proxies]]
name = "web"
type = "http"
localIP = "127.0.0.1"
localPort = 8080
customDomains = ["<your-http-endpoint-host>"]
```

Open `https://<your-http-endpoint-host>` after frpc reports that the proxy started successfully.

## Resource Baseline

The frps workload uses `100m` CPU and `128 MiB` memory limits, with `10m` CPU and `12 MiB` requests. A live v0.70.0 test connected an official frpc client, forwarded an external TCP request, verified byte-for-byte response integrity, and kept the pod at zero restarts. Increase resources for many concurrent tunnels or high traffic volume.

## Security Notes

- Rotate `frp_auth_token` and restart frpc clients after any credential exposure.
- Keep dashboard credentials separate from the frp client token.
- Restrict the private service itself when it exposes sensitive protocols such as SSH or databases.
- Use frp transport encryption and TLS options for clients that cross untrusted networks.

## Troubleshooting

### frpc cannot connect

Confirm the public `server` port in Sealos, the `serverAddr` hostname, and the shared token. The client and server versions should use the same v0.70.0 release.

### A TCP proxy stays offline

Set `remotePort` to the public `tcp-proxy` port shown by Sealos and confirm the local service is listening on `localIP:localPort`.

### The dashboard opens with an authentication prompt

Enter the `dashboard_username` and `dashboard_password` values supplied during deployment. Successful login opens the monitoring dashboard.

## Resources

- [frp Documentation](https://gofrp.org/en/docs/)
- [frp GitHub Repository](https://github.com/fatedier/frp)
- [frp v0.70.0 Release](https://github.com/fatedier/frp/releases/tag/v0.70.0)

## License

frp is licensed under the Apache License 2.0. This Sealos template follows the templates repository license.
