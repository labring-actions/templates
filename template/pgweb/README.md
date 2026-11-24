# Pgweb

## Overview

Pgweb is a lightweight, cross-platform web client for PostgreSQL. It lets you browse tables, run SQL queries, inspect query plans, export data, and manage multiple database sessions from a browser.

This Sealos template deploys Pgweb `0.17.0`. It does not create a PostgreSQL database; connect it to an existing Sealos PostgreSQL instance or another PostgreSQL server reachable from the Pgweb container.

## Deploy on Sealos

Open this template in the Sealos App Store, keep the generated HTTP authentication password or replace it, and click **Deploy**.

## Access

Open the public URL shown by Sealos. Your browser first displays an HTTP Basic Auth prompt:

- Username: the `auth_username` value, `admin` by default
- Password: the generated or custom `auth_password` value

After signing in, enter the target PostgreSQL connection details in Pgweb. For a PostgreSQL instance in the same Sealos namespace, use its internal service hostname and port `5432`. Choose the SSL mode required by that database.

## Configuration

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `auth_username` | Username protecting the Pgweb web interface | Yes | `admin` |
| `auth_password` | Password protecting the Pgweb web interface | Yes | Random 24-character value |

Pgweb runs in multiple-session mode, so each browser session can connect to a different PostgreSQL database. Database credentials are entered in Pgweb and are not part of this template.

## Security

- Keep HTTP authentication enabled because Pgweb can execute SQL using the database credentials supplied to it.
- Use a dedicated PostgreSQL account with only the permissions you need.
- Do not share the public URL or authentication password.

## Official Links

- Website: https://sosedoff.github.io/pgweb/
- Source: https://github.com/sosedoff/pgweb
- Documentation: https://github.com/sosedoff/pgweb/wiki
