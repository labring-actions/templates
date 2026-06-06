# BillionMail

BillionMail is an open-source mail server, newsletter, and email marketing platform. This Sealos template runs the official BillionMail services with PostgreSQL and Redis provided by KubeBlocks.

## Deploy on Sealos

1. Open [BillionMail on Sealos](https://sealos.io/products/app-store/billionmail).
2. Click **Deploy Now**.
3. Set the administrator username, administrator password, security entrance path, mail hostname, timezone, and log retention days.
4. Wait for the application status to become running.
5. Open `https://<app-host>.<sealos-domain>/<safe-path>` once to unlock the console entrance, then sign in with the administrator credentials.

## First Login

The BillionMail console uses the security entrance path from the template input. The default path is `billionmail`, so the first console URL looks like:

```text
https://<app-host>.<sealos-domain>/billionmail
```

After that visit, use the administrator username and password you entered during deployment on the login page.

## Webmail

Roundcube webmail is served by the same web container at `/roundcube/`. Create a mail domain and mailbox in the BillionMail console before using webmail.

## Mail DNS and Port Notes

BillionMail includes SMTP, SMTPS, Submission, IMAP, IMAPS, POP3, and POP3S services inside the Kubernetes Service. Public mail delivery needs DNS and network configuration beyond the web Ingress:

- Point MX records to the mail hostname you configured.
- Add SPF, DKIM, and DMARC records for each sending domain.
- Confirm that SMTP and IMAP/POP ports are reachable from the networks where you plan to send or receive mail.
- Many cloud environments restrict inbound or outbound port 25; use Submission port 587 for authenticated sending when appropriate.

## Data

The template provisions:

- PostgreSQL 16.4 through KubeBlocks for BillionMail application and mail metadata.
- Redis 7.2.7 through KubeBlocks for sessions, cache, and service coordination.
- A persistent volume for mail data, webmail data, Rspamd data, Postfix spool, TLS files, logs, and mutable configuration.

## Source

- [BillionMail GitHub](https://github.com/Billionmail/BillionMail)
- [BillionMail Website](https://www.billionmail.com/)
