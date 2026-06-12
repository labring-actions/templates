# Deploy and Host Logto on Sealos

[Logto](https://logto.io/) is an open-source identity platform for modern applications. It provides sign-in and sign-up experiences, user management, OIDC/OAuth 2.0, SAML, multi-tenancy, and authorization from a self-hosted control plane.

## What You Get

- Logto `1.40.1` running from the fixed `svhd/logto:1.40.1` image.
- A dedicated PostgreSQL database created and initialized by the template.
- Two public HTTPS endpoints: one for application authentication traffic and one for the Admin Console.
- Automatic database creation, seed, and alteration deployment during first startup.

## Requirements

- A [Sealos](https://sealos.io/) account.
- No external database is required; this template provisions PostgreSQL for you.

## Deploy on Sealos

1. Open the [Logto template on Sealos](https://sealos.io/products/app-store/logto).
2. Click **Deploy Now** and keep the generated app name and domain, or customize them before deployment.
3. Wait until the Logto app and PostgreSQL database are both running.
4. Open the Admin Console URL shown in the Sealos app details.

## First Registration and Login

Logto exposes two URLs:

- **Admin Console**: `https://${{ defaults.app_host }}-admin.${{ SEALOS_CLOUD_DOMAIN }}`
- **Core/Auth endpoint**: `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`

On the first launch, open the **Admin Console** URL. The welcome page lets you click **Create account** to create the initial administrator account with a username and password. The open-source edition allows this initial account creation only once. After the administrator account is created, return to the Admin Console and use **Sign in**.

Use the **Core/Auth endpoint** as the issuer and redirect target base when connecting your own applications to Logto through OIDC/OAuth.

## Post-Deployment Checklist

- Create the first administrator account from the Admin Console.
- Configure your application redirect URIs in Logto.
- Keep both the Core/Auth endpoint and Admin Console endpoint on HTTPS.
- Review Logto's official documentation before enabling production identity flows.

## References

- [Logto documentation](https://docs.logto.io/)
- [Logto GitHub repository](https://github.com/logto-io/logto)
- [Sealos documentation](https://sealos.io/docs/)
